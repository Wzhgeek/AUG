from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from .models import QueryRequest, QueryResponse, HealthResponse
from llm.doubao_flash import DOUBAO_SEED_1_6_FLASH
from llm.deepseekv3 import DEEPSEEK_V3
from prompt.system_prompts import DEFAULT_PROMPT, MULTIMODAL_ASSISTANT
import json
import time
from typing import Generator

router = APIRouter()

# 初始化模型客户端
doubao_client = DOUBAO_SEED_1_6_FLASH()
deepseek_client = DEEPSEEK_V3()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    return HealthResponse(
        status="healthy",
        message="服务运行正常",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )

@router.post("/query")
async def query_stream(request: QueryRequest):
    """流式查询接口"""
    
    # 验证输入
    if not request.input.strip():
        raise HTTPException(status_code=400, detail="输入内容不能为空")
    
    # 选择系统提示词
    system_prompt = MULTIMODAL_ASSISTANT if request.img_url else DEFAULT_PROMPT
    
    # 根据是否有图片URL选择模型和调用方式
    if request.img_url:
        # 多模态对话，使用豆包模型
        def generate_response() -> Generator[str, None, None]:
            try:
                for chunk in doubao_client.chat_multimodal_stream(
                    text=request.input,
                    image_url=request.img_url,
                    system_prompt=system_prompt
                ):
                    yield f"data: {json.dumps({'chunk': chunk, 'userid': request.userid})}\n\n"
            except Exception as e:
                error_data = json.dumps({'error': str(e), 'userid': request.userid})
                yield f"data: {error_data}\n\n"
    else:
        # 文本对话，使用DeepSeek模型
        def generate_response() -> Generator[str, None, None]:
            try:
                for chunk in deepseek_client.chat_stream(
                    user_input=request.input,
                    system_prompt=system_prompt
                ):
                    yield f"data: {json.dumps({'chunk': chunk, 'userid': request.userid})}\n\n"
            except Exception as e:
                error_data = json.dumps({'error': str(e), 'userid': request.userid})
                yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@router.post("/query/sync", response_model=QueryResponse)
async def query_sync(request: QueryRequest):
    """同步查询接口"""
    
    # 验证输入
    if not request.input.strip():
        raise HTTPException(status_code=400, detail="输入内容不能为空")
    
    try:
        # 选择系统提示词
        system_prompt = MULTIMODAL_ASSISTANT if request.img_url else DEFAULT_PROMPT
        
        # 根据是否有图片URL选择模型和调用方式
        if request.img_url:
            # 多模态对话，使用豆包模型
            response = doubao_client.chat_multimodal(
                text=request.input,
                image_url=request.img_url,
                system_prompt=system_prompt
            )
        else:
            # 文本对话，使用DeepSeek模型
            response = deepseek_client.chat(
                user_input=request.input,
                system_prompt=system_prompt
            )
        
        return QueryResponse(
            response=response,
            userid=request.userid,
            success=True
        )
        
    except Exception as e:
        return QueryResponse(
            response="",
            userid=request.userid,
            success=False,
            error=str(e)
        ) 