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

## API文档

启动服务后，可以访问以下地址查看API文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 使用示例

### Python客户端示例

```python
import requests
import json

# 流式查询
def stream_query(input_text, userid="123", img_url=""):
    url = "http://localhost:8000/api/v1/query"
    data = {
        "input": input_text,
        "userid": userid,
        "img_url": img_url
    }
    
    response = requests.post(url, json=data, stream=True)
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if 'chunk' in data:
                    print(data['chunk'], end='', flush=True)
                elif 'error' in data:
                    print(f"错误: {data['error']}")

# 使用示例
stream_query("你好，请介绍一下自己")
```

### JavaScript客户端示例

```javascript
// 流式查询
async function streamQuery(inputText, userId = "123", imgUrl = "") {
    const response = await fetch('http://localhost:8000/api/v1/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input: inputText,
            userid: userId,
            img_url: imgUrl
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                try {
                    const data = JSON.parse(line.slice(6));
                    if (data.chunk) {
                        console.log(data.chunk);
                    } else if (data.error) {
                        console.error('错误:', data.error);
                    }
                } catch (e) {
                    // 忽略解析错误
                }
            }
        }
    }
}

// 使用示例
streamQuery("你好，请介绍一下自己");
```

## 注意事项

1. 确保已正确配置API密钥
2. 图片URL必须是可公开访问的
3. 输入文本长度限制为2000字符
4. 生产环境中请配置适当的CORS策略

## 许可证

MIT License 