from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Depends
from fastapi.responses import StreamingResponse, FileResponse
from .models import QueryRequest, QueryResponse, HealthResponse, PlantUMLResult, ImageListResponse
from llm.doubao_flash import DOUBAO_SEED_1_6_FLASH
from llm.deepseekv3 import DeepSeekV3Client
from llm.system_prompts import MAIN, MAIN_IMG
from util.plantuml_service import plantuml_service
from database.services import DatabaseService
from database.connection import get_db
from .logger import conversation_logger
import json
import time
import uuid
import shutil
from typing import Generator, List, Dict, Any
from pathlib import Path
from sqlalchemy.orm import Session

router = APIRouter()

# 初始化模型客户端
doubao_client = DOUBAO_SEED_1_6_FLASH()
deepseek_client = DeepSeekV3Client()

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
    
    # 生成对话ID
    conversation_id = f"conv_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    
    # 记录对话开始
    log_entry = conversation_logger.log_conversation_start(
        conversation_id=conversation_id,
        user_id=request.userid,
        user_input=request.input,
        has_image=bool(request.img_url),
        image_url=request.img_url
    )
    start_time = log_entry["start_time"]
    
    # 选择系统提示词
    system_prompt = MAIN_IMG if request.img_url else MAIN
    
    # 根据是否有图片URL选择模型和调用方式
    if request.img_url and request.img_url.strip():
        # 有图片时，优先尝试多模态对话（豆包模型），如果失败则降级为DeepSeek
        def generate_response() -> Generator[str, None, None]:
            try:
                # 先尝试豆包多模态
                full_response = ""
                for chunk in doubao_client.chat_multimodal_stream(
                    text=request.input,
                    image_url=request.img_url,  # 现在已经是完整URL
                    system_prompt=system_prompt
                ):
                    full_response += chunk
                    yield f"data: {json.dumps({'chunk': chunk, 'userid': request.userid})}\n\n"
                
                # 处理完整的响应，提取 PlantUML 代码并转换为图片
                plantuml_result = plantuml_service.process_llm_response(full_response, request.userid)
                if plantuml_result["success"]:
                    yield f"data: {json.dumps({'plantuml_result': plantuml_result, 'userid': request.userid})}\n\n"
                    
            except Exception as e:
                # 如果豆包失败，降级为DeepSeek处理
                try:
                    enhanced_input = f"{request.input}\n\n(用户上传了图片: {request.img_url}，请根据图片内容和用户需求生成相应的UML图表)"
                    full_response = ""
                    for chunk in deepseek_client.chat_stream(
                        user_input=enhanced_input,
                        system_prompt=system_prompt
                    ):
                        full_response += chunk
                        yield f"data: {json.dumps({'chunk': chunk, 'userid': request.userid})}\n\n"
                    
                    plantuml_result = plantuml_service.process_llm_response(full_response, request.userid)
                    if plantuml_result["success"]:
                        yield f"data: {json.dumps({'plantuml_result': plantuml_result, 'userid': request.userid})}\n\n"
                        
                except Exception as fallback_error:
                    error_data = json.dumps({'error': f"多模态处理失败，降级处理也失败: {str(fallback_error)}", 'userid': request.userid})
                    yield f"data: {error_data}\n\n"
    else:
        # 文本对话，使用DeepSeek模型
        def generate_response() -> Generator[str, None, None]:
            try:
                full_response = ""
                for chunk in deepseek_client.chat_stream(
                    user_input=request.input,
                    system_prompt=system_prompt
                ):
                    full_response += chunk
                    yield f"data: {json.dumps({'chunk': chunk, 'userid': request.userid})}\n\n"
                
                # 处理完整的响应，提取 PlantUML 代码并转换为图片
                plantuml_result = plantuml_service.process_llm_response(full_response, request.userid)
                if plantuml_result["success"]:
                    yield f"data: {json.dumps({'plantuml_result': plantuml_result, 'userid': request.userid})}\n\n"
                    
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
        system_prompt = MAIN_IMG if request.img_url else MAIN
        
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
        
        # 处理响应，提取 PlantUML 代码并转换为图片
        plantuml_result = plantuml_service.process_llm_response(response, request.userid)
        
        # 构建 PlantUML 结果对象
        plantuml_result_obj = None
        if plantuml_result["success"]:
            plantuml_result_obj = PlantUMLResult(
                plantuml_code=plantuml_result["plantuml_code"],
                image_path=plantuml_result["image_path"],
                image_url=plantuml_result["image_url"],
                success=plantuml_result["success"],
                error=plantuml_result["error"]
            )
        
        return QueryResponse(
            response=response,
            userid=request.userid,
            success=True,
            plantuml_result=plantuml_result_obj
        )
        
    except Exception as e:
        return QueryResponse(
            response="",
            userid=request.userid,
            success=False,
            error=str(e)
        )

@router.get("/images/{filename}")
async def get_image(filename: str):
    """获取生成的图片"""
    image_path = Path("workspace/img") / filename
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="图片不存在")
    
    return FileResponse(
        path=str(image_path),
        media_type="image/png",
        filename=filename
    )

@router.get("/images", response_model=ImageListResponse)
async def list_images():
    """列出所有生成的图片"""
    try:
        images = plantuml_service.list_generated_images()
        return ImageListResponse(
            images=images,
            total=len(images),
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取图片列表失败: {str(e)}")

@router.post("/plantuml/convert")
async def convert_plantuml(request: dict):
    """直接转换 PlantUML 代码为图片"""
    plantuml_code = request.get("plantuml_code", "")
    userid = request.get("userid", "default")
    
    if not plantuml_code.strip():
        raise HTTPException(status_code=400, detail="PlantUML 代码不能为空")
    
    try:
        result = plantuml_service.process_llm_response(
            f"@startuml\n{plantuml_code}\n@enduml", 
            userid
        )
        
        return {
            "success": result["success"],
            "image_url": result["image_url"],
            "image_path": result["image_path"],
            "error": result["error"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}")

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """上传图片"""
    
    # 检查文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    # 检查文件大小（限制为10MB）
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
    
    try:
        # 创建上传目录
        upload_dir = Path("workspace/upload_img")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成唯一文件名
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = upload_dir / unique_filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 返回文件URL - 使用公网地址
        from config import BASE_URL
        image_url = f"{BASE_URL}/api/v1/upload_images/{unique_filename}"
        
        return {
            "success": True,
            "image_url": image_url,
            "filename": unique_filename,
            "original_name": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

@router.get("/upload_images/{filename}")
async def get_upload_image(filename: str):
    """获取上传的图片"""
    image_path = Path("workspace/upload_img") / filename
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="图片不存在")
    
    return FileResponse(
        path=str(image_path),
        media_type="image/*",
        filename=filename
    )

# 对话历史相关API
@router.post("/conversations")
async def save_conversation(
    conversation_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """保存对话到数据库"""
    try:
        db_service = DatabaseService(db)
        
        # 保存或更新对话
        conversation_id = conversation_data.get("conversation_id")
        title = conversation_data.get("title", "新对话")
        messages = conversation_data.get("messages", [])
        
        # 创建或获取对话
        conversation = await db_service.get_or_create_conversation(
            conversation_id=conversation_id,
            title=title,
            user_id="web_user"  # 默认用户ID
        )
        
        # 保存消息
        for message in messages:
            await db_service.add_message(
                conversation_id=conversation.id,
                sender_type=message.get("type", "user"),
                content=message.get("content", ""),
                meta_data={
                    "timestamp": message.get("timestamp"),
                    "image_file": message.get("imageFile"),
                    "plantuml_result": message.get("plantumlResult"),
                    "has_error": message.get("hasError", False),
                    "is_streaming": message.get("isStreaming", False)
                }
            )
        
        return {"success": True, "conversation_id": conversation.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存对话失败: {str(e)}")

@router.get("/conversations")
async def get_conversations(db: Session = Depends(get_db)):
    """获取所有对话历史"""
    try:
        db_service = DatabaseService(db)
        
        # 获取用户的所有对话
        conversations = await db_service.get_user_conversations_async("web_user")
        
        # 转换为前端格式
        result = []
        for conv in conversations:
            messages = await db_service.get_conversation_messages(conv.id)
            
            formatted_messages = []
            for msg in messages:
                formatted_msg = {
                    "id": str(msg.id),
                    "type": msg.sender_type,
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat() if msg.created_at else None
                }
                
                # 添加元数据
                if msg.meta_data:
                    formatted_msg.update({
                        "imageFile": msg.meta_data.get("image_file"),
                        "plantumlResult": msg.meta_data.get("plantuml_result"),
                        "hasError": msg.meta_data.get("has_error", False),
                        "isStreaming": msg.meta_data.get("is_streaming", False)
                    })
                
                formatted_messages.append(formatted_msg)
            
            result.append({
                "id": str(conv.id),
                "title": conv.title,
                "messages": formatted_messages,
                "createdAt": conv.created_at.isoformat() if conv.created_at else None
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取对话历史失败: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """删除指定对话"""
    try:
        db_service = DatabaseService(db)
        
        # 删除对话及其消息
        success = await db_service.delete_conversation_async(conversation_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="对话不存在")
        
        return {"success": True, "message": "对话删除成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除对话失败: {str(e)}") 