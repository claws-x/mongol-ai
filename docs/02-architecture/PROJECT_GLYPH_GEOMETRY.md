# 项目字形几何契约

**阶段**：S2.2 Geometry Contract

**版本**：0.8.0

**状态**：18个要求已生成，0个轮廓资产就绪

## 目的

当语义层要求某个字形而锁定字体后端不能提供时，引擎不能继续静默使用错误的
默认 glyph。项目字形层必须先通过一个与具体字体无关、可自动验证的几何合同，
才能进入正式输出。

```text
semanticRole
  → geometry requirement
  → licensed outline asset
  → deterministic geometry validation
  → run composition
  → vertical output
```

## 坐标系统

项目字形采用 `logical-font-space-x-forward-y-up`：塑形流在旋转前沿正 X 方向前进。
leading edge 映射为最终竖排的顶部，trailing edge 映射为底部。这样可与当前
HarfBuzz 横向塑形后整体旋转的确定性管线组合，而不混淆“字形坐标”和“页面
竖排坐标”。

## 连接拓扑

| joining state | entry | exit |
|---|---:|---:|
| isolate | 否 | 否 |
| initial | 否 | 是 |
| medial | 是 | 是 |
| final | 是 | 否 |

入口必须接近 bounding box 的 leading edge，出口必须接近 trailing edge；同时
存在时，两者的 stem-axis 偏差不得超过合同容差。

## 自动否决条件

- SVG path 为空或包含非路径语法；
- `advance <= 0`；
- bounding box 为空、反向或不是有限数；
- 缺少必须的连接锚点或出现不该存在的锚点；
- 入口／出口没有落在对应边界；
- medial 入口和出口不在允许的主干容差内；
- 轮廓来源不是 `mongol-ai-original` 或 `ofl-derived`；
- 没有许可证声明。

## 当前事实

`data/engine/project-glyph-geometry.json` 由语义注册表确定性生成。当前18个
`project-glyph-required` 角色都有合同，但没有任何轮廓被登记为 `asset-ready`。
`MONGOLIAN_A.medial.form3` 在锁定 Noto 字体中仍与默认 medial glyph 使用相同
glyph ID，因此不能把该默认轮廓重新命名后冒充第三形。正式页面遇到这些角色时
停止 SVG 输出，只返回 `asset-missing` 缺口；不会一边警告一边继续画错误默认字形。

下一步是建立第一个原创或 OFL 兼容轮廓资产，并从 path 本身计算真实边界框，
而不是信任资产声明的 bbox。
