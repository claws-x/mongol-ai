# SVG 竖排方案

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [SVG 竖排基础](#svg 竖排基础)
3. [text 元素与 writing-mode](#text 元素与 writing-mode)
4. [glyph-orientation-vertical](#glyph-orientation-vertical)
5. [完整实现方案](#完整实现方案)
6. [代码示例](#代码示例)
7. [高级技巧](#高级技巧)
8. [性能优化](#性能优化)
9. [与 CSS 方案对比](#与 css 方案对比)
10. [测试用例](#测试用例)
11. [参考资料](#参考资料)
12. [交叉引用](#交叉引用)

---

## 概述

### 为什么使用 SVG

SVG (Scalable Vector Graphics) 为传统蒙古文竖排提供了另一种实现方案，相比纯 CSS 方案具有以下优势：

| 优势 | 描述 | 重要性 |
|------|------|--------|
| **精确控制** | 每个字符位置可精确控制 | ⭐⭐⭐⭐⭐ |
| **高质量渲染** | 矢量图形，无限缩放不失真 | ⭐⭐⭐⭐⭐ |
| **跨平台一致** | 不依赖系统字体渲染引擎 | ⭐⭐⭐⭐ |
| **静态内容优化** | 适合标题、标识等静态展示 | ⭐⭐⭐⭐ |
| **动画支持** | 内置动画能力 | ⭐⭐⭐ |

### 适用场景

**推荐使用 SVG 的场景**:
- 标题、标语、标识
- 印刷品导出（PDF 生成）
- 需要高质量渲染的静态文本
- 复杂排版需求（特殊布局）
- 需要精确控制字符位置的场景

**不推荐使用 SVG 的场景**:
- 长篇幅动态内容
- 需要用户编辑的文本
- 需要搜索引擎索引的内容
- 对可访问性要求高的场景

### 技术限制

| 限制 | 描述 | 影响 |
|------|------|------|
| 不可编辑 | SVG 文本不可直接编辑 | 不适合输入场景 |
| SEO 不友好 | 搜索引擎索引困难 | 影响内容发现 |
| 文件体积 | 长文本文件体积大 | 影响加载性能 |
| 可访问性 | 屏幕阅读器支持有限 | 影响无障碍访问 |

---

## SVG 竖排基础

### 基础 SVG 结构

```xml
<svg width="400" height="600" xmlns="http://www.w3.org/2000/svg">
  <text x="50" y="100" writing-mode="vertical-lr" font-family="Noto Sans Mongolian" font-size="24">
    ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ
  </text>
</svg>
```

### SVG 坐标系

SVG 使用二维坐标系：
- **x 轴**: 从左到右递增
- **y 轴**: 从上到下递增
- **原点 (0,0)**: 左上角

对于竖排蒙古文：
- 文本从上到下排列（y 轴方向）
- 列从左到右排列（x 轴方向）

### 基础属性

```xml
<text
  x="50"                      <!-- 起始 x 坐标 -->
  y="100"                     <!-- 起始 y 坐标 -->
  writing-mode="vertical-lr"  <!-- 竖排方向 -->
  glyph-orientation-vertical="0"  <!-- 字符方向 -->
  font-family="Noto Sans Mongolian"  <!-- 字体 -->
  font-size="24"              <!-- 字号 -->
  fill="#333333"              <!-- 填充颜色 -->
  stroke="none"               <!-- 描边 -->
  text-anchor="start"         <!-- 文本对齐 -->
>
  ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ
</text>
```

---

## text 元素与 writing-mode

### writing-mode 属性

SVG 2.0 支持 CSS Writing Modes 属性：

```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <style>
    .mongolian-text {
      writing-mode: vertical-lr;
      text-orientation: upright;
      font-family: 'Noto Sans Mongolian', sans-serif;
    }
  </style>
  
  <text x="50" y="50" class="mongolian-text">
    ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃
  </text>
</svg>
```

### SVG 1.1 vs SVG 2.0

**SVG 1.1** (旧标准):
- 使用 `glyph-orientation-vertical` 属性
- 浏览器支持较好
- 功能有限

**SVG 2.0** (新标准):
- 使用 CSS `writing-mode` 和 `text-orientation`
- 与 HTML/CSS 一致
- 部分浏览器支持不完整

**建议**: 同时提供两种方案以确保兼容性

---

## glyph-orientation-vertical

### 属性说明

`glyph-orientation-vertical` 是 SVG 1.1 中控制字符方向的属性：

```xml
<text
  x="50"
  y="100"
  glyph-orientation-vertical="0"  <!-- 或 90, 180, 270 -->
  font-family="Noto Sans Mongolian"
>
  ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ
</text>
```

### 属性值

| 值 | 描述 | 蒙古文适用性 |
|----|------|--------------|
| `0` | 字符直立（顶部朝上）| ❌ 不适用 |
| `90` | 顺时针旋转 90 度 | ❌ 不适用 |
| `180` | 旋转 180 度 | ❌ 不适用 |
| `270` | 逆时针旋转 90 度（顶部朝左）| ✅ **推荐** |
| `auto` | 自动（依赖字体）| ⚠️ 不推荐 |

### 蒙古文推荐设置

```xml
<text
  x="50"
  y="100"
  writing-mode="vertical-lr"
  glyph-orientation-vertical="270"  <!-- 顶部朝左 -->
  font-family="Noto Sans Mongolian"
>
  ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ
</text>
```

**注意**: 对于蒙古文，字符应该顶部朝左，所以需要逆时针旋转 90 度（270 度或 -90 度）。

---

## 完整实现方案

### 方案 1: 纯 SVG 实现

```xml
<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .mongolian {
        font-family: 'Noto Sans Mongolian', sans-serif;
        font-size: 24px;
        fill: #333333;
        writing-mode: vertical-lr;
        glyph-orientation-vertical: 270;
        line-height: 2;
      }
    </style>
  </defs>
  
  <!-- 背景 -->
  <rect width="100%" height="100%" fill="#f5f5f5"/>
  
  <!-- 蒙古文文本 -->
  <text x="50" y="50" class="mongolian">
    ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ
    ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ
    ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ
    ᠪᠣᠯᠤᠨ᠎ᠠ᠃
  </text>
</svg>
```

### 方案 2: SVG + CSS 混合

```xml
<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        .mongolian-vertical {
          writing-mode: vertical-lr;
          text-orientation: upright;
          font-family: 'Noto Sans Mongolian', sans-serif;
          font-size: 24px;
          line-height: 2;
          color: #333;
        }
      </style>
      <div class="mongolian-vertical">
        ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃
      </div>
    </div>
  </foreignObject>
</svg>
```

**优点**: 使用 HTML/CSS 渲染，浏览器支持更好  
**缺点**: foreignObject 在某些环境不支持

### 方案 3: 字符级精确控制

```xml
<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .mongolian-char {
        font-family: 'Noto Sans Mongolian', sans-serif;
        font-size: 24px;
        fill: #333333;
      }
    </style>
  </defs>
  
  <!-- 手动定位每个字符 -->
  <text x="50" y="50" class="mongolian-char">ᠮ</text>
  <text x="50" y="80" class="mongolian-char">ᠣ</text>
  <text x="50" y="110" class="mongolian-char">ᠩ</text>
  <text x="50" y="140" class="mongolian-char">ᠭ</text>
  <text x="50" y="170" class="mongolian-char">ᠣ</text>
  <text x="50" y="200" class="mongolian-char">ᠯ</text>
  
  <!-- 第二列 -->
  <text x="100" y="50" class="mongolian-char">ᠦ</text>
  <text x="100" y="80" class="mongolian-char">ᠰ</text>
  <text x="100" y="110" class="mongolian-char">ᠦ</text>
  <text x="100" y="140" class="mongolian-char">ᠭ</text>
</svg>
```

**优点**: 完全控制每个字符位置  
**缺点**: 工作量大，不适合长文本

---

## 代码示例

### 示例 1: 竖排标题

```xml
<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4a90d9;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#357abd;stop-opacity:1" />
    </linearGradient>
    
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <!-- 背景 -->
  <rect width="100%" height="100%" fill="#f8f9fa"/>
  
  <!-- 装饰线 -->
  <line x1="150" y1="20" x2="150" y2="180" stroke="#4a90d9" stroke-width="3"/>
  
  <!-- 标题 -->
  <text
    x="200"
    y="50"
    writing-mode="vertical-lr"
    glyph-orientation-vertical="270"
    font-family="'Noto Sans Mongolian', sans-serif"
    font-size="36"
    font-weight="bold"
    fill="url(#titleGradient)"
    filter="url(#shadow)"
    letter-spacing="0.1em"
  >
    ᠮᠣᠩᠭᠣᠯ ᠠᠢ ᠲᠡᠭᠦᠰᠯᠡᠯ
  </text>
  
  <!-- 副标题 -->
  <text
    x="280"
    y="50"
    writing-mode="vertical-lr"
    glyph-orientation-vertical="270"
    font-family="'Noto Sans Mongolian', sans-serif"
    font-size="18"
    fill="#666666"
  >
    Traditional Mongolian AI Technology
  </text>
</svg>
```

### 示例 2: 多栏布局

```xml
<svg width="1000" height="600" xmlns="http://www.w3.org/2000/svg">
  <style>
    .column {
      font-family: 'Noto Sans Mongolian', sans-serif;
      font-size: 20px;
      fill: #333