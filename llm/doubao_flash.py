import os
from openai import OpenAI
import dotenv
from llm.system_prompts import MAIN_IMG
from typing import AsyncGenerator, Generator

dotenv.load_dotenv()

class DOUBAO_SEED_1_6_FLASH:
    """豆包 SEED 1.6 客户端类，支持非流式响应"""
    
    def __init__(self):
        """初始化客户端"""
        # 获取环境变量
        self.base_url = os.environ.get("ARK_BASE_URL")
        self.api_key = os.environ.get("ARK_API_KEY")
        self.model = os.environ.get("DOUBAO_FLASH")
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
    
    def chat(self, user_input: str, system_prompt: str = None) -> str:
        """
        非流式聊天方法
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词，默认为MAIN_PROMPT
            
        Returns:
            str: 完整的响应文本
        """
        if system_prompt is None:
            system_prompt = MAIN_IMG
            
        try:
            # 创建非流式响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                stream=False,
            )
            
            # 返回完整响应
            return response.choices[0].message.content
                    
        except Exception as e:
            return f"错误: {str(e)}"
    
    def chat_multimodal(self, text: str, image_url: str, system_prompt: str = None) -> str:
        """
        多模态聊天方法（非流式）
        
        Args:
            text: 文本输入
            image_url: 图片URL
            system_prompt: 系统提示词
            
        Returns:
            str: 完整的响应文本
        """
        if system_prompt is None:
            system_prompt = MAIN_IMG
            
        try:
            # 构建多模态消息
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": text},
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}}
                    ]
                }
            ]
            
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
    
    def chat_multimodal_stream(self, text: str, image_url: str, system_prompt: str = None) -> Generator[str, None, None]:
        """
        多模态聊天方法（流式）
        
        Args:
            text: 文本输入
            image_url: 图片URL
            system_prompt: 系统提示词
            
        Yields:
            str: 流式响应片段
        """
        if system_prompt is None:
            system_prompt = MAIN_IMG
            
        try:
            # 构建多模态消息
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": text},
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}}
                    ]
                }
            ]
            
            # 创建流式响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )
            
            # 流式返回响应
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"错误: {str(e)}"
    
    def chat_print(self, user_input: str, system_prompt: str = None) -> None:
        """
        聊天并直接打印输出
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词，默认为MAIN_PROMPT
        """
        response = self.chat(user_input, system_prompt)
        return response