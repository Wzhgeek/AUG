import os
from dotenv import load_dotenv

load_dotenv()

# 服务器配置
IP_ADD = os.getenv("IP_ADD")
PORT = os.getenv("PORT", "8078")
BASE_URL = f"http://{IP_ADD}:{PORT}"

# 数据库配置
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://aug_user:aug_password@localhost:5432/aug_db"
)

# Redis配置
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# API配置
ARK_BASE_URL = os.getenv("ARK_BASE_URL")
ARK_API_KEY = os.getenv("ARK_API_KEY")
DOUBAO_SEED_1_6_FLASH = os.getenv("DOUBAO_SEED_1_6_FLASH") 