import os
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm.deepseekv3 import DeepSeekV3Client
from llm.doubao_flash import DOUBAO_SEED_1_6_FLASH
from api.routes import router
import dotenv

# 加载环境变量
dotenv.load_dotenv()

# class QueryRequest(BaseModel):
#     """查询请求模型"""
#     input: str
#     userid: str = "dev"
#     img_url: str = ""


# class QueryResponse(BaseModel):
#     """查询响应模型"""
#     hangye: str
#     api_tool_result: dict
#     status: str = "success"

# 创建FastAPI应用
app = FastAPI(
    title="AUG",
    description="自然语言2UML",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["AI对话"])



@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "大模型应用API服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

# @app.post("/query", summary="智能查询接口")
# async def query(request: QueryRequest) -> QueryResponse:
#     """智能查询接口"""
#     pass



@app.get("/api/health")
async def health():
    """API健康检查"""
    return {"status": "healthy", "message": "服务运行正常"}


# 模型定义
deepseekv3 = DeepSeekV3Client()
doubao_flash = DOUBAO_SEED_1_6_FLASH()




if __name__ == "__main__":
    # 从环境变量获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8077))
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
