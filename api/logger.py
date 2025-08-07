import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class ConversationLogger:
    """对话日志记录器"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 设置日志格式
        self.logger = logging.getLogger("conversation_logger")
        self.logger.setLevel(logging.INFO)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 文件handler
            file_handler = logging.FileHandler(
                self.log_dir / f"conversation_{datetime.now().strftime('%Y%m%d')}.log",
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            
            # 控制台handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def log_conversation_start(self, 
                             conversation_id: str,
                             user_id: str,
                             user_input: str,
                             has_image: bool = False,
                             image_url: str = None) -> Dict[str, Any]:
        """记录对话开始"""
        
        log_entry = {
            "event": "conversation_start",
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "user_id": user_id,
            "user_input": user_input,
            "has_image": has_image,
            "image_url": image_url,
            "start_time": time.time()
        }
        
        self.logger.info(f"CONVERSATION_START: {json.dumps(log_entry, ensure_ascii=False)}")
        return log_entry
    
    def log_first_response(self,
                          conversation_id: str,
                          start_time: float,
                          first_chunk_received: bool = True) -> float:
        """记录首字响应时间"""
        
        first_response_time = time.time() - start_time
        
        log_entry = {
            "event": "first_response",
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "first_response_time_ms": round(first_response_time * 1000, 2),
            "first_chunk_received": first_chunk_received
        }
        
        self.logger.info(f"FIRST_RESPONSE: {json.dumps(log_entry, ensure_ascii=False)}")
        return first_response_time
    
    def log_conversation_complete(self,
                                conversation_id: str,
                                user_id: str,
                                user_input: str,
                                ai_response: str,
                                start_time: float,
                                plantuml_result: Optional[Dict] = None,
                                error_info: Optional[str] = None,
                                token_usage: Optional[Dict] = None) -> None:
        """记录对话完成"""
        
        total_time = time.time() - start_time
        
        log_entry = {
            "event": "conversation_complete",
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "user_id": user_id,
            "user_input": user_input,
            "ai_response": ai_response,
            "total_response_time_ms": round(total_time * 1000, 2),
            "plantuml_result": plantuml_result,
            "error_info": error_info,
            "token_usage": token_usage,
            "response_length": len(ai_response) if ai_response else 0,
            "has_plantuml": bool(plantuml_result),
            "status": "error" if error_info else "success"
        }
        
        self.logger.info(f"CONVERSATION_COMPLETE: {json.dumps(log_entry, ensure_ascii=False)}")
    
    def log_image_generation(self,
                           conversation_id: str,
                           plantuml_code: str,
                           image_path: str,
                           generation_time: float,
                           success: bool = True,
                           error: str = None) -> None:
        """记录图片生成"""
        
        log_entry = {
            "event": "image_generation",
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "plantuml_code_length": len(plantuml_code) if plantuml_code else 0,
            "image_path": image_path,
            "generation_time_ms": round(generation_time * 1000, 2),
            "success": success,
            "error": error
        }
        
        self.logger.info(f"IMAGE_GENERATION: {json.dumps(log_entry, ensure_ascii=False)}")
    
    def log_error(self,
                 conversation_id: str,
                 error_type: str,
                 error_message: str,
                 context: Dict[str, Any] = None) -> None:
        """记录错误"""
        
        log_entry = {
            "event": "error",
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {}
        }
        
        self.logger.error(f"ERROR: {json.dumps(log_entry, ensure_ascii=False)}")

# 全局日志记录器实例
conversation_logger = ConversationLogger() 