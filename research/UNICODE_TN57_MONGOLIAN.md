# Unicode 技术笔记第 57 号学习笔记

## 文档信息

**标题**：Encoding and Shaping of the Mongolian Script（蒙古文脚本的编码与字形变换）

**编号**：Unicode Technical Note #57 (UTN #57)

**版本**：Version 4（最新版本）

**作者**：Kushim Jiang

**日期**：2024-08-14（最新版本）

**URL**：
- 主页：https://www.unicode.org/notes/tn57/
- HTML: https://www.unicode.org/notes/tn57/tn57-4.html
- PDF: https://www.unicode.org/notes/tn57/utn57-mong-4.pdf

**状态**：Unicode Technical Note（技术笔记）

---

## 核心内容

### 摘要

本文档提供了蒙古文脚本的**文本表示系统**和**文本字形变换规则**：

1. **文本表示 (Text Representation)**
   - 列出每个书写系统中使用的字母和标记的字符及其变体
   - 涵盖传统蒙古文、托忒文、锡伯文、满文等

2. **文本字形变换 (Text Shaping)**
   - 提供分层字形变换规则
   - 详细说明每个变换步骤的行为
   - 说明每个变体呈现的条件

---

## 蒙古文 Unicode 编码

### 编码范围

- **基本区块**：U+1800 - U+18AF
- **扩展区块**：U+11660 - U+1167F (Mongolian Supplement)

### 字符分类

1. **字母 (Letters)**
   - 元音字母
   - 辅音字母

2. **标记 (Marks)**
   - 自由变体选择符 (FVS1, FVS2, FVS3)
   - 零宽连接符 (ZWJ)
   - 零宽非连接符 (ZWNJ)

3. **标点符号 (Punctuation)**
   - 蒙古文逗号
   - 蒙古文句号
   - 蒙古文冒号等

---

## 字形变换规则

### 分层变换系统

```
输入文本 (Unicode 码点序列)
  ↓
第 1 层：基础变换
  ↓
第 2 层：上下文变换
  ↓
第 3 层：变体选择
  ↓
输出：最终字形呈现
```

### 词形变体

蒙古文字母根据位置有不同变体：

1. **词首形式 (Initial Form)**
   - 出现在单词开头
   - 特殊的顶部连接

2. **词中形式 (Medial Form)**
   - 出现在单词中间
   - 上下都有连接

3. **词尾形式 (Final Form)**
   - 出现在单词结尾
   - 特殊的底部收尾

4. **独立形式 (Isolated Form)**
   - 单独出现
   - 不与任何字符连接

---

## 自由变体选择符 (FVS)

### 作用

蒙古文中存在**同形异码**现象，需要使用 FVS 来区分：

- **FVS1** (U+180B)：自由变体选择符 1
- **FVS2** (U+180C)：自由变体选择符 2
- **FVS3** (U+180D)：自由变体选择符 3

### 使用场景

```
基本字符 + FVS1 → 变体 1
基本字符 + FVS2 → 变体 2
基本字符 + FVS3 → 变体 3
```

### 示例

某些字母在相同位置可能有多种写法，使用 FVS 来指定：

```
ᠭᠠ (ga) - 标准形式
ᠭ᠎ᠠ (ga+FVS1) - 变体形式 1
```

---

## 对我们的项目的指导

### 1. 文本规范化

根据 UTN #57，我们需要：

```python
class MongolianNormalizer:
    """
    蒙古文文本规范化器（基于 Unicode UTN #57）
    
    功能：
    1. 统一使用 Unicode 编码
    2. 规范化 FVS 使用
    3. 处理同形异码问题
    4. 应用字形变换规则
    """
```

### 2. 字形变换引擎

```python
class MongolianShaper:
    """
    蒙古文字形变换引擎
    
    分层变换：
    1. 基础变换 - 识别词位置
    2. 上下文变换 - 应用上下文规则
    3. 变体选择 - 处理 FVS
    """
    
    def shape(self, text):
        # 第 1 层：基础变换
        text = self.basic_shaping(text)
        
        # 第 2 层：上下文变换
        text = self.contextual_shaping(text)
        
        # 第 3 层：变体选择
        text = self.variant_selection(text)
        
        return text
```

### 3. 字体支持

根据 UTN #57，字体需要：

- 支持 OpenType 蒙古文特性
- 实现字形变换规则
- 提供所有变体字形

推荐字体：
- Mongolian Baiti (Windows 默认)
- Mongolfont 系列
- Noto Sans Mongolian (Google)

### 4. CSS 实现

```css
.mongolian-text {
    /* 书写模式 */
    writing-mode: vertical-lr;
    
    /* 字符方向 */
    text-orientation: upright;
    
    /* 字体 - 支持 OpenType 蒙古文特性 */
    font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
    
    /* OpenType 特性 */
    font-feature-settings: 'mong';
}
```

---

## 关键发现

### 1. 同形异码问题

**现象**：同一单词的字形正确但内码序列不正确

**原因**：
- 历史编码不统一
- FVS 使用不规范
- 输入法不标准

**解决**：
- 推广 Unicode 标准
- 使用智能输入法
- 应用校对工具

### 2. 字形变换复杂性

蒙古文不是简单的"字符映射"，而是需要：
- 上下文分析
- 位置判断
- 变体选择
- 规则应用

### 3. 标准化进展

- **2000 年**：Unicode 3.0 收录蒙古文
- **2006 年**：Windows Vista 首次支持
- **2016 年**：UTN #57 首次发布
- **2024 年**：UTN #57 Version 4（最新版本）

---

## 与其他文档的关系

### W3C Mongolian Layout Requirements

- **W3C**：关注 Web 排版和 CSS
- **Unicode UTN #57**：关注编码和字形变换
- **互补关系**：两者结合使用

### ACL 2020 论文

- **ACL 2020**：研究拼写形式多样化现象
- **Unicode UTN #57**：提供标准化解决方案
- **关系**：ACL 论文指出的问题，UTN #57 提供标准

---

## 下一步行动

### 1. 实现规范化模块

```python
# 基于 UTN #57 实现
class MongolianTextNormalizer:
    def normalize(self, text):
        # 1. 统一编码
        # 2. 规范化 FVS
        # 3. 应用字形变换
        # 4. 输出标准化文本
        pass
```

### 2. 集成到 CSS

```css
/* 使用 OpenType 特性 */
font-feature-settings: 'mong';
```

### 3. 开发校对工具

- 检测不规范编码
- 提供纠正建议
- 批量处理

### 4. 学习 PDF 全文

- 下载 utn57-mong-4.pdf
- 详细学习字形变换规则
- 应用到项目中

---

## 参考资源

### 官方文档
- Unicode TN #57: https://www.unicode.org/notes/tn57/
- PDF 版本：https://www.unicode.org/notes/tn57/utn57-mong-4.pdf
- Mongolian Unicode Block: https://unicode.org/charts/PDF/U1800.pdf

### 相关标准
- W3C Mongolian Layout: https://www.w3.org/TR/mlreq/
- OpenType Mongolian: https://docs.microsoft.com/typography/script-development/mongolian

### 字体资源
- Mongolfont: http://www.mongolfont.com/
- Noto Sans Mongolian: https://fonts.google.com/noto

---

**笔记整理**：OpenClaw Mongolian AI Team  
**日期**：2026-03-30  
**版本**：v1.0  
**基于**：Unicode Technical Note #57 Version 4 (2024-08-14)
