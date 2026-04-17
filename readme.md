# 简历分析系统

一个前后端分离的智能简历分析系统，支持 PDF 简历上传、解析、关键信息提取和岗位匹配评分。

## 项目架构

```
resume-analysis-system/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── modules/
│   │   │   ├── parser.py      # 模块一：简历上传与解析
│   │   │   ├── extractor.py   # 模块二：关键信息提取
│   │   │   ├── matcher.py     # 模块三：简历评分与匹配
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── main.py              # 模块四：结果返回与缓存
│   └── requirements.txt
└── frontend/                # 模块五：前端页面
    ├── src/
    │   ├── components/
    │   │   ├── FileUpload.vue    # 文件上传组件
    │   │   ├── ScoreDisplay.vue  # 评分展示组件
    │   │   └── InfoCard.vue      # 信息卡片组件
    │   ├── types/
    │   │   └── index.ts          # TypeScript 类型定义
    │   ├── App.vue               # 主页面
    │   ├── main.ts               # 入口文件
    │   └── vite-env.d.ts
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── tsconfig.node.json
```

## 技术选型

### 后端技术栈
- **Web 框架**: FastAPI - 现代、快速的 Python Web 框架
- **PDF 解析**: PyPDF2 - PDF 文件文本提取
- **中文分词**: jieba - 中文关键词提取
- **文本匹配**: scikit-learn - TF-IDF + 余弦相似度计算
- **ASGI 服务器**: Uvicorn - ASGI 服务器

### 前端技术栈
- **框架**: Vue 3 - 渐进式 JavaScript 框架
- **语言**: TypeScript - 类型安全的 JavaScript 超集
- **构建工具**: Vite - 下一代前端构建工具

## 功能模块说明

### 模块一：简历上传与解析
- 支持上传单个 PDF 格式的简历文件
- 兼容多页简历的文本提取
- 对提取的文本进行清洗和结构化处理（去除冗余字符、合理分段等）

### 模块二：关键信息提取
利用正则表达式从简历文本中提取以下关键信息：

**基本信息（必选）**
- 姓名
- 电话
- 邮箱
- 地址

**求职信息（加分项）**
- 求职意向
- 期望薪资

**背景信息（加分项）**
- 工作年限
- 学历背景
- 项目经历

### 模块三：简历评分与匹配
- 接收招聘岗位的需求描述（文本）
- 对岗位需求进行关键词提取和分析
- 将解析后的简历信息与岗位需求进行匹配，计算匹配度评分
  - 技能匹配率：基于关键词重叠度计算
  - 内容相似度：基于 TF-IDF + 余弦相似度计算
  - 综合评分 = 技能匹配率 × 60% + 内容相似度 × 40%

### 模块四：结果返回与缓存
- 以 JSON 格式结构化返回解析结果、关键信息和匹配度评分
- 实现内存缓存机制，对已解析和评分的简历进行缓存，避免重复计算

### 模块五：前端页面
- 使用 Vue 3 + TypeScript + Vite 构建
- 简洁美观的交互页面
- 支持拖拽上传 PDF 简历
- 实时展示匹配评分环形图
- 结构化展示所有提取信息
- 动画效果和交互反馈

## 部署方式

### 后端部署

#### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 2. 运行服务
```bash
python main.py
```
后端服务将在 http://localhost:9000 启动

#### 3. 生产环境部署
使用 Gunicorn + Uvicorn Worker：
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:9000
```

### 前端部署

#### 1. 安装依赖
```bash
cd frontend
npm install
```

#### 2. 开发模式
```bash
npm run dev
```
前端将在 http://localhost:3000 启动

#### 3. 构建生产版本
```bash
npm run build
```
构建产物将输出到 `dist` 目录

#### 4. 预览构建结果
```bash
npm run preview
```

#### 5. GitHub Pages 部署
1. 在项目根目录创建 `.github/workflows/deploy.yml`
2. 配置 GitHub Actions 自动构建和部署
3. 在仓库设置中启用 GitHub Pages

## 使用说明

### 1. 启动后端服务
```bash
cd backend
python main.py
```

### 2. 启动前端服务（新终端）
```bash
cd frontend
npm install
npm run dev
```

### 3. 访问系统
打开浏览器访问 http://localhost:3000

### 4. 使用步骤
1. **上传简历**：点击或拖拽 PDF 简历文件到上传区域
2. **填写岗位需求**：在文本框中输入招聘岗位的需求描述
3. **开始分析**：点击"开始分析"按钮
4. **查看结果**：系统将展示以下信息：
   - 匹配评分（环形图展示）
   - 技能匹配率和内容相似度
   - 匹配关键词
   - 基本信息（姓名、电话、邮箱、地址）
   - 求职信息（求职意向、期望薪资）
   - 背景信息（工作年限、学历背景、项目经历）
   - 简历原文

## API 接口文档

### POST /api/analyze
分析简历并计算匹配度

**请求参数**
- `resume`: PDF 文件（multipart/form-data）
- `job_requirement`: 岗位需求描述（字符串）

**响应示例**
```json
{
  "success": true,
  "data": {
    "raw_text": "简历原始文本...",
    "cleaned_text": "清洗后的文本...",
    "info": {
      "basic_info": {
        "name": "张三",
        "phone": "13800138000",
        "email": "zhangsan@example.com",
        "address": "北京市朝阳区"
      },
      "job_info": {
        "job_intention": "高级软件工程师",
        "expected_salary": "25K-35K"
      },
      "background_info": {
        "work_years": "5年",
        "education": "本科",
        "projects": "项目经历详情..."
      }
    },
    "match_score": {
      "overall_score": 78.5,
      "skill_match_rate": 85.0,
      "content_similarity": 68.75,
      "matched_keywords": ["Python", "FastAPI", "机器学习", ...]
    }
  }
}
```

### GET /health
健康检查接口

**响应示例**
```json
{
  "status": "ok"
}
```

## 注意事项

1. 仅支持 PDF 格式的简历文件
2. 简历格式越规范，信息提取准确率越高
3. 建议使用标准的简历模板
4. 岗位需求描述越详细，匹配结果越准确

## 项目特点

- 前后端分离架构，职责清晰
- 模块化设计，易于扩展和维护
- TypeScript 类型安全
- 内存缓存提升性能
- 美观的 UI 设计和良好的用户体验
