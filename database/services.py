from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from .models import User, Conversation, Message
from .redis_client import redis_session_manager

class DatabaseService:
    """数据库服务层"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # 用户相关操作
    def get_or_create_user(self, user_id: str, name: str = None, email: str = None) -> User:
        """获取或创建用户"""
        user = self.db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            user = User(
                user_id=user_id,
                name=name,
                email=email
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        else:
            # 更新最后活动时间
            user.last_active = datetime.utcnow()
            self.db.commit()
        
        return user
    
    # 对话相关操作
    def create_conversation(self, user_id: str, title: str = "新对话") -> Conversation:
        """创建新对话"""
        # 确保用户存在
        self.get_or_create_user(user_id)
        
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation
    
    def get_conversation(self, conversation_id: str, user_id: str = None) -> Optional[Conversation]:
        """获取对话"""
        query = self.db.query(Conversation).filter(Conversation.id == conversation_id)
        
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        
        return query.first()
    
    def get_user_conversations(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Conversation]:
        """获取用户的对话列表"""
        return self.db.query(Conversation)\
                     .filter(Conversation.user_id == user_id)\
                     .filter(Conversation.status == 'active')\
                     .order_by(Conversation.updated_at.desc())\
                     .offset(offset)\
                     .limit(limit)\
                     .all()
    
    def update_conversation_title(self, conversation_id: str, title: str, user_id: str = None) -> bool:
        """更新对话标题"""
        query = self.db.query(Conversation).filter(Conversation.id == conversation_id)
        
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        
        result = query.update({"title": title, "updated_at": datetime.utcnow()})
        self.db.commit()
        
        return result > 0
    
    def delete_conversation(self, conversation_id: str, user_id: str = None) -> bool:
        """删除对话"""
        query = self.db.query(Conversation).filter(Conversation.id == conversation_id)
        
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        
        conversation = query.first()
        if conversation:
            # 清除Redis中的会话记忆
            redis_session_manager.clear_conversation(conversation.user_id, str(conversation.id))
            
            # 软删除
            conversation.status = 'deleted'
            conversation.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        
        return False
    
    async def get_or_create_conversation(self, conversation_id: str, title: str = "新对话", user_id: str = "web_user") -> Conversation:
        """获取或创建对话"""
        # 如果提供了conversation_id，尝试获取现有对话
        if conversation_id:
            conversation = self.get_conversation(conversation_id, user_id)
            if conversation:
                return conversation
        
        # 如果没有找到现有对话，创建新的
        return self.create_conversation(user_id, title)
    
    async def get_user_conversations_async(self, user_id: str) -> List[Conversation]:
        """异步获取用户对话列表"""
        return self.get_user_conversations(user_id)
    
    async def get_conversation_messages(self, conversation_id: str) -> List[Message]:
        """获取对话的所有消息"""
        return self.db.query(Message)\
                      .filter(Message.conversation_id == conversation_id)\
                      .order_by(Message.created_at.asc())\
                      .all()
    
    async def delete_conversation_async(self, conversation_id: str) -> bool:
        """异步删除对话"""
        return self.delete_conversation(conversation_id)
    
    # 消息相关操作
    def add_message(self, conversation_id: str, message_type: str, content: str, 
                   image_url: str = None, plantuml_code: str = None, 
                   plantuml_image_url: str = None, meta_data: Dict[str, Any] = None) -> Message:
        """添加消息"""
        message = Message(
            conversation_id=conversation_id,
            message_type=message_type,
            content=content,
            image_url=image_url,
            plantuml_code=plantuml_code,
            plantuml_image_url=plantuml_image_url,
            meta_data=meta_data or {}
        )
        
        self.db.add(message)
        
        # 更新对话的更新时间
        conversation = self.get_conversation(str(conversation_id))
        if conversation:
            conversation.updated_at = datetime.utcnow()
            
            # 如果是第一条用户消息，更新对话标题
            if message_type == 'user' and len(conversation.messages) == 0:
                title = content[:50] + "..." if len(content) > 50 else content
                conversation.title = title
        
        self.db.commit()
        self.db.refresh(message)
        
        # 添加到Redis会话记忆
        if conversation:
            redis_message = {
                "type": message_type,
                "content": content,
                "image_url": image_url,
                "plantuml_code": plantuml_code,
                "plantuml_image_url": plantuml_image_url
            }
            redis_session_manager.add_message(
                conversation.user_id, 
                str(conversation.id), 
                redis_message
            )
        
        return message
    
    def get_conversation_messages(self, conversation_id: str, limit: int = 100, offset: int = 0) -> List[Message]:
        """获取对话消息"""
        return self.db.query(Message)\
                     .filter(Message.conversation_id == conversation_id)\
                     .order_by(Message.created_at.asc())\
                     .offset(offset)\
                     .limit(limit)\
                     .all()
    
    def get_conversation_with_context(self, conversation_id: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """获取对话及其上下文（包括Redis中的记忆）"""
        conversation = self.get_conversation(conversation_id, user_id)
        
        if not conversation:
            return None
        
        # 获取Redis中的对话上下文
        context = redis_session_manager.get_context_for_llm(
            conversation.user_id, 
            str(conversation.id)
        )
        
        return {
            "conversation": conversation,
            "context": context,
            "recent_messages": self.get_conversation_messages(conversation_id, limit=10)
        }

# 辅助函数
def get_database_service(db: Session) -> DatabaseService:
    """获取数据库服务实例"""
    return DatabaseService(db) 