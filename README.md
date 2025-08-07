# AUG - AI UML Generator

**自然语言转UML图生成器** - 基于大模型的智能UML图表生成工具

<img src="readme_img/logo.png" alt="AUG Logo" width="600" height="300" class="center" />

## 📖 项目简介

AUG是一个基于大模型（DeepSeek V3 + 豆包）的智能UML图表生成工具，支持通过自然语言描述或图片上传来生成各种类型的UML图表。项目采用前后端分离架构，具备完整的会话管理、多轮对话记忆和历史存储功能。

### 🌟 核心特性

- 🤖 **智能对话**: 支持自然语言描述生成UML图
- 🖼️ **多模态输入**: 支持文本+图片的混合输入
- 📊 **多种图表**: 类图、时序图、用例图、流程图等
- 💾 **会话存储**: PostgreSQL持久化存储历史会话
- 🧠 **对话记忆**: Redis缓存多轮对话上下文
- ⚡ **流式响应**: 实时显示AI生成过程
- 🎨 **现代UI**: Vue3 + Tailwind CSS美观界面
- 🔄 **代码编辑**: 支持修改PlantUML代码重新生成
- 📝 **详细日志**: 完整的对话日志记录，包括响应时间、错误信息等
- 🖼️ **图片上传**: 支持图片上传并生成公网可访问的URL
- 🔧 **错误处理**: 完善的错误处理和降级机制

## 🏗️ 技术架构

### 后端技术栈
- **框架**: FastAPI + Python 3.10+
- **AI模型**: DeepSeek V3 (文本) + 豆包 (多模态)
- **数据库**: PostgreSQL (历史存储) + Redis (会话记忆)
- **图表引擎**: PlantUML
- **部署**: Docker + Docker Compose

### 前端技术栈
- **框架**: Vue 3 + Composition API
- **状态管理**: Pinia
- **UI组件**: Element Plus + Tailwind CSS
- **图标**: Heroicons
- **构建工具**: Vite

---

## 项目演示

### 启动项目界面

![](readme_img/first.jpg)

### 功能演示
正常对话可行，生成类图是卡片形式，点击展开

![](readme_img/use.jpg)

### 可更改的uml代码

生成之后可以更改代码重新生成

![](readme_img/code.jpg)

---

## 📁 项目结构

```
AUG/
├── api/                    # API接口层
│   ├── __init__.py
│   ├── models.py          # 数据模型
│   └── routes.py          # API路由
├── aug_web/               # 前端Vue项目
│   ├── src/
│   │   ├── components/    # Vue组件
│   │   ├── stores/        # Pinia状态管理
│   │   └── assets/        # 静态资源
│   ├── dist/              # 构建产物
│   └── package.json
├── database/              # 数据库层
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy模型
│   ├── connection.py      # 数据库连接
│   ├── redis_client.py    # Redis客户端
│   └── services.py        # 业务服务层
├── llm/                   # 大模型客户端
│   ├── __init__.py
│   ├── deepseekv3.py      # DeepSeek客户端
│   ├── doubao_flash.py    # 豆包客户端
│   └── system_prompts.py  # 系统提示词
├── util/                  # 工具模块
│   ├── plantuml_converter.py  # PlantUML转换器
│   ├── plantuml_service.py    # PlantUML服务
│   └── README.md
├── workspace/             # 工作目录
│   ├── img/               # 生成的UML图片
│   └── upload_img/        # 用户上传图片
├── sql/                   # 数据库脚本
│   └── init.sql           # 初始化脚本
├── logs/                  # 日志目录
│   └── conversation_*.log # 对话日志文件
├── docker-compose.yml     # Docker编排文件
├── requirements.txt       # Python依赖
├── config.py             # 配置文件
└── main.py               # 应用入口
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.10+ (推荐 3.10+)
- **Node.js**: 16+ (推荐 18+)
- **Docker**: 20.10+ & Docker Compose 2.0+
- **Git**: 2.30+
- **PostgreSQL**: 13+ (通过Docker提供)
- **Redis**: 6.0+ (通过Docker提供)
- **PlantUML**: 1.2023+ (系统级安装)

### 1. 克隆项目

```bash
git clone <repository-url>
cd AUG
```

### 2. 环境配置

#### 2.1 创建环境变量文件

创建 `.env` 文件：

```env
# 服务器配置
IP_ADD=118.196.22.104
PORT=8078

# 数据库配置 (Docker容器)
DATABASE_URL=postgresql://aug_user:aug_password@localhost:5432/aug_db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# AI模型API配置
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_API_KEY=your_ark_api_key_here
DOUBAO_SEED_1_6_FLASH=your_doubao_api_key_here

# 可选配置
LOG_LEVEL=INFO
LOG_DIR=logs
```

#### 2.2 系统依赖安装

**Ubuntu/Debian系统**:
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
sudo apt install -y curl wget git build-essential

# 安装PostgreSQL客户端库
sudo apt install -y postgresql-client libpq-dev

# 安装Java (PlantUML依赖)
sudo apt install -y openjdk-11-jre-headless

# 安装PlantUML
sudo apt install -y plantuml
```

**CentOS/RHEL系统**:
```bash
# 安装基础依赖
sudo yum install -y curl wget git gcc gcc-c++ make

# 安装PostgreSQL客户端库
sudo yum install -y postgresql postgresql-devel

# 安装Java
sudo yum install -y java-11-openjdk-headless

# 安装PlantUML
sudo yum install -y plantuml
```

**macOS系统**:
```bash
# 使用Homebrew安装
brew install postgresql
brew install plantuml
brew install openjdk@11
```

### 3. 安装Docker和Docker Compose

#### 3.1 安装Docker

**Ubuntu/Debian**:
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 将用户添加到docker组
sudo usermod -aG docker $USER
```

**CentOS/RHEL**:
```bash
# 安装Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker
```

**macOS**:
```bash
# 下载并安装Docker Desktop
# https://www.docker.com/products/docker-desktop
```

#### 3.2 安装Docker Compose

```bash
# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker-compose --version
```

### 4. 启动基础服务

```bash
# 启动PostgreSQL和Redis
docker-compose up -d

# 检查服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

### 5. 安装Python依赖

```bash
# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装后端依赖
pip install -r requirements.txt

# 验证安装
python -c "import fastapi, sqlalchemy, redis; print('依赖安装成功')"
```

### 6. 安装Node.js和前端依赖

#### 6.1 安装Node.js

**Ubuntu/Debian**:
```bash
# 使用NodeSource仓库安装Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

**CentOS/RHEL**:
```bash
# 使用NodeSource仓库
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# 验证安装
node --version
npm --version
```

**macOS**:
```bash
# 使用Homebrew
brew install node@18

# 或下载安装包
# https://nodejs.org/
```

#### 6.2 构建前端

```bash
# 进入前端目录
cd aug_web

# 安装依赖
npm install

# 开发模式 (可选)
npm run dev

# 生产构建
npm run build

# 返回根目录
cd ..
```

### 7. 启动应用

```bash
# 启动后端服务
python main.py

# 或后台运行
nohup python main.py > app.log 2>&1 &
```

### 8. 访问应用

- **Web界面**: http://localhost:8078
- **API文档**: http://localhost:8078/docs
- **Redis管理**: http://localhost:8081
- **PostgreSQL管理**: http://localhost:8082
- **日志文件**: `logs/conversation_YYYYMMDD.log`

## 📦 部署步骤

### 生产环境部署

#### 1. 服务器准备

**系统要求**:
- Ubuntu 20.04+ / CentOS 8+ / RHEL 8+
- 至少 2GB RAM
- 至少 10GB 可用磁盘空间
- 开放端口: 8078 (应用), 5432 (PostgreSQL), 6379 (Redis)

**基础环境安装**:
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl wget git vim htop

# 安装Docker和Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
sudo systemctl enable docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装Python依赖
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y postgresql-client libpq-dev
sudo apt install -y openjdk-11-jre-headless plantuml
```

#### 2. 代码部署

```bash
# 创建应用目录
sudo mkdir -p /opt/aug
sudo chown $USER:$USER /opt/aug

# 上传项目文件 (从本地)
scp -r AUG/* user@your-server:/opt/aug/

# 或从Git仓库克隆
cd /opt/aug
git clone https://github.com/your-repo/AUG.git .
```

#### 3. 环境配置

```bash
# 创建环境配置文件
cat > .env << EOF
# 服务器配置
IP_ADD=your-server-ip
PORT=8078

# 数据库配置
DATABASE_URL=postgresql://aug_user:aug_password@localhost:5432/aug_db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# AI模型API配置
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_API_KEY=your_deepseek_api_key
DOUBAO_SEED_1_6_FLASH=your_doubao_api_key

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=logs
EOF

# 设置权限
chmod 600 .env
```

#### 4. 启动服务

```bash
# 启动数据库服务
docker-compose up -d

# 等待数据库启动
sleep 10

# 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 构建前端
cd aug_web
npm install
npm run build
cd ..

# 创建必要目录
mkdir -p logs workspace/img workspace/upload_img
chmod 755 workspace/upload_img/

# 启动应用
python main.py
```

#### 5. 系统服务配置 (推荐)

```bash
# 创建systemd服务文件
sudo tee /etc/systemd/system/aug.service << EOF
[Unit]
Description=AUG UML Generator
After=network.target

[Service]
Type=simple
User=aug
WorkingDirectory=/opt/aug
Environment=PATH=/opt/aug/venv/bin
ExecStart=/opt/aug/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 创建用户
sudo useradd -r -s /bin/false aug
sudo chown -R aug:aug /opt/aug

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable aug
sudo systemctl start aug

# 查看状态
sudo systemctl status aug
```

#### 6. 反向代理配置 (Nginx)

```nginx
# /etc/nginx/sites-available/aug
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8078;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # 静态文件缓存
    location /assets/ {
        proxy_pass http://localhost:8078;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# 启用站点
sudo ln -s /etc/nginx/sites-available/aug /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 7. SSL证书配置 (可选)

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔧 配置说明

### 数据库配置

#### PostgreSQL配置
- **用途**: 持久化存储历史会话和消息
- **版本**: PostgreSQL 15 (Docker容器)
- **端口**: 5432
- **数据库**: aug_db
- **用户**: aug_user
- **密码**: aug_password
- **管理工具**: pgAdmin (http://localhost:8082)

#### Redis配置
- **用途**: 缓存多轮对话上下文和会话状态
- **版本**: Redis 7 (Docker容器)
- **端口**: 6379
- **数据库**: 0
- **管理工具**: Redis Commander (http://localhost:8081)

#### 数据库初始化
```bash
# 查看数据库初始化脚本
cat sql/init.sql

# 手动连接数据库 (可选)
docker exec -it aug_postgres psql -U aug_user -d aug_db

# 查看表结构
\dt
\d conversations
\d messages
```

### AI模型配置

#### 支持的模型
- **DeepSeek V3**: 处理纯文本对话
- **豆包SEED 1.6 Flash**: 处理多模态（文本+图片）对话

#### API密钥配置
```bash
# 获取API密钥
# 1. DeepSeek: https://platform.deepseek.com/
# 2. 豆包: https://platform.doubao.com/

# 配置环境变量
export ARK_API_KEY="your_deepseek_api_key"
export DOUBAO_SEED_1_6_FLASH="your_doubao_api_key"

# 或编辑.env文件
nano .env
```

#### 模型选择策略
- **纯文本对话**: 自动使用DeepSeek V3
- **多模态对话**: 优先使用豆包，失败时自动降级到DeepSeek
- **错误处理**: 完善的异常处理和重试机制

#### 本地模型 (可选) 二次开发
- 支持ollama部署本地大模型，通过http协议端口11434访问
- 支持vllm本地部署，通过http协议端口11435访问

### 日志配置

系统自动记录详细的对话日志，包括：
- **对话开始时间**: 记录用户输入和图片上传
- **首字响应时间**: 记录AI首次响应的时间
- **总响应时间**: 记录完整对话的耗时
- **错误信息**: 记录各种错误和异常
- **Token消耗**: 记录API调用消耗
- **图片生成**: 记录PlantUML图片生成过程

### PlantUML配置

#### 系统级安装
```bash
# Ubuntu/Debian
sudo apt install plantuml

# CentOS/RHEL
sudo yum install plantuml

# macOS
brew install plantuml

# 验证安装
plantuml -version
```

#### Docker版本安装 (推荐)
```bash
# 使用Docker运行PlantUML
docker run -d -p 8080:8080 plantuml/plantuml-server

# 或使用本地安装
# 下载PlantUML JAR文件
wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar

# 创建启动脚本
echo '#!/bin/bash
java -jar plantuml.jar "$@"' > /usr/local/bin/plantuml
chmod +x /usr/local/bin/plantuml
```

#### 支持的图表类型
- **类图** (Class Diagram)
- **时序图** (Sequence Diagram)
- **用例图** (Use Case Diagram)
- **活动图** (Activity Diagram)
- **状态图** (State Diagram)
- **组件图** (Component Diagram)
- **部署图** (Deployment Diagram)

### 图片上传配置

#### 上传目录结构
```
workspace/
├── img/                    # 生成的UML图片
│   └── uml_*.png
└── upload_img/            # 用户上传的图片
    └── {uuid}.{ext}
```

#### 公网访问配置
- **环境变量**: `IP_ADD` 配置服务器公网IP
- **端口**: `PORT` 配置服务端口 (默认8078)
- **URL格式**: `http://{IP_ADD}:{PORT}/api/v1/upload_images/{filename}`

#### 支持的图片格式
- **格式**: JPG, JPEG, PNG, GIF, WebP
- **大小限制**: 10MB
- **文件命名**: 自动生成UUID避免冲突

#### 安全配置
```bash
# 设置上传目录权限
chmod 755 workspace/upload_img/
chown www-data:www-data workspace/upload_img/  # 如果使用nginx

# 配置防火墙 (可选)
sudo ufw allow 8078/tcp
```

## 🛠️ 二次开发

### 添加新的AI模型

1. 在 `llm/` 目录下创建新的客户端文件
2. 实现标准接口：`chat()`, `chat_stream()`, `chat_multimodal()`
3. 在 `api/routes.py` 中集成新模型

### 扩展UML图表类型

1. 修改 `llm/system_prompts.py` 添加新的提示词
2. 更新 `util/plantuml_service.py` 支持新的图表格式
3. 前端添加相应的UI支持

### 自定义前端界面

```bash
cd aug_web

# 开发模式
npm run dev

# 修改组件
# - src/components/ - Vue组件
# - src/stores/ - 状态管理
# - tailwind.config.js - 样式配置

# 构建部署
npm run build
```

### 数据库扩展

1. 修改 `database/models.py` 添加新表或字段
2. 更新 `sql/init.sql` 初始化脚本
3. 在 `database/services.py` 中添加相应的业务方法

---

## 🐛 常见问题

### Q: 前端页面无法加载？
A: 确保已经构建前端：`cd aug_web && npm run build`

### Q: API调用失败？
A: 检查环境变量配置，确保AI模型API密钥正确

### Q: 数据库连接失败？
A: 确保Docker服务正常运行：`docker-compose ps`

### Q: PlantUML生成失败？
A: 检查PlantUML是否正确安装，或使用Docker版本

### Q: 图片上传失败？
A: 检查 `workspace/upload_img/` 目录权限

### Q: 聊天气泡显示错误？
A: 已修复消息ID冲突问题，确保消息类型正确识别

### Q: 对话历史不保存？
A: 检查PostgreSQL连接和数据库表是否正确创建

### Q: 日志文件不生成？
A: 检查 `logs/` 目录权限，确保应用有写入权限

### Q: 多模态对话失败？
A: 系统会自动降级到DeepSeek模型，检查豆包API配置


---

## 📝 API文档

### 主要接口

- `POST /api/v1/query` - 流式对话接口
- `POST /api/v1/query/sync` - 同步对话接口  
- `POST /api/v1/upload` - 图片上传接口
- `GET /api/v1/upload_images/{filename}` - 上传图片获取接口
- `GET /api/v1/images/{filename}` - 生成的UML图片获取接口
- `POST /api/v1/plantuml/convert` - PlantUML转换接口
- `POST /api/v1/conversations` - 保存对话到数据库
- `GET /api/v1/conversations` - 获取对话历史
- `DELETE /api/v1/conversations/{id}` - 删除指定对话

详细API文档请访问：http://localhost:8078/docs

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 📈 性能指标

系统会自动记录以下性能指标：
- **首字响应时间**: 通常 < 2秒
- **总响应时间**: 根据内容复杂度 5-30秒
- **图片生成时间**: 通常 < 3秒
- **并发处理能力**: 支持多用户同时使用
- **错误率**: < 1% (自动降级机制)

## 🔄 更新日志

### v1.1.0 (2025-08-07)
- ✅ 修复聊天气泡显示问题
- ✅ 添加完整的对话历史持久化
- ✅ 实现详细的日志记录系统
- ✅ 优化图片上传和公网访问
- ✅ 完善错误处理和降级机制
- ✅ 添加数据库存储API接口

### v1.0.0 (2025-08-06)
- 🎉 初始版本发布
- ✅ 基础对话功能
- ✅ PlantUML图表生成
- ✅ 多模态输入支持

## 📞 联系方式

- 项目地址: [GitHub Repository]
- 问题反馈: [Issues]
- 邮箱: wangzihan011031@163.com

---

**AUG** - 让UML图表生成变得简单智能 🚀
