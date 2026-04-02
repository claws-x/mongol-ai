# 📖 HarfBuzz 字体整形引擎学习笔记

**学习日期**: 2026-04-01  
**资料来源**: HarfBuzz Official Documentation  
**链接**: https://harfbuzz.github.io/

---

## 🎯 核心要点

### 1. 什么是 HarfBuzz？

**定义**: HarfBuzz 是一个**开源的字体整形引擎**（Font Shaping Engine）。

**作用**:
- 将 Unicode 文本转换为字形（glyphs）
- 处理复杂文字的连字规则
- 处理上下文相关的字符变形
- 支持多种文字系统（阿拉伯文、蒙古文、梵文等）

**使用场景**:
- 🌐 浏览器（Chrome、Firefox、Safari 都有使用）
- 🖥️ 操作系统（Linux、Android 默认使用）
- 📱 移动应用（跨平台文本渲染）

---

### 2. HarfBuzz 的工作原理

### 整形流程

```
Unicode 文本
    ↓
[hb_buffer_t] - 创建缓冲区
    ↓
设置 direction/script/language
    ↓
[hb_shape()] - 执行整形
    ↓
Glyph 输出（带位置信息）
```

### 关键 API

```c
// 1. 创建缓冲区
hb_buffer_t *buf = hb_buffer_create();

// 2. 设置文本方向（蒙古文：从上到下）
hb_buffer_set_direction(buf, HB_DIRECTION_TTB);

// 3. 设置文字脚本（蒙古文）
hb_buffer_set_script(buf, HB_SCRIPT_MONGOLIAN);

// 4. 设置语言
hb_buffer_set_language(buf, hb_language_from_string("mn", -1));

// 5. 添加文本
hb_buffer_add_codepoints(buf, text, text_length, 0, -1);

// 6. 执行整形
hb_shape(font, buf, NULL, 0);

// 7. 获取结果
hb_glyph_info_t *info = hb_buffer_get_glyph_infos(buf, &info_count);
hb_glyph_position_t *pos = hb_buffer_get_glyph_positions(buf, &pos_count);
```

---

### 3. 蒙古文支持情况

### 3.1 支持的特性

| 特性 | 支持度 | 说明 |
|------|--------|------|
| 词首变形 | ✅ 支持 | 需要字体支持 |
| 词中变形 | ✅ 支持 | 需要字体支持 |
| 词尾变形 | ✅ 支持 | 需要字体支持 |
| 连字规则 | ✅ 支持 | 需要 OpenType 字体 |
| 变体选择符 | ⚠️ 部分 | VS1-VS16 支持有限 |
| 竖排布局 | ❌ 不支持 | 需要 CSS/上层处理 |

### 3.2 关键限制

**HarfBuzz 不处理**:
- ❌ 文本布局方向（writing-mode）
- ❌ 列间距/行间距
- ❌ 字符旋转方向
- ❌ 页面级排版

**这些需要**:
- ✅ CSS 处理（`writing-mode: vertical-lr`）
- ✅ 浏览器布局引擎处理
- ✅ 应用层代码处理

---

### 4. 与当前项目的关联

### 4.1 我们的问题定位

根据 HarfBuzz 文档分析：

| 问题 | 原因分析 | 解决层级 |
|------|----------|----------|
| 蒙古文躺着 | CSS `writing-mode` 问题 | CSS 层 |
| 字符方向错 | CSS `text-orientation` 问题 | CSS 层 |
| 连字异常 | HarfBuzz + 字体问题 | 字体/引擎层 |
| 变体错误 | Unicode + 字体问题 | Unicode/字体层 |

### 4.2 当前方案评估

**CSS 方案（当前使用）**:
```css
.key-char {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
}
```

**优点**:
- ✅ 简单易实施
- ✅ 浏览器原生支持
- ✅ 符合 W3C 标准

**局限**:
- ⚠️ 依赖浏览器 HarfBuzz 集成
- ⚠️ 不处理复杂连字
- ⚠️ 字体要求高

### 4.3 备选方案研究

#### 方案 A: Canvas + HarfBuzz（高级）

```javascript
// 伪代码示例
const buffer = hb.Buffer.create();
buffer.addText('ᠮᠣᠩᠭᠣᠯ');
buffer.guessSegmentProperties();
hb.shape(font, buffer);

const glyphs = buffer.glyphInfo;
const positions = buffer.glyphPosition;

// 在 Canvas 上绘制
ctx.save();
ctx.rotate(Math.PI / 2);  // 旋转 90 度
glyphs.forEach((glyph, i) => {
    const x = positions[i].xOffset;
    const y = positions[i].yOffset;
    drawGlyph(glyph, x, y);
});
ctx.restore();
```

**优点**:
- ✅ 完全控制渲染
- ✅ 正确处理连字
- ✅ 不依赖浏览器竖排支持

**局限**:
- ❌ 实现复杂
- ❌ 需要 HarfBuzz WASM 编译
- ❌ 性能开销大
- ❌ 不支持文本选择

#### 方案 B: SVG 文本（中级）

```svg
<svg>
  <text writing-mode="vertical-lr" text-orientation="upright">
    ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ
  </text>
</svg>
```

**优点**:
- ✅ 高质量渲染
- ✅ 支持文本选择
- ✅ 可缩放

**局限**:
- ⚠️ 仍然依赖浏览器 HarfBuzz
- ⚠️ 实现复杂度中等

---

### 5. 行动计划

### P0 - 当前方案优化（CSS 层）
- [x] 所有蒙古文元素添加竖排 CSS
- [x] 使用 `!important` 确保优先级
- [ ] 测试不同浏览器效果
- [ ] 收集渲染问题数据

### P1 - 字体层优化
- [ ] 研究蒙古文 OpenType 字体
- [ ] 测试 Noto Sans Mongolian 渲染效果
- [ ] 考虑本地字体备用方案
- [ ] 优化字体加载策略

### P2 - 引擎层研究（长期）
- [ ] 研究 HarfBuzz WASM 集成
- [ ] 评估 Canvas 渲染方案
- [ ] 评估 SVG 渲染方案
- [ ] 性能测试和对比

### P3 - 标准参与（超长期）
- [ ] 关注 W3C 蒙古文标准进展
- [ ] 参与浏览器蒙古文支持讨论
- [ ] 贡献开源项目

---

## 📊 技术栈对比

| 方案 | 复杂度 | 渲染质量 | 性能 | 推荐场景 |
|------|--------|----------|------|----------|
| CSS 竖排 | ⭐ 简单 | ⭐⭐⭐ 好 | ⭐⭐⭐⭐ 高 | 基本显示 |
| SVG 文本 | ⭐⭐ 中等 | ⭐⭐⭐⭐ 很好 | ⭐⭐⭐ 中 | 高质量需求 |
| Canvas+HarfBuzz | ⭐⭐⭐⭐ 复杂 | ⭐⭐⭐⭐⭐ 完美 | ⭐⭐ 低 | 专业应用 |

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| HarfBuzz 文档 | https://harfbuzz.github.io/ |
| HarfBuzz GitHub | https://github.com/harfbuzz/harfbuzz |
| HarfBuzz WASM | https://github.com/harfbuzz/harfbuzzjs |
| W3C Mongolian Gap | https://www.w3.org/TR/mong-gap/ |

---

**笔记完成时间**: 2026-04-01 11:20 JST  
**下一步**: 学习 Unicode 编码和研究论文
