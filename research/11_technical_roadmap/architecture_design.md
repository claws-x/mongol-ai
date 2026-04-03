# 系统架构设计文档

**版本**: v1.0  
**创建时间**: 2026-04-03  
**最后更新**: 2026-04-03  
**状态**: ✅ 完成

---

## 📋 概述

本文档定义 Mongolian AI Assistant 的整体系统架构，包括技术选型、组件设计、数据流、部署方案等核心决策。

### 设计原则

1. **竖排优先**: 所有 UI 组件默认竖排显示
2. **移动优先**: 移动端体验优先于桌面端
3. **Web 原生**: HTML5 + CSS3 + JavaScript + Python
4. **开源开放**: 核心代码 MIT/Apache 2.0
5. **可验证性**: 所有决策有文档、有测试、可追溯
6. **渐进增强**: 基础功能全平台，高级功能渐进支持

---

## 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Web App   │  │  Mobile App │  │  Desktop    │     │
│  │  (PWA)      │  │  (React     │  │  (Electron) │     │
│  │             │  │   Native)   │  │             │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                          │
                          │ HTTPS / WebSocket
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Kong / Traefik (路由、限流、认证、日志)          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          │ gRPC / REST
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  Render  │ │   NLP    │ │   OCR    │ │   TTS    │  │
│  │ Service  │ │ Service  │ │ Service  │ │ Service  │  │
│  │          │ │          │ │          │ │          │  │
│  │ - 竖排   │ │ - 分词   │ │ - 检测   │ │ - 合成   │  │
│  │ - 字形   │ │ - POS    │ │ - 识别   │ │ - ASR    │  │
│  │ - FVS    │ │ - NER    │ │ - 校正   │ │ - 翻译   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │   Auth   │ │   User   │ │  Content │ │  Analytics│ │
│  │ Service  │ │ Service  │ │ Service  │ │  Service  │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Layer                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │PostgreSQL│ │   Redis  │ │  MinIO   │ │Elastic   │  │
│  │ (主数据库)│ │  (缓存)  │ │ (对象存储)│ │ (搜索)   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🖥️ 前端架构

### 技术栈

| 层次 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 框架 | React | 18.x | 组件化开发 |
| 语言 | TypeScript | 5.x | 类型安全 |
| 状态管理 | Zustand | 4.x | 轻量状态管理 |
| 路由 | React Router | 6.x | 客户端路由 |
| 样式 | Tailwind CSS | 3.x | 原子化 CSS |
| 构建 | Vite | 5.x | 快速构建 |
| 测试 | Vitest + RTL | - | 单元/集成测试 |
| PWA | Workbox | - | 离线支持 |

### 核心组件

```
src/
├── components/
│   ├── common/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   └── ...
│   │
│   ├── mongolian/
│   │   ├── MongolianText.tsx      # 竖排文本组件
│   │   ├── MongolianInput.tsx     # 竖排输入框
│   │   ├── MongolianKeyboard.tsx  # 虚拟键盘
│   │   ├── FVSSelector.tsx        # 变体选择器
│   │   └── GlyphPreview.tsx       # 字形预览
│   │
│   ├── editor/
│   │   ├── Editor.tsx             # 主编辑器
│   │   ├── Toolbar.tsx            # 工具栏
│   │   ├── FontSelector.tsx       # 字体选择
│   │   └── ExportPanel.tsx        # 导出面板
│   │
│   └── ...
│
├── hooks/
│   ├── useMongolianText.ts        # 文本处理 hook
│   ├── useFVS.ts                  # FVS 处理 hook
│   ├── useVerticalLayout.ts       # 竖排布局 hook
│   └── ...
│
├── utils/
│   ├── unicode.ts                 # Unicode 工具
│   ├── fvs.ts                     # FVS 处理
│   ├── rendering.ts               # 渲染引擎
│   └── ...
│
├── styles/
│   ├── vertical-writing.css       # 竖排样式
│   ├── fonts.css                  # 字体定义
│   └── ...
│
└── assets/
    ├── fonts/                     # 字库文件
    └── images/
```

### 竖排渲染引擎

**核心文件**: `src/core/MongolianRenderer.js`

```javascript
/**
 * 蒙古文竖排渲染引擎
 * 职责:
 * 1. 文本规范化 (NFC/NFKC)
 * 2. FVS 处理 (变体选择符)
 * 3. 字形选择 (上下文相关)
 * 4. 竖排布局计算
 * 5. SVG/Canvas 渲染
 */
class MongolianRenderer {
    constructor(options = {}) {
        this.writingMode = options.writingMode || 'vertical-lr';
        this.fontFamily = options.fontFamily || 'Noto Sans Mongolian';
        this.fvsMap = new Map(); // FVS 映射表
        this.glyphCache = new Map(); // 字形缓存
    }

    /**
     * 渲染蒙古文文本
     * @param {string} text - 输入文本
     * @param {HTMLElement} container - 容器元素
     */
    render(text, container) {
        // 1. 文本规范化
        const normalized = this.normalize(text);
        
        // 2. FVS 处理
        const withFVS = this.applyFVS(normalized);
        
        // 3. 字形选择
        const glyphs = this.selectGlyphs(withFVS);
        
        // 4. 布局计算
        const layout = this.calculateLayout(glyphs);
        
        // 5. 渲染输出
        return this.draw(layout, container);
    }

    normalize(text) {
        return text.normalize('NFC');
    }

    applyFVS(text) {
        // 处理 FVS1/FVS2/FVS3
        // 根据上下文选择正确字形
        return text;
    }

    selectGlyphs(text) {
        // 根据 Unicode 码位选择字形
        // 考虑上下文连字
        return [];
    }

    calculateLayout(glyphs) {
        // 计算竖排位置
        // 处理换行、对齐
        return [];
    }

    draw(layout, container) {
        // SVG 或 Canvas 渲染
        // 支持导出为图片/PDF
    }
}

export default MongolianRenderer;
```

### 竖排输入框

**核心文件**: `src/components/mongolian/MongolianInput.tsx`

```tsx
import React, { useRef, useEffect } from 'react';

interface MongolianInputProps {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    vertical?: boolean;
}

const MongolianInput: React.FC<MongolianInputProps> = ({
    value,
    onChange,
    placeholder,
    vertical = true
}) => {
    const inputRef = useRef<HTMLInputElement>(null);
    const svgRef = useRef<SVGSVGElement>(null);

    // 移动端降级方案：SVG 渲染 + 隐藏输入框
    useEffect(() => {
        if (vertical && isMobile()) {
            renderSVG(value, svgRef.current);
        }
    }, [value, vertical]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onChange(e.target.value);
    };

    return (
        <div className="mongolian-input-container">
            {vertical && isMobile() ? (
                <>
                    <svg ref={svgRef} className="mongolian-input-svg" />
                    <input
                        ref={inputRef}
                        type="text"
                        value={value}
                        onChange={handleChange}
                        className="hidden-input"
                        placeholder={placeholder}
                    />
                </>
            ) : (
                <input
                    ref={inputRef}
                    type="text"
                    value={value}
                    onChange={handleChange}
                    className="mongolian-input"
                    placeholder={placeholder}
                />
            )}
        </div>
    );
};

export default MongolianInput;
```

---

## 🔧 后端架构

### 技术栈

| 服务 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 主框架 | FastAPI | 0.100+ | 异步 Python |
| 语言 | Python | 3.11+ | 类型注解 |
| ORM | SQLAlchemy | 2.x | 数据库 ORM |
| 缓存 | Redis | 7.x | 会话/缓存 |
| 消息队列 | Celery + Redis | - | 异步任务 |
| 搜索 | Elasticsearch | 8.x | 全文搜索 |
| 存储 | MinIO | - | S3 兼容对象存储 |

### 服务目录

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── render.py        # 渲染 API
│   │   │   │   ├── nlp.py           # NLP API
│   │   │   │   ├── ocr.py           # OCR API
│   │   │   │   ├── tts.py           # TTS API
│   │   │   │   ├── auth.py          # 认证 API
│   │   │   │   └── user.py          # 用户 API
│   │   │   └── deps.py              # 依赖注入
│   │   └── deps.py
│   │
│   ├── core/
│   │   ├── config.py                # 配置管理
│   │   ├── security.py              # 安全模块
│   │   └── exceptions.py            # 异常处理
│   │
│   ├── models/
│   │   ├── user.py                  # 用户模型
│   │   ├── document.py              # 文档模型
│   │   └── ...
│   │
│   ├── schemas/
│   │   ├── user.py                  # 用户 Schema
│   │   ├── document.py              # 文档 Schema
│   │   └── ...
│   │
│   ├── services/
│   │   ├── renderer.py              # 渲染服务
│   │   ├── nlp.py                   # NLP 服务
│   │   ├── ocr.py                   # OCR 服务
│   │   ├── tts.py                   # TTS 服务
│   │   └── ...
│   │
│   ├── tasks/
│   │   ├── ocr_task.py              # OCR 异步任务
│   │   ├── export_task.py           # 导出任务
│   │   └── ...
│   │
│   └── utils/
│       ├── unicode.py               # Unicode 工具
│       ├── fvs.py                   # FVS 处理
│       └── ...
│
├── tests/
│   ├── test_api.py
│   ├── test_services.py
│   └── ...
│
├── alembic/                         # 数据库迁移
│   └── versions/
│
└── requirements.txt
```

### 核心 API 设计

**渲染 API**: `POST /api/v1/render`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.renderer import MongolianRendererService

router = APIRouter()

class RenderRequest(BaseModel):
    text: str
    font: str = "Noto Sans Mongolian"
    writing_mode: str = "vertical-lr"
    format: str = "svg"  # svg, png, pdf
    width: int = 800
    height: int = 600

class RenderResponse(BaseModel):
    success: bool
    data: str  # Base64 encoded
    format: str
    width: int
    height: int

@router.post("/render", response_model=RenderResponse)
async def render_text(request: RenderRequest):
    try:
        renderer = MongolianRendererService()
        result = await renderer.render(
            text=request.text,
            font=request.font,
            writing_mode=request.writing_mode,
            format=request.format,
            dimensions=(request.width, request.height)
        )
        return RenderResponse(
            success=True,
            data=result.data,
            format=request.format,
            width=result.width,
            height=result.height
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**NLP API**: `POST /api/v1/nlp/analyze`

```python
from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    text: str
    start: int
    end: int
    pos: str
    lemma: Optional[str]

class NLPRequest(BaseModel):
    text: str
    tasks: List[str] = ["tokenize", "pos", "ner"]

class NLPResponse(BaseModel):
    tokens: List[Token]
    entities: List[dict]
    dependencies: List[dict]

@router.post("/nlp/analyze", response_model=NLPResponse)
async def analyze_text(request: NLPRequest):
    nlp_service = NLPService()
    result = await nlp_service.analyze(
        text=request.text,
        tasks=request.tasks
    )
    return result
```

---

## 🗄️ 数据层设计

### 数据库 Schema

**PostgreSQL 主表**:

```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 文档表
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    font VARCHAR(100) DEFAULT 'Noto Sans Mongolian',
    writing_mode VARCHAR(50) DEFAULT 'vertical-lr',
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 字体表
CREATE TABLE fonts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    family VARCHAR(100) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    license VARCHAR(100),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- OCR 任务表
CREATE TABLE ocr_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random