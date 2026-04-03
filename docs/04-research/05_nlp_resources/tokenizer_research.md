# 蒙古文分词器调研

**版本**: v1.0  
**创建时间**: 2026-04-03  
**状态**: 高优先级  
**相关文档**: [[pretrained_models.md]], [[../02_vertical_writing/unicode_control_codes.md]]

---

## 1. 蒙古文分词挑战

### 1.1 文字特性带来的困难

传统蒙古文（Traditional Mongolian Script）的分词面临以下独特挑战：

#### 1.1.1 连写特性

蒙古文是竖排连写文字，词内字母通过连笔连接，但词与词之间有明显间隔：

```
ᠬᠥᠭᠡᠭᠰᠡᠨ ᠪᠣᠯᠲᠤᠭ᠎ᠠ ᠪᠠᠢᠨ᠎ᠠ
(kö'gesen boltuγ-a bain-a)
"说过 是 - 在"
```

**问题**:
- 词内连写可能导致边界模糊
- 某些词缀与词干连接紧密
- 变体选择符 (FVS) 影响字形但不影响分词

#### 1.1.2 形态丰富性

蒙古文是黏着语，一个词可以包含多个词缀：

```
ᠭᠡᠷᠡᠯᠲᠡᠢ (gerel-tei) = ᠭᠡᠷᠡᠯ (gerel, 光) + ᠲᠡᠢ (-tei, 有)
"有光的"

ᠪᠢᠳᠡᠨᠡᠷ (biden-er) = ᠪᠢᠳᠡ (bide, 我们) + ᠨᠡᠷ (-ner, 复数)
"我们 (复数)"
```

**分词策略选择**:
- 粗粒度：只分词干，词缀不分离
- 细粒度：词干 + 词缀分别标注
- 混合：常用词缀合并，罕见词缀分离

#### 1.1.3 元音和谐律

蒙古语遵循元音和谐律，影响词缀形式：

```
ᠭᠡᠷ ᠡᠴᠡ (ger-ece) = 从家
ᠬᠥᠬᠡ ᠡᠴᠡ (köke-ece) = 从蓝色

词缀 -ece/-ece 根据词干元音变化
```

**影响**: 分词器需要识别元音和谐模式以正确切分词缀。

#### 1.1.4 Unicode 编码复杂性

```python
# 蒙古文 Unicode 编码示例
word = "ᠬᠥᠭᠡᠭᠰᠡᠨ"  # kö'gesen (说过)
codepoints = [ord(c) for c in word]
# [U+182C, U+1825, U+182D, U+1825, U+182D, U+1830, U+1825, U+1828]

# 包含 FVS 的情况
word_fvs = "ᠭᠠ"  # ga
word_fvs_var = "ᠭ᠎ᠠ"  # ga + FVS1
# FVS1 (U+180B) 是零宽字符
```

**挑战**:
- FVS 字符不影响分词但影响字形
- NNBSP (U+202F) 用于词内连接控制
- 需要规范化处理 (NFC/NFD)

---

## 2. 现有分词工具调研

### 2.1 开源工具

#### 2.1.1 Stanza (Stanford NLP)

```python
import stanza

# 蒙古语支持 (实验性)
stanza.download('mn')  # 西里尔蒙古语
# 传统蒙古文支持有限

nlp = stanza.Pipeline('mn')
doc = nlp("Би монгол хэл сулж байна.")
for word in doc.sentences[0].words:
    print(word.text, word.upos)
```

**状态**: 主要支持西里尔蒙古语，传统蒙古文需自定义训练。

#### 2.1.2 spaCy

```python
# spaCy 无官方蒙古语模型
# 需自定义训练

import spacy
from spacy.training.example import Example

nlp = spacy.blank('mn')  # 创建空白蒙古语模型

# 添加分词器规则
nlp.tokenizer = CustomMongolianTokenizer(nlp.vocab)
```

**状态**: 需完全自定义实现。

#### 2.1.3 Jieba (中文分词器参考)

```python
# Jieba 不适用于蒙古文
# 但算法可参考

import jieba

# 蒙古文需类似但不同的实现
# - 基于词典的匹配
# - HMM 未登录词识别
# - CRF 序列标注
```

### 2.2 学术工具

#### 2.2.1 Mongolian NLP Toolkit (内蒙古大学)

**功能**:
- 西里尔蒙古语分词
- 词性标注
- 依存句法分析

**局限**: 不支持传统蒙古文。

#### 2.2.2 OpenMongolia Project

**GitHub**: `openmongolia/nlp` (假设)

```bash
# 安装 (假设)
pip install openmongolia-nlp

from openmongolia import TraditionalMongolianTokenizer

tokenizer = TraditionalMongolianTokenizer()
tokens = tokenizer.tokenize("ᠬᠥᠭᠡᠭᠰᠡᠨ ᠪᠣᠯᠲᠤᠭ᠎ᠠ")
# ['ᠬᠥᠭᠡᠭᠰᠡᠨ', 'ᠪᠣᠯᠲᠤᠭ᠎ᠠ']
```

**状态**: 需调研实际可用性。

### 2.3 商业 API

#### 2.3.1 Menksoft Mongolian IME

**功能**: 输入法内置简单分词
**API**: 未公开
**适用性**: 不适合 NLP 任务

---

## 3. 基于 BERT 的分词方案

### 3.1 WordPiece vs BPE vs Unigram

| 算法 | 优点 | 缺点 | 适用性 |
|------|------|------|--------|
| WordPiece (BERT) | 平衡粒度，OOV 处理好 | 需预定义词表 | ★★★★☆ |
| BPE (GPT) | 灵活，可压缩词表 | 可能过分割 | ★★★☆☆ |
| Unigram (SentencePiece) | 概率优化，支持多语言 | 训练慢 | ★★★★☆ |

**推荐**: WordPiece 或 SentencePiece (Unigram)

### 3.2 训练自定义 Tokenizer

#### 3.2.1 使用 Hugging Face tokenizers

```python
from tokenizers import Tokenizer, models, trainers, pre_tokenizers
from tokenizers.processors import TemplateProcessing

# 1. 初始化 tokenizer
tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))

# 2. 预分词器 (蒙古文需自定义)
# 蒙古文以空格分词为基础
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

# 3. 训练器
trainer = trainers.WordPieceTrainer(
    vocab_size=30000,
    min_frequency=2,
    special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
)

# 4. 训练
files = ["mongolian_corpus.txt"]
tokenizer.train(files, trainer)

# 5. 保存
tokenizer.save("mongolian_wordpiece.json")
```

#### 3.2.2 使用 SentencePiece

```python
import sentencepiece as spm

# 训练
spm.SentencePieceTrainer.train(
    input="mongolian_corpus.txt",
    model_prefix="mongolian_sp",
    vocab_size=30000,
    model_type="unigram",  # 或 "bpe"
    pad_id=0,
    bos_id=1,
    eos_id=2,
    unk_id=3,
    character_coverage=0.9995,
    split_by_whitespace=True
)

# 加载
sp = spm.SentencePieceProcessor()
sp.load("mongolian_sp.model")

# 分词
tokens = sp.encode("ᠬᠥᠭᠡᠭᠰᠡᠨ ᠪᠣᠯᠲᠤᠭ᠎ᠠ", out_type=str)
# ['▁ᠬᠥᠭᠡᠭ', 'ᠰᠡᠨ', '▁ᠪᠣᠯᠲᠤᠭ', '᠎ᠠ']
```

### 3.3 处理蒙古文特殊字符

```python
import unicodedata
import re

class MongolianTextNormalizer:
    def __init__(self):
        # 蒙古文 Unicode 范围
        self.mongolian_range = re.compile(r'[\u1800-\u18AF]')
        
    def normalize(self, text):
        """
        规范化蒙古文文本
        """
        # 1. Unicode 规范化 (NFC)
        text = unicodedata.normalize('NFC', text)
        
        # 2. 移除零宽非字符 (可选)
        # text = text.replace('\u180E', '')  # MVS (已弃用)
        
        # 3. 统一 FVS 表示
        # 保持 FVS1/FVS2/FVS3
        
        # 4. 处理 NNBSP
        # 词内 NNBSP 保留，词间替换为空格
        text = text.replace('\u202F', ' ')
        
        return text
    
    def tokenize_basic(self, text):
        """
        基础分词 (按空格)
        """
        normalized = self.normalize(text)
        return normalized.split()

# 测试
normalizer = MongolianTextNormalizer()
text = "ᠬᠥᠭᠡᠭᠰᠡᠨ ᠪᠣᠯᠲᠤᠭ᠎ᠠ ᠪᠠᠢᠨ᠎ᠠ"
tokens = normalizer.tokenize_basic(text)
print(tokens)
# ['ᠬᠥᠭᠡᠭᠰᠡᠨ', 'ᠪᠣᠯᠲᠤᠭ᠎ᠠ', 'ᠪᠠᠢᠨ᠎ᠠ']
```

### 3.4 集成到 BERT Tokenizer

```python
from transformers import BertTokenizerFast

# 加载自定义 tokenizer
tokenizer = BertTokenizerFast(
    vocab_file="mongolian_wordpiece.json",
    do_lower_case=False,  # 蒙古文不区分大小写
    strip_accents=False,
)

# 编码
encoding = tokenizer(
    "ᠬᠥᠭᠡᠭᠰᠡᠨ ᠪᠣᠯᠲᠤᠭ᠎ᠠ ᠪᠠᠢᠨ᠎ᠠ",
    padding="max_length",
    truncation=True,
    max_length=128,
    return_tensors="pt"
)

print(encoding.input_ids.shape)  # torch.Size([1, 128])
print(tokenizer.convert_ids_to_tokens(encoding.input_ids[0][:10]))
# ['[CLS]', 'ᠬᠥᠭᠡᠭ', 'ᠰᠡᠨ', 'ᠪᠣᠯᠲᠤᠭ', '᠎ᠠ', 'ᠪᠠᠢᠨ᠎ᠠ', '[SEP]', '[PAD]', ...]
```

---

## 4. 代码示例和测试

### 4.1 完整分词器类

```python
"""
mongolian_tokenizer.py
传统蒙古文分词器实现
"""

import re
import json
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Token:
    """分词结果"""
    text: str
    start: int
    end: int
    pos: Optional[str] = None  # 词性 (可选)

class MongolianTokenizer:
    """传统蒙古文分词器"""
    
    def __init__(self, vocab_path: Optional[str] = None):
        """
        初始化分词器
        
        Args:
            vocab_path: 词表文件路径 (可选)
        """
        self.vocab = None
        if vocab_path:
            self.load_vocab(vocab_path)
        
        # 蒙古文 Unicode 范围
        self.mongolian_pattern = re.compile(r'[\u1800-\u18AF]+')
        
        # 标点符号
        self.punctuation = set([
            '\u1800',  # BIRGA
            '\u1801',  # ELLIPSIS
            '\u1802',  # COMMA
            '\u1803',  # FULL STOP
            '\u1804',  # COLON
            '\u1805',  # FOUR DOTS
        ])
    
    def load_vocab(self, path: str):
        """加载词表"""
        with open(path, 'r', encoding='utf-8') as f:
            self.vocab = json.load(f)
    
    def normalize(self, text: str) -> str:
        """文本规范化"""
        import unicodedata
        return unicodedata.normalize('NFC', text)
    
    def tokenize(self, text: str) -> List[Token]:
        """
        基础分词
        
        Args:
            text: 输入文本
            
        Returns:
            Token 列表
        """
        text = self.normalize(text)
        tokens = []
        
        # 按空格分割
        words = text.split()
        
        pos = 0
        for word in words:
            start = text.find(word, pos)
            end = start + len(word)
            
            # 移除标点 (可选)
            clean_word = word
            for punct in self.punctuation:
                clean_word = clean_word.replace(punct, '')
            
            if clean_word:
                tokens.append(Token(
                    text=clean_word,
                    start=start,
                    end=end
                ))
            
            pos = end
        
        return tokens
    
    def tokenize_with_subwords(self, text: str) -> List[str]:
        """
        子词分词 (使用词表)
        
        Args:
            text: 输入文本
            
        Returns:
            子词列表
        """
        if not self.vocab:
            raise ValueError("词表未加载")
        
        tokens = self.tokenize(text)
        subwords = []
        
        for token in tokens:
            # 最长匹配
            word = token.text
            start = 0
            while start