# 大模型应用API

基于火山平台和豆包的大模型应用服务，支持文本对话和多模态对话。

## 功能特性

- 🤖 支持豆包SEED 1.6 Flash模型（多模态）
- 🧠 支持DeepSeek V3模型（文本对话）
- 🔄 流式响应支持
- 🌐 RESTful API接口
- 📝 自动API文档
- 🔒 输入验证和错误处理

## 项目结构

```
AUG/
├── api/                    # API相关文件
│   ├── __init__.py
│   ├── models.py          # 数据模型
│   └── routes.py          # 路由定义
├── llm/                   # 大模型客户端
│   ├── __init__.py
│   ├── doubao_flash.py    # 豆包模型
│   └── deepseekv3.py      # DeepSeek模型
├── prompt/                # 提示词
│   ├── __init__.py
│   └── system_prompts.py  # 系统提示词
├── main.py               # 主应用
├── requirements.txt      # 依赖包
└── README.md            # 项目说明
```

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 环境变量配置

创建 `.env` 文件并配置以下环境变量：

```env
# 火山平台配置
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_API_KEY=your_ark_api_key_here

# 豆包模型配置
DOUBAO_SEED_1_6_FLASH=your_doubao_api_key_here

# DeepSeek模型配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 服务器配置
HOST=0.0.0.0
PORT=8000
```

### 3. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

## API接口

### 健康检查

```http
GET /api/v1/health
```

### 流式查询

```http
POST /api/v1/query
Content-Type: application/json

{
    "input": "你好，我是小明，我今年10岁，我喜欢吃苹果",
    "userid": "123",
    "img_url": ""
}
```

### 同步查询

```http
POST /api/v1/query/sync
Content-Type: application/json

{
    "input": "你好，我是小明，我今年10岁，我喜欢吃苹果",
    "userid": "123",
    "img_url": ""
}
```

## 多模态对话

当提供 `img_url` 参数时，系统会自动使用豆包模型进行多模态对话：

```json
{
    "input": "这张图片里有什么？",
    "userid": "123",
    "img_url": "https://example.com/image.jpg"
}
```
