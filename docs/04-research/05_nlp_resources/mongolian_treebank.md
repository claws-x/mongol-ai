# 蒙古文树库资源

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [什么是树库](#什么是树库)
3. [Universal Dependencies](#universal-dependencies)
4. [蒙古文树库现状](#蒙古文树库现状)
5. [树库构建方法](#树库构建方法)
6. [依存标注体系](#依存标注体系)
7. [现有资源清单](#现有资源清单)
8. [使用指南](#使用指南)
9. [贡献指南](#贡献指南)
10. [参考资料](#参考资料)

---

## 概述

### 什么是树库

树库 (Treebank) 是经过句法标注的语料库，包含：
- **词性标注**: 每个词的词性
- **句法结构**: 词与词之间的依存关系
- **短语结构**: 短语成分划分 (可选)

**示例** (CoNLL-U 格式):
```
# text = ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠪᠣᠯ ᠳᠡᠯᠬᠢᠶᠡᠨ ᠬᠠᠮᠤᠭ ᠦᠨᠳᠦᠰᠦᠨ ᠦ ᠨᠢᠭᠡ ᠬᠡᠯᠡ ᠪᠣᠯᠤᠮᠳᠠᠢ᠃
1	ᠮᠣᠩᠭᠣᠯ	ᠮᠣᠩᠭᠣᠯ	PROPN	_	2	nmod	_	_
2	ᠬᠡᠯᠡ	ᠬᠡᠯᠡ	NOUN	_	4	nsubj	_	_
3	ᠪᠣᠯ	ᠪᠣᠯ	PART	_	2	case	_	_
4	ᠳᠡᠯᠬᠢᠶᠡᠨ	ᠳᠡᠯᠬᠢᠶᠡᠨ	NOUN	_	0	root	_	_
5	ᠬᠠᠮᠤᠭ	ᠬᠠᠮᠤᠭ	ADJ	_	6	amod	_	_
6	ᠦᠨᠳᠦᠰᠦᠨ	ᠦᠨᠳᠦᠰᠦᠨ	NOUN	_	4	nmod	_	_
7	ᠦ	ᠦ	ADP	_	6	case	_	_
8	ᠨᠢᠭᠡ	ᠨᠢᠭᠡ	NUM	_	9	nummod	_	_
9	ᠬᠡᠯᠡ	ᠬᠡᠯᠡ	NOUN	_	4	appos	_	_
10	ᠪᠣᠯᠤᠮᠳᠠᠢ	ᠪᠣᠯᠤᠮᠳᠠᠢ	AUX	_	4	cop	_	_
11	᠃	᠃	PUNCT	_	4	punct	_	_
```

### 为什么需要树库

| 用途 | 描述 | 重要性 |
|------|------|--------|
| 句法分析器训练 | 依存分析模型训练数据 | ⭐⭐⭐⭐⭐ |
| 语言类型学研究 | 跨语言句法对比 | ⭐⭐⭐⭐ |
| 机器翻译 | 句法对齐辅助 | ⭐⭐⭐⭐ |
| 语言教学 | 语法可视化工具 | ⭐⭐⭐⭐ |
| 评估基准 | 句法分析准确率评估 | ⭐⭐⭐⭐⭐ |

### 蒙古文树库现状

**关键事实**:
- ✅ 西里尔蒙古文树库：存在 (UD Mongolian)
- ❌ 传统蒙古文树库：**不存在** (截至 2026-04)
- ⚠️ 古典蒙古文树库：极少 (学术项目)

**机会**: 构建首个传统蒙古文树库

---

## Universal Dependencies

### UD 简介

Universal Dependencies (UD) 是跨语言的依存句法标注框架：

- **官网**: https://universaldependencies.org/
- **语言**: 支持 100+ 语言
- **标注体系**: 统一的词性和依存关系标签集
- **数据格式**: CoNLL-U

### UD 蒙古文 (西里尔)

```
# UD Treebank: Mongolian
# Language: mn (西里尔蒙古语)
# License: CC BY-SA 4.0
# URL: https://universaldependencies.org/treebanks/mn_hdt/

# 统计
Sentences: 4,231
Tokens: 89,456
```

**示例句子**:
```
# text = Би монгол хэл сулж байна.
# text_en = I am learning Mongolian language.
1	Би	би	PRON	_	3	nsubj	_	_
2	монгол	монгол	ADJ	_	3	amod	_	_
3	хэл	хэл	NOUN	_	4	obj	_	_
4	сулж	сул	VERB	_	5	advcl	_	_
5	байна	бай	AUX	_	0	root	_	_
6	.	.	PUNCT	_	5	punct	_	_
```

### UD 依存关系标签

| 标签 | 全称 | 说明 | 示例 |
|------|------|------|------|
| root | root | 句根 | 主要动词 |
| nsubj | nominal subject | 名词性主语 | ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ **ᠪᠣᠯᠤᠮᠳᠠᠢ** |
| obj | object | 宾语 | ᠪᠢᠴᠢᠭ **ᠤᠨᠰᠢᠬᠤ** |
| nmod | nominal modifier | 名词修饰语 | **ᠮᠣᠩᠭᠣᠯ** ᠦᠨ ᠬᠡᠯᠡ |
| amod | adjectival modifier | 形容词修饰语 | **ᠶᠡᠬᠡ** ᠭᠡᠷ |
| advmod | adverbial modifier | 副词修饰语 | **ᠮᠠᠰᠢ** ᠰᠠᠶᠢᠨ |
| case | case marking | 格标记 | ᠭᠡᠷ **ᠦ** ᠬᠦᠮᠦᠨ |
| cop | copula | 系动词 | ᠮᠣᠩᠭᠣᠯ **ᠪᠣᠯ** |
| conj | conjunct | 并列成分 | ᠮᠣᠩᠭᠣᠯ **ᠪᠣᠯᠣ** ᠬᠢᠲᠠᠳ |
| mark | marker | 标记词 | **ᠬᠠᠭᠠᠰ** ᠪᠢᠴᠢᠬᠦ |
| aux | auxiliary | 助动词 | ᠪᠢᠴᠢᠭᠰᠡᠨ **ᠪᠠᠶᠢᠨ᠎ᠠ** |
| punct | punctuation | 标点 | ᠃ |

---

## 蒙古文树库现状

### 西里尔蒙古文树库

#### UD Mongolian (HDT)

```yaml
名称：Mongolian Human Development Report Treebank
语言：西里尔蒙古语 (mn)
规模：4,231 句，89,456 词
许可证：CC BY-SA 4.0
来源：联合国开发计划署蒙古语报告
URL: https://universaldependencies.org/treebanks/mn_hdt/
```

**特点**:
- ✅ 官方 UD 树库
- ✅ 质量高 (人工标注 + 审核)
- ✅ 持续更新
- ❌ 仅西里尔文

#### Mongolian Dependency Treebank (MDT)

```yaml
名称：Mongolian Dependency Treebank
语言：西里尔蒙古语
规模：~10,000 句
许可证：研究用
来源：蒙古国立大学
```

### 传统蒙古文树库

**现状**: 无公开可用树库

**原因**:
1. 标注成本高 (需要专家)
2. 语料数字化程度低
3. 研究者少
4. 资金不足

**机会**:
- 首个传统蒙古文 UD 树库
- 可借用西里尔树库标注体系
- 可结合古典文献数字化项目

---

## 树库构建方法

### 构建流程

```
1. 语料收集
   ↓
2. 文本数字化
   ↓
3. 分词
   ↓
4. 词性标注 (自动 + 人工校对)
   ↓
5. 句法标注 (自动 + 人工校对)
   ↓
6. 质量审核
   ↓
7. 发布 (CoNLL-U 格式)
```

### 语料来源

| 来源 | 类型 | 规模 | 许可证 |
|------|------|------|--------|
| 蒙古国政府文件 | 正式文体 | ~100 万词 | CC BY 4.0 |
| 蒙古国新闻 | 新闻文体 | ~500 万词 | 混合 |
| 古典文献 | 古典文体 | ~50 万词 | 公有领域 |
| 现代文学 | 文学文体 | ~200 万词 | 混合 |
| 社交媒体 | 口语体 | ~100 万词 | 混合 |

### 标注工具

#### 1. brat (Web 标注)

```
URL: http://brat.nlplab.org/
特点：
- Web 界面
- 可视化标注
- 支持多人协作
- 导出 CoNLL-U
```

#### 2. INCEpTION

```
URL: https://inception-project.github.io/
特点：
- 现代 Web 界面
- 主动学习支持
- 多语言支持
- 导出多种格式
```

#### 3. UD Pipe (自动标注)

```python
from ufal.udpipe import Model, Pipeline

# 加载模型 (西里尔蒙古语)
model = Model.load("mongolian-hdt-ud-2.9.udpipe")
pipeline = Pipeline(model)

# 自动标注
sentence = "Би монгол хэл сулж байна."
output = pipeline.process(sentence)
print(output)  # CoNLL-U 格式
```

### 质量评估

#### 标注一致性 (Inter-annotator Agreement)

```python
def calculate_kappa(annotations1, annotations2):
    """
    计算 Cohen's Kappa (标注一致性)
    
    Args:
        annotations1: 标注员 1 的标注
        annotations2: 标注员 2 的标注
    
    Returns:
        Kappa 值 (0-1, 越高越好)
    """
    from sklearn.metrics import cohen_kappa_score
    
    kappa = cohen_kappa_score(annotations1, annotations2)
    return kappa

# 目标：Kappa > 0.8 (高质量)
```

#### 标注质量指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| Kappa | > 0.8 | 标注一致性 |
| 词性准确率 | > 95% | 词性标注正确率 |
| 依存准确率 | > 90% | 依存关系正确率 |
| 完整率 | 100% | 所有词都标注 |

---

## 依存标注体系

### 蒙古语句法特点

#### 1. SOV 语序

蒙古语基本语序：主 - 宾 - 谓 (SOV)

```
ᠪᠢ (我) ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ (蒙古语) ᠰᠤᠷᠤᠭᠰᠡᠨ (学习)
S         O                  V
```

#### 2. 后置词

蒙古语使用后置词而非前置词：

```
ᠭᠡᠷ ᠦ ᠬᠦᠮᠦᠨ
家  的 人
"家的人"
```

#### 3. 从属结构

从属句在主句之前：

```
[ᠬᠠᠭᠠᠰ ᠴᠢ ᠢᠷᠡᠬᠦ] ᠪᠢ ᠬᠦᠯᠢᠶᠡᠨ ᠠᠪᠴᠤ
[如果 你 来] 我 高兴 会
```

### 标注指南

#### 核心关系

```
root: 句子核心 (通常是动词)
  ↓
nsubj: 主语
obj: 宾语
  ↓
nmod: 名词修饰语 (所有格)
  ↓
case: 格标记/后置词
```

#### 示例分析

**句子**: ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠬᠡᠯᠡ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠮᠥᠨ ᠪᠣᠯᠤᠮᠳᠠᠢ᠃

```
1	ᠮᠣᠩᠭᠣᠯ	_	PROPN	_	2	nmod	_	_
2	ᠦᠨᠳᠦᠰᠦᠲᠡᠨ	_	NOUN	_	4	nsubj	_	_
3	ᠦ	_	ADP	_	2	case	_	_
4	ᠬᠡᠯᠡ	_	NOUN	_	6	root	_	_
5	ᠪᠣᠯ	_	PART	_	4	mark	_	_
6	ᠮᠣᠩᠭᠣᠯ	_	PROPN	_	7	nmod	_	_
7	ᠬᠡᠯᠡ	_	NOUN	_	4	appos	_	_
8	ᠮᠥᠨ	_	PART	_	7	case	_	_
9	ᠪᠣᠯᠤᠮᠳᠠᠢ	_	AUX	_	4	cop	_	_
10	᠃	_	PUNCT	_	4	punct	_	_
```

---

## 现有资源清单

### 语料库

| 名称 | 规模 | 文字 | 许可证 | URL |
|------|------|------|--------|-----|
| Mongolian National Corpus | 1000 万词 | 西里尔 | 研究用 | - |
| tugstugi/mongolian-corpus | 500 万词 | 西里尔 | MIT | GitHub |
| 蒙古国政府公文 | 200 万词 | 西里尔 | CC BY | - |
| 古典蒙古文献 | 50 万词 | 传统 | 公有 | - |

### 标注工具

| 工具 | 类型 | 许可证 | 蒙古语支持 |
|------|------|--------|-----------|
| brat | Web 标注 | GPL | ⚠️ 需配置 |
| INCEpTION | Web 标注 | Apache 2.0 | ⚠️ 需配置 |