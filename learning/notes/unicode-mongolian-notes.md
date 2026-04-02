# 📖 Unicode 蒙古文编码学习笔记

**学习日期**: 2026-04-01  
**资料来源**: Unicode Standard 16.0  
**链接**: https://www.unicode.org/versions/Unicode16.0.0/

---

## 🎯 核心要点

### 1. 蒙古文 Unicode 区块

### 1.1 基本区块

| 区块名称 | Unicode 范围 | 字符数量 |
|----------|--------------|----------|
| Mongolian | U+1800 - U+18AF | 176 个字符 |
| Mongolian Supplement | U+11660 - U+1167F | 32 个字符 |

### 1.2 字符分类

**元音字母 (7 个)**:
```
U+1820 ᠠ A
U+1821 ᠡ E
U+1822 ᠢ I
U+1823 ᠣ O
U+1824 ᠤ U
U+1825 ᠥ Ö
U+1826 ᠦ Ü
```

**辅音字母 (21 个常用)**:
```
U+1828 ᠨ N
U+182A ᠪ B
U+182B ᠫ P
U+182C ᠬ Q
U+182D ᠭ G
U+182E ᠮ M
U+182F ᠯ L
U+1830 ᠰ S
U+1831 ᠱ Š
U+1832 ᠲ T
U+1833 ᠳ D
U+1834 ᠴ Č
U+1835 ᠵ J
U+1836 ᠶ Y
U+1837 ᠷ R
U+1838 ᠸ W
U+1839 ᠹ F
U+183A ᠺ K
U+183B ᠻ KHA
U+183C ᠼ TSA
U+183D ᠽ ZA
```

**标点符号**:
```
U+1800 ᠀ MONGOLIAN BIRGA
U+1801 ᠁ MONGOLIAN ELLIPSIS
U+1802 ᠂ MONGOLIAN COMMA
U+1803 ᠃ MONGOLIAN FULL STOP
U+1804 ᠄ MONGOLIAN COLON
```

**变体选择符**:
```
U+180B ᠋ MONGOLIAN FREE VARIATION SELECTOR 1 (FVS1)
U+180C ᠌ MONGOLIAN FREE VARIATION SELECTOR 2 (FVS2)
U+180D ᠍ MONGOLIAN FREE VARIATION SELECTOR 3 (FVS3)
U+180E ᠎ MONGOLIAN VOWEL SEPARATOR (MVS)
```

---

### 2. 蒙古文编码的特殊性

### 2.1 上下文相关变形

**传统蒙古文的核心特点**:
- 同一个字母在**词首**、**词中**、**词尾**有不同形状
- 这些变形**不是**通过不同 Unicode 码位实现
- 而是通过**字体整形引擎**（如 HarfBuzz）自动处理

**示例**: 字母 ᠭ (G)
```
词首形式：ᠭᠡ (ge) - 显示为词首形状
词中形式：ᠠᠭᠠ (aga) - 显示为词中形状
词尾形式：ᠠᠭ (ag) - 显示为词尾形状
```

**Unicode 编码**:
```
同一个字母 G 始终使用 U+182D
变形由字体和渲染引擎处理
```

### 2.2 变体选择符 (Variation Selectors)

**问题**: 有些情况下，同一个字母有**多种合法变形**，需要根据语义选择。

**解决方案**: 使用变体选择符 (FVS1, FVS2, FVS3)

**示例**:
```
ᠠ᠋ (A + FVS1) - 选择变体 1
ᠠ᠌ (A + FVS2) - 选择变体 2
ᠠ᠍ (A + FVS3) - 选择变体 3
```

**应用场景**:
- 区分同形异义词
- 强制特定字形
- 解决歧义

---

### 3. 蒙古文渲染流程

### 3.1 完整流程

```
Unicode 文本
    ↓
词法分析（识别词边界）
    ↓
上下文分析（词首/词中/词尾）
    ↓
变体选择符处理
    ↓
字体整形（HarfBuzz）
    ↓
字形选择（OpenType 字体）
    ↓
布局引擎（CSS writing-mode）
    ↓
最终渲染
```

### 3.2 各层职责

| 层级 | 职责 | 技术 |
|------|------|------|
| Unicode 编码 | 字符表示 | Unicode Standard |
| 变体选择 | 字形选择 | FVS1/FVS2/FVS3 |
| 字体整形 | 连字/变形 | HarfBuzz + OpenType |
| 文本布局 | 方向/间距 | CSS writing-mode |
| 字符方向 | 旋转角度 | CSS text-orientation |
| 最终渲染 | 像素输出 | 浏览器/操作系统 |

---

### 4. 常见问题与解决方案

### 4.1 问题：字符显示为方框 □

**原因**:
- 字体不支持蒙古文 Unicode 范围
- 系统缺少蒙古文字体

**解决**:
```css
font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
```

### 4.2 问题：变形不正确

**原因**:
- 字体缺少 OpenType 规则
- 渲染引擎不支持蒙古文整形

**解决**:
- 使用专业蒙古文 OpenType 字体
- 确保浏览器/系统支持 HarfBuzz

### 4.3 问题：变体选择符无效

**原因**:
- 字体不支持变体选择符
- 渲染引擎忽略 FVS

**解决**:
- 使用支持 FVS 的字体
- 报告给字体开发者

### 4.4 问题：竖排显示但字符方向错误

**原因**:
- CSS `text-orientation` 设置错误
- 使用了 `sideways` 而不是 `upright`

**解决**:
```css
text-orientation: upright !important;  /* 不是 sideways */
```

---

### 5. 与当前项目的关联

### 5.1 我们已做的修复

| 问题 | 层级 | 修复方案 | 状态 |
|------|------|----------|------|
| 蒙古文躺着 | CSS 布局 | `writing-mode: vertical-lr` | ✅ 完成 |
| 字符方向错 | CSS 方向 | `text-orientation: upright` | ✅ 完成 |
| 字体缺失 | 字体层 | Noto Sans Mongolian | ✅ 完成 |
| 连字异常 | 整形层 | 依赖浏览器 HarfBuzz | ⏳ 待测试 |
| 变体错误 | Unicode 层 | 需要 FVS 支持 | ⏳ 待研究 |

### 5.2 待优化的方面

**字体优化**:
- [ ] 测试 Noto Sans Mongolian 的连字支持
- [ ] 研究 Mongolian Baiti 的变体支持
- [ ] 考虑本地字体备用方案

**Unicode 规范化**:
- [ ] 检查所有蒙古文字符的 Unicode 编码
- [ ] 确保变体选择符正确使用
- [ ] 避免使用私有区字符

**测试验证**:
- [ ] 不同浏览器的 Unicode 支持测试
- [ ] 不同操作系统的字体渲染测试
- [ ] 移动端兼容性测试

---

## 📊 蒙古文 Unicode 快速参考

### 元音字母
| 字母 | Unicode | 名称 |
|------|---------|------|
| ᠠ | U+1820 | A |
| ᠡ | U+1821 | E |
| ᠢ | U+1822 | I |
| ᠣ | U+1823 | O |
| ᠤ | U+1824 | U |
| ᠥ | U+1825 | Ö |
| ᠦ | U+1826 | Ü |

### 常用辅音
| 字母 | Unicode | 名称 |
|------|---------|------|
| ᠨ | U+1828 | N |
| ᠪ | U+182A | B |
| ᠬ | U+182C | Q |
| ᠭ | U+182D | G |
| ᠮ | U+182E | M |
| ᠯ | U+182F | L |
| ᠰ | U+1830 | S |
| ᠲ | U+1832 | T |
| ᠶ | U+1836 | Y |

### 变体选择符
| 符号 | Unicode | 名称 |
|------|---------|------|
| ᠋ | U+180B | FVS1 |
| ᠌ | U+180C | FVS2 |
| ᠍ | U+180D | FVS3 |
| ᠎ | U+180E | MVS |

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| Unicode Standard 16.0 | https://www.unicode.org/versions/Unicode16.0.0/ |
| Unicode Mongolian Block | https://unicode.org/charts/PDF/U1800.pdf |
| W3C Mongolian Layout | https://www.w3.org/TR/mlreq/ |
| HarfBuzz Documentation | https://harfbuzz.github.io/ |

---

**笔记完成时间**: 2026-04-01 11:25 JST  
**下一步**: 学习研究论文（5 篇）
