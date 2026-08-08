# 确定性传统蒙古文引擎

**状态**：S1 数学验证基线

**版本**：0.4.0

**日期**：2026-08-08

## 1. 纠正目标

旧引擎只检测 `writing-mode: vertical-lr`、字体是否加载以及列是否从左向右推进。它能证明“页面发生了竖排”，不能证明“输入序列、上下文字形或词形正确”。用户已明确否决 Pages 旧示例的第二个显示字形，因此该示例被登记为 `rejected_reference` 并撤下。

新引擎把以下对象分开：

1. 原始按键与候选提交结果；
2. 编码体系和输入法来源；
3. Unicode 码位、FVS/MVS/NNBSP/连接控制符；
4. HarfBuzz 输出的 glyph ID、位置和轮廓；
5. 语义字形规则及其版本化证据；
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
- 使用 HarfBuzz 默认 buffer flags：FVS、MVS、ZWJ 等控制符仍参与 Joining/GSUB，但不要求字体输出其占位 glyph；
- SVG 安全层按字体 glyph name 识别 `fvs1`–`fvs4` 与 `mvs` 控制占位，保留在调试证据中，但禁止绘入正文。

不能直接用 `TTB` 替代这个流程：对当前 OpenType 蒙古文字体，直接 TTB 会选择另一套推进度量，实测会破坏常见字体的连接。该差异已经通过 `hb-shape` 和浏览器输出复现。

## 6. 双输出

- **确定性视觉层**：HarfBuzz WASM 产生 glyph ID 和 path，页面输出 SVG；不同浏览器不再重新选择字形。
- **可访问文本层**：原始 Unicode 保存在隐藏文本节点中，用于复制、搜索和辅助技术。

字体轮廓、HarfBuzz 版本和规则覆盖都会影响结果，因此全部纳入版本和哈希。

## 6.1 第一性原理中间层

引擎不把某个字体 glyph ID 当作语言规则。一个变体先表示成：

```text
基础码位 + Joining位置(00/01/11/10) + FVS意图 + 标准来源
```

连接位置由两个布尔量构造：`00=isolate`、`01=initial`、`11=medial`、`10=final`。自动探针用 ZWJ 强制连接，不引入特定单词、元音和谐或载体字母。FVS 必须紧跟被修饰字符。

60 条标准变体被展开成 234 对 selector/baseline 差分探针：93 个 Unicode 声明目标，141 个范围外观察。只有声明目标参与评分；范围外结果只保留为兼容证据。

锁定 Noto 当前结果：44/60 条标准变体在全部声明位置产生机械响应，16 条进入标准—字体冲突队列；35 个基础字符通过四位置覆盖检查；4 个裸 FVS 被正确隐藏；MVS 需要上下文。该结果说明 backend 支持范围，不等于语言学真值。

## 7. 语义规则与证据分离

引擎规则是否可执行，不再取决于人工 `approved`。每条规则必须保存：

1. 精确输入 profile 和完整码位序列；
2. joining state 与 variation intent；
3. 唯一、稳定的 `semanticRole`；
4. 规则来源、版本和反例；
5. 后端支持、替代或缺失状态；
6. 可自动运行的码位、选择、控制符和几何断言。

真实网页码位语料、Onon／蒙科立输出和具名审核可以提高证据等级、发现错误或
否决规则，但不是研发审批。证据不足时应明确标记置信等级并继续求解，不能让
规则系统退回浏览器默认输出。截图只用于视觉回归，不作为字形规则来源。

完整原则见 [`项目宪章`](../00_PROJECT_CHARTER.md)。

## 8. 尚未解决且不能伪装解决的部分

- 未取得 Onon MK、MW 和蒙科立编码的授权完整映射表；
- Onon 官网字体只用于临时技术对比，未复制进仓库，也未在产品中调用；
- 当前 Noto 字形指纹只能证明输出可复现，不能证明语言学正确；
- 93 个声明目标尚未全部进入项目自己的语义角色注册表；
- 16 个当前字体无差分目标尚未具备项目自有兼容许可轮廓；
- MVS 尚未完成词级上下文模型；
- “任意输入都正确”需要持续扩展规则、反例和自动断言，不能靠一次性声明。

## 9. Phase S2 的第一条纵向切片

以 `U+1820 U+180C` 在 medial 上下文中的 `third form` 为第一条实现：解析为
`MONGOLIAN_A.medial.form3`，记录当前后端是否支持；控制符只参与选择；输出轮廓
必须通过连接入口、出口、边界框和推进量断言，并能追溯回原始两个码位。公开
网页语料、Onon／蒙科立输出和人工判断用于交叉验证这一结果，而不决定工作能否
开始。采集规范见
[`WEB_CORPUS_ACQUISITION.md`](../04-research/WEB_CORPUS_ACQUISITION.md)。
