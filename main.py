import os
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from llm.deepseekv3 import DeepSeekV3Client
from llm.doubao_flash import DOUBAO_SEED_1_6_FLASH
from api.routes import router
import dotenv

# 加载环境变量
dotenv.load_dotenv()
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

# 静态文件服务
app.mount("/assets", StaticFiles(directory="aug_web/dist/assets"), name="assets")

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["AI对话"])



@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    index_file = "aug_web/dist/index.html"
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        return {
            "message": "大模型应用API服务",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/v1/health",
            "note": "前端未构建，请运行 cd aug_web && npm run build"
        }



@app.get("/api/health")
async def health():
    """API健康检查"""
    return {"status": "healthy", "message": "服务运行正常"}

# 前端路由 - 处理所有非API路由
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """服务前端页面"""
    # 如果是API路由，返回404
    if full_path.startswith("api/"):
        return {"error": "API route not found", "path": full_path}
    
    # 返回前端index.html
    index_file = "aug_web/dist/index.html"
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        return {"error": "Frontend not built", "note": "Please run: cd aug_web && npm run build"}

def create_worksapce():
    if not os.path.exists("workspace"):
        os.makedirs("workspace")
    if not os.path.exists("workspace/img"):
        os.makedirs("workspace/img")
    if not os.path.exists("workspace/upload_img"):
        os.makedirs("workspace/upload_img")


if __name__ == "__main__":
    # 从环境变量获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8078))
    # 创建工作目录
    create_worksapce()
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
