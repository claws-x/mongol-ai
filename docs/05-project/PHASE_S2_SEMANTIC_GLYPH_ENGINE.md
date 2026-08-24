# Phase S2 — 语义字形计算引擎

**当前子阶段**：S2.0 Foundation 已实现  
**版本**：0.5.0  
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

- 真实单词中的 joining state 规则模型；
- MVS、NNBSP 和词法变体的完整语义；
- 18个缺失目标的项目字形轮廓；
- 连接入口、出口、主干、推进量和边界框几何断言；
- 大规模、多地区、多类型网页语料；
- 完整的多列竖排输出接入。

## 下一子阶段：S2.1 Context Model

1. 引入版本锁定的 Unicode Joining_Type 数据；
2. 从网页语料生成词与控制符共现索引；
3. 计算真实文本中的 isolate／initial／medial／final；
4. 将语义解析器接入引擎实验室；
5. 为 `MONGOLIAN_A.medial.form3` 建立第一套项目字形几何接口，但不复制闭源轮廓；
6. 对所有18个 `project-glyph-required` 目标建立失败测试。

## Ollama 使用边界

本地 Ollama 可以执行来源标签初稿、重复命名检查、日志归类和文档格式整理。
模型输出不能直接修改码位、Unicode 来源、语义角色、许可状态或字形规则；所有
这类结果必须由确定性生成器、Schema和测试重新验证。本轮曾尝试用 `qwen3:8b`
检查93条名称，因长输入响应效率不理想而中止，最终使用唯一性与字段一致性测试
完成验证。这是正常的成本路由结果，不把本地模型使用本身当成交付指标。
