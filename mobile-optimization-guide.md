# 📱 移动端优化指南

**创建日期**: 2026-04-01  
**负责人**: OpenClaw Main Agent  
**优先级**: P3-2 (长期优化)

---

## 📋 优化目标

优化蒙古文 AI 助手在移动设备（iOS/Android）上的显示和使用体验。

---

## 📊 移动端现状分析

### 浏览器支持情况（2026）

| 平台 | 浏览器 | writing-mode | text-orientation | 综合评分 |
|------|--------|--------------|------------------|----------|
| iOS 16+ | Safari | ✅ 支持 | ✅ 支持 | ⭐⭐⭐ |
| iOS 17+ | Safari | ✅ 支持 | ✅ 支持 | ⭐⭐⭐⭐ |
| Android 13+ | Chrome | ✅ 支持 | ⚠️ 部分 | ⭐⭐⭐ |
| Android 14+ | Chrome | ✅ 支持 | ✅ 支持 | ⭐⭐⭐⭐ |
| Android 13+ | Firefox | ✅ 支持 | ✅ 支持 | ⭐⭐⭐⭐ |

### 移动端特殊挑战

1. **屏幕尺寸小**
   - 键盘按键需要更大
   - 文本需要适当放大
   - 布局需要重新设计

2. **触摸交互**
   - 按键需要更大的点击区域
   - 需要防止误触
   - 需要触摸反馈

3. **性能限制**
   - 移动设备 CPU/GPU 较弱
   - 需要优化渲染性能
   - 需要减少内存占用

4. **字体加载**
   - 移动网络速度慢
   - 需要优化字体加载策略
   - 需要考虑流量消耗

---

## 🔧 优化方案

### 1. 响应式布局优化

#### 键盘布局

**桌面端** (当前):
```css
.key {
    min-width: 40px;
    max-width: 50px;
    height: 44px;
    font-size: 20px;
}
```

**移动端优化**:
```css
@media (max-width: 768px) {
    .key {
        min-width: 45px;      /* 增大按键 */
        max-width: 60px;
        height: 55px;         /* 增加高度 */
        font-size: 24px;      /* 放大字体 */
        margin: 3px;          /* 增加间距 */
    }
}

@media (max-width: 480px) {
    .key {
        min-width: 50px;
        height: 60px;
        font-size: 26px;
        margin: 4px;
    }
}
```

#### 输入框优化

**桌面端**:
```css
.mongolian-textarea {
    font-size: 24px;
    min-height: 120px;
}
```

**移动端**:
```css
@media (max-width: 768px) {
    .mongolian-textarea {
        font-size: 28px;      /* 放大字体 */
        min-height: 150px;    /* 增加高度 */
        padding: 20px;        /* 增加内边距 */
    }
}
```

### 2. 触摸优化

#### 点击区域扩大

```css
.key {
    /* 视觉大小 */
    width: 50px;
    height: 55px;
    
    /* 实际点击区域（使用 padding 扩大） */
    padding: 10px;
    margin: -10px;
    
    /* 防止误触 */
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
}
```

#### 触摸反馈

```css
.key {
    transition: transform 0.1s, background-color 0.1s;
}

.key:active {
    transform: scale(0.90);   /* 按下时缩小 */
    background-color: #667eea;
    color: white;
}

/* iOS 优化 */
@media (-webkit-touch-callout: default) {
    .key:active {
        transform: scale(0.85);  /* iOS 上更大的反馈 */
    }
}
```

#### 防止双击缩放

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```

```css
* {
    touch-action: manipulation;
    -webkit-user-select: none;  /* 防止文本选择干扰 */
    user-select: none;
}

/* 但允许输入框选择文本 */
.mongolian-textarea {
    -webkit-user-select: text;
    user-select: text;
}
```

### 3. 性能优化

#### 字体加载优化

```html
<!-- 预连接字体服务器 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 预加载字体 -->
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mongolian&display=swap" as="style">

<!-- 异步加载字体 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mongolian&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mongolian&display=swap" rel="stylesheet">
</noscript>
```

#### CSS 优化

```css
/* 使用 will-change 提示浏览器优化 */
.key {
    will-change: transform, background-color;
}

/* 避免使用昂贵的 CSS 属性 */
.key {
    /* ❌ 避免 */
    filter: blur(5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    
    /* ✅ 推荐 */
    background: linear-gradient(...);
    border: 1px solid #ddd;
}
```

#### JavaScript 优化

```javascript
// 防抖处理快速点击
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 使用防抖的输入处理
const handleInput = debounce((char) => {
    inputChar(char);
}, 50);  // 50ms 防抖
```

### 4. 竖排显示优化

#### 移动端竖排特殊处理

```css
@media (max-width: 768px) {
    .mongolian-vertical {
        font-size: 28px;      /* 移动端放大 */
        line-height: 2.2;     /* 增加行距 */
    }
    
    /* 横屏模式特殊处理 */
    @media (orientation: landscape) {
        .mongolian-vertical {
            font-size: 32px;  /* 横屏时更大 */
            max-height: 60vh; /* 限制高度 */
        }
    }
}
```

#### 安全区域适配

```css
.container {
    /* iOS 安全区域适配 */
    padding: env(safe-area-inset-top) 
             env(safe-area-inset-right) 
             env(safe-area-inset-bottom) 
             env(safe-area-inset-left);
}

/* Android 状态栏适配 */
@media (display-mode: standalone) {
    body {
        padding-top: env(safe-area-inset-top);
    }
}
```

---

## 📱 平台特殊优化

### iOS 优化

```css
/* iOS Safari 优化 */
@supports (-webkit-touch-callout: default) {
    /* iOS 特有的 CSS */
    .mongolian-textarea {
        font-size: 16px;  /* 防止 iOS 自动缩放 */
    }
    
    /* 禁用 iOS 长按菜单 */
    .key {
        -webkit-touch-callout: none;
    }
}
```

```html
<!-- iOS Web App 支持 -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="蒙古文 AI">
<link rel="apple-touch-icon" href="icon-180.png">
```

### Android 优化

```css
/* Android Chrome 优化 */
@supports (display-mode: standalone) {
    /* PWA 模式下的 CSS */
    body {
        padding-top: 24px;  /* 状态栏高度 */
    }
}
```

```html
<!-- Android PWA 支持 -->
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#667eea">
<link rel="manifest" href="manifest.json">
```

---

## 🧪 测试计划

### 测试设备

| 平台 | 设备 | 系统 | 浏览器 | 测试状态 |
|------|------|------|--------|----------|
| iOS | iPhone 14 | iOS 17 | Safari | ⏳ 待测试 |
| iOS | iPhone 13 | iOS 16 | Safari | ⏳ 待测试 |
| Android | Pixel 8 | Android 14 | Chrome | ⏳ 待测试 |
| Android | Galaxy S23 | Android 14 | Chrome | ⏳ 待测试 |
| Android | Pixel 7 | Android 13 | Firefox | ⏳ 待测试 |

### 测试项目

1. **布局测试**
   - [ ] 键盘布局正确
   - [ ] 输入框显示正常
   - [ ] 按钮大小合适

2. **交互测试**
   - [ ] 触摸反馈正常
   - [ ] 无延迟响应
   - [ ] 无意外缩放

3. **性能测试**
   - [ ] 页面加载 < 3 秒
   - [ ] 按键响应 < 100ms
   - [ ] 无明显卡顿

4. **竖排测试**
   - [ ] 蒙古文正确竖排
   - [ ] 字符方向正确
   - [ ] 字体渲染清晰

---

## 📊 优化效果预估

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| 按键大小 | 40-50px | 50-60px | +20% |
| 字体大小 | 20-24px | 24-28px | +17% |
| 点击区域 | 50px | 70px | +40% |
| 加载时间 | ~2.5s | ~1.5s | -40% |
| 触摸响应 | ~150ms | ~80ms | -47% |

---

## 📁 实施清单

### P3 阶段（长期）

- [ ] 创建移动端测试页面
- [ ] 实施响应式布局优化
- [ ] 添加触摸优化 CSS
- [ ] 优化字体加载策略
- [ ] 添加 PWA 支持
- [ ] 实际设备测试
- [ ] 性能测试和调优
- [ ] 用户反馈收集

### 预计时间线

```
2026-04-01 ──→ 2026-05-01 ──→ 2026-06-01
    │              │              │
  开始设计      实施优化      设备测试
```

---

## 📚 参考资料

- [MDN: 移动 Web 开发](https://developer.mozilla.org/zh-CN/docs/Web/Mobile)
- [iOS Safari 指南](https://developer.apple.com/safari/web/)
- [Android Chrome 指南](https://developer.chrome.com/docs/android/)
- [PWA 开发指南](https://web.dev/progressive-web-apps/)

---

**指南创建时间**: 2026-04-01 11:40 JST  
**首次实施**: 计划 2026-05-01  
**设备测试**: 计划 2026-06-01
