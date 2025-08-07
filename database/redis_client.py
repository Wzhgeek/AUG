import os
import json
import redis
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

class RedisSessionManager:
    """Redis会话管理器，用于多轮对话记忆"""
    
    def __init__(self):
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_db = int(os.getenv("REDIS_DB", 0))
        self.redis_password = os.getenv("REDIS_PASSWORD", None)
        
        # 创建Redis连接
        self.redis_client = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db,
            password=self.redis_password,
            decode_responses=True
        )
        
        # 配置
        self.session_ttl = 86400 * 7  # 7天过期
        self.max_messages_per_session = 50  # 每个会话最多保存50条消息
    
    def _get_session_key(self, user_id: str, conversation_id: str) -> str:
        """生成会话键"""
        return f"session:{user_id}:{conversation_id}"
    
    def _get_user_conversations_key(self, user_id: str) -> str:
        """生成用户对话列表键"""
        return f"user_conversations:{user_id}"
    
    def add_message(self, user_id: str, conversation_id: str, message: Dict[str, Any]):
        """添加消息到会话记忆"""
        session_key = self._get_session_key(user_id, conversation_id)
        
        # 添加时间戳
        message["timestamp"] = datetime.utcnow().isoformat()
        
        # 将消息添加到列表
        self.redis_client.lpush(session_key, json.dumps(message, ensure_ascii=False))
        
        # 限制消息数量
        self.redis_client.ltrim(session_key, 0, self.max_messages_per_session - 1)
        
        # 设置过期时间
        self.redis_client.expire(session_key, self.session_ttl)
        
        # 更新用户对话列表
        user_conversations_key = self._get_user_conversations_key(user_id)
        conversation_info = {
            "conversation_id": conversation_id,
            "last_activity": datetime.utcnow().isoformat()
        }
        self.redis_client.hset(
            user_conversations_key, 
            conversation_id, 
            json.dumps(conversation_info, ensure_ascii=False)
        )
        self.redis_client.expire(user_conversations_key, self.session_ttl)
    
    def get_conversation_history(self, user_id: str, conversation_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取对话历史"""
        session_key = self._get_session_key(user_id, conversation_id)
        
        # 获取消息列表（从最新到最旧）
        messages = self.redis_client.lrange(session_key, 0, limit - 1)
        
        # 解析并返回（按时间正序）
        parsed_messages = []
        for msg in reversed(messages):
            try:
                parsed_messages.append(json.loads(msg))
            except json.JSONDecodeError:
                continue
        
        return parsed_messages
    
    def get_context_for_llm(self, user_id: str, conversation_id: str, max_tokens: int = 2000) -> List[Dict[str, str]]:
        """获取适合LLM的对话上下文"""
        history = self.get_conversation_history(user_id, conversation_id, limit=10)
        
        context = []
        total_chars = 0
        
        for msg in history:
            # 估算token数（简单按字符数/4估算）
            msg_chars = len(msg.get("content", ""))
            if total_chars + msg_chars > max_tokens * 4:
                break
            
            role = "user" if msg.get("type") == "user" else "assistant"
            context.append({
                "role": role,
                "content": msg.get("content", "")
            })
            total_chars += msg_chars
        
        return context
    
    def clear_conversation(self, user_id: str, conversation_id: str):
        """清除对话记忆"""
        session_key = self._get_session_key(user_id, conversation_id)
        self.redis_client.delete(session_key)
        
        # 从用户对话列表中移除
        user_conversations_key = self._get_user_conversations_key(user_id)
        self.redis_client.hdel(user_conversations_key, conversation_id)
    
    def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户的所有对话"""
        user_conversations_key = self._get_user_conversations_key(user_id)
        conversations = self.redis_client.hgetall(user_conversations_key)
        
        result = []
        for conv_id, conv_info in conversations.items():
            try:
                info = json.loads(conv_info)
                result.append({
                    "conversation_id": conv_id,
                    "last_activity": info["last_activity"]
                })
            except json.JSONDecodeError:
                continue
        
        # 按最后活动时间排序
        result.sort(key=lambda x: x["last_activity"], reverse=True)
        return result
    
    def cleanup_expired_sessions(self):
        """清理过期会话（可以设置为定时任务）"""
        # Redis会自动过期，这里可以添加额外的清理逻辑
        pass

# 全局Redis会话管理器实例
redis_session_manager = RedisSessionManager() 