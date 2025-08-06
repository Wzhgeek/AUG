import os
from openai import OpenAI
import dotenv
from typing import AsyncGenerator, Generator, Optional, List, Dict, Any

dotenv.load_dotenv()

class DEEPSEEK_V3:
    """DeepSeek V3 客户端类，支持非流式和流式响应"""
    
    def __init__(self):
        """初始化客户端"""
        # 获取环境变量
        self.base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.api_key = os.environ.get("DEEPSEEK_API_KEY")
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        
        # 模型ID
        self.model = "deepseek-chat"
    
    def chat(self, user_input: str, system_prompt: str = None) -> str:
        """
        非流式聊天方法
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词
            
        Returns:
            str: 完整的响应文本
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_input})
            
            # 创建非流式响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
            )
            
            # 返回完整响应
            return response.choices[0].message.content
                    
        except Exception as e:
            return f"错误: {str(e)}"
    
    def chat_stream(self, user_input: str, system_prompt: str = None) -> Generator[str, None, None]:
        """
        流式聊天方法
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词
            
        Yields:
            str: 流式响应片段
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_input})
            
            # 创建流式响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )
            
            # 返回流式响应
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"错误: {str(e)}"
    
    def chat_print(self, user_input: str, system_prompt: str = None) -> str:
        """
        聊天并直接打印输出
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词
        """
        response = self.chat(user_input, system_prompt)
        print(response)
        return response 