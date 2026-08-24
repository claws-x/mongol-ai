# Mongol AI

传统蒙古文输入、竖排预览与语言技术研究项目。

> **首次接手必读：**[`项目宪章：我们到底在解决什么`](docs/00_PROJECT_CHARTER.md)。
> 它是最高优先级事实源：本项目正在建立独立于单一字体、输入法和浏览器默认
> 行为的传统蒙古文语义字形计算引擎，而不只是给网页添加竖排 CSS。

当前状态：**Phase 0–2 基础能力与 Phase S1 机器证据闭环已完成；Phase S2.2
项目字形几何合同已经启动**。完整跨浏览器验证和生产级语言准确率评估尚未完成，
但它们不是继续建设底层引擎的前置审批。

## 正式体验

当前唯一正式入口是 [`index.html`](index.html)，核心体验位于：

- [`demos/input/ai-chat.html`](demos/input/ai-chat.html) — 本地优先写作工作台与 Unicode 诊断 Alpha
- [`knowledge/index.html`](knowledge/index.html) — 可追溯的传统蒙古文数字化科研知识库
- [`engine/index.html`](engine/index.html) — 无损输入、确定性 HarfBuzz WASM 塑形与码位诊断实验室

确定性引擎逐码位保留输入，锁定 HarfBuzz 与字体哈希生成 SVG glyph path；未取得可靠映射的私有编码会被无损保存并阻止猜测转换。下一阶段在字体后端之上建立项目自己的 `semanticRole` 与几何规则；旧工作台仍保留在 [Labs](demos/README.md)，不再代表字形正确性承诺。

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
- Phase S2.0：93个标准目标的语义角色注册表，75个后端支持目标与18个项目字形待实现目标
- Phase S2.1：锁定 Unicode 17.0.0 Joining_Type，普通单词自动计算首／中／尾／独立字位并输出语义轨迹
- MVS／NNBSP 结构语义：区分现代 MVS、旧 NNBSP 和分离词尾元音候选，不在缺少词典时猜词义
- 控制符共现索引：只保存码位上下文、次数和来源，不把网页正文或字体结果当作规则
- Phase S2.2：18个项目字形缺口具有连接锚点、推进量、边界框、路径安全和许可证合同；当前0个轮廓资产就绪
- 可重放网页语料爬虫：robots 检查、TLS 安全、限速、短片段提取与码位统计

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

机器证据与历史审核数据见 [`data/quality/`](data/quality/)。人工材料用于交叉验证和
发现反例，不是引擎继续开发的许可门禁。架构边界以[项目宪章](docs/00_PROJECT_CHARTER.md)
为准。

科研知识库的当前索引、证据等级和覆盖缺口见
[`KNOWLEDGE_BASE_INDEX.md`](docs/04-research/KNOWLEDGE_BASE_INDEX.md)。旧研究文档中的人物、准确率和“完全支持”声明默认不再视为事实源。

真实传统蒙古文用法将通过可重放网页语料管线采集原始 Unicode 和词级上下文，
而不是收集所谓“正确截图”；执行规范见
[`WEB_CORPUS_ACQUISITION.md`](docs/04-research/WEB_CORPUS_ACQUISITION.md)。

## 产品路线与质量原则

Phase 0–2 的已交付能力、退出条件和明确边界见
[`PRODUCT_ROADMAP.md`](docs/05-project/PRODUCT_ROADMAP.md)。

1. 对外声明必须标明依据：可复现测试、标准、实现观测或人工证据，不把其中任一种伪装成全部真值。
2. 正式体验必须使用原生竖排，不通过旋转模拟。
3. 用户输入必须作为文本处理，不注入 HTML。
4. 核心流程必须可通过键盘操作，并提供可理解的标签和状态。
5. 历史演示与正式产品能力必须明确分开。

竖排引擎的能力探测、兼容回退和 Unicode 契约见
[`MONGOL_VERTICAL_ENGINE.md`](docs/02-architecture/MONGOL_VERTICAL_ENGINE.md)。

## 贡献

欢迎提交测试语料、浏览器兼容性报告、无障碍修复和母语文字审核。请不要在缺少数据集、评估脚本和结果记录时新增准确率声明。

项目采用 [MIT License](LICENSE)。
