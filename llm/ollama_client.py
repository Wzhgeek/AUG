import requests
import json
import time
from typing import Generator, Optional
import logging

logger = logging.getLogger(__name__)

class OllamaClient:
    """Ollama本地模型客户端"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "llama3.2"):
        """
        初始化Ollama客户端
        
        Args:
            base_url: Ollama服务地址，默认localhost:11434
            model_name: 模型名称，默认llama3.2
        """
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.api_url = f"{self.base_url}/api"
        
        # 测试连接
        self._test_connection()
    
    def _test_connection(self):
        """测试与Ollama服务的连接"""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=5)
            if response.status_code == 200:
                logger.info(f"Ollama连接成功: {self.base_url}")
                # 检查模型是否可用
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                if self.model_name not in available_models:
                    logger.warning(f"模型 {self.model_name} 不可用，可用模型: {available_models}")
            else:
                logger.error(f"Ollama连接失败: {response.status_code}")
        except Exception as e:
            logger.error(f"无法连接到Ollama服务: {e}")
    
    def chat(self, user_input: str, system_prompt: str = None) -> str:
        """
        非流式对话
        
        Args:
            user_input: 用户输入
            system_prompt: 系统提示词
            
        Returns:
            AI回复内容
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_input})
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2048
                }
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', '')
            else:
                logger.error(f"Ollama API调用失败: {response.status_code} - {response.text}")
                return f"错误: API调用失败 ({response.status_code})"
                
        except Exception as e:
            logger.error(f"Ollama对话失败: {e}")
            return f"错误: {str(e)}"
    
    def chat_stream(self, user_input: str, system_prompt: str = None) -> Generator[str, None, None]:
        """
        流式对话
        
        Args:
            user_input: 用户输入
            system_prompt: 系统提示词
            
        Yields:
            AI回复的文本片段
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_input})
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2048
                }
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                stream=True,
                timeout=60
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'message' in data and 'content' in data['message']:
                                yield data['message']['content']
                        except json.JSONDecodeError:
                            continue
            else:
                error_msg = f"错误: API调用失败 ({response.status_code})"
                logger.error(f"Ollama流式API调用失败: {response.status_code} - {response.text}")
                yield error_msg
                
        except Exception as e:
            logger.error(f"Ollama流式对话失败: {e}")
            yield f"错误: {str(e)}"
    
    def chat_multimodal(self, text: str, image_url: str, system_prompt: str = None) -> str:
        """
        多模态对话 (非流式)
        
        Args:
            text: 文本输入
            image_url: 图片URL
            system_prompt: 系统提示词
            
        Returns:
            AI回复内容
        """
        try:
            # 读取图片文件
            image_data = self._load_image(image_url)
            if not image_data:
                return "错误: 无法加载图片"
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # 构建多模态消息
            message_content = [
                {"type": "text", "text": text},
                {"type": "image", "image": image_data}
            ]
            messages.append({"role": "user", "content": message_content})
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2048
                }
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                timeout=120  # 多模态需要更长时间
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', '')
            else:
                logger.error(f"Ollama多模态API调用失败: {response.status_code} - {response.text}")
                return f"错误: 多模态API调用失败 ({response.status_code})"
                
        except Exception as e:
            logger.error(f"Ollama多模态对话失败: {e}")
            return f"错误: {str(e)}"
    
    def chat_multimodal_stream(self, text: str, image_url: str, system_prompt: str = None) -> Generator[str, None, None]:
        """
        多模态流式对话
        
        Args:
            text: 文本输入
            image_url: 图片URL
            system_prompt: 系统提示词
            
        Yields:
            AI回复的文本片段
        """
        try:
            # 读取图片文件
            image_data = self._load_image(image_url)
            if not image_data:
                yield "错误: 无法加载图片"
                return
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # 构建多模态消息
            message_content = [
                {"type": "text", "text": text},
                {"type": "image", "image": image_data}
            ]
            messages.append({"role": "user", "content": message_content})
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2048
                }
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                stream=True,
                timeout=120
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'message' in data and 'content' in data['message']:
                                yield data['message']['content']
                        except json.JSONDecodeError:
                            continue
            else:
                error_msg = f"错误: 多模态API调用失败 ({response.status_code})"
                logger.error(f"Ollama多模态流式API调用失败: {response.status_code} - {response.text}")
                yield error_msg
                
        except Exception as e:
            logger.error(f"Ollama多模态流式对话失败: {e}")
            yield f"错误: {str(e)}"
    
    def _load_image(self, image_url: str) -> Optional[str]:
        """
        加载图片并转换为base64格式
        
        Args:
            image_url: 图片URL或文件路径
            
        Returns:
            base64编码的图片数据
        """
        try:
            import base64
            from pathlib import Path
            
            # 如果是本地文件路径
            if Path(image_url).exists():
                with open(image_url, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                    return image_data
            
            # 如果是HTTP URL
            elif image_url.startswith('http'):
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    image_data = base64.b64encode(response.content).decode('utf-8')
                    return image_data
                else:
                    logger.error(f"无法下载图片: {response.status_code}")
                    return None
            
            else:
                logger.error(f"不支持的图片URL格式: {image_url}")
                return None
                
        except Exception as e:
            logger.error(f"加载图片失败: {e}")
            return None
    
    def list_models(self) -> list:
        """
        获取可用模型列表
        
        Returns:
            模型列表
        """
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=5)
            if response.status_code == 200:
                result = response.json()
                return result.get('models', [])
            else:
                logger.error(f"获取模型列表失败: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"获取模型列表异常: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """
        拉取模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            是否成功
        """
        try:
            payload = {"name": model_name}
            response = requests.post(f"{self.api_url}/pull", json=payload, timeout=300)
            
            if response.status_code == 200:
                logger.info(f"模型 {model_name} 拉取成功")
                return True
            else:
                logger.error(f"模型拉取失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"模型拉取异常: {e}")
            return False 