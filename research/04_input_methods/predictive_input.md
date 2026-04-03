# 智能预测输入

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [预测输入技术原理](#预测输入技术原理)
3. [蒙古文预测特殊挑战](#蒙古文预测特殊挑战)
4. [词典设计](#词典设计)
5. [算法实现](#算法实现)
6. [深度学习方案](#深度学习方案)
7. [用户界面设计](#用户界面设计)
8. [性能优化](#性能优化)
9. [测试评估](#测试评估)
10. [参考资料](#参考资料)

---

## 概述

### 什么是预测输入

预测输入 (Predictive Input) 是根据用户已输入内容预测后续可能输入的词语或短语的技术，也称为：
- 智能联想
- 自动补全
- 下一词预测 (Next Word Prediction)

### 为什么需要预测输入

| 优势 | 描述 | 蒙古文场景价值 |
|------|------|---------------|
| 减少击键 | 减少 30-50% 输入量 | ⭐⭐⭐⭐⭐ 竖排输入效率低 |
| 降低错误 | 减少拼写错误 | ⭐⭐⭐⭐ FVS 选择复杂 |
| 学习辅助 | 帮助非母语者 | ⭐⭐⭐⭐⭐ 教育场景 |
| 提速 | 提升输入速度 | ⭐⭐⭐⭐ 移动端小键盘 |

### 市场现状

**西里尔蒙古文**:
- 标准输入法 (Windows/macOS/Android/iOS)
- 基础词库预测
- 技术成熟

**传统蒙古文**:
- Menksoft: 基础预测 (封闭词库)
- 开源项目: 无成熟方案
- **机会**: 首个开源智能预测方案

---

## 预测输入技术原理

### 技术架构

```
┌─────────────────────────────────────────────────────┐
│                   用户输入界面                        │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│                  输入预处理模块                       │
│  - 规范化 (NFC/NFD)  - FVS 提取  - 词边界检测          │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│                  预测引擎核心                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  词典匹配    │  │  N-gram 模型  │  │  神经网络    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│                  候选排序模块                         │
│  - 频率排序  - 上下文加权  - 用户习惯学习             │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│                  候选展示界面                         │
│  [候选 1] [候选 2] [候选 3] [候选 4] [候选 5]        │
└─────────────────────────────────────────────────────┘
```

### 预测类型

#### 1. 词内预测 (Intra-word)

预测当前词的后续字母/音节。

```
用户输入：ᠮᠣᠩ (moŋ)
预测候选:
  - ᠮᠣᠩᠭᠣᠯ (mongɣol)     频率：高
  - ᠮᠣᠩᠭᠤᠯ (mongɣul)     频率：中
  - ᠮᠣᠩᠭᠡᠷ (mongɣer)     频率：低
```

#### 2. 词间预测 (Inter-word)

预测下一个完整词语。

```
用户输入：ᠪᠢ (bi 我)
预测候选:
  - ᠪᠣᠯᠨ᠎ᠠ (bolna 是)    频率：高
  - ᠬᠦᠭᠦᠮ (küküm 我的)   频率：中
  - ᠮᠣᠩᠭᠣᠯ (mongɣol 蒙古) 频率：中
```

#### 3. 短语预测 (Phrase)

预测常用短语/搭配。

```
用户输入：ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ (mongɣol ündüsüten 蒙古族)
预测候选:
  - ᠦᠨ ᠬᠡᠯᠡ (ün kele 语言)
  - ᠦᠨ ᠪᠢᠴᠢᠭ (ün bičig 文字)
  - ᠦᠨ ᠲᠦᠬᠡ (ün tükhe 历史)
```

---

## 蒙古文预测特殊挑战

### 挑战 1: 竖排书写方向

**问题**: 传统从左到右的输入逻辑需要适配竖排显示

**解决方案**:
```javascript
class VerticalInputAdapter {
  constructor(inputElement) {
    this.input = inputElement;
    this.isVertical = true;
  }
  
  // 将竖排光标位置转换为逻辑位置
  verticalToLogicalPosition(verticalPos) {
    // 竖排：从上到下 = 逻辑：从左到右
    return verticalPos;
  }
  
  // 更新候选框位置
  updateCandidatePosition(cursorRect) {
    // 竖排时候选框显示在右侧
    return {
      x: cursorRect.right + 10,
      y: cursorRect.top,
      direction: 'vertical'
    };
  }
}
```

### 挑战 2: FVS 变体选择

**问题**: 同一词根可能有多种 FVS 变体

**解决方案**:
```javascript
class FVSAwarePredictor {
  constructor() {
    this.fvsPatterns = new Map();
    this.loadFVSPatterns();
  }
  
  loadFVSPatterns() {
    // 预加载常见 FVS 模式
    this.fvsPatterns.set('ᠭᠠ', ['ᠭ᠎ᠠ', 'ᠭ᠏ᠠ']);
    this.fvsPatterns.set('ᠨᠠ', ['ᠨ᠎ᠠ']);
  }
  
  predictWithFVS(input) {
    const basePredictions = this.predict(input);
    
    // 为每个预测添加 FVS 变体
    return basePredictions.map(pred => ({
      text: pred,
      variants: this.getFVSVariants(pred),
      score: this.calculateScore(pred)
    }));
  }
}
```

### 挑战 3: 词边界模糊

**问题**: 蒙古文连写导致词边界不明显

**解决方案**:
```javascript
class MongolianSegmenter {
  // 基于规则的分词
  segmentByRules(text) {
    const possessiveMarkers = ['ᠤᠨ', 'ᠦᠨ', 'ᠢᠨ', 'ᠶᠢᠨ'];
    const pluralMarkers = ['ᠦᠳ', 'ᠦᠨᠦᠳ', 'ᠰ', 'ᠴᠦᠳ'];
    
    let segments = [];
    let remaining = text;
    
    for (const marker of [...possessiveMarkers, ...pluralMarkers]) {
      if (remaining.endsWith(marker)) {
        segments.unshift(marker);
        remaining = remaining.slice(0, -marker.length);
      }
    }
    
    segments.unshift(remaining);
    return segments;
  }
}
```

---

## 词典设计

### 词典结构

```json
{
  "version": "1.0",
  "language": "traditional-mongolian",
  "entries": [
    {
      "word": "ᠮᠣᠩᠭᠣᠯ",
      "frequency": 9850,
      "pos": "noun",
      "definition": "蒙古",
      "variants": ["ᠮᠣᠩᠭᠣᠯᠤᠨ", "ᠮᠣᠩᠭᠣᠯᠳᠠ"]
    },
    {
      "word": "ᠪᠢᠴᠢᠭ",
      "frequency": 7230,
      "pos": "noun",
      "definition": "文字、书写"
    }
  ],
  "bigrams": [
    {"from": "ᠮᠣᠩᠭᠣᠯ", "to": "ᠦᠨᠳᠦᠰᠦᠲᠡᠨ", "frequency": 4520},
    {"from": "ᠪᠢ", "to": "ᠪᠣᠯᠨ᠎ᠠ", "frequency": 3890}
  ]
}
```

### 词典来源

| 来源 | 词量 | 许可证 | 质量 |
|------|------|--------|------|
| tugstugi/mongolian-nlp | ~50k | MIT | ⭐⭐⭐⭐ |
| 蒙古国教育部标准词表 | ~80k | 未知 | ⭐⭐⭐⭐⭐ |
| 自建网络爬虫 | ~200k | CC BY 4.0 | ⭐⭐⭐ |

---

## 算法实现

### N-gram 模型

```javascript
class NGramPredictor {
  constructor(n = 2) {
    this.n = n;
    this.ngramCounts = new Map();
    this.contextCounts = new Map();
  }
  
  train(corpus) {
    for (const sentence of corpus) {
      const tokens = sentence.split(/\s+/);
      const padded = [
        ...Array(this.n - 1).fill('<START>'),
        ...tokens,
        ...Array(this.n - 1).fill('<END>')
      ];
      
      for (let i = this.n - 1; i < padded.length; i++) {
        const context = padded.slice(i - this.n + 1, i).join(' ');
        const word = padded[i];
        const key = `${context} → ${word}`;
        
        this.ngramCounts.set(key, (this.ngramCounts.get(key) || 0) + 1);
        this.contextCounts.set(context, (this.contextCounts.get(context) || 0) + 1);
      }
    }
  }
  
  predict(context) {
    const contextKey = context.slice(-(this.n - 1)).join(' ');
    const candidates = [];
    
    for (const [key, count] of this.ngramCounts.entries()) {
      if (key.startsWith(`${contextKey} → `)) {
        const word = key.split(' → ')[1];
        const prob = count / (this.contextCounts.get(contextKey) || 1);
        candidates.push({ word, probability: prob });
      }
    }
    
    return candidates.sort((a, b) => b.probability - a.probability);
  }
}
```

###  Trie 树加速查找

```javascript
class TrieNode {
  constructor() {
    this.children = new Map();
    this.isEndOfWord = false;
    this.frequency = 0;
    this.word = null;
  }
}

class MongolianTrie {
  constructor() {
    this.root = new TrieNode();
  }
  
  insert(word, frequency) {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char);
    }
    node.isEndOfWord = true;
    node.frequency = frequency;
    node.word = word;
  }
  
  // 前缀搜索
  searchWithPrefix(prefix) {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) return [];
      node = node.children.get(char);
    }
    return this.collectAllWords(node);
  }
  
  collectAllWords(node, results = []) {
    if (node.isEndOfWord) {
      results.push({ word: node.word, frequency: node.frequency });
    }
    for (const child of node.children.values()) {
      this.collectAllWords(child, results);
    }
    return results.sort((a, b) => b.frequency - a.frequency);
  }
}
```

---

## 深度学习方案

### Transformer 模型

使用 Hugging Face 的蒙古文 BERT 模型进行下一词预测：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class MongolianNeuralPredictor:
    def __init__(self, model_name='tugstugi/mongolian-gpt2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
    def predict(self, text, top_k=5, max_length=50):
        """
        预测后续文本
        
        Args:
            text: 输入文本
            top_k: 返回候选数量
            max_length: 最大生成长度
        
        Returns:
            预测候选列表
        """
        inputs = self.tokenizer(text, return_tensors='pt')
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                num_return_sequences=top_k,
                do_sample=True,
                top_p=0.95,
                temperature=0.7
            )
        
        predictions = []
        for output in outputs:
            pred_text = self.tokenizer.decode(output, skip_special_tokens=True)
            predictions.append({
                'text': pred_text,
                'confidence': self.calculate_confidence(output)
            })
        
        return sorted(predictions, key=lambda x: x['confidence'], reverse=True)
    
    def calculate_confidence(self, output):
        # 基于生成概率计算置信度
        return 0.9  # 简化实现
```

### 模型训练数据准备

```python
def prepare_training_data():
    """
    准备蒙古文预测模型训练数据
    
    数据来源:
    1. tugstugi/mongolian-nlp 语料
    2. 蒙古国新闻网站爬虫
    3. 维基百科蒙古文版
    4. 古典文献数字化文本
    """
    import datasets
    
    # 加载现有语料
    corpus = datasets.load_dataset('tugstugi/mongolian-corpus')
    
    # 数据清洗
    cleaned = []
    for item in corpus['train']:
        text = item['text']
        # 规范化
        text = unicodedata.normalize('NFC', text)
        # 移除噪声
        text = re.sub(r'[^\u1800-\u18AF\s]', '', text)
        if len(text) > 10:
            cleaned.append(text)
    
    return cleaned
```

---

## 用户界面设计

### 候选框设计

```css
/* 预测候选框 */
.candidate-popup {
  position: absolute;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 8px;
  z-index: 1000;
  
  /* 竖排候选 */
  display: flex;
  flex-direction: column;
  gap: 4px;
  
  max-height: 200px;
  overflow-y: auto;
}

.candidate-item {
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Noto Sans Mongolian', sans-serif;
  font-size: 16px;
  
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.candidate-item:hover,
.candidate-item.selected {
  background: #4a90d9;
  color: white;
}

.candidate-frequency {
  font-size: 12px;
  opacity: 0.6;
}
```

### 键盘集成

```javascript
class PredictiveKeyboard {
  constructor(inputElement) {
    this.input = inputElement;
    this.predictor