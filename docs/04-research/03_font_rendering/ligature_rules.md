# 蒙古文连字规则研究

**版本**: v1.0  
**创建时间**: 2026-04-03  
**最后更新**: 2026-04-03  
**状态**: ✅ 完成

---

## 📋 概述

蒙古文是一种连写文字 (cursive script)，字母在词内会根据位置 (词首、词中、词尾) 和相邻字母发生字形变化，形成连字 (ligature)。

### 连字类型

| 类型 | 说明 | 触发条件 | 示例 |
|------|------|----------|------|
| 位置连字 | 字母根据位置变形 | 词首/词中/词尾 | ᠮᠣᠩ᠇ᠢᠶᠠ |
| 上下文连字 | 相邻字母影响字形 | 特定字母组合 | ᠪᠢᠴᠢᠭ |
| FVS 连字 | FVS 触发的变体 | FVS1/2/3 | ᠨ᠋ vs ᠨ᠌ |
| 强制连字 | ZWJ 强制连接 | ZWJ (U+200D) | ᠠ‍ᠪ |
| 禁止连字 | ZWNJ 禁止连接 | ZWNJ (U+200C) | ᠠ‌ᠪ |

---

## 📍 位置连字规则

### 基本位置形式

蒙古文字母有四种基本位置形式:

| 位置 | 名称 | 说明 | 示例 (字母 A) |
|------|------|------|---------------|
| 词首 | Initial | 单词开头的形式 | ᠠ |
| 词中 | Medial | 单词中间的形式 | ᠠ᠋ |
| 词尾 | Final | 单词结尾的形式 | ᠠ᠌ |
| 独立 | Isolated | 单独出现的形式 | ᠠ |

### 位置判断规则

```
词首：单词的第一个字母
词中：单词的中间字母 (非首非尾)
词尾：单词的最后一个字母
独立：单独出现的字母 (前后有空格或标点)
```

**示例分析**:

```
单词：ᠮᠣᠩᠭᠣᠯ (monggol - 蒙古)

位置分解:
ᠮ - 词首 (M)
ᠣ - 词中 (O)
ᠩ - 词中 (NG)
ᠭ - 词中 (G)
ᠣ - 词中 (O)
ᠯ - 词尾 (L)
```

### 位置连字表

#### 元音字母位置形式

| 字母 | 词首 | 词中 | 词尾 | 独立 |
|------|------|------|------|------|
| A (ᠠ) | ᠠ | ᠠ᠋ | ᠠ᠌ | ᠠ |
| E (ᠡ) | ᠡ | ᠡ᠋ | ᠡ᠌ | ᠡ |
| I (ᠢ) | ᠢ | ᠢ᠋ | ᠢ᠌ | ᠢ |
| O (ᠣ) | ᠣ | ᠣ᠋ | ᠣ᠌ | ᠣ |
| U (ᠤ) | ᠤ | ᠤ᠋ | ᠤ᠌ | ᠤ |
| Ö (ᠥ) | ᠥ | ᠥ᠋ | ᠥ᠌ | ᠥ |
| Ü (ᠦ) | ᠦ | ᠦ᠋ | ᠦ᠌ | ᠦ |
| NA (ᠨᠠ) | ᠨᠠ | ᠨᠠ᠋ | ᠨᠠ᠌ | ᠨᠠ |

#### 辅音字母位置形式

| 字母 | 词首 | 词中 | 词尾 | 独立 |
|------|------|------|------|------|
| N (ᠨ) | ᠨ | ᠨ᠋ | ᠨ᠌ | ᠨ |
| B (ᠪ) | ᠪ | ᠪ᠋ | ᠪ᠌ | ᠪ |
| P (ᠫ) | ᠫ | ᠫ᠋ | ᠫ᠌ | ᠫ |
| Q (ᠬ) | ᠬ | ᠬ᠋ | ᠬ᠌ | ᠬ |
| G (ᠭ) | ᠭ | ᠭ᠋ | ᠭ᠌ | ᠭ |
| M (ᠮ) | ᠮ | ᠮ᠋ | ᠮ᠌ | ᠮ |
| L (ᠯ) | ᠯ | ᠯ᠋ | ᠯ᠌ | ᠯ |
| S (ᠰ) | ᠰ | ᠰ᠋ | ᠰ᠌ | ᠰ |
| Š (ᠱ) | ᠱ | ᠱ᠋ | ᠱ᠌ | ᠱ |
| T (ᠲ) | ᠲ | ᠲ᠋ | ᠲ᠌ | ᠲ |
| D (ᠳ) | ᠳ | ᠳ᠋ | ᠳ᠌ | ᠳ |
| Č (ᠴ) | ᠴ | ᠴ᠋ | ᠴ᠌ | ᠴ |
| J (ᠵ) | ᠵ | ᠵ᠋ | ᠵ᠌ | ᠵ |
| Y (ᠶ) | ᠶ | ᠶ᠋ | ᠶ᠌ | ᠶ |
| R (ᠷ) | ᠷ | ᠷ᠋ | ᠷ᠌ | ᠷ |
| W (ᠸ) | ᠸ | ᠸ᠋ | ᠸ᠌ | ᠸ |
| F (ᠹ) | ᠹ | ᠹ᠋ | ᠹ᠌ | ᠹ |
| K (ᠺ) | ᠺ | ᠺ᠋ | ᠺ᠌ | ᠺ |
| TS (ᠻ) | ᠻ | ᠻ᠋ | ᠻ᠌ | ᠻ |
| Z (ᠼ) | ᠼ | ᠼ᠋ | ᠼ᠌ | ᠼ |
| H (ᠽ) | ᠽ | ᠽ᠋ | ᠽ᠌ | ᠽ |
| Ž (ᠾ) | ᠾ | ᠾ᠋ | ᠾ᠌ | ᠾ |
| Č' (ᠿ) | ᠿ | ᠿ᠋ | ᠿ᠌ | ᠿ |

---

## 🔗 上下文连字规则

### 特定字母组合

某些字母组合会产生特殊的连字效果:

#### 1. NG (ᠩ) 后接元音

```
规则：ᠩ + 元音 → 特殊连字
示例:
ᠮᠣᠩᠭᠣᠯ (monggol) - ᠩ 后接 ᠭ
ᠬᠠᠩᠭᠠ (qangqa) - ᠩ 后接 ᠭ
```

#### 2. 双元音组合

```
规则：元音 + 元音 → 连写
示例:
ᠠᠢ (ai) - 双元音 ai
ᠣᠢ (oi) - 双元音 oi
ᠤᠢ (ui) - 双元音 ui
```

#### 3. 辅音丛

```
规则：辅音 + 辅音 → 特殊处理
示例:
ᠪᠢᠴᠢᠭ (bičig - 文字) - č + g
ᠬᠦᠮᠦᠨ (kümün - 人) - m + ü + n
```

### 连字优先级

```
1. FVS 变体 (最高优先级)
2. ZWJ/ZWNJ 控制
3. 特定字母组合规则
4. 位置形式规则 (默认)
```

---

## 🎛️ 控制字符

### ZWJ (Zero Width Joiner, U+200D)

**用途**: 强制连接两个本不连接的字母

```
示例:
正常：ᠠ ᠪ (有空格，不连写)
强制连字：ᠠ‍ᠪ (ZWJ 连接)

Unicode: U+1820 U+200D U+182A
```

**使用场景**:
- 特殊拼写
- 外来词
- 专有名词
- 诗歌排版

### ZWNJ (Zero Width Non-Joiner, U+200C)

**用途**: 禁止连接两个本应连接的字母

```
示例:
正常连写：ᠠᠪ (连写)
禁止连字：ᠠ‌ᠪ (ZWNJ 分隔)

Unicode: U+1820 U+200C U+182A
```

**使用场景**:
- 词根分隔
- 特殊发音
- 避免歧义

### NNBSP (Narrow No-Break Space, U+202F)

**用途**: 窄不换行空格，用于词内分隔

```
示例:
前缀 + NNBSP + 词根
ᠡᠷᠡᠬᠲᠡᠢ ᠶᠢᠨ (erehgtei-yin)
```

---

## 💻 编程实现

### Python 连字引擎

```python
from typing import Dict, List, Optional, Tuple
from enum import Enum

class Position(Enum):
    INITIAL = "initial"
    MEDIAL = "medial"
    FINAL = "final"
    ISOLATED = "isolated"

# 控制字符常量
FVS1 = '\u180B'
FVS2 = '\u180C'
FVS3 = '\u180D'
ZWJ = '\u200D'
ZWNJ = '\u200C'
NNBSP = '\u202F'

class MongolianLigatureEngine:
    def __init__(self):
        self.position_forms = self._load_position_forms()
        self.context_rules = self._load_context_rules()
    
    def _load_position_forms(self) -> Dict[str, Dict[Position, str]]:
        """加载位置形式映射表"""
        return {
            '\u1820': {  # A
                Position.INITIAL: '\u1820',
                Position.MEDIAL: '\u1820' + FVS1,
                Position.FINAL: '\u1820' + FVS2,
                Position.ISOLATED: '\u1820'
            },
            '\u1828': {  # N
                Position.INITIAL: '\u1828',
                Position.MEDIAL: '\u1828' + FVS1,
                Position.FINAL: '\u1828' + FVS2,
                Position.ISOLATED: '\u1828'
            },
            # ... 其他字母
        }
    
    def _load_context_rules(self) -> List[Tuple[str, str, str]]:
        """加载上下文规则"""
        return [
            # (模式，替换，说明)
            ('\u1829\u1820', '\u1829\u180B\u1820', 'NG + A 特殊连字'),
            # ... 其他规则
        ]
    
    def get_position(self, text: str, index: int) -> Position:
        """
        判断字母在词中的位置
        
        规则:
        1. 第一个字母 = 词首
        2. 最后一个字母 = 词尾
        3. 中间字母 = 词中
        4. 单独字母 = 独立
        """
        # 移除非字母字符
        letters = [c for c in text if self._is_mongolian_letter(c)]
        
        if len(letters) == 0:
            return Position.ISOLATED
        
        char = text[index]
        if char not in letters:
            return Position.ISOLATED
        
        char_index = letters.index(char)
        
        if len(letters) == 1:
            return Position.ISOLATED
        elif char_index == 0:
            return Position.INITIAL
        elif char_index == len(letters) - 1:
            return Position.FINAL
        else:
            return Position.MEDIAL
    
    def _is_mongolian_letter(self, char: str) -> bool:
        """判断是否为蒙古文字母"""
        code = ord(char)
        return 0x1820 <= code <= 0x1878
    
    def apply_ligatures(self, text: str) -> str:
        """
        应用连字规则
        
        步骤:
        1. 分词
        2. 判断每个字母的位置
        3. 应用位置形式
        4. 应用上下文规则
        5. 处理控制字符
        """
        words = text.split()
        result_words = []
        
        for word in words:
            result_word = self._process_word(word)
            result_words.append(result_word)
        
        return ' '.join(result_words)
    
    def _process_word(self, word: str) -> str:
        """处理单个单词的连字"""
        # 1. 分离字母和控制符
        letters = []
        control_chars = []
        
        i = 0
        while i < len(word):
            char = word[i]
            if char in {FVS1, FVS2, FVS3, ZWJ, ZWNJ}:
                control_chars.append((len(letters), char))
            else:
                letters.append(char)
            i += 1
        
        # 2. 应用位置形式
        result = []
        for i, letter in enumerate(letters):
            position = self.get_position(word, i)
            
            if letter in self.position_forms:
                form = self.position_forms[letter].get(position, letter)
                result.append(form)
            else:
                result.append(letter)
        
        # 3. 插入控制符
        for pos, char in control_chars:
            if pos < len(result):
                result[pos] += char
        
        # 4. 应用上下文规则
        result_str = ''.join(result)
        for pattern, replacement, _ in self.context_rules:
            result_str = result_str.replace(pattern, replacement)
        
        return result_str
    
    def normalize(self, text: str) -> str:
        """
        规范化连字
        移除冗余控制符，确保一致性
        """
        # 1. Unicode 规范化
        text = text.normalize('NFC')
        
        # 2. 移除冗余 FVS
        text = self._remove_redundant_fvs(text)
        
        # 3. 修正 ZWJ/ZWNJ
        text = self._fix_joiners(text)
        
        return text
    
    def _remove_redundant_fvs(self, text: str) -> str:
        """移除冗余的 FVS"""
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            result.append(char)
            
            if char in {FVS1, FVS2, FVS3}:
                # 跳过后续重复的 FVS
                while i + 1 < len(text) and text[i + 1] in {FVS1, FVS2, FVS3}:
                    i += 1
            i += 1
        
        return ''.join(result)
    
    def _fix_joiners(self, text: str) -> str:
        """修正 ZWJ/ZWNJ 使用"""
        # 移除词首的 ZWJ
        text = text.lstrip(ZWJ)
        
        # 移除词尾的 ZWNJ
        text = text.rstrip(ZWNJ)
        
        return text
```

### JavaScript 连字处理

```javascript
/**
 * 蒙古文连字处理引擎
 */
class MongolianLigatureEngine {
    constructor() {
        this.FVS1 = '\u180B';
        this.FVS2 = '\u180C';
        this.FVS3 = '\u180D';
        this.ZWJ = '\u200D';
        this.ZWNJ = '\u200C';
        this.NNBSP = '\u202F';
        
        this.positionForms = this._loadPositionForms();
        this