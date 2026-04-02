# 📊 传统蒙古文竖排技术调研报告

**报告日期**: 2026-04-01  
**调研负责人**: OpenClaw Main Agent  
**学习状态**: 进行中（18% 完成）

---

## 🎯 执行摘要

### 问题背景
用户反馈：蒙古文 AI 助手中，部分蒙古文字符"躺着"显示，而不是正确的"竖排"显示。

### 根本原因
1. **HTML 结构问题**: 蒙古文字符缺少 `.key-char` 类
2. **CSS 规则缺失**: `.key` 容器本身没有竖排规则
3. **优先级不足**: 部分 CSS 规则缺少 `!important`
4. **文件引用缺失**: 部分 HTML 未引用 `mongolian-vertical.css`

### 修复状态
- ✅ HTML 结构修复（17 个文件）
- ✅ CSS 规则修复（mongolian-vertical.css v2.1）
- ✅ 文件引用修复（6 个 HTML 文件）
- ⏳ 浏览器兼容性测试（待进行）

---

## 📚 技术标准调研

### 1. W3C 标准规范

#### 1.1 Mongolian Layout Requirements

**核心定义**:
- 书写方向：**从上到下**
- 列排列：**从左到右**
- CSS 实现：`writing-mode: vertical-lr`

**参考**: https://www.w3.org/TR/mlreq/

#### 1.2 CSS Vertical Text Styling

**标准属性**:
```css
writing-mode: vertical-lr;      /* 竖排，列从左到右 */
text-orientation: upright;      /* 字符直立（顶部朝左）*/
```

**浏览器支持**:
| 浏览器 | 支持度 | 蒙古文特殊支持 |
|--------|--------|----------------|
| Chrome | ✅ 完全 | ⚠️ 有限 |
| Firefox | ✅ 完全 | ⚠️ 有限 |
| Safari | ✅ 完全 | ⚠️ 有限 |

**参考**: https://www.w3.org/International/articles/vertical-text/

---

### 2. 技术限制与挑战

#### 2.1 CSS 的局限性

**CSS 能做的**:
- ✅ 控制文本布局方向
- ✅ 控制字符方向
- ✅ 控制间距和对齐

**CSS 不能做的**:
- ❌ 处理字符变形（词首/词中/词尾）
- ❌ 处理连字规则
- ❌ 处理变体选择符

#### 2.2 字体要求

**必需的字体特性**:
1. 支持蒙古文 Unicode 范围 (U+1800-U+18AF)
2. 支持 OpenType 整形规则
3. 支持上下文相关变形

**推荐字体**:
```css
font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
```

#### 2.3 渲染引擎

**关键组件**:
- **HarfBuzz**: 开源字体整形引擎
- **浏览器引擎**: Blink (Chrome), Gecko (Firefox), WebKit (Safari)
- **操作系统**: Windows, macOS, Linux 的字体渲染支持

---

## 🔧 修复方案

### 方案 A: CSS 修复（已实施）✅

**适用范围**: 所有 HTML 文件

**核心修复**:
```css
/* 容器竖排 */
.key {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
    -webkit-writing-mode: vertical-lr !important;
    -webkit-text-orientation: upright !important;
}

/* 字符竖排 */
.key-char {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
    -webkit-writing-mode: vertical-lr !important;
    -webkit-text-orientation: upright !important;
    font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
}
```

**优点**:
- ✅ 简单易实施
- ✅ 不需要额外依赖
- ✅ 符合 W3C 标准

**局限**:
- ⚠️ 依赖浏览器支持
- ⚠️ 不处理复杂连字
- ⚠️ 字体要求较高

---

### 方案 B: Canvas 渲染（备选）

**适用范围**: CSS 方案不工作时的备选

**核心思路**:
```javascript
// 使用 Canvas 手动绘制竖排蒙古文
function drawVerticalMongolian(text, x, y) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(Math.PI / 2);  // 旋转 90 度
    ctx.fillText(text, 0, 0);
    ctx.restore();
}
```

**优点**:
- ✅ 完全控制渲染
- ✅ 不依赖浏览器竖排支持
- ✅ 可以处理复杂布局

**局限**:
- ❌ 性能较低
- ❌ 不支持文本选择
- ❌ 实现复杂

---

### 方案 C: SVG 文本（备选）

**适用范围**: 需要高质量渲染的场景

**核心思路**:
```svg
<text writing-mode="vertical-lr" text-orientation="upright">
    ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ
</text>
```

**优点**:
- ✅ 高质量渲染
- ✅ 支持文本选择
- ✅ 可缩放

**局限**:
- ⚠️ 实现复杂
- ⚠️ 需要 SVG 知识

---

## 📋 实施检查清单

### HTML 结构

- [x] 所有蒙古文字符使用 `<span class="key-char">` 包裹
- [x] 所有 HTML 文件引用 `mongolian-vertical.css`
- [x] `lang` 属性正确设置

### CSS 规则

- [x] `.key` 容器有竖排规则
- [x] `.key-char` 字符有竖排规则
- [x] 使用 `!important` 确保优先级
- [x] 包含 `-webkit-` 前缀
- [x] `text-orientation` 设置为 `upright`
- [x] `writing-mode` 设置为 `vertical-lr`

### 字体

- [x] 加载 Noto Sans Mongolian (Google Fonts)
- [x] 有备用字体方案
- [x] 字体大小适中 (20-24px for keys, 24px for textarea)

### 测试

- [ ] Chrome 浏览器测试
- [ ] Firefox 浏览器测试
- [ ] Safari 浏览器测试
- [ ] 移动端测试
- [ ] Chrome Headless 截图验证

---

## 📊 修复统计

| 类别 | 数量 | 状态 |
|------|------|------|
| 修复的 HTML 文件 | 17 个 | ✅ 完成 |
| 修复的 CSS 文件 | 1 个 | ✅ 完成 |
| 新增的 CSS 规则 | 3 个 | ✅ 完成 |
| 新增的学习笔记 | 2 个 | ✅ 完成 |
| 技术调研报告 | 1 个 | ✅ 完成 |

---

## 📚 学习进度

| 阶段 | 资料数量 | 已完成 | 进度 |
|------|----------|--------|------|
| 阶段 1: W3C 标准 | 4 个 | 2 个 | 50% |
| 阶段 2: 底层技术 | 2 个 | 0 个 | 0% |
| 阶段 3: 研究论文 | 5 个 | 0 个 | 0% |
| **总计** | **11 个** | **2 个** | **18%** |

---

## 📌 后续工作

### 立即执行（P0）
- [ ] 浏览器兼容性测试
- [ ] 用户确认修复效果

### 短期优化（P1）
- [ ] 完成 W3C 标准学习（剩余 2 个文档）
- [ ] 学习 Unicode 编码规范
- [ ] 学习 HarfBuzz 整形引擎

### 长期研究（P2）
- [ ] 研究论文阅读（5 篇）
- [ ] 考虑 Canvas/SVG 备选方案
- [ ] 优化字体加载策略

---

## 🔗 参考资料

### W3C 标准
1. [Mongolian Layout Requirements](https://www.w3.org/TR/mlreq/)
2. [Mongolian Gap Analysis](https://www.w3.org/TR/mong-gap/)
3. [Mongolian Script Resources](https://www.w3.org/International/mlreq/mong/)
4. [Styling vertical text](https://www.w3.org/International/articles/vertical-text/)

### 研究论文
1. [A Study of Traditional Mongolian Script Encodings and Rendering](https://www.colips.org/journals/volume21/21.1.3-Biligsaikhan.pdf)
2. [A Survey on Rendering Traditional Mongolian Script](https://www.academia.edu/66087780/A_Survey_on_Rendering_Traditional_Mongolian_Script)
3. [Mongolian Script Rendering Issues](https://www.unicode.org/L2/L2010/10279-mongolian-rendering.pdf)
4. [Traditional Mongolian on Modern Devices](https://www.researchgate.net/publication/369295363_Traditional_Mongolian_on_Modern_Devices)
5. [The Digitisation Odyssey of the Mongolian Script in Unicode](https://brill.com/view/journals/inas/27/2/article-p277_6.pdf)

### 技术文档
1. [Unicode Standard 16.0](https://www.unicode.org/versions/Unicode16.0.0/UnicodeStandard-16.0.pdf)
2. [HarfBuzz Documentation](https://harfbuzz.github.io/harfbuzz-hb-buffer.html)

---

**报告完成时间**: 2026-04-01 11:10 JST  
**下次更新**: 完成阶段 2 学习后
