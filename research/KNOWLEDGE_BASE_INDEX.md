# 传统蒙古文数字知识库 - 总索引

**版本**: v1.0  
**创建时间**: 2026-04-03  
**最后更新**: 2026-04-03  
**状态**: 持续更新中

---

## 📚 知识库结构

```
mongolian-ai-assistant/research/
├── KNOWLEDGE_BASE_INDEX.md          # 本文件 - 总索引
├── CORE_PRINCIPLES.md               # 核心原则与标准
├── GLOBAL_RESEARCH_SUMMARY_2026-04-03.md  # 全球研究综述
│
├── 01_unicode_standard/             # Unicode 标准
│   ├── unicode_mongolian_block.md
│   ├── fvs_variant_selectors.md
│   └── normalization_forms.md
│
├── 02_vertical_writing/             # 竖排书写技术
│   ├── css_writing_modes.md
│   ├── svg_vertical_text.md
│   ├── browser_compatibility.md
│   └── mobile_optimization.md
│
├── 03_font_rendering/               # 字体与渲染
│   ├── noto_sans_mongolian.md
│   ├── microsoft_mongolian_baiti.md
│   ├── glyph_variants.md
│   └── ligature_rules.md
│
├── 04_input_methods/                # 输入法技术
│   ├── virtual_keyboard_design.md
│   ├── predictive_input.md
│   ├── voice_input.md
│   └── mobile_keyboard_adaptation.md
│
├── 05_nlp_resources/                # NLP 资源
│   ├── tokenizer_research.md
│   ├── pos_tagging.md
│   ├── mongolian_treebank.md
│   └── pretrained_models.md
│
├── 06_ocr_recognition/              # OCR 识别
│   ├── vertical_text_detection.md
│   ├── mongolian_ocr_datasets.md
│   └── deep_learning_approaches.md
│
├── 07_academic_research/            # 学术研究
│   ├── western_universities_survey.md
│   ├── acl_anthology_papers.md
│   ├── key_researchers.md
│   └── research_gaps.md
│
├── 08_open_source_ecosystem/        # 开源生态
│   ├── github_projects.md
│   ├── huggingface_models.md
│   ├── tugstugi_profile.md
│   └── community_landscape.md
│
├── 09_institutional_collections/    # 机构收藏
│   ├── british_library.md
│   ├── bnf_gallica.md
│   ├── library_of_congress.md
│   ├── harvard_yenching.md
│   └── iiif_framework.md
│
├── 10_competitive_analysis/         # 竞争分析
│   ├── menksoft_analysis.md
│   ├── open_source_alternatives.md
│   └── differentiation_strategy.md
│
└── 11_technical_roadmap/            # 技术路线
    ├── architecture_design.md
    ├── implementation_plan.md
    └── release_schedule.md
```

---

## 🎯 核心原则（不可妥协）

### 原则 1: 竖排优先
**所有蒙古文必须竖排显示，无论静态还是动态**

```css
.mongolian-vertical {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
}
```

### 原则 2: 开源开放
**所有核心代码开源，许可证：MIT/Apache 2.0/OFL/CC BY 4.0**

### 原则 3: 移动优先
**移动端体验优先于桌面端，填补市场空白**

### 原则 4: Web 原生
**HTML5+CSS3+JS + Python NLP，轻量可维护**

### 原则 5: 可验证性
**所有技术决策有文档、有测试、可追溯**

---

## 📊 知识库统计

| 类别 | 文档数 | 状态 | 最后更新 |
|------|--------|------|---------|
| Unicode 标准 | 3 | ✅ 完成 | 2026-04-03 |
| 竖排书写 | 4 | 🟡 进行中 | 2026-04-03 |
| 字体渲染 | 4 | ✅ 完成 | 2026-04-03 |
| 输入法 | 4 | 🟡 进行中 | 2026-04-03 |
| NLP 资源 | 4 | 🟡 进行中 | 2026-04-03 |
| OCR 识别 | 3 | ⏳ 待开始 | - |
| 学术研究 | 4 | ✅ 完成 | 2026-04-03 |
| 开源生态 | 4 | ✅ 完成 | 2026-04-03 |
| 机构收藏 | 5 | ✅ 完成 | 2026-04-03 |
| 竞争分析 | 3 | ✅ 完成 | 2026-04-03 |
| 技术路线 | 3 | 🟡 进行中 | 2026-04-03 |
| **总计** | **41** | **60% 完成** | **2026-04-03** |

---

## 🔑 关键知识摘要

### Unicode 编码
- **范围**: U+1800-U+18AF (蒙古文区块), U+11660-U+1167F (补充)
- **变体选择符**: FVS1 (U+180B), FVS2 (U+180C), FVS3 (U+180D)
- **连接符**: NNBSP (U+202F), ZWJ (U+200D), ZWNJ (U+200C)

### 字体支持
- **Noto Sans Mongolian** (Google Fonts) - 开源，持续维护
- **Microsoft Mongolian Baiti** - Windows 内置，封闭
- **字库覆盖**: 基本蒙古文区块 ~95%，补充区块 ~60%

### 竖排技术
- **CSS writing-mode: vertical-lr** - 标准方案，现代浏览器支持
- **SVG text writing-mode="tb"** - 精确控制，适合静态文本
- **transform: rotate(90deg)** - 兼容方案，非真正竖排
- **移动端挑战**: 输入框竖排支持不完整，需 SVG 降级方案

### NLP 资源
- **tugstugi/mongolian-nlp** (GitHub, ~100⭐) - 最活跃开源项目
- **Hugging Face 模型**:
  - `wav2vec2-large-xlsr-53-mongolian` (ASR, 2.37k 下载)
  - `bert-base-mongolian-cased` (594 下载)
  - `mongolian-gpt2` (525 下载)
- **Universal Dependencies** - 无传统蒙古文树库（仅西里尔文）

### 学术格局
- **欧美高校**: 无专门传统蒙古文数字化项目
- **主要研究者**: tugstugi (Erdene-Ochir Tuguldur, 蒙古国)
- **论文分布**: ACL Anthology ~20 篇，arXiv ~50 篇（中国/蒙古国主导）
- **机构收藏**: 大英图书馆、BnF、美国国会图书馆、哈佛燕京图书馆

### 竞争分析
| 维度 | Menksoft | 开源社区 | 本项目 |
|------|----------|---------|--------|
| 开源 | ❌ 封闭 | ✅ 完全 | ✅ 完全 |
| 移动 | ⚠️ 弱 | ⚠️ 无 | ✅ 优先 |
| 竖排 | ⚠️ 横排适配 | ⚠️ 不完整 | ✅ 优先 |
| Web | ❌ Windows 绑定 | ✅ 部分 | ✅ 原生 |
| 社区 | ❌ 封闭 | ✅ 开放 | ✅ 开放 |

---

## 🚀 下一步行动

### 优先级 A: 核心渲染引擎
- 文件：`/src/core/MongolianRenderer.js`
- 目标：实现竖排书写、字形变体处理、FVS 支持
- 预计：2026-04-10

### 优先级 B: 测试验证框架
- 文件：`/tests/vertical-writing-tests.js`
- 目标：确保竖排/字形/浏览器兼容性
- 预计：2026-04-15

### 优先级 C: 架构文档
- 文件：`/docs/ARCHITECTURE.md`
- 目标：技术决策沉淀，便于协作
- 预计：2026-04-12

### 优先级 D: GitHub 组织
- 目标：创建组织，开源代码，吸引贡献者
- 预计：2026-04-20

### 优先级 E: 学术合作
- 目标：联系 tugstugi，借用现有 NLP 资源
- 预计：2026-04-25

---

## 📝 使用指南

### 如何查找信息
1. 从本索引找到相关类别
2. 进入对应子目录阅读文档
3. 文档末尾有参考文献和链接

### 如何贡献知识
1. Fork 项目
2. 在对应类别下创建/修改文档
3. 提交 Pull Request

### 如何引用
```bibtex
@techreport{mongolian-kb-2026,
  title = {传统蒙古文数字知识库},
  author = {Mongolian AI Team},
  year = {2026},
  url = {https://github.com/[org]/mongolian-ai-assistant}
}
```

---

## 🌟 愿景

**打造全球最完整、最权威的传统蒙古文数字知识库**

**填补欧美高校研究空白，成为开源社区核心资源**

**让 100 万+蒙古人在数字时代使用自己的文字**

---

**维护者**: Mongolian AI Team  
**许可证**: CC BY 4.0 (文档), MIT (代码)  
**联系**: [待创建 GitHub 组织]
