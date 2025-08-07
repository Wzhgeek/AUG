# UML助手前端

这是一个基于Vue 3的UML图表生成工具前端界面，具有以下特性：

## 功能特性

- 🎨 **现代化UI设计** - 采用高级红、灰、黑配色方案
- 📱 **响应式布局** - 左侧控制台(20%) + 右侧对话区域(80%)
- 💬 **智能对话** - 支持文本输入和图片上传
- 🖼️ **UML图表生成** - 实时生成PlantUML图表
- 📋 **历史记录** - 保存和管理对话历史
- 🔍 **详情查看** - 侧边栏展示UML代码和图片
- ⚡ **流式响应** - 实时显示AI生成过程
- 🛠️ **代码编辑** - 支持修改PlantUML代码并重新生成

## 技术栈

- **Vue 3** - 采用Composition API
- **Pinia** - 状态管理
- **Tailwind CSS** - 样式框架
- **Element Plus** - UI组件库
- **Heroicons** - 图标库
- **Vite** - 构建工具

## 安装和运行

### 方式一：使用安装脚本
```bash
chmod +x install.sh
./install.sh
```

### 方式二：手动安装
```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 页面布局

### 左侧控制台 (20%)
- 应用标题和新建对话按钮
- 历史对话列表
- 对话统计信息
- 服务状态指示器

### 右侧对话区域 (80%)
- **对话界面**
  - 消息列表区域
  - 支持用户消息和AI回复
  - UML图片卡片展示
  - 流式响应动画
- **消息输入框**
  - 文本输入支持多行
  - 图片上传功能
  - 快捷键支持 (Enter发送, Shift+Enter换行)

### 详情侧边栏 (弹出式)
- **图片视图**
  - 高清UML图表显示
  - 下载和刷新功能
- **代码视图**
  - PlantUML代码编辑器
  - 代码复制功能
  - 修改后重新生成

## API接口

前端通过以下API与后端通信：

- `POST /api/query` - 流式对话接口
- `POST /api/plantuml/convert` - PlantUML代码转换
- `GET /api/images/{filename}` - 获取生成的图片

## 开发说明

### 项目结构
```
src/
├── components/          # Vue组件
│   ├── MainLayout.vue   # 主布局
│   ├── SidebarPanel.vue # 左侧控制台
│   ├── ChatArea.vue     # 对话区域
│   ├── MessageInput.vue # 消息输入
│   ├── MessageBubble.vue # 消息气泡
│   ├── UMLImageCard.vue # UML图片卡片
│   └── DetailSidebar.vue # 详情侧边栏
├── stores/              # Pinia状态管理
│   └── chat.js          # 聊天状态
└── style.css            # 全局样式
```

### 状态管理

使用Pinia管理应用状态，主要包括：
- 对话列表和当前对话
- 消息列表和实时更新
- 加载状态和错误处理
- 侧边栏显示控制

### 样式设计

- 采用Tailwind CSS响应式设计
- 自定义主题色彩（红色系主色调）
- 深色模式界面
- 平滑过渡动画效果

## 注意事项

1. 确保后端API服务运行在 `http://localhost78`
2. 支持的图片格式：JPG、PNG、GIF等常见格式
3. 建议使用现代浏览器以获得最佳体验
4. 开发时启用Vite热重载功能
