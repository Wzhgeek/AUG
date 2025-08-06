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
        self.doubao_api_key = os.environ.get("DOUBAO_SEED_1_6_FLASH")
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        
        # 模型ID
        self.model = "ep-20250208190113-n7r6v"  # 根据实际豆包模型ID调整
    
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
    
    def chat_print(self, user_input: str, system_prompt: str = None) -> None:
        """
        聊天并直接打印输出
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词，默认为MAIN_PROMPT
        """
        response = self.chat(user_input, system_prompt)
        return response