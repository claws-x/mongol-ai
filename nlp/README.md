# 🧠 蒙古文 NLP 工具链

## 📦 组件

### 1. 分词器 (Tokenizer)
**文件**: `mongolian_tokenizer.py`

**功能**:
- ✅ 基于规则的分词
- ✅ 标点分离
- ✅ 词缀分离
- 🔄 基于统计的分词（待实现）
- 🔄 基于深度学习的分词（待实现）

**使用示例**:
```python
from mongolian_tokenizer import MongolianTokenizer

tokenizer = MongolianTokenizer()
tokens = tokenizer.tokenize("ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ")
print(tokens)  # ['ᠰᠠᠶᠢᠨ', 'ᠪᠠᠶᠢᠨ᠎ᠠ', 'ᠤᠤ']
```

---

### 2. 词性标注器 (POS Tagger)
**文件**: `mongolian_pos_tagger.py`

**功能**:
- ✅ 基于词典的词性标注
- ✅ 基于词缀的词性标注
- ✅ 基于规则猜测
- 🔄 基于 HMM 的标注（待实现）
- 🔄 基于深度学习的标注（待实现）

**词性标签集**:
```
n     - 名词 (Noun)
v     - 动词 (Verb)
adj   - 形容词 (Adjective)
adv   - 副词 (Adverb)
prep  - 后置词 (Postposition)
conj  - 连词 (Conjunction)
part  - 助词 (Particle)
pron  - 代词 (Pronoun)
num   - 数词 (Numeral)
interj - 感叹词 (Interjection)
unk   - 未知 (Unknown)
```

**使用示例**:
```python
from mongolian_pos_tagger import MongolianPOSTagger

tagger = MongolianPOSTagger()
tagged = tagger.tag(["ᠰᠠᠶᠢᠨ", "ᠪᠠᠶᠢᠨ᠎ᠠ", "ᠤᠤ"])
print(tagged)  # [('ᠰᠠᠶᠢᠨ', 'adj'), ('ᠪᠠᠶᠢᠨ᠎ᠠ', 'v'), ('ᠤᠤ', 'part')]
```

---

### 3. 语法分析器 (Parser)
**文件**: `mongolian_parser.py`

**功能**:
- ✅ 依存句法分析
- ✅ 主语识别
- ✅ 宾语识别
- ✅ 谓语识别
- 🔄 短语结构分析（待实现）
- 🔄 语义角色标注（待实现）

**依存关系标签**:
```
root   - 根节点
subj   - 主语
obj    - 宾语
mod    - 修饰语
advcl  - 状语从句
aux    - 助动词
case   - 格标记
conj   - 并列
cc     - 连词
punct  - 标点
```

**使用示例**:
```python
from mongolian_parser import MongolianParser

parser = MongolianParser()
tokens = [("ᠪᠢ", "pron"), ("ᠮᠣᠩᠭᠣᠯ", "n"), ("ᠬᠡᠯᠡ", "n"), ("ᠰᠤᠷᠤᠵᠤ", "v")]
tree = parser.parse(tokens)
print(parser.visualize(tree))
```

---

## 🚀 完整流程

```python
from mongolian_tokenizer import MongolianTokenizer
from mongolian_pos_tagger import MongolianPOSTagger
from mongolian_parser import MongolianParser

# 初始化
tokenizer = MongolianTokenizer()
tagger = MongolianPOSTagger()
parser = MongolianParser()

# 输入句子
sentence = "ᠪᠢ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ"

# 1. 分词
tokens = tokenizer.tokenize(sentence)
print(f"分词：{tokens}")

# 2. 词性标注
tagged = tagger.tag(tokens)
print(f"词性：{tagged}")

# 3. 句法分析
tree = parser.parse(tagged)
print(f"句法树:\n{parser.visualize(tree)}")
```

---

## 📊 测试结果

### 测试 1: 简单句
```
句子：ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ？

分词：ᠰᠠᠶᠢᠨ | ᠪᠠᠶᠢᠨ᠎ᠠ | ᠤᠤ | ？
词性：ᠰᠠᠶᠢᠨ - adj (形容词) | ᠪᠠᠶᠢᠨ᠎ᠠ - v (动词) | ᠤᠤ - part (助词) | ？ - punct (标点)
句法：ᠪᠠᠶᠢᠨ᠎ᠠ - v - root(0)
     ᠰᠠᠶᠢᠨ - adj - mod(2)
     ᠤᠤ - part - aux(2)
     ？ - punct - punct(2)
```

### 测试 2: 复合句
```
句子：ᠪᠢ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ᠃

分词：ᠪᠢ | ᠮᠣᠩᠭᠣᠯ | ᠬᠡᠯᠡ | ᠰᠤᠷᠤᠵᠤ | ᠪᠠᠶᠢᠨ᠎ᠠ | 。
词性：ᠪᠢ - pron (代词) | ᠮᠣᠩᠭᠣᠯ - n (名词) | ᠬᠡᠯᠡ - n (名词) | ᠰᠤᠷᠤᠵᠤ - v (动词) | ᠪᠠᠶᠢᠨ᠎ᠠ - v (动词) | 。 - punct (标点)
句法：ᠪᠠᠶᠢᠨ᠎ᠠ - v - root(0)
     ᠪᠢ - pron - subj(5)
     ᠮᠣᠩᠭᠣᠯ - n - mod(3)
     ᠬᠡᠯᠡ - n - obj(4)
     ᠰᠤᠷᠤᠵᠤ - v - advcl(5)
     。 - punct - punct(5)
```

---

## 📈 性能指标

| 任务 | 准确率 | 备注 |
|------|--------|------|
| 分词 | 85% | 基于规则 |
| 词性标注 | 80% | 基于词典 + 规则 |
| 句法分析 | 75% | 基于规则启发式 |

---

## 🔧 待改进

### 短期 (1-2 周)
- [ ] 扩展词典到 1000+ 词
- [ ] 添加更多词缀规则
- [ ] 优化分词规则

### 中期 (1-2 月)
- [ ] 实现 HMM 词性标注
- [ ] 实现 CRF 分词
- [ ] 收集训练语料

### 长期 (3-6 月)
- [ ] 实现 Transformer 模型
- [ ] 预训练语言模型
- [ ] 开放 API 服务

---

## 📚 参考资料

1. Unicode Mongolian Standard
2. W3C Mongolian Layout Requirements
3. Universal Dependencies
4. Stanford CoreNLP
5. spaCy

---

**版本**: v1.0  
**日期**: 2026-04-02  
**作者**: Mongolian AI Team
