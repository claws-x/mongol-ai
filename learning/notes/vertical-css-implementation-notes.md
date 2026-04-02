# 📖 W3C Vertical Text Styling 学习笔记

**学习日期**: 2026-04-01  
**资料来源**: W3C Internationalization  
**链接**: https://www.w3.org/International/articles/vertical-text/

---

## 🎯 核心要点

### 1. CSS 竖排基础

**标准 CSS 属性**:
```css
/* 书写模式 */
writing-mode: vertical-lr;  /* 竖排，列从左到右 */
writing-mode: vertical-rl;  /* 竖排，列从右到左 */

/* 字符方向 */
text-orientation: upright;      /* 字符直立 */
text-orientation: sideways;     /* 字符侧向（旋转 90 度）*/
text-orientation: mixed;        /* 混合模式 */
```

---

### 2. 浏览器支持情况

**主流浏览器支持**:

| 浏览器 | writing-mode | text-orientation | 蒙古文支持 |
|--------|--------------|------------------|------------|
| Chrome | ✅ 支持 | ✅ 支持 | ⚠️ 有限 |
| Firefox | ✅ 支持 | ✅ 支持 | ⚠️ 有限 |
| Safari | ✅ 支持 | ✅ 支持 | ⚠️ 有限 |
| Edge | ✅ 支持 | ✅ 支持 | ⚠️ 有限 |

**关键问题**:
- 基本 CSS 属性有支持
- 但**复杂文字**（蒙古文、阿拉伯文等）的竖排支持有限
- 需要字体和渲染引擎配合

---

### 3. 常见问题与解决方案

#### 问题 1: 文本方向错误

**症状**: 文字"躺着"显示

**原因**: 
- 容器没有设置 `writing-mode`
- 或者设置了但被覆盖

**解决**:
```css
.container {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
}
```

#### 问题 2: 字符旋转错误

**症状**: 字符方向不对（顶部不朝左）

**原因**:
- `text-orientation` 设置错误
- 使用了 `sideways` 而不是 `upright`

**解决**:
```css
.text {
    text-orientation: upright !important;  /* 不是 sideways */
}
```

#### 问题 3: 布局混乱

**症状**: 列顺序错误或间距异常

**原因**:
- `writing-mode` 的 lr/rl 设置错误
- 缺少适当的间距控制

**解决**:
```css
.text {
    writing-mode: vertical-lr;  /* 蒙古文用 lr */
    letter-spacing: 0.1em;      /* 调整字符间距 */
    line-height: 1.5;           /* 调整列间距 */
}
```

---

### 4. 蒙古文特殊考虑

#### 4.1 字体要求

**必需的字体特性**:
- 支持蒙古文 Unicode 范围 (U+1800-U+18AF)
- 支持 OpenType 整形规则
- 支持词首/词中/词尾变形

**推荐字体**:
```css
font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
```

#### 4.2 连字处理

蒙古文有复杂的连字规则：
- CSS `writing-mode` **不处理**连字
- 需要字体和渲染引擎支持
- HarfBuzz 是常用的整形引擎

#### 4.3 变体选择符

蒙古文使用变体选择符 (VS1, VS2, etc.) 来区分字形：
- 这些是** Unicode 编码层**的问题
- CSS 无法解决
- 需要正确的字体支持

---

## 🔧 与当前项目的关联

### 我们已做的修复

```css
/* ✅ 容器竖排 */
.key {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
    -webkit-writing-mode: vertical-lr !important;
    -webkit-text-orientation: upright !important;
}

/* ✅ 字符竖排 */
.key-char {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
    -webkit-writing-mode: vertical-lr !important;
    -webkit-text-orientation: upright !important;
    font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
}

/* ✅ 输入框竖排 */
.mongolian-textarea {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
}

/* ✅ 短语建议竖排 */
.suggestion-phrase {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
    display: inline-block;
}
```

### 还需要的优化

1. **测试不同浏览器**
   - Chrome Headless 截图验证
   - 实际浏览器中测试

2. **字体优化**
   - 确保 Noto Sans Mongolian 正确加载
   - 考虑本地字体备用方案

3. **间距调整**
   - 测试不同 `line-height` 值
   - 调整列间距

---

## 📋 检查清单

### CSS 规则检查

- [x] `.key` 容器有竖排规则
- [x] `.key-char` 字符有竖排规则
- [x] 使用 `!important` 确保优先级
- [x] 包含 `-webkit-` 前缀
- [x] `text-orientation` 设置为 `upright`
- [x] `writing-mode` 设置为 `vertical-lr`

### HTML 结构检查

- [x] 所有蒙古文字符有 `.key-char` 类
- [x] HTML 引用 `mongolian-vertical.css`
- [x] `lang` 属性设置为 `mn` 或 `zh-CN`

### 字体检查

- [x] 加载 Noto Sans Mongolian
- [x] 有备用字体方案
- [x] 字体大小适中 (20-24px)

---

## 📚 下一步学习

1. ⏳ W3C Mongolian Gap Analysis
2. ⏳ Unicode 蒙古文编码
3. ⏳ HarfBuzz 整形引擎
4. ⏳ 研究论文（编码与渲染）

---

**笔记完成时间**: 2026-04-01 11:05 JST  
**下一步**: 学习 Mongolian Gap Analysis 文档
