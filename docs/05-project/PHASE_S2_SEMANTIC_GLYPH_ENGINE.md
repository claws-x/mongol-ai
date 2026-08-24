# Phase S2 — 语义字形计算引擎

**当前子阶段**：S2.2 Geometry Contract 已启动

**版本**：0.8.0

**日期**：2026-08-24

## 目标

把“输入码位”和“字体碰巧输出的 glyph”之间增加项目自己的语义决策层：

```text
输入 → 语义角色 → 后端能力 → 项目字形 → 几何 → 竖排输出
```

## S2.0 已交付

- `data/engine/s2-semantic-registry.json`：93个 Unicode 声明目标；
- `core/semantic_glyph_engine.mjs`：无损分词、显式 joining context 与语义角色解析；
- `MONGOLIAN_A.medial.form3` 第一条纵向切片，明确标为 `project-glyph-required`；
- 当前锁定 Noto/HarfBuzz 后端：75个具体目标 `supported`，18个具体目标 `project-glyph-required`；
- `tools/corpus/crawl.mjs`：robots 检查、TLS 校验、限速、HTML 类型限制和失败隔离；
- `core/web_corpus.mjs`：HTML 文本提取、控制符保留、短片段和上下文采集；
- 5个首批来源记录，其中2个因 TLS 问题安全禁用、1个标准参考不进入自然语料统计；
- 首次真实采集2个独立域名、2段短文本、23个蒙古文相关码位，包含1个 FVS2；
- 语料 Schema、统计器、构建命令与自动测试。

这些结果证明基础管线可运行，不证明全部字形已经正确。

## 明确未完成

- MVS、NNBSP 的具体后缀词典与多后缀消歧；
- 18个缺失目标的项目字形轮廓；
- 连接入口、出口、主干、推进量和边界框几何断言；
- 大规模、多地区、多类型网页语料；
- 完整的多列竖排输出接入。

## S2.1 已交付的确定性纵向切片

- 锁定 Unicode 17.0.0 `DerivedJoiningType.txt` 的来源 URL 与 SHA-256；
- 抽取蒙古文相关的 `D`、`C`、`T` 和默认 `U` 连接属性，版本化保存；
- 普通蒙古文单词自动计算 isolate／initial／medial／final，不再依赖人为插入 ZWJ；
- FVS 保留在原始 grapheme 中并作为 Transparent 处理，不破坏相邻连接；
- NNBSP、MVS、ZWNJ 明确断开连接，Nirugu 与 ZWJ 明确促成连接；
- 引擎实验室展示每个 grapheme 的 Joining_Type、计算字位、semanticRole 与后端状态；
- 18个 `project-glyph-required` 目标全部具有显式失败状态测试。
- 从网页观察生成不含正文的控制符共现索引，只保存左右码位、次数、来源和域名；
- 当前2个真实网页观察中记录1次 FVS2、0次 MVS、0次 NNBSP，零覆盖也作为事实保存；
- 将 MVS 分离词尾元音、Unicode 16+ 分离后缀和旧 NNBSP 后缀结构分开标注；
- 没有词典证据的结构统一返回 `requires-lexical-resolution`，不猜具体词义。

这套模型计算字符连接位置，不擅自推断词义，也不把字体输出倒推为 Unicode 语义。

## S2.1 接下来完成

1. 扩展多地区、多类型网页来源，取得真实 MVS／NNBSP 共现，不用标准示例冒充自然语料；
2. 建立版本化分离后缀词典和多后缀结构，但所有词条必须有可追溯来源；

## S2.2 已交付的几何契约

- 由语义注册表确定性生成18个 `project-glyph-required` 几何要求；
- 明确定义旋转前正 X 流向与旋转后的自上而下映射；
- isolate／initial／medial／final 分别映射到不同入口和出口拓扑；
- 验证 path、推进量、边界框、边缘锚点、主干连续性和轮廓许可证；
- 页面把 `project-glyph-required` 继续解析为 `asset-missing`，不隐藏缺口；
- 当前0／18资产就绪，不复制闭源轮廓，也不把 Noto 默认字形冒充第三形。

详细合同见 [`PROJECT_GLYPH_GEOMETRY.md`](../02-architecture/PROJECT_GLYPH_GEOMETRY.md)。

## S2.2 接下来完成

1. 从 SVG path 自身推导真实 bounding box，消除对资产声明的信任；
2. 为 `MONGOLIAN_A.medial.form3` 建立第一套原创或 OFL 兼容轮廓资产；
3. 将通过验证的项目字形插入 glyph run，并保持 cluster 到原始码位的追踪；
4. 对入口、出口与相邻字体 glyph 建立组合级连续性断言。

## Ollama 使用边界

本地 Ollama 可以执行来源标签初稿、重复命名检查、日志归类和文档格式整理。
模型输出不能直接修改码位、Unicode 来源、语义角色、许可状态或字形规则；所有
这类结果必须由确定性生成器、Schema和测试重新验证。本轮曾尝试用 `qwen3:8b`
检查93条名称，因长输入响应效率不理想而中止，最终使用唯一性与字段一致性测试
完成验证。这是正常的成本路由结果，不把本地模型使用本身当成交付指标。
