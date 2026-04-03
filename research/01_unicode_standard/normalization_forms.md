# Unicode 规范化形式详解

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [Unicode 规范化基础](#unicode-规范化基础)
3. [四种规范化形式](#四种规范化形式)
4. [蒙古文规范化特殊考虑](#蒙古文规范化特殊考虑)
5. [代码实现](#代码实现)
6. [测试用例](#测试用例)
7. [最佳实践](#最佳实践)
8. [常见问题](#常见问题)
9. [参考资料](#参考资料)

---

## 概述

### 什么是 Unicode 规范化

Unicode 规范化是将同一字符的不同编码表示转换为统一形式的过程。由于历史原因和编码灵活性，同一文本可能有多种合法的 Unicode 表示方式。

### 为什么需要规范化

| 问题场景 | 描述 | 影响 |
|---------|------|------|
| 文本比较 | 同一内容不同编码 | 比较失败 |
| 搜索索引 | 编码不一致 | 搜索遗漏 |
| 数据存储 | 重复存储 | 浪费空间 |
| 变体处理 | FVS 序列不一致 | 渲染错误 |

### 蒙古文特殊挑战

传统蒙古文的 Unicode 规范化比拉丁文更复杂：

- **变体选择符 (FVS)**: 需要保留字形变体信息
- **连接行为**: 字母位置影响字形
- **控制字符**: NNBSP、ZWJ 等影响连写
- **字体依赖**: 不同字体对 FVS 响应不同

---

## Unicode 规范化基础

### 规范等价的两种类型

#### 1. 规范等价 (Canonical Equivalence)

两个序列在视觉上和功能上完全相同。

**示例**:
```
U+00C0  À (带重音的拉丁大写字母 A)
U+0041 U+0300  A + 组合重音符号

两者规范等价，规范化后应相同
```

#### 2. 兼容等价 (Compatibility Equivalence)

两个序列在某些上下文中可互换，但视觉上可能不同。

**示例**:
```
U+00C6  Æ (AE 连字)
U+0041 U+0045  A + E

两者兼容等价，但不完全相同
```

### 规范化稳定属性

| 属性 | 描述 |
|------|------|
| 稳定性 | 多次规范化结果相同 |
| 可逆性 | NFC(NFD(text)) = NFD(text) |
| 保序性 | 字符顺序不变 |

---

## 四种规范化形式

### NFC (Normalization Form C)

**合成形式 (Canonical Composition)**

- 将分解序列合成为预组合字符
- 保留规范等价
- **推荐用于存储和传输**

```javascript
const text = "A\u0300";  // A + 组合重音
const nfc = text.normalize('NFC');  // "À" (U+00C0)
```

### NFD (Normalization Form D)

**分解形式 (Canonical Decomposition)**

- 将预组合字符分解为基础字符 + 组合标记
- 保留规范等价
- **推荐用于文本处理和比较**

```javascript
const text = "À";  // U+00C0
const nfd = text.normalize('NFD');  // "A\u0300"
```

### NFKC (Normalization Form KC)

**兼容合成形式 (Compatibility Composition)**

- 应用兼容分解后再合成
- 丢失部分格式信息
- **不推荐用于蒙古文**

```javascript
const text = "Æ";  // U+00C6
const nfkc = text.normalize('NFKC');  // "AE"
```

### NFKD (Normalization Form KD)

**兼容分解形式 (Compatibility Decomposition)**

- 完全分解，包括兼容等价
- 丢失最多信息
- **不推荐用于蒙古文**

```javascript
const text = "²";  // U+00B2 (上标 2)
const nfkd = text.normalize('NFKD');  // "2"
```

---

## 蒙古文规范化特殊考虑

### FVS 序列处理

**问题**: FVS (自由变体选择符) 在规范化中可能被错误处理

```javascript
// 蒙古文变体序列
const variant1 = "\u182D\u180B\u1820";  // ga + FVS1 + a
const variant2 = "\u182D\u1820";         // ga + a (无变体)

// NFC 规范化
variant1.normalize('NFC');  // 应保持 FVS
variant2.normalize('NFC');  // 无变化
```

**最佳实践**:
1. 使用 NFC 存储，保留 FVS 序列
2. 避免使用 NFKC/NFKD (可能丢失 FVS)
3. 比较时先规范化到 NFD

### 连接控制符处理

**NNBSP (U+202F)**: 窄不折行空格

```javascript
// 控制连写断点
const text1 = "\u182C\u1825\u182D\u1822\u182D\u1830\u1822\u1828";  // kö'gesen
const text2 = "\u182C\u1825\u182D\u1822\u182D\u202F\u1830\u1822\u1828";  // 带 NNBSP

// 规范化后 NNBSP 应保留
text2.normalize('NFC');  // NNBSP 保留
```

**ZWJ/ZWNJ (U+200D/U+200C)**: 零宽连接符/非连接符

```javascript
// 强制连接或断开
const forcedJoin = "\u182D\u200D\u1820";  // ga + ZWJ + a
const forcedNoJoin = "\u182D\u200C\u1820";  // ga + ZWNJ + a
```

### 规范化对渲染的影响

| 规范化形式 | FVS 保留 | NNBSP 保留 | 渲染一致性 | 推荐场景 |
|-----------|---------|-----------|-----------|---------|
| NFC | ✅ | ✅ | 高 | 存储、传输 |
| NFD | ✅ | ✅ | 高 | 处理、比较 |
| NFKC | ❌ | ⚠️ | 中 | 不推荐 |
| NFKD | ❌ | ⚠️ | 低 | 不推荐 |

---

## 代码实现

### JavaScript 实现

```javascript
class MongolianNormalizer {
  /**
   * 安全规范化 - 保留 FVS 和控制符
   * @param {string} text - 输入文本
   * @param {string} form - 规范化形式 (NFC|NFD|NFKC|NFKD)
   * @returns {string} 规范化后的文本
   */
  static normalize(text, form = 'NFC') {
    // 避免使用兼容形式处理蒙古文
    if (form === 'NFKC' || form === 'NFKD') {
      console.warn('NFKC/NFKD may lose FVS information for Mongolian text');
    }
    
    return text.normalize(form);
  }
  
  /**
   * 提取 FVS 序列
   * @param {string} text - 输入文本
   * @returns {Array} FVS 序列数组
   */
  static extractFVS(text) {
    const fvsPattern = /([\u1820-\u1884])([\u180B-\u180D]+)/g;
    const matches = [];
    let match;
    
    while ((match = fvsPattern.exec(text)) !== null) {
      matches.push({
        baseChar: match[1],
        fvsSequence: match[2],
        index: match.index,
        unicodeBase: match[1].codePointAt(0).toString(16).toUpperCase(),
        unicodeFVS: [...match[2]].map(c => 
          'U+' + c.codePointAt(0).toString(16).toUpperCase()
        )
      });
    }
    
    return matches;
  }
  
  /**
   * 验证 FVS 位置
   * @param {string} text - 输入文本
   * @returns {boolean} 是否有效
   */
  static validateFVS(text) {
    // FVS 必须紧跟基础字符
    const invalidPattern = /[\u180B-\u180D](?![\u1820-\u1884]|[\u180B-\u180D]|$)/g;
    return !invalidPattern.test(text);
  }
  
  /**
   * 比较两个蒙古文文本 (规范化后)
   * @param {string} text1 - 文本 1
   * @param {string} text2 - 文本 2
   * @returns {boolean} 是否相等
   */
  static compare(text1, text2) {
    const nfd1 = text1.normalize('NFD');
    const nfd2 = text2.normalize('NFD');
    return nfd1 === nfd2;
  }
  
  /**
   * 规范化并验证
   * @param {string} text - 输入文本
   * @returns {Object} 结果对象
   */
  static normalizeAndValidate(text) {
    const normalized = this.normalize(text, 'NFC');
    const fvsList = this.extractFVS(normalized);
    const isValid = this.validateFVS(normalized);
    
    return {
      original: text,
      normalized: normalized,
      fvsCount: fvsList.length,
      fvsList: fvsList,
      isValid: isValid,
      length: normalized.length
    };
  }
}

// 使用示例
const text = "ᠭ᠎ᠠᠷᠤ";  // garu (带 FVS)
const result = MongolianNormalizer.normalizeAndValidate(text);
console.log(result);
```

### Python 实现

```python
import unicodedata
import re
from typing import List, Dict, Any

class MongolianNormalizer:
    """蒙古文 Unicode 规范化工具类"""
    
    # Unicode 范围常量
    MONGOLIAN_BASE = (0x1820, 0x1884)
    FVS_RANGE = (0x180B, 0x180D)
    CONTROL_CHARS = {
        'NNBSP': 0x202F,
        'ZWJ': 0x200D,
        'ZWNJ': 0x200C,
        'MVS': 0x180E,  # 已弃用
    }
    
    @classmethod
    def normalize(cls, text: str, form: str = 'NFC') -> str:
        """
        安全规范化蒙古文文本
        
        Args:
            text: 输入文本
            form: 规范化形式 (NFC|NFD|NFKC|NFKD)
        
        Returns:
            规范化后的文本
        """
        if form in ('NFKC', 'NFKD'):
            import warnings
            warnings.warn(
                'NFKC/NFKD may lose FVS information for Mongolian text',
                UserWarning
            )
        
        return unicodedata.normalize(form, text)
    
    @classmethod
    def extract_fvs(cls, text: str) -> List[Dict[str, Any]]:
        """
        提取 FVS 序列
        
        Args:
            text: 输入文本
        
        Returns:
            FVS 序列列表
        """
        pattern = r'([\u1820-\u1884])([\u180B-\u180D]+)'
        matches = []
        
        for match in re.finditer(pattern, text):
            base_char = match.group(1)
            fvs_seq = match.group(2)
            
            matches.append({
                'base_char': base_char,
                'fvs_sequence': fvs_seq,
                'index': match.start(),
                'unicode_base': f'U+{ord(base_char):04X}',
                'unicode_fvs': [f'U+{ord(c):04X}' for c in fvs_seq]
            })
        
        return matches
    
    @classmethod
    def validate_fvs(cls, text: str) -> bool:
        """
        验证 FVS 位置是否正确
        
        Args:
            text: 输入文本
        
        Returns:
            是否有效
        """
        # FVS 后必须跟基础字符、另一个 FVS、或字符串结尾
        pattern = r'[\u180B-\u180D](?![\u1820-\u1884\u180B-\u180D]|$)'
        return not bool(re.search(pattern, text))
    
    @classmethod
    def compare(cls, text1: str, text2: str) -> bool:
        """
        比较两个蒙古文文本 (规范化后)
        
        Args:
            text1: 文本 1
            text2: 文本 2
        
        Returns:
            是否相等
        """
        nfd1 = unicodedata.normalize('NFD', text1)
        nfd2 = unicodedata.normalize('NFD', text2)
        return nfd1 == nfd2
    
    @classmethod
    def normalize_and_validate(cls, text: str) -> Dict[str, Any]:
        """
        规范化并验证
        
        Args:
            text: 输入文本
        
        Returns:
            结果字典
        """
        normalized = cls.normalize(text, 'NFC')
        fvs_list = cls.extract_fvs(normalized)
        is_valid = cls.validate_fvs(normalized)
        
        return {
            'original': text,
            'normalized': normalized,
            'fvs_count': len(fvs_list),
            'fvs_list': fvs_list,
            'is_valid': is_valid,
            'length': len(normalized)
        }

# 使用示例
if __name__ == '__main__':
    text = "ᠭ᠎ᠠᠷᠤ"  # garu (带 FVS)
    result = MongolianNormalizer.normalize_and_validate(text)
    print(result)
```

---

## 测试用例

### 基础规范化测试

```javascript
describe('Mongolian Normalizer', () => {
  test('NFC 合成', () => {
    // 虽然蒙古文没有预组合字符，但测试框架应工作
    const text = "ᠬᠥᠭᠡᠭᠰᠡᠨ";
    const normalized = MongolianNormalizer.normalize(text, 'NFC');
    expect(normalized).toBe(text);  // 无变化
  });
  
  test('NFD 分解', () => {
    const text = "ᠬᠥᠭᠡᠭᠰᠡᠨ";
    const normalized = MongolianNormalizer.normalize(text, 'NFD');
    expect(normalized).toBe(text);  // 无变化
  });
  
  test('FVS 保留', () => {
    const text = "ᠭ᠎ᠠ";  // ga + FVS1 + a
    const normalized = MongolianNormalizer.normalize(text, 'NFC');
    expect(normalized).toBe(text);  // FVS 应保留
    expect(normalized.includes('\u180B')).toBe(true);
  });
  
  test('NNBSP 保留', () => {
    const text = "ᠬᠥᠭᠡᠭ\u202Fᠰᠡᠨ";  // 带 NNBSP
    const normalized = MongolianNormalizer.normalize(text, 'NFC');
    expect(normalized.includes('\u202F')).toBe(true);
  });
});
```

### FVS 提取测试

```javascript
test('提取单个 FVS', () => {
  const text = "ᠭ᠎ᠠᠷᠤ";  // garu (ga+FVS1)
  const fvsList = MongolianNormalizer.extractFVS(text);
  
  expect(fvsList.length).toBe(1);
  expect(fvsList[0].baseChar).toBe('ᠭ');
  expect(fvsList[0].fvsSequence).toBe('\u180B');
  expect(fvsList[0].unicodeBase).toBe('U+182D');
  expect(fvsList[0].unicodeFVS).toEqual(['U+180B']);
});

test('提取多个 FVS', () => {
  const text = "ᠭ᠎ᠠ ᠮᠣᠩᠭᠣᠯ";  // 多个带 FVS 的字符
  const fvsList = Mong