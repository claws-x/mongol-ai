# CSS 竖排技术详解

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [CSS Writing Modes 核心属性](#css-writing-modes-核心属性)
3. [传统蒙古文竖排实现](#传统蒙古文竖排实现)
4. [代码示例](#代码示例)
5. [高级技巧](#高级技巧)
6. [测试用例](#测试用例)
7. [性能优化](#性能优化)
8. [常见问题](#常见问题)
9. [参考资料](#参考资料)
10. [交叉引用](#交叉引用)

---

## 概述

### 什么是 CSS Writing Modes

CSS Writing Modes 模块定义了文本在块级容器中的书写方向，是 Web 排版的核心技术之一。对于传统蒙古文这种天然竖排的文字系统，Writing Modes 是实现 Web 渲染的基础。

### 为什么需要竖排

传统蒙古文是世界上少数几种仍然保持竖排书写的主要文字系统之一：

- **历史传承**: 800 多年的竖排书写传统
- **文字特性**: 字母形态沿垂直方向流动
- **文化认同**: 竖排是蒙古文身份的重要标志
- **阅读习惯**: 蒙古族读者习惯从上到下、从左到右阅读

### 技术挑战

在 Web 上实现高质量蒙古文竖排面临以下挑战：

| 挑战 | 描述 | 难度 |
|------|------|------|
| 浏览器兼容性 | 不同浏览器实现差异 | ⭐⭐⭐ |
| 字形方向 | 字符需要逆时针旋转 90 度 | ⭐⭐⭐⭐ |
| 混排处理 | 与拉丁文/数字混排时的方向切换 | ⭐⭐⭐⭐ |
| 输入体验 | 输入框竖排支持不完善 | ⭐⭐⭐⭐⭐ |
| 移动端适配 | 小屏幕竖排布局优化 | ⭐⭐⭐⭐⭐ |

---

## CSS Writing Modes 核心属性

### writing-mode 属性

`writing-mode` 是控制书写方向的核心属性。

```css
/* 语法 */
writing-mode: horizontal-tb | vertical-rl | vertical-lr | sideways-rl | sideways-lr;
```

#### 属性值详解

| 值 | 描述 | 行方向 | 块方向 | 适用场景 |
|----|------|--------|--------|----------|
| `horizontal-tb` | 水平书写，从上到下 | 水平 | 垂直 | 拉丁文、中文横排 |
| `vertical-rl` | 竖排，从右到左 | 垂直 | 水平（右→左） | 中文、日文传统竖排 |
| `vertical-lr` | 竖排，从左到右 | 垂直 | 水平（左→右） | **传统蒙古文** |
| `sideways-rl` | 侧排，从右到左 | 垂直 | 水平 | 特殊排版需求 |
| `sideways-lr` | 侧排，从左到右 | 垂直 | 水平 | 特殊排版需求 |

#### 蒙古文推荐设置

```css
.mongolian-vertical {
  writing-mode: vertical-lr;  /* 蒙古文标准：从左到右竖排 */
}
```

**注意**: 蒙古文使用 `vertical-lr` 而非 `vertical-rl`，这与中文/日文的传统竖排方向相反。

### text-orientation 属性

`text-orientation` 控制字符在竖排容器中的旋转方向。

```css
/* 语法 */
text-orientation: mixed | upright | sideways;
```

#### 属性值详解

| 值 | 描述 | 蒙古文适用性 |
|----|------|--------------|
| `mixed` | 混合方向（默认）| ⚠️ 不推荐 |
| `upright` | 字符直立 | ✅ **推荐** |
| `sideways` | 字符侧转 90 度 | ❌ 不适用 |

#### 蒙古文推荐设置

```css
.mongolian-vertical {
  writing-mode: vertical-lr;
  text-orientation: upright;  /* 字符保持直立，顶部朝左 */
}
```

### text-combine-upright 属性

`text-combine-upright` 用于在竖排文本中合并多个字符为一个字符宽度。

```css
/* 语法 */
text-combine-upright: none | all | digits <integer>;
```

对于蒙古文，通常不需要此属性：

```css
.mongolian-vertical {
  text-combine-upright: none;  /* 默认值，不合并字符 */
}
```

---

## 传统蒙古文竖排实现

### 基础实现

```html
<!DOCTYPE html>
<html lang="mn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>传统蒙古文竖排示例</title>
  <style>
    .mongolian-text {
      writing-mode: vertical-lr;
      text-orientation: upright;
      font-family: 'Noto Sans Mongolian', 'Microsoft Baiti', sans-serif;
      font-size: 24px;
      line-height: 1.8;
      letter-spacing: 0.05em;
    }
  </style>
</head>
<body>
  <div class="mongolian-text">
    ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭᠡᠨ ᠦᠭᠡᠢ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃
  </div>
</body>
</html>
```

### 完整样式方案

```css
/* 蒙古文竖排基础样式 */
.mongolian-vertical {
  /* 核心竖排属性 */
  writing-mode: vertical-lr;
  text-orientation: upright;
  text-combine-upright: none;
  
  /* 字体设置 */
  font-family: 'Noto Sans Mongolian', 'Microsoft Baiti', 'Mongolian Baiti', sans-serif;
  font-size: 24px;
  line-height: 2;
  letter-spacing: 0.1em;
  
  /* 布局优化 */
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  
  /* 文本对齐 */
  text-align: justify;
  text-justify: inter-ideograph;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .mongolian-vertical {
    font-size: 18px;
    line-height: 1.8;
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .mongolian-vertical {
    font-size: 16px;
    line-height: 1.6;
    padding: 10px;
  }
}
```

### 混排处理

当蒙古文与拉丁文/数字混排时，需要特殊处理：

```css
/* 混排容器 */
.mixed-text {
  writing-mode: vertical-lr;
  text-orientation: upright;
}

/* 拉丁文嵌入 */
.mixed-text .latin {
  text-orientation: sideways;  /* 拉丁文侧转 90 度 */
  writing-mode: horizontal-tb;
  display: inline-block;
  transform: rotate(90deg);
}

/* 数字保持正向 */
.mixed-text .number {
  text-orientation: upright;
}
```

```html
<div class="mixed-text">
  <span>ᠮᠣᠩᠭᠣᠯ </span>
  <span class="latin">Unicode</span>
  <span> ᠦᠰᠦᠭ U+1820</span>
</div>
```

---

## 代码示例

### 示例 1: 基础竖排段落

```html
<!DOCTYPE html>
<html lang="mn">
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: 'Noto Sans Mongolian', sans-serif;
      background: #f5f5f5;
      padding: 40px;
    }
    
    .vertical-paragraph {
      writing-mode: vertical-lr;
      text-orientation: upright;
      font-size: 20px;
      line-height: 2.2;
      letter-spacing: 0.08em;
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      max-height: 500px;
      overflow-y: auto;
    }
  </style>
</head>
<body>
  <div class="vertical-paragraph">
    ᠲᠡᠦᠬᠡ ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃ 
    ᠡᠨᠡ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠨᠢ ᠳᠦᠷᠪᠡᠯᠵᠢᠨ ᠡᠬᠡ ᠦᠰᠦᠭ ᠮᠡᠨᠳᠦ ᠭᠦᠷᠪᠡᠨ ᠵᠠᠬᠢᠨ ᠭᠠᠷᠭᠠᠭᠰᠠᠨ ᠪᠠᠶᠢᠨ᠎ᠠ᠃
  </div>
</body>
</html>
```

### 示例 2: 多栏竖排布局

```html
<!DOCTYPE html>
<html lang="mn">
<head>
  <meta charset="UTF-8">
  <style>
    .multi-column {
      display: flex;
      flex-direction: row;
      gap: 20px;
      padding: 20px;
      background: #fafafa;
    }
    
    .column {
      writing-mode: vertical-lr;
      text-orientation: upright;
      font-family: 'Noto Sans Mongolian', sans-serif;
      font-size: 18px;
      line-height: 2;
      letter-spacing: 0.05em;
      flex: 1;
      max-height: 600px;
      overflow-y: auto;
      padding: 20px;
      background: white;
      border-left: 3px solid #4a90d9;
    }
    
    .column-title {
      font-weight: bold;
      font-size: 20px;
      margin-bottom: 15px;
      color: #2c3e50;
    }
  </style>
</head>
<body>
  <div class="multi-column">
    <div class="column">
      <div class="column-title">ᠲᠡᠦᠬᠡ</div>
      <p>ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃</p>
    </div>
    <div class="column">
      <div class="column-title">ᠭᠢᠰᠡᠨ ᠲᠦᠬᠡᠢ</div>
      <p>ᠲᠡᠦᠬᠡ ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠨᠢ ᠳᠦᠷᠪᠡᠯᠵᠢᠨ ᠡᠬᠡ ᠦᠰᠦᠭ ᠮᠡᠨᠳᠦ ᠭᠦᠷᠪᠡᠨ ᠵᠠᠬᠢᠨ ᠭᠠᠷᠭᠠᠭᠰᠠᠨ ᠪᠠᠶᠢᠨ᠎ᠠ᠃ ᠡᠨᠡ ᠨᠢ ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠦᠨ ᠦᠵᠡᠭᠦᠷ ᠲᠥᠷᠥᠭᠡᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃</p>
    </div>
    <div class="column">
      <div class="column-title">ᠳᠦᠭᠦᠯᠵᠢᠯᠡᠯ</div>
      <p>ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠨᠢ ᠣᠳᠣᠭᠠᠨ ᠦᠶ᠎ᠡ ᠳᠢᠭᠢᠲᠠᠯ ᠦᠶ᠎