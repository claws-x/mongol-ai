# 移动端竖排优化方案

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [移动端竖排挑战](#移动端竖排挑战)
3. [响应式布局策略](#响应式布局策略)
4. [触摸交互优化](#触摸交互优化)
5. [性能优化](#性能优化)
6. [输入体验优化](#输入体验优化)
7. [代码实现](#代码实现)
8. [测试清单](#测试清单)
9. [参考资料](#参考资料)

---

## 概述

### 为什么移动端优先

传统蒙古文的数字化面临独特的移动端挑战：

| 指标 | 桌面端 | 移动端 |
|------|--------|--------|
| 屏幕宽度 | 1024px+ | 320-428px |
| 竖排栏数 | 多栏 | 单栏 |
| 字体大小 | 18-24px | 14-18px |
| 交互方式 | 鼠标 | 触摸 |
| 输入支持 | 完整 | 有限 |

**市场现状**:
- Menksoft: 桌面端为主，移动端弱
- 开源项目: 几乎无移动端优化
- **机会**: 首个移动优先的蒙古文竖排方案

### 核心设计原则

```
原则 1: 单栏优先
移动端只用单栏竖排，避免多栏切换

原则 2: 字体自适应
根据屏幕宽度动态调整字体大小

原则 3: 触摸友好
按钮尺寸 ≥ 44x44px，避免误触

原则 4: 性能优先
首屏渲染 < 1s，滚动流畅 60fps

原则 5: 降级兼容
不支持 writing-mode 时使用 SVG 降级
```

---

## 移动端竖排挑战

### 挑战 1: 屏幕空间有限

**问题**: 竖排文本需要足够宽度显示完整字符

```
桌面端：600px 宽度 → 可显示 20-25 个字符/行
移动端：375px 宽度 → 仅可显示 12-15 个字符/行
```

**影响**:
- 单行字符数减少
- 需要更多水平滚动或换列
- 阅读体验碎片化

**解决方案**:
```css
/* 动态字体大小 */
.mongolian-text {
  font-size: clamp(14px, 4vw, 18px);
  line-height: 1.8;
  letter-spacing: 0.05em;
}
```

### 挑战 2: 输入框竖排支持不完整

**问题**: iOS/Android 原生输入框不支持 `writing-mode`

| 平台 | 版本 | writing-mode 支持 |
|------|------|------------------|
| iOS Safari | 16+ | ⚠️ 部分支持 |
| Android Chrome | 110+ | ⚠️ 部分支持 |
| Android WebView |  varies | ❌ 通常不支持 |

**解决方案**:
1. 使用 `contenteditable` 自定义编辑器
2. SVG 降级方案
3. 横排输入 + 竖排预览

### 挑战 3: 滚动方向冲突

**问题**: 竖排文本水平滚动 vs 页面垂直滚动

```css
/* 问题：水平滚动与页面垂直滚动冲突 */
.vertical-container {
  writing-mode: vertical-lr;
  overflow-x: auto;  /* 水平滚动 */
}
```

**解决方案**:
```css
/* 固定高度容器，内部水平滚动 */
.vertical-scroller {
  height: 80vh;
  max-height: 600px;
  overflow-x: auto;
  overflow-y: hidden;
  
  /* 隐藏滚动条但保留功能 */
  scrollbar-width: none;  /* Firefox */
  -ms-overflow-style: none;  /* IE/Edge */
}

.vertical-scroller::-webkit-scrollbar {
  display: none;  /* Chrome/Safari */
}
```

### 挑战 4: 触摸手势冲突

**问题**: 水平滑动切换内容 vs 水平滚动文本

**解决方案**:
```javascript
// 区分单指滚动和双指切换
let touchStartX = 0;
let touchStartY = 0;

container.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
});

container.addEventListener('touchmove', (e) => {
  const deltaX = e.touches[0].clientX - touchStartX;
  const deltaY = e.touches[0].clientY - touchStartY;
  
  // 水平移动为主 → 滚动文本
  if (Math.abs(deltaX) > Math.abs(deltaY)) {
    e.preventDefault();  // 阻止页面滚动
  }
  // 垂直移动为主 → 页面滚动
});
```

---

## 响应式布局策略

### 断点设计

```css
/* 移动优先断点 */
:root {
  --font-size-mobile: 16px;
  --font-size-tablet: 18px;
  --font-size-desktop: 20px;
  
  --line-height-mobile: 1.6;
  --line-height-tablet: 1.8;
  --line-height-desktop: 2.0;
}

/* 基础样式 (移动优先) */
.mongolian-vertical {
  writing-mode: vertical-lr;
  text-orientation: upright;
  font-size: var(--font-size-mobile);
  line-height: var(--line-height-mobile);
  letter-spacing: 0.05em;
}

/* 平板优化 */
@media (min-width: 768px) {
  .mongolian-vertical {
    font-size: var(--font-size-tablet);
    line-height: var(--line-height-tablet);
    letter-spacing: 0.06em;
  }
}

/* 桌面优化 */
@media (min-width: 1024px) {
  .mongolian-vertical {
    font-size: var(--font-size-desktop);
    line-height: var(--line-height-desktop);
    letter-spacing: 0.08em;
  }
}
```

### 单栏 vs 多栏布局

```css
/* 移动端：单栏 */
@media (max-width: 767px) {
  .mongolian-layout {
    display: block;
  }
  
  .mongolian-column {
    max-height: 70vh;
    overflow-x: auto;
  }
}

/* 平板：可选双栏 */
@media (min-width: 768px) and (max-width: 1023px) {
  .mongolian-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
}

/* 桌面：多栏 */
@media (min-width: 1024px) {
  .mongolian-layout {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
  }
}
```

### 安全区域适配

```css
/* iOS 安全区域适配 */
.mongolian-container {
  padding: env(safe-area-inset-top) env(safe-area-inset-right) 
         env(safe-area-inset-bottom) env(safe-area-inset-left);
  
  /* 竖排时的特殊处理 */
  writing-mode: vertical-lr;
  padding-top: env(safe-area-inset-left);   /* 注意方向转换 */
  padding-right: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-right);
  padding-left: env(safe-area-inset-bottom);
}
```

---

## 触摸交互优化

### 触摸目标尺寸

```css
/* 按钮最小尺寸 44x44px (WCAG 标准) */
.mongolian-btn {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 16px;
  
  /* 触摸反馈 */
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

/* 竖排工具栏 */
.vertical-toolbar {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  
  display: flex;
  flex-direction: column;
  gap: 8px;
  
  padding: 16px 8px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 0 8px 8px 0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}
```

### 手势支持

```javascript
class MongolianTouchHandler {
  constructor(element) {
    this.element = element;
    this.touchStartX = 0;
    this.touchStartY = 0;
    this.scrollThreshold = 10;  // 滚动阈值
    
    this.init();
  }
  
  init() {
    this.element.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
    this.element.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
    this.element.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true });
  }
  
  handleTouchStart(e) {
    this.touchStartX = e.touches[0].clientX;
    this.touchStartY = e.touches[0].clientY;
  }
  
  handleTouchMove(e) {
    const deltaX = e.touches[0].clientX - this.touchStartX;
    const deltaY = e.touches[0].clientY - this.touchStartY;
    
    // 水平滚动为主
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > this.scrollThreshold) {
      e.preventDefault();  // 阻止页面垂直滚动
    }
  }
  
  handleTouchEnd(e) {
    const deltaX = e.changedTouches[0].clientX - this.touchStartX;
    
    // 快速滑动检测
    if (Math.abs(deltaX) > 100) {
      this.handleSwipe(deltaX > 0 ? 'right' : 'left');
    }
  }
  
  handleSwipe(direction) {
    // 自定义滑动处理逻辑
    console.log(`Swiped ${direction}`);
  }
}

// 使用
const touchHandler = new MongolianTouchHandler(document.querySelector('.mongolian-text'));
```

### 长按菜单

```javascript
// 长按显示操作菜单
let longPressTimer;

element.addEventListener('touchstart', (e) => {
  longPressTimer = setTimeout(() => {
    showContextMenu(e.touches[0].clientX, e.touches[0].clientY);
  }, 500);  // 500ms 长按
});

element.addEventListener('touchend', () => {
  clearTimeout(longPressTimer);
});

element.addEventListener('touchmove', () => {
  clearTimeout(longPressTimer);  // 移动取消长按
});
```

---

## 性能优化

### 字体加载优化

```css
/* 字体加载策略 */
@font-face {
  font-family: 'Noto Sans Mongolian';
  src: url('/fonts/NotoSansMongolian-Regular.woff2') format('woff2');
  font-display: swap;  /* 先显示 fallback，加载后切换 */
  unicode-range: U+1800-18AF, U+11660-1167F;  /* 仅蒙古文范围 */
}

/* Fallback 字体 */
.mongolian-text {
  font-family: 'Noto Sans Mongolian', 'Mongolian Baiti', sans-serif;
  font-size: 16px;
}

/* 加载完成后的优化 */
.font-loaded .mongolian-text {
  font-feature-settings: 'liga' 1;  /* 启用连字 */
}
```

```javascript
// 字体加载检测
if ('fonts' in document) {
  document.fonts.load('16px "Noto Sans Mongolian"').then(() => {
    document.body.classList.add('font-loaded');
  });
}
```

### 渲染优化

```css
/* 硬件加速 */
.mongolian-vertical {
  will-change: transform;
  transform: translateZ(0);  /* 触发 GPU 加速 */
  
  /* 避免重排 */
  contain: layout style;
}

/* 滚动优化 */
.vertical-scroller {
  -webkit-overflow-scrolling: touch;  /* iOS 惯性滚动 */
  overscroll-behavior: contain;  /* 阻止滚动链式传播 */
}
```

### 懒加载策略

```javascript
// 视口外内容懒加载
class MongolianLazyLoader {
  constructor() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.loadContent(entry.target);
          this.observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '100px',  // 提前 100px 加载
    });
  }
  
  observe(element) {
    this.observer.observe(element);
  }
  
  loadContent(element) {
    const src = element.dataset.src;
    if (src) {
      fetch(src)
        .then(res => res.text())
        .then(html => {
          element.innerHTML = html;
          element.classList.add('loaded');
        });
    }
  }
}

// 使用
const lazyLoader = new MongolianLazyLoader();
document.querySelectorAll('.lazy-mongolian').forEach(el => {
  lazyLoader.observe(el);
});
```

---

## 输入体验优化

### 自定义输入框方案

```html
<!-- 竖排输入编辑器 -->
<div class="mongolian-editor" contenteditable="true" autocorrect="off" autocapitalize="off">
  ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ
</div>

<!-- 横排输入 + 竖排预览 -->
<div class="input-preview-container">
  <input type="text" class="horizontal-input" placeholder="横排输入蒙古文">
  <div class="vertical-preview mongolian-vertical"></div>
</div>
```

```css
/* 自定义编辑器样式 */
.mongolian-editor {
  writing-mode: vertical-lr;
  text-orientation: upright;
  min-height: 200px;
  padding: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 18px;
  line-height: 1.8;
  
  /* 禁用默认行为 */
  outline: none;
  -webkit-user-modify: read-write;
}

.mongolian-editor:focus {
  border-color: #4a90d9;
  box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.2);
}

/* 横排输入 + 竖排预览 */
.input-preview-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.horizontal-input {
  font-size: 16px;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
}

.vertical-preview {
  writing-mode: vertical-lr;
  text-orientation: upright;
  min-height: 150px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  font-size: 18px;
}
```

```javascript
// 实时预览同步
const input = document.querySelector('.horizontal-input');
const preview = document.querySelector('.vertical-preview');

input.addEventListener('input', (e) => {
  preview.textContent = e.target.value;
});
```

### 虚拟键盘适配

```javascript
// 检测虚拟键盘显示
function detectVirtualKeyboard() {
  const initialHeight = window.innerHeight;
  
  window.addEventListener('resize', () => {
    if (window.innerHeight