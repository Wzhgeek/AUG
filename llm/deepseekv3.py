import os
from openai import OpenAI
import dotenv
from llm.system_prompts import MAIN
from typing import AsyncGenerator, Generator

dotenv.load_dotenv()


class DeepSeekV3Client:
    """DeepSeek V3 客户端类，支持流式响应"""
    
    def __init__(self):
        """初始化客户端"""
        # 获取环境变量
        self.base_url = os.environ.get("ARK_BASE_URL")
        self.api_key = os.environ.get("ARK_API_KEY")
        self.model = os.environ.get("DEEPSEEK_V3")
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    
    def chat_stream(self, user_input: str, system_prompt: str = None) -> Generator[str, None, None]:
        """
        流式聊天方法
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词，默认为MAIN_PROMPT
            
        Yields:
            str: 流式响应的文本片段
        """
        if system_prompt is None:
            system_prompt = MAIN
            
        try:
            # 创建流式响应
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                stream=True,
            )
            
            # 流式输出响应
            for chunk in stream:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    
        except Exception as e:
            yield f"错误: {str(e)}"
    
    def chat_stream_print(self, user_input: str, system_prompt: str = None) -> None:
        """
        流式聊天并直接打印输出
        
        Args:
            user_input: 用户输入的消息
            system_prompt: 系统提示词，默认为MAIN_PROMPT
        """
        for chunk in self.chat_stream(user_input, system_prompt):
            print(chunk, end="")
        print()



# 使用示例
if __name__ == "__main__":
    # 创建 DeepSeek 客户端实例
    client = DeepSeekV3Client()
    
    # # 方式1: 流式输出并打印
    # client.chat_stream_print("你好")
    
    # 方式2: 获取流式响应进行处理
    for response_chunk in client.chat_stream("你好"):
        # 在这里可以对每个响应片段进行处理
        print(response_chunk, end="")
    print()
    
