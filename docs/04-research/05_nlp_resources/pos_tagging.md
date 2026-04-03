# 词性标注研究

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [蒙古语词性系统](#蒙古语词性系统)
3. [词性标注技术原理](#词性标注技术原理)
4. [现有资源调研](#现有资源调研)
5. [基于规则的方法](#基于规则的方法)
6. [基于统计的方法](#基于统计的方法)
7. [深度学习方法](#深度学习方法)
8. [实现示例](#实现示例)
9. [评估与测试](#评估与测试)
10. [参考资料](#参考资料)

---

## 概述

### 什么是词性标注

词性标注 (Part-of-Speech Tagging, POS Tagging) 是为文本中的每个词语分配词性标签 (名词、动词、形容词等) 的过程。

**示例**:
```
输入：ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠪᠣᠯ ᠳᠡᠯᠬᠢᠶᠡᠨ ᠬᠠᠮᠤᠭ ᠦᠨᠳᠦᠰᠦᠨ ᠦ ᠨᠢᠭᠡ ᠬᠡᠯᠡ ᠪᠣᠯᠤᠮᠳᠠᠢ᠃
输出：
ᠮᠣᠩᠭᠣᠯ    [PROPN]   专有名词
ᠬᠡᠯᠡ       [NOUN]    名词
ᠪᠣᠯ       [PART]    助词
ᠳᠡᠯᠬᠢᠶᠡᠨ   [NOUN]    名词
ᠬᠠᠮᠤᠭ     [ADJ]     形容词
ᠦᠨᠳᠦᠰᠦᠨ   [NOUN]    名词
ᠦ         [ADP]     后置词
ᠨᠢᠭᠡ      [NUM]     数词
ᠬᠡᠯᠡ      [NOUN]    名词
ᠪᠣᠯᠤᠮᠳᠠᠢ  [AUX]     系动词
```

### 为什么需要词性标注

| 应用场景 | 描述 | 价值 |
|---------|------|------|
| 句法分析 | 依存关系识别基础 | ⭐⭐⭐⭐⭐ |
| 信息检索 | 词性过滤提升精度 | ⭐⭐⭐⭐ |
| 机器翻译 | 词性对齐辅助 | ⭐⭐⭐⭐⭐ |
| 语言教学 | 语法学习工具 | ⭐⭐⭐⭐⭐ |
| 语音合成 | 词性影响语调 | ⭐⭐⭐ |

### 蒙古语特殊挑战

| 挑战 | 描述 | 难度 |
|------|------|------|
| 黏着语特性 | 词干 + 多词缀 | ⭐⭐⭐⭐ |
| 元音和谐 | 词缀形式变化 | ⭐⭐⭐ |
| 无空格历史文本 | 古典文献分词困难 | ⭐⭐⭐⭐⭐ |
| 标注标准不统一 | 中西方标注体系差异 | ⭐⭐⭐ |

---

## 蒙古语词性系统

### 主要词性类别

参照 Universal Dependencies (UD) 标准，结合蒙古语特性：

#### 实词 (Open Class)

| 标签 | 全称 | 说明 | 示例 |
|------|------|------|------|
| NOUN | Noun | 名词 | ᠭᠡᠷ (家), ᠬᠦᠮᠦᠨ (人) |
| PROPN | Proper Noun | 专有名词 | ᠮᠣᠩᠭᠣᠯ (蒙古), ᠴᠢᠩᠭᠢᠰ ᠬᠠᠭᠠᠨ (成吉思汗) |
| VERB | Verb | 动词 | ᠪᠢᠴᠢᠬᠦ (写), ᠤᠨᠰᠢᠬᠦ (读) |
| ADJ | Adjective | 形容词 | ᠶᠡᠬᠡ (大), ᠰᠠᠶᠢᠨ (好) |
| ADV | Adverb | 副词 | ᠮᠠᠰᠢ (很), ᠮᠡᠳᠡᠭᠦ (非常) |
| NUM | Numeral | 数词 | ᠨᠢᠭᠡ (一), ᠬᠣᠶᠠᠷ (二) |
| PRON | Pronoun | 代词 | ᠪᠢ (我), ᠲᠡᠷ (他) |

#### 虚词 (Closed Class)

| 标签 | 全称 | 说明 | 示例 |
|------|------|------|------|
| ADP | Adposition | 后置词 | ᠦ (的), ᠳᠤ (在) |
| AUX | Auxiliary | 助动词 | ᠪᠣᠯᠬᠤ (是), ᠪᠠᠶᠢᠬᠤ (在) |
| CCONJ | Coordinating Conj | 并列连词 | ᠪᠣᠯᠣ (和), ᠡᠴᠦ (或) |
| SCONJ | Subordinating Conj | 从属连词 | ᠬᠡᠮᠡᠭᠡᠴᠦ (因为), ᠬᠠᠭᠠᠰ (如果) |
| PART | Particle | 助词 | ᠪᠣᠯ (吧), ᠱᠦ (啊) |
| DET | Determiner | 限定词 | ᠡᠨᠡ (这), ᠲᠡᠷᠡ (那) |

#### 其他

| 标签 | 全称 | 说明 | 示例 |
|------|------|------|------|
| INTJ | Interjection | 感叹词 | ᠥᠥ (哦), ᠭᠡᠵᠢ (唉) |
| PUNCT | Punctuation | 标点 | ᠂ (逗号), ᠃ (句号) |
| X | Other | 未分类 | 外来词、错误 |

### 蒙古语特殊词性

#### 词缀标注方案

**方案 A: 词缀不分离**
```
ᠭᠡᠷᠲᠡᠢᠭᠡᠷ [NOUN]  (从家)
- 整体标注为名词
```

**方案 B: 词缀分离**
```
ᠭᠡᠷ [NOUN] + ᠲᠡᠢ [ADJ] + ᠭᠡᠷ [ABL]
- 词干：名词
- 词缀 1: 形容词化
- 词缀 2: 从格
```

**推荐**: 方案 A (简化标注，降低复杂度)

#### 动词变位标注

```
ᠪᠢᠴᠢᠭᠰᠡᠨ [VERB]  - 过去分词
ᠪᠢᠴᠢᠵᠤ [VERB]    - 副动词
ᠪᠢᠴᠢᠨ᠎ᠡ [VERB]   - 现在时
ᠪᠢᠴᠢᠭᠳᠡᠭᠰᠡᠨ [VERB] - 被动态
```

---

## 词性标注技术原理

### 技术演进

```
1980s: 基于规则 (手工编写)
    ↓
1990s: HMM (隐马尔可夫模型)
    ↓
2000s: MaxEnt (最大熵)
    ↓
2010s: CRF (条件随机场)
    ↓
2015s: BiLSTM-CRF
    ↓
2020s: Transformer (BERT 等)
```

### HMM 模型

```python
# HMM POS Tagger 简化实现
import numpy as np

class HMMPPOSTagger:
    def __init__(self):
        self.states = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON']
        self.observations = []  # 词汇表
        
        # 转移概率 P(state_t | state_{t-1})
        self.transition_prob = np.zeros((len(self.states), len(self.states)))
        
        # 发射概率 P(obs_t | state_t)
        self.emission_prob = np.zeros((len(self.states), len(self.observations)))
        
        # 初始概率 P(state_0)
        self.initial_prob = np.zeros(len(self.states))
    
    def train(self, tagged_corpus):
        """
        从标注语料库训练 HMM 参数
        
        Args:
            tagged_corpus: [(word1, tag1), (word2, tag2), ...]
        """
        # 统计计数
        state_counts = np.zeros(len(self.states))
        transition_counts = np.zeros((len(self.states), len(self.states)))
        emission_counts = np.zeros((len(self.states), len(self.observations)))
        
        for sentence in tagged_corpus:
            for i, (word, tag) in enumerate(sentence):
                state_idx = self.states.index(tag)
                obs_idx = self.observations.index(word)
                
                if i == 0:
                    self.initial_prob[state_idx] += 1
                else:
                    prev_tag = sentence[i-1][1]
                    prev_idx = self.states.index(prev_tag)
                    transition_counts[prev_idx, state_idx] += 1
                
                state_counts[state_idx] += 1
                emission_counts[state_idx, obs_idx] += 1
        
        # 归一化为概率
        self.initial_prob /= sum(self.initial_prob)
        self.transition_prob = transition_counts / transition_counts.sum(axis=1, keepdims=True)
        self.emission_prob = emission_counts / emission_counts.sum(axis=1, keepdims=True)
    
    def viterbi(self, sentence):
        """
        Viterbi 算法寻找最优标注序列
        """
        n = len(sentence)
        m = len(self.states)
        
        # 初始化
        viterbi = np.zeros((n, m))
        backpointer = np.zeros((n, m), dtype=int)
        
        # 第一步
        obs_idx = self.observations.index(sentence[0]) if sentence[0] in self.observations else 0
        viterbi[0] = self.initial_prob * self.emission_prob[:, obs_idx]
        
        # 递推
        for t in range(1, n):
            obs_idx = self.observations.index(sentence[t]) if sentence[t] in self.observations else 0
            for s in range(m):
                probs = viterbi[t-1] * self.transition_prob[:, s]
                backpointer[t, s] = np.argmax(probs)
                viterbi[t, s] = np.max(probs) * self.emission_prob[s, obs_idx]
        
        # 回溯
        path = [np.argmax(viterbi[-1])]
        for t in range(n-1, 0, -1):
            path.insert(0, backpointer[t, path[0]])
        
        return [self.states[s] for s in path]
```

### CRF 模型

```python
# 使用 sklearn-crfsuite
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

class CRFPOSTagger:
    def __init__(self):
        self.crf = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )
    
    def extract_features(self, sentence, position):
        """
        提取词性标注特征
        """
        word = sentence[position]
        
        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'word[-3:]': word[-3:],
            'word[:3]': word[:3],
            'word.isupper()': word.isupper(),
            'word.isdigit()': word.isdigit(),
        }
        
        # 上下文特征
        if position > 0:
            prev_word = sentence[position - 1]
            features['prev.word'] = prev_word
            features['prev.word.lower()'] = prev_word.lower()
        
        if position