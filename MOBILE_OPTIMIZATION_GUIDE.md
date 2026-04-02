# 📱 蒙古文 AI 助手移动端优化指南

**版本**: v1.0  
**创建日期**: 2026-04-03  
**状态**: 🟡 进行中

---

## 🎯 优化目标

| 指标 | 当前值 | 目标值 | 优先级 |
|------|--------|--------|--------|
| 移动端加载时间 | ~800ms | <500ms | P0 |
| 触摸响应延迟 | ~100ms | <50ms | P0 |
| 竖排显示正确率 | 100% | 100% | P0 |
| 屏幕适配度 | 85% | 95%+ | P1 |
| 字体加载优化 | 未优化 | 系统字体优先 | P1 |

---

## 📐 响应式断点设计

### 当前断点
```css
/* 移动端 */
@media (max-width: 768px) { ... }

/* 平板 */
@media (min-width: 769px) and (max-width: 1024px) { ... }

/* 桌面 */
@media (min-width: 1025px) { ... }
```

### 优化后断点 (推荐)
```css
/* 小屏手机 */
@media (max-width: 375px) { ... }

/* 大屏手机 */
@media (min-width: 376px) and (max-width: 428px) { ... }

/* 小屏平板 */
@media (min-width: 429px) and (max-width: 768px) { ... }

/* 大屏平板 */
@media (min-width: 769px) and (max-width: 1024px) { ... }

/* 桌面 */
@media (min-width: 1025px) { ... }
```

---

## 🔧 竖排显示移动端优化

### 问题 1: 小屏幕竖排文字过长

**解决方案**:
```css
@media (max-width: 428px) {
    .mongolian-text {
        font-size: 18px; /* 桌面 28px -> 移动 18px */
        line-height: 1.5; /* 桌面 2.0 -> 移动 1.5 */
        max-height: 300px; /* 限制最大高度 */
        overflow-y: auto; /* 允许滚动 */
    }
}
```

### 问题 2: 虚拟键盘遮挡

**解决方案**:
```css
/* 检测虚拟键盘显示 */
@supports (env(safe-area-inset-bottom)) {
    .input-container {
        padding-bottom: env(safe-area-inset-bottom);
    }
}

/* iOS Safari 键盘检测 */
.window-keyboard-visible {
    transform: translateY(-100px); /* 上移内容 */
}
```

### 问题 3: 触摸区域过小

**解决方案**:
```css
@media (max-width: 768px) {
    .btn {
        min-height: 44px; /* Apple 推荐最小触摸区域 */
        min-width: 44px;
        padding: 12px 24px;
    }
    
    .keyboard-key {
        min-width: 36px;
        min-height: 36px;
        font-size: 16px;
    }
}
```

---

## ⚡ 性能优化

### 1. 字体加载优化

**当前问题**: Google Fonts 加载慢 (~300ms)

**优化方案**:
```html
<!-- 预连接 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 字体显示交换 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mongolian&display=swap" rel="stylesheet">

<!-- 系统字体回退 -->
<style>
    .mongolian-text {
        font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', system-ui, sans-serif;
        font-display: swap;
    }
</style>
```

### 2. CSS 优化

**方案**:
```css
/* 关键 CSS 内联 */
<style>
    /* 首屏必需的竖排样式 */
    .mongolian-vertical {
        writing-mode: vertical-lr;
        text-orientation: upright;
    }
</style>

<!-- 非关键 CSS 异步加载 -->
<link rel="preload" href="mongolian-vertical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="mongolian-vertical.css"></noscript>
```

### 3. 图片优化

**方案**:
```html
<!-- WebP 格式优先 -->
<picture>
    <source srcset="image.webp" type="image/webp">
    <img src="image.png" alt="...">
</picture>

<!-- 懒加载 -->
<img src="image.jpg" loading="lazy" alt="...">
```

### 4. JavaScript 优化

**方案**:
```javascript
// 代码分割
// main.js - 核心功能
// keyboard.js - 虚拟键盘 (按需加载)
// ai-chat.js - AI 聊天 (按需加载)

// 按需加载示例
function loadKeyboard() {
    if (!window.KeyboardLoaded) {
        return import('./keyboard.js').then(module => {
            window.KeyboardLoaded = true;
            return module;
        });
    }
    return Promise.resolve();
}
```

---

## 🎨 移动端 UI 优化

### 1. 导航栏优化

```css
@media (max-width: 768px) {
    .navbar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        background: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 12px;
    }
    
    .nav-icon {
        font-size: 24px;
        margin-bottom: 4px;
    }
}
```

### 2. 输入框优化

```css
@media (max-width: 768px) {
    .mongolian-input {
        font-size: 16px; /* 防止 iOS 自动缩放 */
        min-height: 100px;
        padding: 12px;
    }
    
    .input-toolbar {
        display: flex;
        gap: 8px;
        padding: 8px;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}
```

### 3. 聊天界面优化

```css
@media (max-width: 768px) {
    .chat-container {
        height: calc(100vh - 120px); /* 减去导航栏和输入框 */
        display: flex;
        flex-direction: column;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch; /* iOS 平滑滚动 */
    }
    
    .chat-input-area {
        padding: 10px;
        background: white;
        border-top: 1px solid #e0e0e0;
    }
}
```

---

## 🧪 移动端测试清单

### 设备覆盖

- [ ] iPhone SE (小屏)
- [ ] iPhone 14/15 (标准屏)
- [ ] iPhone 14/15 Pro Max (大屏)
- [ ] iPad mini (小平板)
- [ ] iPad Air (标准平板)
- [ ] Android 手机 (多种尺寸)
- [ ] Android 平板

### 浏览器覆盖

- [ ] Safari iOS
- [ ] Chrome Android
- [ ] Firefox Mobile
- [ ] Samsung Internet

### 功能测试

- [ ] 竖排显示正确性
- [ ] 虚拟键盘响应
- [ ] 触摸手势支持
- [ ] 滚动流畅度
- [ ] 字体加载速度
- [ ] 页面加载性能
- [ ] 离线功能 (PWA)

---

## 📊 性能基准

### 目标指标 (Lighthouse)

| 指标 | 移动端目标 | 桌面端目标 |
|------|-----------|-----------|
| Performance | 90+ | 95+ |
| Accessibility | 90+ | 95+ |
| Best Practices | 90+ | 95+ |
| SEO | 90+ | 95+ |
| First Contentful Paint | <1.5s | <1.0s |
| Time to Interactive | <3.0s | <2.0s |
| Total Blocking Time | <200ms | <100ms |
| Cumulative Layout Shift | <0.1 | <0.1 |

---

## 🚀 实施计划

### Phase 1: 基础优化 (本周)
- [ ] 响应式断点调整
- [ ] 字体加载优化
- [ ] 触摸区域优化
- [ ] 基础性能测试

### Phase 2: 进阶优化 (下周)
- [ ] 代码分割实施
- [ ] PWA 支持添加
- [ ] 离线缓存配置
- [ ] 详细性能分析

### Phase 3: 深度优化 (下月)
- [ ] WebP 图片格式
- [ ] Service Worker 优化
- [ ] 预加载策略
- [ ] A/B 测试

---

## 📝 相关文档

- [PROJECT_RULES.md](PROJECT_RULES.md) - 项目规则
- [CORE_PRINCIPLE.md](CORE_PRINCIPLE.md) - 核心宗旨
- [demo-comprehensive-test.html](demo-comprehensive-test.html) - 综合测试页面

---

**最后更新**: 2026-04-03  
**维护者**: OpenClaw Main Agent
