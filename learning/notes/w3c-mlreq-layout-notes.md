# 📖 W3C Mongolian Layout Requirements 学习笔记

**学习日期**: 2026-04-01  
**资料来源**: W3C Mongolian Layout Requirements  
**链接**: https://www.w3.org/TR/mlreq/

---

## 🎯 核心要点

### 1. 书写方向（Writing Direction）

**传统蒙古文的标准书写方式**:
- **从上到下**书写（top-to-bottom）
- **列从左到右**排列（left-to-right columns）
- 这是蒙古文的**默认书写模式**

**W3C 标准定义**:
```
writing-mode: vertical-lr
```
- `vertical` = 竖排（文字从上到下）
- `lr` = 列从左到右（left-to-right）

---

### 2. 基线（Baseline）

蒙古文竖排时的基线特点：
- 基线是**垂直的**
- 字符沿着基线从上到下排列
- 与横排文本的基线（水平）完全不同

---

### 3. 字符方向（Character Orientation）

**重要概念**:
- 蒙古文字符在竖排时应该保持**直立**（upright）
- 字符的顶部朝向**左侧**
- 这不是"旋转"90 度，而是字符的**自然方向**

**CSS 实现**:
```css
text-orientation: upright;
```

---

### 4. 行间逻辑（Inter-line Logic）

竖排蒙古文的行（列）间距：
- 列与列之间的间距应该适当
- 需要考虑蒙古文的连字特性
- 可能需要特殊的间距调整

---

## ⚠️ 关键发现：为什么 CSS 竖排不工作

### W3C 指出的问题

1. **浏览器支持不完整**
   - `writing-mode: vertical-lr` 在主流浏览器中有支持
   - 但对于**复杂文字布局**（如蒙古文）支持有限

2. **字体整形（Font Shaping）问题**
   - 蒙古文是**上下文相关**的文字
   - 同一个字符在词首、词中、词尾有不同形状
   - 需要 OpenType 字体和整形引擎支持

3. **CSS 的局限性**
   - `writing-mode` 只控制**布局方向**
   - 不处理**字符变形**和**连字**
   - 需要底层渲染引擎支持

---

## 🔧 与当前项目的关联

### 我们项目的问题

**现象**: 蒙古文"躺着"显示

**可能原因**:

| 原因 | 说明 | 优先级 |
|------|------|--------|
| 1. 容器方向错误 | `.key` 容器没有竖排 | 🔴 高 |
| 2. 字体不支持 | 缺少蒙古文 OpenType 字体 | 🟠 中 |
| 3. 浏览器限制 | Chrome 对蒙古文竖排支持有限 | 🟡 低 |
| 4. CSS 优先级 | 竖排规则被覆盖 | 🔴 高 |

### 已确认的问题

根据用户反馈和截图分析：
- ✅ **原因 1 确认**: `.key` 容器缺少竖排 CSS
- ✅ **原因 4 确认**: 部分 CSS 规则缺少 `!important`

---

## 📋 行动计划

### 立即修复（P0）

1. ✅ 所有 `.key` 容器添加竖排 CSS
2. ✅ 所有 `.key-char` 添加竖排 CSS
3. ✅ 使用 `!important` 确保优先级
4. ✅ 所有 HTML 文件引用 `mongolian-vertical.css`

### 后续优化（P1）

1. ⏳ 测试不同浏览器的显示效果
2. ⏳ 考虑使用专门的蒙古文字体
3. ⏳ 研究 HarfBuzz 整形引擎集成

### 长期研究（P2）

1. ⏳ 了解 Unicode 蒙古文编码细节
2. ⏳ 研究 OpenType 字体规则
3. ⏳ 考虑自定义渲染方案

---

## 📚 相关 W3C 文档

| 文档 | 用途 | 链接 |
|------|------|------|
| Mongolian Layout Requirements | 版式需求标准 | https://www.w3.org/TR/mlreq/ |
| Mongolian Gap Analysis | 实现缺口分析 | https://www.w3.org/TR/mong-gap/ |
| Styling vertical text | CSS 实践指南 | https://www.w3.org/International/articles/vertical-text/ |

---

**笔记完成时间**: 2026-04-01 11:00 JST  
**下一步**: 学习 W3C Gap Analysis 文档
