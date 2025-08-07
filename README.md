# AUG - AI UML Generator

<div align="center">

![AUG Logo](readme_img/logo.png)

**自然语言转UML图生成器** - 基于大模型的智能UML图表生成工具

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[🚀 快速开始](#-快速开始) • [📖 项目简介](#-项目简介) • [🏗️ 技术架构](#️-技术架构) • [📦 部署指南](#-部署指南) • [🔧 配置说明](#-配置说明) • [🛠️ 开发指南](#️-开发指南)

</div>

---

## 📋 目录

- [📖 项目简介](#-项目简介)
  - [🌟 核心特性](#-核心特性)
  - [🎯 应用场景](#-应用场景)
- [🏗️ 技术架构](#️-技术架构)
  - [后端技术栈](#后端技术栈)
  - [前端技术栈](#前端技术栈)
- [📸 项目演示](#-项目演示)
- [📁 项目结构](#-项目结构)
- [🚀 快速开始](#-快速开始)
  - [环境要求](#环境要求)
  - [安装步骤](#安装步骤)
  - [启动应用](#启动应用)
- [📦 部署指南](#-部署指南)
  - [生产环境部署](#生产环境部署)
  - [Docker部署](#docker部署)
  - [系统服务配置](#系统服务配置)
- [🔧 配置说明](#-配置说明)
  - [数据库配置](#数据库配置)
  - [AI模型配置](#ai模型配置)
  - [日志配置](#日志配置)
- [🛠️ 开发指南](#️-开发指南)
  - [二次开发](#二次开发)
  - [API文档](#api文档)
  - [常见问题](#-常见问题)
- [📈 性能指标](#-性能指标)
- [📄 许可证](#-许可证)

---

## 📖 项目简介

AUG是一个基于大模型（DeepSeek V3 + 豆包）的智能UML图表生成工具，支持通过自然语言描述或图片上传来生成各种类型的UML图表。项目采用前后端分离架构，具备完整的会话管理、多轮对话记忆和历史存储功能。

### 🌟 核心特性

| 功能模块 | 特性描述 |
|---------|---------|
| 🤖 **智能对话** | 支持自然语言描述生成UML图 |
| 🖼️ **多模态输入** | 支持文本+图片的混合输入 |
| 📊 **多种图表** | 类图、时序图、用例图、流程图等 |
| 💾 **会话存储** | PostgreSQL持久化存储历史会话 |
| 🧠 **对话记忆** | Redis缓存多轮对话上下文 |
| ⚡ **流式响应** | 实时显示AI生成过程 |
| 🎨 **现代UI** | Vue3 + Tailwind CSS美观界面 |
| 🔄 **代码编辑** | 支持修改PlantUML代码重新生成 |
| 📝 **详细日志** | 完整的对话日志记录 |
| 🖼️ **图片上传** | 支持图片上传并生成公网可访问的URL |
| 🔧 **错误处理** | 完善的错误处理和降级机制 |

### 🎯 应用场景

- **软件设计**: 快速生成系统架构图和类图
- **需求分析**: 通过自然语言描述生成用例图
- **流程设计**: 自动生成业务流程图和时序图
- **文档生成**: 为技术文档自动生成UML图表
- **教学演示**: 辅助软件工程教学和演示

---

## 🏗️ 技术架构

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | 0.100+ | Web框架，提供高性能API |
| **Python** | 3.10+ | 主要开发语言 |
| **DeepSeek V3** | 最新 | 文本对话AI模型 |
| **豆包SEED 1.6** | Flash | 多模态AI模型 |
| **PostgreSQL** | 15 | 关系型数据库，存储历史数据 |
| **Redis** | 7 | 缓存数据库，会话记忆 |
| **PlantUML** | 1.2023+ | UML图表生成引擎 |
| **Docker** | 20.10+ | 容器化部署 |

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue 3** | 3.0+ | 前端框架 |
| **Composition API** | - | Vue 3响应式API |
| **Pinia** | 2.0+ | 状态管理 |
| **Element Plus** | 2.0+ | UI组件库 |
| **Tailwind CSS** | 3.0+ | 样式框架 |
| **Vite** | 4.0+ | 构建工具 |
| **Heroicons** | 2.0+ | 图标库 |

---

## 📸 项目演示

### 🎯 启动界面

<div align="center">

![启动界面](readme_img/first.jpg)

*简洁现代的启动界面，支持多模态输入*

</div>

### 💬 智能对话

<div align="center">

![对话演示](readme_img/use.jpg)

*自然语言生成UML图表，支持卡片式展示和展开查看*

</div>

### 🔧 代码编辑

<div align="center">

![代码编辑](readme_img/code.jpg)

*支持修改PlantUML代码，实时重新生成图表*

</div>

---

## 📁 项目结构

```
AUG/
├── 📁 api/                    # API接口层
│   ├── __init__.py
│   ├── models.py              # 数据模型定义
│   ├── routes.py              # API路由配置
│   └── logger.py              # 日志配置
├── 📁 aug_web/               # 前端Vue项目
│   ├── 📁 src/
│   │   ├── 📁 components/    # Vue组件
│   │   │   ├── ChatArea.vue      # 聊天区域组件
│   │   │   ├── MessageBubble.vue # 消息气泡组件
│   │   │   ├── UMLImageCard.vue  # UML图片卡片组件
│   │   │   └── ...
│   │   ├── 📁 stores/        # Pinia状态管理
│   │   │   └── chat.js           # 聊天状态管理
│   │   ├── 📁 assets/        # 静态资源
│   │   └── App.vue           # 主应用组件
│   ├── 📁 dist/              # 构建产物
│   ├── package.json          # 前端依赖配置
│   └── vite.config.js        # Vite构建配置
├── 📁 database/              # 数据库层
│   ├── __init__.py
│   ├── models.py              # SQLAlchemy模型
│   ├── connection.py          # 数据库连接配置
│   ├── redis_client.py        # Redis客户端
│   └── services.py            # 业务服务层
├── 📁 llm/                   # 大模型客户端
│   ├── __init__.py
│   ├── deepseekv3.py          # DeepSeek客户端
│   ├── doubao_flash.py        # 豆包客户端
│   ├── ollama_client.py       # Ollama客户端
│   └── system_prompts.py      # 系统提示词
├── 📁 util/                  # 工具模块
│   ├── plantuml_converter.py  # PlantUML转换器
│   └── plantuml_service.py    # PlantUML服务
├── 📁 workspace/             # 工作目录
│   ├── 📁 img/               # 生成的UML图片
│   └── 📁 upload_img/        # 用户上传图片
├── 📁 sql/                   # 数据库脚本
│   └── init.sql              # 数据库初始化脚本
├── 📁 logs/                  # 日志目录
├── 📁 readme_img/            # README图片资源
├── docker-compose.yml        # Docker编排文件
├── requirements.txt          # Python依赖
├── config.py                 # 应用配置
└── main.py                   # 应用入口
```

---

## 🚀 快速开始

### 环境要求

| 组件 | 最低版本 | 推荐版本 | 说明 |
|------|----------|----------|------|
| **Python** | 3.10 | 3.11+ | 主要开发语言 |
| **Node.js** | 16 | 18+ | 前端构建工具 |
| **Docker** | 20.10 | 24+ | 容器化部署 |
| **Docker Compose** | 2.0 | 2.20+ | 多容器编排 |
| **Git** | 2.30 | 2.40+ | 版本控制 |
| **PostgreSQL** | 13 | 15+ | 数据库服务 |
| **Redis** | 6.0 | 7+ | 缓存服务 |
| **PlantUML** | 1.2023 | 最新 | UML图表生成 |

### 安装步骤

#### 1️⃣ 克隆项目

```bash
git clone <repository-url>
cd AUG
```

#### 2️⃣ 环境配置

**创建环境变量文件** `.env`:

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

#### 3️⃣ 系统依赖安装

<details>
<summary><strong>Ubuntu/Debian系统</strong></summary>

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

</details>

<details>
<summary><strong>CentOS/RHEL系统</strong></summary>

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

</details>

<details>
<summary><strong>macOS系统</strong></summary>

```bash
# 使用Homebrew安装
brew install postgresql
brew install plantuml
brew install openjdk@11
```

</details>

#### 4️⃣ Docker环境配置

<details>
<summary><strong>安装Docker</strong></summary>

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

</details>

<details>
<summary><strong>安装Docker Compose</strong></summary>

```bash
# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker-compose --version
```

</details>

#### 5️⃣ 启动基础服务

```bash
# 启动PostgreSQL和Redis
docker-compose up -d

# 检查服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

#### 6️⃣ Python环境配置

```bash
# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装后端依赖
pip install -r requirements.txt

# 验证安装
python -c "import fastapi, sqlalchemy, redis; print('✅ 依赖安装成功')"
```

#### 7️⃣ 前端环境配置

<details>
<summary><strong>安装Node.js</strong></summary>

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

</details>

**构建前端**:
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

### 启动应用

```bash
# 启动后端服务
python main.py

# 或后台运行
nohup python main.py > app.log 2>&1 &
```

### 访问应用

| 服务 | 地址 | 说明 |
|------|------|------|
| **Web界面** | http://localhost:8078 | 主应用界面 |
| **API文档** | http://localhost:8078/docs | Swagger API文档 |
| **Redis管理** | http://localhost:8081 | Redis Commander |
| **PostgreSQL管理** | http://localhost:8082 | pgAdmin |
| **日志文件** | `logs/conversation_*.log` | 对话日志 |

---

## 📦 部署指南

### 生产环境部署

#### 1️⃣ 服务器准备

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

#### 2️⃣ 代码部署

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

#### 3️⃣ 环境配置

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

#### 4️⃣ 启动服务

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

#### 5️⃣ 系统服务配置

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

#### 6️⃣ 反向代理配置 (Nginx)

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

#### 7️⃣ SSL证书配置

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🔧 配置说明

### 数据库配置

#### PostgreSQL配置
| 配置项 | 值 | 说明 |
|--------|----|----|
| **用途** | 持久化存储历史会话和消息 | 主要数据存储 |
| **版本** | PostgreSQL 15 | Docker容器版本 |
| **端口** | 5432 | 默认端口 |
| **数据库** | aug_db | 数据库名称 |
| **用户** | aug_user | 数据库用户 |
| **密码** | aug_password | 数据库密码 |
| **管理工具** | pgAdmin | http://localhost:8082 |

#### Redis配置
| 配置项 | 值 | 说明 |
|--------|----|----|
| **用途** | 缓存多轮对话上下文和会话状态 | 缓存数据库 |
| **版本** | Redis 7 | Docker容器版本 |
| **端口** | 6379 | 默认端口 |
| **数据库** | 0 | 默认数据库 |
| **管理工具** | Redis Commander | http://localhost:8081 |

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
| 模型 | 用途 | 特点 |
|------|------|------|
| **DeepSeek V3** | 处理纯文本对话 | 高性能文本生成 |
| **豆包SEED 1.6 Flash** | 处理多模态（文本+图片）对话 | 多模态理解能力 |

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

#### 本地模型支持
- 支持ollama部署本地大模型，通过http协议端口11434访问
- 支持vllm本地部署，通过http协议端口11435访问

### 日志配置

系统自动记录详细的对话日志，包括：

| 日志项 | 说明 |
|--------|------|
| **对话开始时间** | 记录用户输入和图片上传 |
| **首字响应时间** | 记录AI首次响应的时间 |
| **总响应时间** | 记录完整对话的耗时 |
| **错误信息** | 记录各种错误和异常 |
| **Token消耗** | 记录API调用消耗 |
| **图片生成** | 记录PlantUML图片生成过程 |

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
| 图表类型 | 描述 | 用途 |
|----------|------|------|
| **类图** | Class Diagram | 系统架构设计 |
| **时序图** | Sequence Diagram | 交互流程设计 |
| **用例图** | Use Case Diagram | 需求分析 |
| **活动图** | Activity Diagram | 业务流程设计 |
| **状态图** | State Diagram | 状态机设计 |
| **组件图** | Component Diagram | 系统组件设计 |
| **部署图** | Deployment Diagram | 部署架构设计 |

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
| 配置项 | 说明 |
|--------|------|
| **环境变量** | `IP_ADD` 配置服务器公网IP |
| **端口** | `PORT` 配置服务端口 (默认8078) |
| **URL格式** | `http://{IP_ADD}:{PORT}/api/v1/upload_images/{filename}` |

#### 支持的图片格式
| 格式 | 大小限制 | 说明 |
|------|----------|------|
| **JPG, JPEG** | 10MB | 常用图片格式 |
| **PNG** | 10MB | 无损压缩格式 |
| **GIF** | 10MB | 动图格式 |
| **WebP** | 10MB | 现代图片格式 |

#### 安全配置
```bash
# 设置上传目录权限
chmod 755 workspace/upload_img/
chown www-data:www-data workspace/upload_img/  # 如果使用nginx

# 配置防火墙 (可选)
sudo ufw allow 8078/tcp
```

---

## 🛠️ 开发指南

### 二次开发

#### 添加新的AI模型

1. 在 `llm/` 目录下创建新的客户端文件
2. 实现标准接口：`chat()`, `chat_stream()`, `chat_multimodal()`
3. 在 `api/routes.py` 中集成新模型

#### 扩展UML图表类型

1. 修改 `llm/system_prompts.py` 添加新的提示词
2. 更新 `util/plantuml_service.py` 支持新的图表格式
3. 前端添加相应的UI支持

#### 自定义前端界面

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

#### 数据库扩展

1. 修改 `database/models.py` 添加新表或字段
2. 更新 `sql/init.sql` 初始化脚本
3. 在 `database/services.py` 中添加相应的业务方法

### API文档

#### 主要接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/query` | POST | 流式对话接口 |
| `/api/v1/query/sync` | POST | 同步对话接口 |
| `/api/v1/upload` | POST | 图片上传接口 |
| `/api/v1/upload_images/{filename}` | GET | 上传图片获取接口 |
| `/api/v1/images/{filename}` | GET | 生成的UML图片获取接口 |
| `/api/v1/plantuml/convert` | POST | PlantUML转换接口 |
| `/api/v1/conversations` | POST | 保存对话到数据库 |
| `/api/v1/conversations` | GET | 获取对话历史 |
| `/api/v1/conversations/{id}` | DELETE | 删除指定对话 |

详细API文档请访问：http://localhost:8078/docs

---

## 🐛 常见问题

<details>
<summary><strong>Q: 前端页面无法加载？</strong></summary>

**A**: 确保已经构建前端：`cd aug_web && npm run build`

</details>

<details>
<summary><strong>Q: API调用失败？</strong></summary>

**A**: 检查环境变量配置，确保AI模型API密钥正确

</details>

<details>
<summary><strong>Q: 数据库连接失败？</strong></summary>

**A**: 确保Docker服务正常运行：`docker-compose ps`

</details>

<details>
<summary><strong>Q: PlantUML生成失败？</strong></summary>

**A**: 检查PlantUML是否正确安装，或使用Docker版本

</details>

<details>
<summary><strong>Q: 图片上传失败？</strong></summary>

**A**: 检查 `workspace/upload_img/` 目录权限

</details>

<details>
<summary><strong>Q: 聊天气泡显示错误？</strong></summary>

**A**: 已修复消息ID冲突问题，确保消息类型正确识别

</details>

<details>
<summary><strong>Q: 对话历史不保存？</strong></summary>

**A**: 检查PostgreSQL连接和数据库表是否正确创建

</details>

<details>
<summary><strong>Q: 日志文件不生成？</strong></summary>

**A**: 检查 `logs/` 目录权限，确保应用有写入权限

</details>

<details>
<summary><strong>Q: 多模态对话失败？</strong></summary>

**A**: 系统会自动降级到DeepSeek模型，检查豆包API配置

</details>

---

## 📈 性能指标

系统会自动记录以下性能指标：

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **首字响应时间** | < 2秒 | AI首次响应时间 |
| **总响应时间** | 5-30秒 | 根据内容复杂度 |
| **图片生成时间** | < 3秒 | PlantUML图表生成 |
| **并发处理能力** | 多用户 | 支持多用户同时使用 |
| **错误率** | < 1% | 自动降级机制 |

---

## 📄 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件

---

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

---

## 📞 联系方式

<div align="center">

| 联系方式 | 信息 |
|----------|------|
| **项目地址** | [GitHub Repository] |
| **问题反馈** | [Issues] |
| **邮箱** | wangzihan011031@163.com |

</div>

---

<div align="center">

**AUG** - 让UML图表生成变得简单智能 🚀

[⬆️ 返回顶部](#aug---ai-uml-generator)

</div>
