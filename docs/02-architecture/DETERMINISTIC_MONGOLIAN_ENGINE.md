# 确定性传统蒙古文引擎

**状态**：S0 可运行基线

**版本**：0.3.0

**日期**：2026-08-08

## 1. 纠正目标

旧引擎只检测 `writing-mode: vertical-lr`、字体是否加载以及列是否从左向右推进。它能证明“页面发生了竖排”，不能证明“输入序列、上下文字形或词形正确”。用户已明确否决 Pages 旧示例的第二个显示字形，因此该示例被登记为 `rejected_reference` 并撤下。

新引擎把以下对象分开：

1. 原始按键与候选提交结果；
2. 编码体系和输入法来源；
3. Unicode 码位、FVS/MVS/NNBSP/连接控制符；
4. HarfBuzz 输出的 glyph ID、位置和轮廓；
5. 人工确认的正确字形；
6. 浏览器最终显示。

## 2. 已确认的一手事实

- [Onon 使用指南](https://ime.onon.cn/help-index.html)说明输入法可切换 MN 国家标准编码、MK 蒙科立编码和 MW 民委共享工程编码；指南还说明 `/` 用于字母首、中、尾形态输入。
- [Onon 关于页](https://ime.onon.cn/zh-CN/about)说明其获得蒙科立蒙古文字体授权。这不构成本项目再分发该字体的许可。
- [Unicode 17.0 第 13 章](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-13/)说明蒙古文包含位置相关形式和词汇／正字法相关变体。
- [Unicode Technical Note #57](https://www.unicode.org/notes/tn57/)提供表示和分层塑形规则，但其自身明确属于非规范性技术说明。
- [harfbuzzjs 官方项目](https://github.com/harfbuzz/harfbuzzjs)提供浏览器和 Node 可用的 HarfBuzz WASM，以及从 glyph ID 取得 SVG path 的接口。
- 项目字体来自 [Noto Mongolian 官方仓库](https://github.com/notofonts/mongolian)，许可证为 OFL-1.1。

## 3. 无损输入契约

`LosslessMongolianDocument` 的 `raw` 是最高优先级事实：

- 不自动执行 NFC/NFKC；
- 不删除 FVS1–FVS4、MVS、ZWNJ、ZWJ 或 NNBSP；
- 不把 NNBSP 改成普通空格；
- 不对 PUA 私用区做猜测映射；
- `serialize()` 必须逐码位返回原文。

输入法适配器当前接受“候选已经提交后的文本”，而不是冒充 Onon 或蒙科立的闭源词库、联想和按键算法。

## 4. 编码适配边界

| Profile | 当前行为 | 可塑形 | 原因 |
|---|---|---:|---|
| `unicode-national` | 逐码位保留 | 是 | 已是 Unicode 文本 |
| `onon-mn` | 逐码位保留 | 是 | Onon MN 为国家标准模式 |
| `onon-mk` | 无损保存 | 否 | 缺少经授权、版本化、完整映射表 |
| `onon-mw` | 无损保存 | 否 | 缺少权威完整映射表 |
| `menksoft-raw` | 无损保存 PUA | 否 | 不允许根据字形或二手资料猜码 |

阻止转换是安全功能，不是遗漏。取得映射表后，还必须记录版本、来源、许可证、往返测试和无法一一对应的条目。

## 5. 确定性塑形

当前运行时锁定：

- harfbuzzjs `1.5.0`；
- HarfBuzz `14.3.0`；
- Noto Sans Mongolian 字体 SHA-256：`a28ba3cde3de22de7ddc934bd5d5babe54e6ce28c073a288cd978ffcf26b295b`；
- script：`Mong`；language：`mn`；
- 输入方向：`LTR`，完成连接塑形后把整条 glyph run 旋转为从上到下显示；
- `PRESERVE_DEFAULT_IGNORABLES`，保留默认不可见控制符参与塑形。

不能直接用 `TTB` 替代这个流程：对当前 OpenType 蒙古文字体，直接 TTB 会选择另一套推进度量，实测会破坏常见字体的连接。该差异已经通过 `hb-shape` 和浏览器输出复现。

## 6. 双输出

- **确定性视觉层**：HarfBuzz WASM 产生 glyph ID 和 path，页面输出 SVG；不同浏览器不再重新选择字形。
- **可访问文本层**：原始 Unicode 保存在隐藏文本节点中，用于复制、搜索和辅助技术。

字体轮廓、HarfBuzz 版本和规则覆盖都会影响结果，因此全部纳入版本和哈希。

## 7. 字形覆盖闸门

覆盖规则必须同时具备：

1. 精确输入 profile；
2. 完整码位序列；
3. 锁定字体哈希；
4. 正确参考截图；
5. 输入法名称和版本；
6. 至少一名具名审核者确认；
7. 状态为 `approved`。

缺少任一条件，规则不得加载。目前批准覆盖数为 **0**。这是因为用户已指出错误，但尚未提供正确结果；引擎不会把另一款字体的输出猜成答案。

## 8. 尚未解决且不能伪装解决的部分

- 未取得 Onon MK、MW 和蒙科立编码的授权完整映射表；
- 未取得截图中错误位置的正确字形、原始按键、输入法模式和字体版本；
- Onon 官网字体只用于临时技术对比，未复制进仓库，也未在产品中调用；
- 当前 Noto 字形指纹只能证明输出可复现，不能证明语言学正确；
- “任意输入都正确”需要持续扩充经人工确认的金标准，而不是一次性代码声明。

## 9. 下一条批准规则所需材料

请提供截图中原文在 Onon 的 MN/MK 模式以及蒙科立中的“复制结果”，再提供正确截图。系统会逐码位比较三者，确认是编码差异、控制符差异还是字体 GSUB 字形差异，之后才能创建第一条 approved 规则。
