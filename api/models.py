from pydantic import BaseModel, Field
from typing import Optional

class QueryRequest(BaseModel):
    """查询请求模型"""
    input: str = Field(..., description="用户输入的文本", min_length=1, max_length=2000)
    userid: str = Field(default="123", description="用户ID")
    img_url: Optional[str] = Field(default="", description="图片URL，用于多模态对话")

class QueryResponse(BaseModel):
    """查询响应模型"""
    response: str = Field(..., description="AI响应内容")
    userid: str = Field(..., description="用户ID")
    success: bool = Field(..., description="请求是否成功")
    error: Optional[str] = Field(default=None, description="错误信息")

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    message: str = Field(..., description="状态信息")
    timestamp: str = Field(..., description="时间戳") 