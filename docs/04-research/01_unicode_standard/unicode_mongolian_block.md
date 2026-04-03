# Unicode 蒙古文标准

**版本**: v1.0  
**创建时间**: 2026-04-03  
**参考文献**: Unicode Standard 15.0, TN57

---

## 1. Unicode 编码范围

### 1.1 蒙古文区块 (Mongolian Block)

```
U+1800 - U+18AF  蒙古文主区块 (共 176 个码位)
```

**码位分配**:
| 范围 | 用途 | 数量 |
|------|------|------|
| U+1800-U+1805 | 标点符号 | 6 |
| U+1806-U+180A | 连接符/控制符 | 5 |
| U+1810-U+1819 | 蒙古文数字 0-9 | 10 |
| U+1820-U+1884 | 蒙古文字母 | 101 |
| U+1885-U+18A9 | 扩展字母/变体 | 37 |
| U+18AA-U+18AF | 保留/未分配 | 6 |

### 1.2 蒙古文补充区块 (Mongolian Supplement)

```
U+11660 - U+1167F  蒙古文补充 (共 32 个码位)
```

**用途**: 阿里嘎里字母 (Ali Gali, 用于转写梵文/藏文)

---

## 2. 关键控制字符

### 2.1 自由变体选择符 (Free Variation Selectors)

```
U+180B  FVS1  自由变体选择符 1
U+180C  FVS2  自由变体选择符 2
U+180D  FVS3  自由变体选择符 3
```

**用途**: 控制同一字符的不同字形变体

**示例**:
```
ᠭᠠ (ga)        - 基本形式
ᠭ᠎ᠠ (ga+FVS1)  - 变体形式 1
ᠭ᠏ᠠ (ga+FVS2)  - 变体形式 2
```

**技术要点**:
- FVS 是零宽字符，不影响光标位置
- FVS 必须紧跟在基础字符之后
- 不同字体对 FVS 的渲染可能不同

### 2.2 连接控制符

```
U+202F  NNBSP  窄不折行空格 (用于连写控制)
U+200D  ZWJ    零宽连接符
U+200C  ZWNJ   零宽非连接符
U+180E  MVS    蒙古文变体选择符 (已弃用，改用 FVS)
```

**NNBSP 用途**:
- 防止词内换行
- 控制特定字母组合的连写行为

**示例**:
```
ᠬᠥᠭᠡᠭᠰᠡᠨ (kö'gesen) - 正常连写
ᠬᠥᠭᠡᠭ ᠰᠡᠨ (kö'ge+NNBSP+sen) - 控制连写断点
```

### 2.3 标点符号

```
U+1800  MONGOLIAN BIRGA        章节标记 ᠀
U+1801  MONGOLIAN ELLIPSIS     省略号 ᠁
U+1802  MONGOLIAN COMMA        逗号 ᠂
U+1803  MONGOLIAN FULL STOP    句号 ᠃
U+1804  MONGOLIAN COLON        冒号 ᠄
U+1805  MONGOLIAN FOUR DOTS    四点符 ᠅
```

---

## 3. 规范化形式 (Normalization)

### 3.1 NFC vs NFD

**NFC (Normalization Form C)**:
- 合成形式
- 变体选择符与基础字符合并（如果可能）
- 推荐用于存储和传输

**NFD (Normalization Form D)**:
- 分解形式
- 变体选择符保持独立
- 推荐用于文本处理

### 3.2 规范化影响

```javascript
// 示例：同一文本的不同规范化形式
const text1 = "ᠭᠠ";  // ga (U+182D U+1820)
const text2 = "ᠭ᠎ᠠ"; // ga+FVS1 (U+182D U+180B U+1820)

// 规范化后可能不同
text1.normalize('NFC')  // → ᠭᠠ
text2.normalize('NFC')  // → ᠭ᠎ᠠ (保持变体)
```

**最佳实践**:
1. 统一使用 NFC 存储
2. 比较前先规范化
3. 保留 FVS 信息（不丢失变体）

---

## 4. 字序 vs 显示序

### 4.1 问题描述

**Unicode 存储顺序** (逻辑顺序):
```
从左到右：ᠬᠥᠭᠡᠭᠰᠡᠨ (kö'gesen)
存储：U+182C U+1825 U+182D U+1822 U+182D U+1830 U+1822 U+1828
```

**竖排显示顺序** (视觉顺序):
```
从上到下：
ᠬ
ᠥ
ᠭ
ᠡ
ᠭ
ᠰ
ᠡ
ᠨ
```

### 4.2 处理方案

**方案 1: CSS 自动处理**
```css
.mongolian {
    writing-mode: vertical-lr;
    /* 浏览器自动处理字序→显示序转换 */
}
```

**方案 2: JavaScript 手动处理**
```javascript
function toVerticalDisplay(text) {
    // 不需要手动转换，CSS 处理
    return text;
}
```

---

## 5. 常见编码问题

### 5.1 问题：变体丢失

**原因**: 字体不支持 FVS 或规范化过程丢失

**解决**:
```javascript
// 保留 FVS 的规范化
function safeNormalize(text) {
    // 先提取 FVS 序列
    const fvsPattern = /([\u1820-\u1884])([\u180B-\u180D])/g;
    // 规范化基础字符
    return text.normalize('NFC');
}
```

### 5.2 问题：显示不正确

**原因**: 浏览器不支持 CSS writing-mode 或字体缺失

**解决**:
```css
.mongolian {
    writing-mode: vertical-lr;
    font-family: 'Noto Sans Mongolian', 'Mongolian Baiti', sans-serif;
    
    /* 降级方案 */
    @supports not (writing-mode: vertical-lr) {
        transform: rotate(90deg);
        transform-origin: center center;
    }
}
```

### 5.3 问题：输入框竖排失效

**原因**: 部分浏览器输入框不支持 writing-mode

**解决**:
```javascript
// 使用 contenteditable + 自定义渲染
<div contenteditable="true" class="mongolian-editor"></div>

// 或使用 SVG 作为降级方案
<svg>
    <text writing-mode="tb" direction="rtl">蒙古文</text>
</svg>
```

---

## 6. 参考实现

### 6.1 JavaScript 工具函数

```javascript
class MongolianUnicode {
    // 检查是否为蒙古文字符
    static isMongolian(char) {
        const code = char.codePointAt(0);
        return (code >= 0x1800 && code <= 0x18AF) ||
               (code >= 0x11660 && code <= 0x1167F);
    }
    
    // 提取 FVS 序列
    static extractFVS(text) {
        const pattern = /([\u1820-\u1884])([\u180B-\u180D]+)/g;
        const matches = [];
        let match;
        while ((match = pattern.exec(text)) !== null) {
            matches.push({
                base: match[1],
                fvs: match[2],
                index: match.index
            });
        }
        return matches;
    }
    
    // 规范化文本（保留 FVS）
    static normalize(text) {
        return text.normalize('NFC');
    }
    
    // 验证蒙古文文本
    static validate(text) {
        // 检查非法字符组合
        // 检查 FVS 位置
        // 检查连接符使用
        return true; // 简化示例
    }
}
```

### 6.2 Python 工具函数

```python
import unicodedata

class MongolianUnicode:
    MONGOLIAN_RANGE = (0x1800, 0x18AF)
    MONGOLIAN_SUPPLEMENT = (0x11660, 0x1167F)
    FVS_RANGE = (0x180B, 0x180D)
    
    @classmethod
    def is_mongolian(cls, char):
        code = ord(char)
        return (cls.MONGOLIAN_RANGE[0] <= code <= cls.MONGOLIAN_RANGE[1] or
                cls.MONGOLIAN_SUPPLEMENT[0] <= code <= cls.MONGOLIAN_SUPPLEMENT[1])
    
    @classmethod
    def normalize(cls, text):
        return unicodedata.normalize('NFC', text)
    
    @classmethod
    def extract_fvs(cls, text):
        import re
        pattern = r'([\u1820-\u1884])([\u180B-\u180D]+)'
        return re.findall(pattern, text)
```

---

## 7. 测试用例

### 7.1 基础字符测试

```javascript
// 测试基本字母
assert(isMongolian('ᠠ')); // U+1820
assert(isMongolian('ᠨ')); // U+1828
assert(!isMongolian('A')); // 拉丁字母

// 测试 FVS
assert(extractFVS('ᠭ᠎ᠠ').length === 1);
assert(extractFVS('ᠭ᠎ᠠ')[0].fvs === '\u180B');
```

### 7.2 规范化测试

```javascript
// 测试 NFC 规范化
const text1 = 'ᠭ᠎ᠠ'.normalize('NFC');
const text2 = 'ᠭ᠎ᠠ'.normalize('NFD');
assert(text1 === text2); // 应该相同
```

### 7.3 渲染测试

```javascript
// 测试竖排渲染
const testCases = [
    'ᠬᠥᠭᠡᠭᠰᠡᠨ',  // 基本文本
    'ᠭ᠎ᠠᠷᠤ',     // 带 FVS
    'ᠬᠥᠭᠡᠭ ᠰᠡᠨ',  // 带 NNBSP
];

testCases.forEach(text => {
    renderAndVerify(text);
});
```

---

## 8. 参考资源

- **Unicode Standard 15.0**: https://www.unicode.org/versions/Unicode15.0.0/
- **Unicode TN57**:蒙古文编码技术说明
- **Noto Sans Mongolian**: https://fonts.google.com/noto/specimen/Noto+Sans+Mongolian
- **W3C Mongolian Layout**: https://www.w3.org/TR/mongol-layout/ (本地备份)

---

**维护者**: Mongolian AI Team  
**许可证**: CC BY 4.0  
**最后更新**: 2026-04-03
