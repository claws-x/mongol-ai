# Unicode 蒙古文编码标准研究

## Unicode 编码范围

### 基本区块
- **范围**：U+1800 - U+18AF
- **名称**：Mongolian
- **收录时间**：Unicode 3.0 (2000 年)
- **字符数**：176 个字符

### 扩展区块
- **范围**：U+11660 - U+1167F
- **名称**：Mongolian Supplement
- **收录时间**：Unicode 9.0 (2016 年)
- **字符数**：32 个字符

---

## 字符分类

### 1. 元音字母 (Vowels)

| 字符 | Unicode | 名称 | 拼音 |
|------|---------|------|------|
| ᠠ | U+1820 | MONGOLIAN LETTER A | a |
| ᠡ | U+1821 | MONGOLIAN LETTER E | e |
| ᠢ | U+1822 | MONGOLIAN LETTER I | i |
| ᠣ | U+1823 | MONGOLIAN LETTER O | o |
| ᠤ | U+1824 | MONGOLIAN LETTER U | u |
| ᠥ | U+1825 | MONGOLIAN LETTER OE | ö |
| ᠦ | U+1826 | MONGOLIAN LETTER UE | ü |
| ᠧ | U+1827 | MONGOLIAN LETTER EE | ē |

### 2. 辅音字母 (Consonants)

| 字符 | Unicode | 名称 | 拼音 |
|------|---------|------|------|
| ᠨ | U+1828 | MONGOLIAN LETTER NA | n |
| ᠪ | U+1829 | MONGOLIAN LETTER BA | b |
| ᠫ | U+182A | MONGOLIAN LETTER PA | p |
| ᠬ | U+182B | MONGOLIAN LETTER QA | q |
| ᠭ | U+182C | MONGOLIAN LETTER GA | γ |
| ᠮ | U+182D | MONGOLIAN LETTER MA | m |
| ᠯ | U+182E | MONGOLIAN LETTER LA | l |
| ᠰ | U+182F | MONGOLIAN LETTER SA | s |
| ᠱ | U+1830 | MONGOLIAN LETTER SHA | š |
| ᠲ | U+1831 | MONGOLIAN LETTER TA | t |
| ᠳ | U+1832 | MONGOLIAN LETTER DA | d |
| ᠴ | U+1833 | MONGOLIAN LETTER CHA | č |
| ᠵ | U+1834 | MONGOLIAN LETTER JA | j |
| ᠶ | U+1835 | MONGOLIAN LETTER YA | y |
| ᠷ | U+1836 | MONGOLIAN LETTER RA | r |
| ᠸ | U+1837 | MONGOLIAN LETTER WA | w |
| ᠹ | U+1838 | MONGOLIAN LETTER FA | f |
| ᠺ | U+1839 | MONGOLIAN LETTER KA | k |
| ᠻ | U+183A | MONGOLIAN LETTER KHA | ḳ |
| ᠼ | U+183B | MONGOLIAN LETTER TSA | ts |
| ᠽ | U+183C | MONGOLIAN LETTER ZA | dz |
| ᠾ | U+183D | MONGOLIAN LETTER HAA | h |
| ᠿ | U+183E | MONGOLIAN LETTER ZRA | ž |
| ᡀ | U+183F | MONGOLIAN LETTER LH | lh |

### 3. 元音和谐规则

**阳性元音**：ᠠ (a), ᠣ (o), ᠤ (u)
**阴性元音**：ᠡ (e), ᠥ (ö), ᠦ (ü)
**中性元音**：ᠢ (i)

**和谐规则**：
- 阳性词只能接阳性后缀
- 阴性词只能接阴性后缀
- 中性元音可出现在任何词中

---

## 字形变体规则

### 1. 词位形式 (Positional Forms)

蒙古文字母有 4 种形式：

1. **词首形式 (Initial)**
   - 出现在词的第一个音节
   - 例：ᠮᠣᠩᠭᠣᠯ 中的 ᠮ

2. **词中形式 (Medial)**
   - 出现在词的中间音节
   - 例：ᠮᠣᠩᠭᠣᠯ 中的 ᠣᠩᠭᠣ

3. **词尾形式 (Final)**
   - 出现在词的最后一个音节
   - 例：ᠮᠣᠩᠭᠣᠯ 中的 ᠯ

4. **独立形式 (Isolated)**
   - 单独出现时使用
   - 例：字母表中的 ᠮ

### 2. 自由变体选择符 (FVS)

Unicode 定义了 3 个自由变体选择符：

| 字符 | Unicode | 名称 | 缩写 |
|------|---------|------|------|
| ᠋ | U+180B | MONGOLIAN FREE VARIATION SELECTOR ONE | FVS1 |
| ᠌ | U+180C | MONGOLIAN FREE VARIATION SELECTOR TWO | FVS2 |
| ᠍ | U+180D | MONGOLIAN FREE VARIATION SELECTOR THREE | FVS3 |

**使用方式**：
```
基本字符 + FVS1 = 变体 1
基本字符 + FVS2 = 变体 2
基本字符 + FVS3 = 变体 3
```

**示例**：
```
ᠭᠠ (ga) - 标准形式
ᠭ᠋ᠠ (ga+FVS1) - 变体形式 1
ᠭ᠌ᠠ (ga+FVS2) - 变体形式 2
```

---

## 拼写规则

### 1. 连写规则

蒙古文是连写文字，字符之间通过"牙"（连接符）连接。

**连接规则**：
- 词内字符必须连写
- 词间可以有空格
- 标点符号独立

### 2. 附加成分

蒙古语是粘着语，通过在词根后附加成分构成新词。

**常见附加成分**：
- 复数：ᠴᠤᠳ (čud), ᠰ (s)
- 属格：ᠤᠨ (un), ᠦᠨ (ün), ᠶᠢᠨ (yin)
- 宾格：ᠢᠶᠠᠨ (iyan), ᠢᠶᠡᠨ (iyen)
- 与格：ᠳᠤ (du), ᠳᠡ (de)

### 3. 元音和谐律

**规则**：
1. 一个词内的元音必须和谐
2. 后缀元音根据词干元音选择
3. 中性元音不破坏和谐

**示例**：
```
ᠭᠡᠷ (ger, 房子) + ᠦᠨ (ün) = ᠭᠡᠷᠦᠨ (gerün, 房子的)
ᠬᠣᠲᠠ (qota, 城市) + ᠤᠨ (un) = ᠬᠣᠲᠠᠤᠨ (qotaun, 城市的)
```

---

## Unicode 规范化

### NFC vs NFD

**NFC (Normalization Form C)**:
- 合成形式
- 使用预组合字符
- 推荐使用

**NFD (Normalization Form F)**:
- 分解形式
- 使用基本字符 + 变体符号
- 用于特殊处理

### 蒙古文规范化

蒙古文推荐使用 **NFC** 形式：
- 保持词形完整
- 减少字符数
- 提高处理效率

---

## AI 驱动输入法设计

### 1. 智能预测

**基于规则**：
```python
def predict_next_char(current_word, context):
    # 基于元音和谐规则
    vowel_type = detect_vowel_harmony(current_word)
    
    # 基于词位规则
    position = detect_word_position(current_word)
    
    # 基于语法规则
    grammar_pattern = detect_grammar_pattern(context)
    
    return predict_with_rules(vowel_type, position, grammar_pattern)
```

**基于统计**：
```python
def predict_with_ngram(text, n=3):
    # 使用 N-gram 模型
    # 基于语料库统计
    return most_probable_next_char
```

### 2. 自动纠错

**常见错误类型**：
1. 元音和谐错误
2. 词位形式错误
3. FVS 使用错误
4. 连写错误

**纠错算法**：
```python
def correct_mongolian_text(text):
    # 1. 检查元音和谐
    text = correct_vowel_harmony(text)
    
    # 2. 检查词位形式
    text = correct_positional_forms(text)
    
    # 3. 规范化 FVS
    text = normalize_fvs(text)
    
    # 4. 检查连写
    text = correct_joining(text)
    
    return text
```

### 3. 拉丁转写转换

**转写方案**：
```python
transliteration_map = {
    'sain': 'ᠰᠠᠶᠢᠨ',
    'baina': 'ᠪᠠᠶᠢᠨ᠎ᠠ',
    'bayarlala': 'ᠪᠠᠶᠠᠷᠯᠠᠯ᠎ᠠ',
    'monggol': 'ᠮᠣᠩᠭᠣᠯ',
    'kele': 'ᠬᠡᠯᠡ',
}

def latin_to_mongolian(latin_text):
    # 1. 分词
    words = tokenize(latin_text)
    
    # 2. 查找映射
    mongolian_words = []
    for word in words:
        if word in transliteration_map:
            mongolian_words.append(transliteration_map[word])
        else:
            # 3. 规则转换
            mongolian_words.append(convert_by_rules(word))
    
    return ' '.join(mongolian_words)
```

### 4. 上下文感知

**对话上下文**：
```python
class ContextAwareInput:
    def __init__(self):
        self.conversation_history = []
        self.topic = None
        self.formality = 'neutral'
    
    def predict(self, current_input):
        # 基于对话历史
        context = self.get_context()
        
        # 基于话题
        topic_words = self.get_topic_words(self.topic)
        
        # 基于礼貌程度
        formality_suffix = self.get_formality_suffix(self.formality)
        
        return combine_predictions(context, topic_words, formality_suffix)
```

---

## 实现架构

### 1. 核心模块

```
mongolian_input_engine/
├── unicode_handler.py      # Unicode 编码处理
├── vowel_harmony.py        # 元音和谐检查
├── positional_forms.py     # 词位形式生成
├── fvs_normalizer.py       # FVS 规范化
├── joining_engine.py       # 连写引擎
├── predictor.py            # AI 预测
├── corrector.py            # 自动纠错
└── transliterator.py       # 拉丁转写
```

### 2. AI 模型

**训练数据**：
- 蒙古文语料库
- 新闻文本
- 文学作品
- 对话数据

**模型选择**：
- Transformer (BERT for Mongolian)
- LSTM (序列预测)
- N-gram (快速预测)

### 3. 性能优化

**缓存策略**：
```python
class PredictionCache:
    def __init__(self):
        self.cache = {}
        self.max_size = 10000
    
    def get(self, context):
        return self.cache.get(hash(context))
    
    def set(self, context, prediction):
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        self.cache[hash(context)] = prediction
```

---

## 下一步实现

### 阶段 1: 基础引擎 (1 周)
- [ ] Unicode 编码处理
- [ ] 元音和谐检查
- [ ] 词位形式生成
- [ ] FVS 规范化

### 阶段 2: AI 预测 (2 周)
- [ ] N-gram 模型
- [ ] 语料库收集
- [ ] 模型训练
- [ ] 实时预测

### 阶段 3: 智能纠错 (1 周)
- [ ] 错误检测
- [ ] 自动纠正
- [ ] 用户反馈
- [ ] 模型优化

### 阶段 4: 集成应用 (1 周)
- [ ] 输入法 UI
- [ ] 候选词显示
- [ ] 拉丁转写
- [ ] 性能优化

---

## 参考资料

1. **Unicode Standard**
   - Chapter 9: Central and South Asia
   - https://unicode.org/charts/PDF/U1800.pdf

2. **Unicode TN #57**
   - Encoding and Shaping of the Mongolian Script
   - https://www.unicode.org/notes/tn57/

3. **W3C Mongolian Layout**
   - Mongolian Layout Requirements
   - https://www.w3.org/TR/mlreq/

4. **Mongolfont**
   - http://www.mongolfont.com/

---

**版本**: v1.0  
**日期**: 2026-03-30  
**作者**: OpenClaw Mongolian AI Team
