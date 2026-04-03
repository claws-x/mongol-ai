# 字形变体处理

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [蒙古文字形变体基础](#蒙古文字形变体基础)
3. [位置变体](#位置变体)
4. [FVS 变体选择器](#fvs 变体选择器)
5. [上下文变体](#上下文变体)
6. [字体实现机制](#字体实现机制)
7. [渲染引擎支持](#渲染引擎支持)
8. [代码实现](#代码实现)
9. [测试用例](#测试用例)
10. [常见问题](#常见问题)
11. [参考资料](#参考资料)
12. [交叉引用](#交叉引用)

---

## 概述

### 什么是字形变体

字形变体 (Glyph Variants) 是指同一个 Unicode 字符在不同上下文中显示为不同视觉形式的现象。对于传统蒙古文，字形变体是其书写系统的核心特征之一。

### 为什么蒙古文需要变体

蒙古文的字形变体源于其独特的书写传统：

| 原因 | 描述 | 示例 |
|------|------|------|
| **位置变化** | 字母在词中的位置不同 | 词首、词中、词尾形式不同 |
| **历史演变** | 不同时期的书写习惯 | 古典蒙古文 vs 现代蒙古文 |
| **方言差异** | 不同地区的书写传统 | 内蒙古 vs 蒙古国 |
| **美学考虑** | 书法艺术的需要 | 不同书法风格 |

### 变体类型分类

```
蒙古文字形变体
├── 位置变体 (Positional Variants)
│   ├── 独立形式 (Isolated)
│   ├── 词首形式 (Initial)
│   ├── 词中形式 (Medial)
│   └── 词尾形式 (Final)
├── FVS 变体 (Free Variation Selectors)
│   ├── FVS1 (U+180B)
│   ├── FVS2 (U+180C)
│   └── FVS3 (U+180D)
├── 上下文变体 (Contextual Variants)
│   └── 由相邻字符决定
└── 字体变体 (Font Variants)
    └── 不同字体的设计差异
```

---

## 蒙古文字形变体基础

### Unicode 编码模型

蒙古文 Unicode 采用"基础字符 + 变体选择器"的模型：

```
基础字符 (Base Character): U+1820–U+1842
变体选择器 (Variation Selector): U+180B–U+180D
```

**编码示例**:
```
标准形式：ᠭᠠ (U+182D U+1820)
变体 1:   ᠭ︀ᠠ (U+182D U+180B U+1820)
变体 2:   ᠭ︁ᠠ (U+182D U+180C U+1820)
变体 3:   ᠭ︂ᠠ (U+182D U+180D U+1820)
```

### 变体选择器 (FVS)

| 选择器 | Unicode | 名称 | 用途 |
|--------|---------|------|------|
| FVS1 | U+180B | Free Variation Selector 1 | 选择第一变体 |
| FVS2 | U+180C | Free Variation Selector 2 | 选择第二变体 |
| FVS3 | U+180D | Free Variation Selector 3 | 选择第三变体 |
| MVS | U+180E | Mongolian Vowel Separator | 元音分隔符 |

**注意**: FVS 本身不显示，仅影响前一个字符的字形选择。

### 变体序列 (Variation Sequence)

```
变体序列 = 基础字符 + FVS

标准变体序列 (Standardized Variation Sequence, SVS):
- 由 Unicode 标准定义
- 所有字体应一致渲染
- 记录在 Unicode StandardizedVariants.txt

非标准变体序列:
- 字体自定义
- 不同字体可能渲染不同
```

---

## 位置变体

### 四种位置形式

蒙古文字母根据在词中的位置有四种基本形式：

| 形式 | 名称 | 位置 | 示例 (字母"ga") |
|------|------|------|----------------|
| 独立 | Isolated | 单字母词 | ᠭ |
| 词首 | Initial | 词的第一个字母 | ᠭᠠ (ga) |
| 词中 | Medial | 词的中间字母 | ᠠᠭᠠ (aga) |
| 词尾 | Final | 词的最后一个字母 | ᠠᠭ (ag) |

### 位置变体示例

**字母 "a" (U+1820)**:
```
独立：ᠠ
词首：ᠠᠮ (am)
词中：ᠬᠠᠯᠠ (qala)
词尾：ᠠᠮᠠ (ama)
```

**字母 "n" (U+1831)**:
```
独立：ᠨ
词首：ᠨᠣ (no)
词中：ᠠᠨᠠ (ana)
词尾：ᠠᠨ (an) - 注意词尾 n 的特殊形式
```

**字母 "ng" (U+1829)**:
```
独立：ᠩ
词首：(罕见)
词中：ᠮᠣᠩᠭᠣᠯ (monggol)
词尾：ᠮᠣᠩ (mong)
```

### 位置检测算法

字体渲染引擎通过以下规则检测位置：

```
1. 如果字符前后都是空格/标点 → 独立形式
2. 如果字符前是空格/标点，后是字母 → 词首形式
3. 如果字符前后都是字母 → 词中形式
4. 如果字符前是字母，后是空格/标点 → 词尾形式
```

**伪代码**:
```python
def get_position(char_index, text):
    prev_char = text[char_index - 1] if char_index > 0 else None
    next_char = text[char_index + 1] if char_index < len(text) - 1 else None
    
    is_prev_separator = prev_char is None or is_separator(prev_char)
    is_next_separator = next_char is None or is_separator(next_char)
    
    if is_prev_separator and is_next_separator:
        return 'isolated'
    elif is_prev_separator and not is_next_separator:
        return 'initial'
    elif not is_prev_separator and is_next_separator:
        return 'final'
    else:
        return 'medial'
```

### 特殊情况

某些字母的位置变体有特殊规则：

| 字母 | Unicode | 特殊情况 |
|------|---------|----------|
| n | U+1831 | 词尾有长尾和短尾两种形式 |
| ng | U+1829 | 极少出现在词首 |
| b | U+1834 | 词尾形式特殊 |
| k | U+182E | 位置变体差异大 |

---

## FVS 变体选择器

### FVS1 (U+180B)

**用途**: 选择字母的第一变体形式

**常见用例**:
```
ᠭᠠ (ga) + FVS1 = ᠭ︀ᠠ - 选择特定词中形式
ᠨᠠ (na) + FVS1 = ᠨ︀ᠠ - 选择特定变体
```

**示例文本**:
```
ᠮᠣᠩᠭᠣᠯ (monggol) - 标准形式
ᠮᠣᠩ︀ᠭᠣᠯ (monggol+FVS1) - 使用变体
```

### FVS2 (U+180C)

**用途**: 选择字母的第二变体形式

**常见用例**:
```
ᠭᠡ (ge) + FVS2 = ᠭ︁ᠡ - 选择特定形式
ᠯᠢ (li) + FVS2 = ᠯ︁ᠢ - 选择特定形式
```

### FVS3 (U+180D)

**用途**: 选择字母的第三变体形式

**常见用例**:
```
ᠨᠢ (ni) + FVS3 = ᠨ︂ᠢ - 选择特定形式
```

### MVS (U+180E)

**用途**: 元音分隔符，防止元音连写

**示例**:
```
ᠴᠢᠬᠤ (chiqu) - 可能被误读
ᠴᠢ᠌ᠬᠤ (chi+MVS+khu) - 明确分隔
```

### FVS 使用最佳实践

```
✅ 推荐:
- 仅在必要时使用 FVS
- 遵循 Unicode 标准变体序列
- 测试多字体渲染一致性

❌ 避免:
- 过度使用 FVS
- 依赖非标准变体序列
- 假设所有字体渲染一致
```

---

## 上下文变体

### 什么是上下文变体

上下文变体是由相邻字符触发的字形变化，通过 OpenType 的 `calt` (Contextual Alternates) 特性实现。

### 上下文规则示例

**规则 1: n 后接特定元音**
```
当 n (U+1831) 后接 i (U+1822) 时：
- 使用特殊的词中形式
- 避免与后续字母混淆
```

**规则 2: 双写辅音**
```
当相同辅音连续出现时：
- 第一个使用词中形式
- 第二个根据位置选择形式
```

**规则 3: 元音和谐**
```
当特定元音组合出现时：
- 调整字形以反映元音和谐
- 改善视觉流畅性
```

### OpenType 上下文规则

```
# OpenType 特性代码示例
feature calt {
  # 规则：n 后接 i 时的特殊形式
  sub n i by n_i.contextual;
  
  # 规则：词尾特殊形式
  sub n' space by n.final_alt;
  
  # 规则：双写字母
  sub g g by g_g.ligature;
} calt;
```

---

## 字体实现机制

### OpenType 特性表

字体通过 OpenType 特性表定义变体规则：

| 特性标签 | 名称 | 用途 |
|----------|------|------|
| `init` | Initial Forms | 词首形式 |
| `medi` | Medial Forms | 词中形式 |
| `fina` | Final Forms | 词尾形式 |
| `isol` | Isolated Forms | 独立形式 |
| `calt` | Contextual Alternates | 上下文替代 |
| `liga` | Standard Ligatures | 标准连字 |
| `rlig` | Required Ligatures | 必需连字 |
| `ccmp` | Glyph Composition | 字形组合 |

### 特性处理顺序

```
渲染引擎处理顺序:
1. ccmp (字形组合/分解)
2. init/medi/fina/isol (位置形式)
3. calt (上下文替代)
4. liga/rlig (连字)
5. mark/mkmk (标记定位)
```

### Noto Sans Mongolian 实现

```
Noto Sans Mongolian 支持的特性:
✅ ccmp - 完全支持
✅ init - 完全支持
✅ medi - 完全支持
✅ fina - 完全支持
✅ isol - 完全支持
✅ calt - 完全支持
✅ liga - 部分支持
✅ rlig - 完全支持
✅ mark - 完全支持
✅ mkmk - 完全支持
```

---

## 渲染引擎支持

### HarfBuzz (Chrome/Firefox)

**支持程度**: ⭐⭐⭐⭐⭐

```
H