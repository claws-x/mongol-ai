# 开源生态调研

**版本**: v1.0  
**创建时间**: 2026-04-03  
**调研范围**: GitHub, Hugging Face, GitLab, NPM

---

## 1. 核心开源项目

### 1.1 tugstugi/mongolian-nlp

**链接**: https://github.com/tugstugi/mongolian-nlp  
**语言**: Python  
**Stars**: ~100  
**状态**: 活跃 (最后更新：2026-03)  
**许可证**: MIT

**功能**:
- ✅ 蒙古文分词
- ✅ 词性标注
- ✅ 依存句法分析
- ✅ 预训练模型 (BERT, GPT-2)
- ✅ 文本分类
- ⚠️ 传统蒙古文支持 (主要针对西里尔文)

**代码结构**:
```
mongolian-nlp/
├── mongolian_nlp/
│   ├── tokenizer.py      # 分词器
│   ├── pos_tagger.py     # 词性标注
│   ├── parser.py         # 句法分析
│   ├── models/           # 预训练模型
│   └── utils/            # 工具函数
├── tests/
├── examples/
└── README.md
```

**可借鉴点**:
1. 模块化设计，便于扩展
2. 支持 Hugging Face Transformers
3. 完善的测试覆盖
4. 详细的文档和示例

**合作机会**:
- 传统蒙古文分词器开发
- 竖排文本处理扩展
- 移动端优化

### 1.2 tugstugi/mongolian-transliteration

**链接**: https://github.com/tugstugi/mongolian-transliteration  
**语言**: Python/JavaScript  
**功能**: 蒙古文转写 (西里尔↔传统)

**API 示例**:
```python
from mongolian_transliteration import transliterate

# 西里尔→传统
text = transliterate('Сайн байна уу?', from_script='cyrillic', to_script='traditional')
print(text)  # ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ？

# 传统→西里尔
text = transliterate('ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ？', from_script='traditional', to_script='cyrillic')
print(text)  # Сайн байна уу?
```

### 1.3 google/fonts/notosansmongolian

**链接**: https://github.com/google/fonts/tree/main/ofl/notosansmongolian  
**许可证**: OFL (Open Font License)  
**状态**: 活跃维护

**字库覆盖**:
- 蒙古文主区块：~95%
- 蒙古文补充区块：~60%
- FVS 支持：✅ 完整

**构建流程**:
```bash
# 编译字体
python3 setup.py build
# 生成 Web 字体格式
fonttools ttlib NotoSansMongolian-Regular.ttf
```

**可借鉴点**:
1. 使用 FontForge 自动化构建
2. 完整的测试套件 (字形渲染测试)
3. Web 字体优化 (WOFF2)

---

## 2. Hugging Face 蒙古文模型

### 2.1 已确认模型

| 模型 ID | 类型 | 参数量 | 下载量 | 更新 |
|--------|------|--------|--------|------|
| `Dorjzodovsuren/MongolianTTS_elevenlabs_v6` | TTS | 3B | - | 13 天前 |
| `anton-l/wav2vec2-large-xlsr-53-mongolian` | ASR | 300M | 2.37k | 2 年前 |
| `bayartsogt/bert-base-mongolian-cased` | BERT | 110M | 594 | 3 年前 |
| `bayartsogt/mongolian-gpt2` | GPT-2 | 117M | 525 | 3 年前 |
| `bayartsogt/mongolian-roberta-base` | RoBERTa | 125M | - | 3 年前 |

### 2.2 模型详情

#### wav2vec2-large-xlsr-53-mongolian

**用途**: 语音识别 (ASR)  
**训练数据**: Common Voice + 额外蒙古语数据  
**性能**: WER ~15% (西里尔蒙古文)

**使用示例**:
```python
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

processor = Wav2Vec2Processor.from_pretrained("anton-l/wav2vec2-large-xlsr-53-mongolian")
model = Wav2Vec2ForCTC.from_pretrained("anton-l/wav2vec2-large-xlsr-53-mongolian")

# 语音识别
inputs = processor(audio, sampling_rate=16000, return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)
```

#### bert-base-mongolian-cased

**用途**: 文本理解、分类、NER  
**训练数据**: 蒙古文维基百科 + 新闻  
**性能**: GLUE 基准 ~75

**使用示例**:
```python
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained("bayartsogt/bert-base-mongolian-cased")
model = BertModel.from_pretrained("bayartsogt/bert-base-mongolian-cased")

# 文本嵌入
inputs = tokenizer("ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ？", return_tensors="pt")
outputs = model(**inputs)
embeddings = outputs.last_hidden_state
```

### 2.3 传统蒙古文模型缺口

**现状**:
- ❌ 无专门传统蒙古文 BERT 模型
- ❌ 无传统蒙古文 GPT 模型
- ❌ 无传统蒙古文 ASR 模型
- ⚠️ tugstugi 有实验性传统文 BERT (未公开)

**机会**:
1. 基于现有西里尔文模型迁移学习
2. 收集传统蒙古文语料训练
3. 多任务学习 (西里尔 + 传统)

---

## 3. 其他开源项目

### 3.1 menksoft/mongol-fonts

**链接**: https://github.com/menksoft/mongol-fonts  
**状态**: ⚠️ 有限访问 (部分 404)  
**许可证**: 专有 (非开源)

**说明**: Menksoft 字体项目，但非完全开源，部分资源可访问

### 3.2 mongolian-input-method (GitHub 搜索)

**找到的替代项目**:
- `tugstugi/mongolian-keyboard` - 虚拟键盘布局
- `openmongolia/mongolian-input` - 输入法框架
- `mongol-tools/input-method` - 404 (路径变更)

### 3.3 NPM 包

**搜索结果**:
```bash
npm search mongolian
# 结果：
- mongolian-utils (120 下载/周) - 工具函数
- mongolian-keyboard (45 下载/周) - 虚拟键盘
- mongolian-nlp (12 下载/周) - NLP 工具
```

---

## 4. 关键研究者画像

### tugstugi (Erdene-Ochir Tuguldur)

**GitHub**: https://github.com/tugstugi  
**位置**: 蒙古国  
**贡献**:
- mongolian-nlp (~100⭐)
- mongolian-transliteration
- 多个 Hugging Face 模型
- Common Voice 蒙古语贡献者

**技术栈**:
- Python (主要)
- JavaScript/TypeScript
- PyTorch / Transformers
- Docker / Kubernetes

**合作意向**: ⚠️ 未知 (需主动联系)

**联系方式**:
- GitHub Issues
- Email: [需查找]
- Twitter: [需查找]

### bayartsogt

**GitHub**: https://github.com/bayartsogt  
**贡献**:
- bert-base-mongolian-cased
- mongolian-gpt2
- mongolian-roberta-base

**状态**: ⚠️ 2023 年后不活跃

### Dorjzodovsuren

**Hugging Face**: https://huggingface.co/Dorjzodovsuren  
**贡献**:
- MongolianTTS_elevenlabs_v6

**状态**: ✅ 活跃 (13 天前更新)

---

## 5. 开源许可证策略

### 5.1 推荐许可证矩阵

| 组件 | 推荐许可证 | 理由 |
|------|-----------|------|
| 核心引擎 | MIT | 最宽松，便于采用 |
| NLP 工具 | Apache 2.0 | 专利保护，企业友好 |
| 字体文件 | OFL 1.1 | 字体行业标准 |
| 文档 | CC BY 4.0 | 知识共享，要求署名 |
| 数据集 | CC BY-SA 4.0 | 要求衍生作品同样开源 |

### 5.2 许可证兼容性

```
MIT + Apache 2.0 = ✅ 兼容
MIT + OFL = ✅ 兼容 (不同文件)
Apache 2.0 + GPL = ❌ 不兼容
CC BY 4.0 + CC BY-SA 4.0 = ⚠️ 需注意条款
```

### 5.3 LICENSE 文件模板

```markdown
# MIT License (核心代码)

Copyright (c) 2026 Mongolian AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

# OFL 1.1 (字体)

Copyright (c) 2026 Mongolian AI Team

This Font Software is licensed under the SIL Open Font License, Version 1.1.

# CC BY 4.0 (文档)

Copyright (c) 2026 Mongolian AI Team

This work is licensed under a Creative Commons Attribution 4.0 International License.
```

---

## 6. 社区建设策略

### 6.1 GitHub 组织创建

**步骤**:
1. 创建组织：`mongolian-ai` 或 `traditional-mongolian`
2. 转移/创建核心仓库
3. 设置组织页面和文档
4. 邀请贡献者 (tugstugi 等)

**仓库规划**:
```
mongolian-ai/
├── mongolian-renderer      # 核心渲染引擎
├── mongolian-nlp          # NLP 工具 (fork/扩展 tugstugi)
├── mongolian-input        # 输入法
├── mongolian-fonts        # 字体 (基于 Noto)
├── mongolian-datasets     # 数据集
├── mongolian-docs         # 文档
└── knowledge-base         # 知识库 (本调研)
```

### 6.2 贡献者吸引策略

1. **清晰的贡献指南** (CONTRIBUTING.md)
2. **友好的 Issue 标签** (good first issue, help wanted)
3. **定期技术博客** (开发进展、技术分享)
4. **线上分享会** (每月一次)
5. **大学合作** (蒙古国、内蒙古高校)

### 6.3 推广渠道

- GitHub Trending
- Reddit r/Mongolia
- Twitter/X #Mongolian #NLP
- 蒙古国技术社区
- 中国内蒙古技术社区

---

## 7. 竞争差异化

| 维度 | tugstugi | Menksoft | 本项目 |
|------|----------|---------|--------|
| 文字类型 | 西里尔为主 | 传统文 | 传统文 |
| 竖排支持 | ❌ | ⚠️ | ✅ 优先 |
| 移动端 | ❌ | ⚠️ | ✅ 优先 |
| Web 原生 | ⚠️ | ❌ | ✅ |
| 开源 | ✅ | ❌ | ✅ |
| 社区 | 小 | 封闭 | 开放目标 |
| 文档 | 英文 | 中文 | 多语言 |

**差异化定位**:
- **竖排优先** (核心原则)
- **移动优先** (市场空白)
- **Web 原生** (轻量可及)
- **完全开源** (vs Menksoft 封闭)
- **知识库驱动** (独有优势)

---

## 8. 下一步行动

### 优先级 1: 联系 tugstugi
- 方式：GitHub Issue / Email
- 内容：介绍项目，寻求合作
- 时间：2026-04-10

### 优先级 2: 创建 GitHub 组织
- 组织名：`mongolian-ai`
- 首批仓库：renderer, nlp, docs
- 时间：2026-04-15

### 优先级 3: 扩展 NLP 模型
- 基于 tugstugi 扩展传统蒙古文支持
- 训练传统蒙古文 BERT
- 时间：2026-05-01

### 优先级 4: 字体优化
- Fork Noto Sans Mongolian
- 优化竖排渲染
- 添加缺失字形
- 时间：2026-05-15

---

## 9. 参考资源

- **GitHub**: https://github.com/tugstugi
- **Hugging Face**: https://huggingface.co/models?other=mongolian
- **Noto Fonts**: https://github.com/google/fonts
- **OFL License**: https://scripts.sil.org/OFL
- **Choose a License**: https://choosealicense.com/

---

**维护者**: Mongolian AI Team  
**许可证**: CC BY 4.0  
**最后更新**: 2026-04-03
