# Mongol AI

传统蒙古文输入、竖排预览与语言技术研究项目。

> 当前状态：**Phase 0 工程基线完成，Phase 1/2 基础能力可体验**。项目尚未完成母语专家审核、完整跨浏览器验证或生产级准确率评估。

## 正式体验

当前唯一正式入口是 [`index.html`](index.html)，核心体验位于：

- [`demos/input/ai-chat.html`](demos/input/ai-chat.html) — 本地优先写作工作台与 Unicode 诊断 Alpha
- [`knowledge/index.html`](knowledge/index.html) — 可追溯的传统蒙古文数字化科研知识库
- [`engine/index.html`](engine/index.html) — 无损输入、确定性 HarfBuzz WASM 塑形与码位诊断实验室

确定性引擎逐码位保留输入，锁定 HarfBuzz 与字体哈希生成 SVG glyph path；未取得权威映射的私有编码会被无损保存并阻止猜测转换。旧工作台仍保留在 [Labs](demos/README.md)，不再代表字形正确性承诺。

## 当前已验证能力

- 传统蒙古文物理键盘与虚拟键盘输入
- Mongol AI Vertical Engine 2.0：以 `vertical-lr + mixed` 为主路径，运行时验证连写方向和左→右换列
- 仓库内固定 Noto Sans Mongolian v3.002 字体，不依赖 Google Fonts 或操作系统字体
- 基础文本检测、提取、统计和简化转写
- 规则分词、词性标注和句法分析原型可导入运行
- Python 自动化测试和正式页面契约测试
- 112 条可追溯到 Unicode 17.0 官方资料的编码基线
- 不改写原文的 FVS、MVS、NNBSP、ZWJ、ZWNJ 编码诊断
- 实时竖排预览、浏览器本地草稿、原文复制与 UTF-8 文本导出
- 115 条等待母语专家和来源审核的历史词汇/短语队列
- Phase K0 科研知识库：26 个原始来源、11 个机构/团队、20 位研究者、11 项代表性研究、8 项资源和 5 项标准

## 尚未证明的能力

- 生产级蒙古文拼写、语法或翻译准确率
- 全量 Unicode/FVS 字形正确性
- Chrome、Safari、Firefox 与移动设备的完整兼容性
- 大模型对话、OCR、语音识别或学习系统效果
- 适用于出版、教育评测或政务等高风险场景

历史文档中出现的“100% 正确”“准确率 85%”或五星健康度属于早期自评，不代表当前可复现结论。当前事实源见 [Phase 0 基线](docs/05-project/PHASE_0_BASELINE.md)。

## 快速开始

```bash
git clone https://github.com/claws-x/mongol-ai.git
cd mongol-ai
python3 -m http.server 8000
```

打开 `http://localhost:8000/`。

运行测试：

```bash
PYTHONPYCACHEPREFIX=/tmp/mongol-ai-pycache python3 -m unittest discover -v
```

## 项目结构

```text
core/       竖排渲染引擎、文本、输入与规则响应原型
engine/     确定性传统蒙古文引擎实验室
nlp/        分词、词性标注与句法分析原型
data/       小规模实验词汇和短语
             `data/knowledge/` 为机器可读科研事实源与 JSON Schema
demos/      正式 Alpha 与历史 Labs
docs/       标准研究、技术笔记与历史项目文档
knowledge/  科研知识库公开检索页面
tests/      Phase 0 自动化回归测试
```

质量语料和审核流程见 [`data/quality/`](data/quality/) 与 [`LANGUAGE_REVIEW_WORKFLOW.md`](docs/05-project/LANGUAGE_REVIEW_WORKFLOW.md)。

科研知识库的当前索引、证据等级和覆盖缺口见
[`KNOWLEDGE_BASE_INDEX.md`](docs/04-research/KNOWLEDGE_BASE_INDEX.md)。旧研究文档中的人物、准确率和“完全支持”声明默认不再视为事实源。

## 产品路线与质量原则

Phase 0–2 的已交付能力、退出条件和明确边界见
[`PRODUCT_ROADMAP.md`](docs/05-project/PRODUCT_ROADMAP.md)。

1. 对外声明必须有可复现测试或专家审核证据。
2. 正式体验必须使用原生竖排，不通过旋转模拟。
3. 用户输入必须作为文本处理，不注入 HTML。
4. 核心流程必须可通过键盘操作，并提供可理解的标签和状态。
5. 历史演示与正式产品能力必须明确分开。

竖排引擎的能力探测、兼容回退和 Unicode 契约见
[`MONGOL_VERTICAL_ENGINE.md`](docs/02-architecture/MONGOL_VERTICAL_ENGINE.md)。

## 贡献

欢迎提交测试语料、浏览器兼容性报告、无障碍修复和母语文字审核。请不要在缺少数据集、评估脚本和结果记录时新增准确率声明。

项目采用 [MIT License](LICENSE)。
