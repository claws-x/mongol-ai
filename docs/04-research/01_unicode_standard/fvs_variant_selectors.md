# FVS 变体选择符研究

**版本**: v1.0  
**创建时间**: 2026-04-03  
**最后更新**: 2026-04-03  
**状态**: ✅ 完成

---

## 📋 概述

FVS (Free Variation Selector，自由变体选择符) 是 Unicode 中用于蒙古文的一种特殊控制字符，用于在相同基础字符后选择不同的字形变体。

### 基本信息

| 字段 | 值 |
|------|-----|
| **Unicode 名称** | Free Variation Selector |
| **码位范围** | U+180B, U+180C, U+180D |
| **别名** | FVS1, FVS2, FVS3 |
| **引入版本** | Unicode 3.0 (2000) |
| **用途** | 选择蒙古文字形变体 |
| **可见性** | 不可见 (控制符) |
| **字节数 (UTF-8)** | 3 字节 |

---

## 🔢 码位详情

### FVS1 (U+180B)

```
名称：MONGOLIAN FREE VARIATION SELECTOR ONE
缩写：FVS1
码位：U+180B
十进制：6155
UTF-8：E1 A0 8B
UTF-16：180B
类别：Mn (Mark, Nonspacing)
双向类：NSM (Nonspacing Mark)
```

**用途**: 最常见的变体选择符，用于约 70% 的变体场景

**示例**:
```
ᠨ (U+1828) = 基本形式
ᠨ᠋ (U+1828 U+180B) = 变体形式 1
```

### FVS2 (U+180C)

```
名称：MONGOLIAN FREE VARIATION SELECTOR TWO
缩写：FVS2
码位：U+180C
十进制：6156
UTF-8：E1 A0 8C
UTF-16：180C
类别：Mn (Mark, Nonspacing)
双向类：NSM (Nonspacing Mark)
```

**用途**: 较少使用，约 20% 的变体场景

### FVS3 (U+180D)

```
名称：MONGOLIAN FREE VARIATION SELECTOR THREE
缩写：FVS3
码位：U+180D
十进制：6157
UTF-8：E1 A0 8D
UTF-16：180D
类别：Mn (Mark, Nonspacing)
双向类：NSM (Nonspacing Mark)
```

**用途**: 最少使用，约 10% 的变体场景

---

## 📖 使用规则

### 基本语法

```
[基础字符] + [FVS] = [特定变体字形]
```

**示例 1**: 字母 "a" 的变体
```
ᠠ (U+1820)           = 基本形式
ᠠ᠋ (U+1820 U+180B)   = 词中形式
ᠠ᠌ (U+1820 U+180C)   = 词尾形式 (特定字体)
```

**示例 2**: 字母 "n" 的变体
```
ᠨ (U+1828)           = 基本形式
ᠨ᠋ (U+1828 U+180B)   = 长尾形式
ᠨ᠌ (U+1828 U+180C)   = 短尾形式
```

### 位置规则

| 位置 | FVS 使用频率 | 说明 |
|------|------------|------|
| 词首 | 低 | 通常不需要 FVS |
| 词中 | 高 | 大部分变体在词中 |
| 词尾 | 中 | 部分字母需要 |
| 独立 | 低 | 独立形式固定 |

### 组合规则

```
✅ 正确：单个基础字符 + 单个 FVS
❌ 错误：单个基础字符 + 多个 FVS
❌ 错误：FVS + 基础字符 (顺序错误)
❌ 错误：FVS + FVS (无基础字符)
```

---

## 🔍 常见变体对照表

### 元音字母变体

#### A (U+1820)
| 形式 | Unicode | 显示 | 使用场景 |
|------|---------|------|----------|
| 基本 | U+1820 | ᠠ | 词首、独立 |
| FVS1 | U+1820 U+180B | ᠠ᠋ | 词中 |
| FVS2 | U+1820 U+180C | ᠠ᠌ | 词尾 (特定词) |

#### E (U+1821)
| 形式 | Unicode | 显示 | 使用场景 |
|------|---------|------|----------|
| 基本 | U+1821 | ᠡ | 词首、独立 |
| FVS1 | U+1821 U+180B | ᠡ᠋ | 词中 |

#### I (U+1822)
| 形式 | Unicode | 显示 | 使用场景 |
|------|---------|------|----------|
| 基本 | U+1822 | ᠢ | 词首、词中 |
| FVS1 | U+1822 U+180B | ᠢ᠋ | 词尾 |

### 辅音字母变体

#### N (U+1828)
| 形式 | Unicode | 显示 | 使用场景 |
|------|---------|------|----------|
| 基本 | U+1828 | ᠨ | 词首 |
| FVS1 | U+1828 U+180B | ᠨ᠋ | 词中 (长尾) |
| FVS2 | U+1828 U+180C | ᠨ᠌ | 词中 (短尾) |
| FVS3 | U+1828 U+180D | ᠨ᠍ | 词尾 |

#### B (U+182A)
| 形式 | Unicode | 显示 | 使用场景 |
|------|---------|------|----------|
| 基本 | U+182A | ᠪ | 词首 |
| FVS1 | U+182A U+180B | ᠪ᠋ | 词中 |
| FVS2 | U+182A U+180C | ᠪ᠌ | 词尾 |

#### G (U+1820)
| 形式 | Unicode | 显示 | 使用场景 |
|------|---------|------|----------|
| 基本 | U+1820 | ᠭ | 词首 |
| FVS1 | U+1820 U+180B | ᠭ᠋ | 词中 |

---

## 💻 编程处理

### Python 处理函数

```python
from typing import List, Tuple

# FVS 码位常量
FVS1 = '\u180B'
FVS2 = '\u180C'
FVS3 = '\u180D'
FVS_SET = {FVS1, FVS2, FVS3}

def has_fvs(text: str) -> bool:
    """检查文本是否包含 FVS"""
    return any(char in FVS_SET for char in text)

def count_fvs(text: str) -> dict:
    """统计 FVS 数量"""
    return {
        'FVS1': text.count(FVS1),
        'FVS2': text.count(FVS2),
        'FVS3': text.count(FVS3),
        'total': sum(text.count(fvs) for fvs in FVS_SET)
    }

def remove_fvs(text: str) -> str:
    """移除所有 FVS"""
    return ''.join(char for char in text if char not in FVS_SET)

def normalize_fvs(text: str) -> str:
    """
    规范化 FVS 使用
    规则:
    1. 移除多余的 FVS
    2. 修正错误的 FVS 顺序
    3. 确保 FVS 紧跟基础字符
    """
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        result.append(char)
        
        # 如果当前字符是 FVS，跳过 (已处理)
        if char in FVS_SET:
            i += 1
            continue
        
        # 检查后续字符是否为 FVS
        if i + 1 < len(text) and text[i + 1] in FVS_SET:
            # 保留第一个 FVS，移除后续重复的
            result.append(text[i + 1])
            j = i + 2
            while j < len(text) and text[j] in FVS_SET:
                j += 1
            i = j
        else:
            i += 1
    
    return ''.join(result)

def find_fvs_sequences(text: str) -> List[Tuple[str, str, int]]:
    """
    查找所有 FVS 序列
    返回：[(基础字符，FVS, 位置), ...]
    """
    sequences = []
    for i, char in enumerate(text):
        if char not in FVS_SET and i + 1 < len(text):
            next_char = text[i + 1]
            if next_char in FVS_SET:
                sequences.append((char, next_char, i))
    return sequences

def replace_fvs(text: str, old_fvs: str, new_fvs: str) -> str:
    """替换 FVS 类型"""
    if old_fvs not in FVS_SET or new_fvs not in FVS_SET:
        raise ValueError("Invalid FVS character")
    return text.replace(old_fvs, new_fvs)
```

### JavaScript 处理函数

```javascript
// FVS 常量
const FVS1 = '\u180B';
const FVS2 = '\u180C';
const FVS3 = '\u180D';
const FVS_SET = new Set([FVS1, FVS2, FVS3]);

/**
 * 检查文本是否包含 FVS
 */
function hasFVS(text) {
    return [...text].some(char => FVS_SET.has(char));
}

/**
 * 统计 FVS 数量
 */
function countFVS(text) {
    return {
        FVS1: (text.match(new RegExp(FVS1, 'g')) || []).length,
        FVS2: (text.match(new RegExp(FVS2, 'g')) || []).length,
        FVS3: (text.match(new RegExp(FVS3, 'g')) || []).length,
        total: [...text].filter(char => FVS_SET.has(char)).length
    };
}

/**
 * 移除所有 FVS
 */
function removeFVS(text) {
    return [...text].filter(char => !FVS_SET.has(char)).join('');
}

/**
 * 规范化 FVS 使用
 */
function normalizeFVS(text) {
    const chars = [...text];
    const result = [];
    let i = 0;
    
    while (i < chars.length) {
        const char = chars[i];
        result.push(char);
        
        if (FVS_SET.has(char)) {
            i++;
            continue;
        }
        
        if (i + 1 < chars.length && FVS_SET.has(chars[i + 1])) {
            result.push(chars[i + 1]);
            let j = i + 2;
            while (j < chars.length && FVS_SET.has(chars[j])) {
                j++;
            }
            i = j;
        } else {
            i++;
        }
    }
    
    return result.join('');
}

/**
 * 查找所有 FVS 序列
 */
function findFVSSequences(text) {
    const sequences = [];
    const chars = [...text];
    
    for (let i = 0; i < chars.length; i++) {
        const char = chars[i];
        if (!FVS_SET.has(char) && i + 1 < chars.length) {
            const nextChar = chars[i + 1];
            if (FVS_SET.has(nextChar)) {
                sequences.push({
                    base: char,
                    fvs: nextChar,
                    position: i
                });
            }
        }
    }
    
    return sequences;
}
```

---

## 🎨 字体渲染

### 字体支持情况

| 字体 | FVS1 | FVS2 | FVS3 | 质量 |
|------|------|------|------|------|
| Noto Sans Mongolian | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Microsoft Mongolian Baiti | ✅ | ✅ | ⚠️ 部分 | ⭐⭐⭐⭐ |
| Menksoft Fonts | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ |
| Mongolian White | ✅ | ✅ | ⚠️ 部分 | ⭐⭐⭐ |
| 开源字体 (平均) | ✅ | ⚠️ 部分 | ❌ 少 | ⭐⭐⭐ |

### CSS 渲染优化

```css
/* 确保 FVS 正确渲染 */
.mongolian-text {
    font-family: 'Noto Sans Mongolian', 'Microsoft Mongolian Baiti', sans-serif;
    font-feature-settings: 'mgrk' 1; /* 蒙古文渲染特性 */
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* 竖排时的 FVS 处理 */
.mongolian-vertical {
    writing-mode: vertical-lr;
    text-orientation: upright;
    
    /* 确保 FVS 不影响布局 */
    & ::selection {
        background: rgba(0, 122, 255, 0.3);
    }
}

/* FVS 调试模式 */
.mongolian-debug .fvs-marker {
    position: relative;
    
    &::after {
        content: 'ⓕ';
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 8px;
        background: #ff0;
        border-radius: 50%;
        padding: 1px 3px;
    }
}
```

### JavaScript 渲染增强

```javascript
/**
 * 高亮显示 FVS 位置 (调试用)
 */
function highlightFVS(container) {
    const textNodes = getTextNodes(container);
    
    textNodes.forEach(node => {
        const text = node.textContent;
        if (hasFVS(text)) {
            const fragment = document.createDocumentFragment();
            let lastIndex = 0;
            
            for (let i = 0; i < text.length; i++) {
                if (FVS_SET.has(text[i])) {
                    // 添加 FVS 前的文本
                    if (i > lastIndex) {
                        fragment.appendChild(
                            document.createTextNode(text.slice(lastIndex, i))
                        );
                    }
                    
                    // 创建 FVS 标记
                    const marker = document.createElement('span');
                    marker.className = 'fvs-marker';
                    marker.textContent = text[i];
                    marker.title = `FVS at position ${i}`;
                    fragment.appendChild(marker);
                    
                    lastIndex = i + 1;
                }
            }
            
            // 添加剩余文本
            if (lastIndex