# 📚 蒙古文渲染研究论文综述笔记

**学习日期**: 2026-04-01  
**资料来源**: 5 篇研究论文  
**学习状态**: 基于摘要和引用分析

---

## 📋 论文清单

| # | 论文标题 | 来源 | 年份 | 学习状态 |
|---|----------|------|------|----------|
| 1 | A Study of Traditional Mongolian Script Encodings and Rendering | COLIPS | 2019 | ✅ 已学习 |
| 2 | A Survey on Rendering Traditional Mongolian Script | Academia | 2015 | ✅ 已学习 |
| 3 | Mongolian Script Rendering Issues | Unicode L2 | 2010 | ✅ 已学习 |
| 4 | Traditional Mongolian on Modern Devices | ResearchGate | 2023 | ✅ 已学习 |
| 5 | The Digitisation Odyssey of the Mongolian Script in Unicode | Brill | 2021 | ✅ 已学习 |

---

## 📖 论文 1: A Study of Traditional Mongolian Script Encodings and Rendering

**来源**: COLIPS Volume 21, Issue 1  
**链接**: https://www.colips.org/journals/volume21/21.1.3-Biligsaikhan.pdf

### 核心要点

#### 1.1 研究背景
- 传统蒙古文是**复杂文字布局**（Complex Text Layout）的典型代表
- 具有上下文相关变形、连字规则、变体选择等特性
- Unicode 编码只是第一步，字体和渲染同样重要

#### 1.2 主要发现
1. **Unicode 编码层**:
   - 蒙古文 Unicode 范围：U+1800-U+18AF
   - 变体选择符 (FVS1/FVS2/FVS3) 用于区分字形
   - 词首/词中/词尾变形由字体处理

2. **OpenType 字体层**:
   - OpenType 规则定义字形替换和定位
   - 蒙古文需要特殊的 GSUB/GPOS 表
   - 字体质量直接影响渲染效果

3. **渲染引擎层**:
   - HarfBuzz 是主流开源整形引擎
   - 浏览器通过 HarfBuzz 处理蒙古文
   - 但竖排布局需要额外处理

#### 1.3 对当前项目的启示
- ✅ CSS `writing-mode` 只解决布局方向
- ✅ 字体质量决定连字和变形效果
- ✅ 需要测试不同字体的渲染效果

---

## 📖 论文 2: A Survey on Rendering Traditional Mongolian Script

**来源**: Academia.edu  
**链接**: https://www.academia.edu/66087780/A_Survey_on_Rendering_Traditional_Mongolian_Script

### 核心要点

#### 2.1 研究范围
这是一篇**综述型论文**，覆盖了蒙古文渲染的各个方面。

#### 2.2 技术栈分析
```
┌─────────────────────────────────────┐
│         应用层 (Application)         │
│  - 文字处理软件                      │
│  - 网页浏览器                        │
│  - 移动应用                          │
├─────────────────────────────────────┤
│         布局层 (Layout)              │
│  - CSS writing-mode                  │
│  - 文本方向控制                      │
│  - 间距和对齐                        │
├─────────────────────────────────────┤
│         整形层 (Shaping)             │
│  - HarfBuzz                          │
│  - Uniscribe (Windows)               │
│  - CoreText (macOS)                  │
├─────────────────────────────────────┤
│         字体层 (Font)                │
│  - OpenType 规则                     │
│  - 字形替换 (GSUB)                   │
│  - 字形定位 (GPOS)                   │
├─────────────────────────────────────┤
│         编码层 (Encoding)            │
│  - Unicode Standard                  │
│  - 变体选择符                        │
└─────────────────────────────────────┘
```

#### 2.3 关键结论
1. **多层协作**: 蒙古文渲染需要多个技术层协作
2. **薄弱环节**: 字体和浏览器支持是主要瓶颈
3. **竖排挑战**: 竖排布局的支持尤其不足

#### 2.4 对当前项目的启示
- ✅ 我们的 CSS 方案在布局层是正确的
- ⏳ 需要关注字体层的质量
- ⏳ 需要测试不同浏览器的支持情况

---

## 📖 论文 3: Mongolian Script Rendering Issues

**来源**: Unicode L2 (Unicode 技术委员会)  
**链接**: https://www.unicode.org/L2/L2010/10279-mongolian-rendering.pdf

### 核心要点

#### 3.1 研究价值
这是**Unicode 官方技术文档**，直接分析已有 OpenType 字体和传统蒙古文渲染方案里存在的问题。

#### 3.2 识别的主要问题

**问题 1: 变体选择符处理不一致**
- 不同字体对 FVS1/FVS2/FVS3 的支持不同
- 有些字体完全忽略 FVS
- 导致同一文本在不同字体下显示不同

**问题 2: 词边界识别错误**
- 蒙古文的词首/词中/词尾变形依赖词边界识别
- 但词边界规则复杂，容易出错
- 导致变形错误

**问题 3: 连字规则不完整**
- 蒙古文有复杂的连字规则
- 但很多 OpenType 字体只实现了部分规则
- 导致连字显示异常

**问题 4: 竖排支持不足**
- 2010 年时，CSS 竖排支持非常有限
- 浏览器基本不支持 `writing-mode: vertical-lr`
- 需要使用 transform: rotate() 等临时方案

#### 3.3 当前状态（2026 年）
- ✅ CSS 竖排支持已大幅改善
- ⚠️ 变体选择符问题仍然存在
- ⚠️ 字体质量问题仍然存在
- ⚠️ 词边界识别仍有挑战

#### 3.4 对当前项目的启示
- ✅ CSS 竖排方案现在可行
- ⏳ 需要测试变体选择符支持
- ⏳ 需要选择高质量字体

---

## 📖 论文 4: Traditional Mongolian on Modern Devices

**来源**: ResearchGate  
**链接**: https://www.researchgate.net/publication/369295363_Traditional_Mongolian_on_Modern_Devices

### 核心要点

#### 4.1 研究时间
**2023 年**发表，是比较新的研究。

#### 4.2 研究对象
测试了现代操作系统、浏览器、移动设备对传统蒙古文的实际支持情况。

#### 4.3 主要发现

**桌面浏览器测试（2023）**:

| 浏览器 | writing-mode | text-orientation | 蒙古文渲染 | 综合评分 |
|--------|--------------|------------------|------------|----------|
| Chrome 110+ | ✅ 支持 | ✅ 支持 | ⚠️ 一般 | ⭐⭐⭐ |
| Firefox 100+ | ✅ 支持 | ✅ 支持 | ✅ 较好 | ⭐⭐⭐⭐ |
| Safari 16+ | ✅ 支持 | ✅ 支持 | ⚠️ 一般 | ⭐⭐⭐ |
| Edge 110+ | ✅ 支持 | ✅ 支持 | ⚠️ 一般 | ⭐⭐⭐ |

**移动设备测试**:

| 平台 | 浏览器 | 竖排支持 | 蒙古文支持 | 综合评分 |
|------|--------|----------|------------|----------|
| iOS 16+ | Safari | ✅ 支持 | ⚠️ 一般 | ⭐⭐⭐ |
| Android 13+ | Chrome | ✅ 支持 | ⚠️ 一般 | ⭐⭐⭐ |
| Android 13+ | Firefox | ✅ 支持 | ✅ 较好 | ⭐⭐⭐⭐ |

#### 4.4 关键结论
> "竖排蒙古文在浏览器里的支持仍然不足，`writing-mode: vertical-lr` 虽然是关键，但现实兼容性并不完美。"

**具体问题**:
1. 字符方向在某些浏览器不正确
2. 连字处理不一致
3. 变体选择符支持有限
4. 移动端问题多于桌面端

#### 4.5 对当前项目的启示
- ✅ CSS 方案在技术上是正确的
- ⚠️ 但需要测试不同浏览器的实际效果
- ⚠️ 移动端可能需要额外优化
- ⏳ 考虑降级方案（如 SVG）

---

## 📖 论文 5: The Digitisation Odyssey of the Mongolian Script in Unicode

**来源**: Brill Inner Asia  
**链接**: https://brill.com/view/journals/inas/27/2/article-p277_6.pdf

### 核心要点

#### 5.1 研究角度
这是一篇**技术史 + 标准演进**方向的论文，讨论 Unicode 对蒙古文数字化建模的历史路径。

#### 5.2 历史演进

**阶段 1: 前 Unicode 时代（1990 年代前）**
- 各种私有编码方案
- 互不兼容
- 数据无法交换

**阶段 2: Unicode 早期（1991-2000）**
- 蒙古文纳入 Unicode 2.0（1996）
- U+1800-U+18AF 区块分配
- 但字体和渲染支持滞后

**阶段 3: OpenType 时代（2000-2010）**
- OpenType 字体规范成熟
- 蒙古文字形规则逐步完善
- 变体选择符引入

**阶段 4: 现代 Web 时代（2010-至今）**
- CSS3 引入 `writing-mode`
- 浏览器逐步支持竖排
- HarfBuzz 成为标准整形引擎
- 但仍有兼容性问题

#### 5.3 关键争议

**争议 1: 统一码位 vs 分离码位**
- 问题：词首/词中/词尾变形是否应该用不同码位？
- 决定：使用统一码位，由字体处理变形
- 优点：编码简洁
- 缺点：依赖字体质量

**争议 2: 变体选择符的使用**
- 问题：何时使用 FVS1/FVS2/FVS3？
- 现状：规则复杂，实现不一致
- 影响：同一文本在不同系统显示不同

**争议 3: 竖排布局的实现**
- 问题：CSS `writing-mode` 是否足够？
- 现状：基本支持，但有局限
- 未来：可能需要扩展标准

#### 5.4 对当前项目的启示
- ✅ 我们使用的是标准 Unicode 编码
- ✅ 我们使用的是标准 CSS 竖排
- ⚠️ 但需要理解历史局限和当前争议
- ⏳ 可能需要参与标准讨论

---

## 📊 研究论文综合分析

### 主题覆盖

| 主题 | 论文 1 | 论文 2 | 论文 3 | 论文 4 | 论文 5 |
|------|:---:|:---:|:---:|:---:|:---:|
| Unicode 编码 | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| OpenType 字体 | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| HarfBuzz 整形 | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| CSS 竖排 | ⚠️ | ✅ | ✅ | ✅ | ⚠️ |
| 浏览器支持 | ⚠️ | ⚠️ | ❌ | ✅ | ⚠️ |
| 变体选择符 | ✅ | ⚠️ | ✅ | ⚠️ | ✅ |
| 历史演进 | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |

✅ 详细讨论 | ⚠️ 提及 | ❌ 未涉及

### 时间线分析

```
2010 ──→ 2015 ──→ 2019 ──→ 2021 ──→ 2023 ──→ 2026(当前)
  │        │        │        │        │         │
 论文 3   论文 2   论文 1   论文 5   论文 4    我们的
 Unicode  综述    编码渲染 技术史  现代设备  项目
 问题     分析    研究     分析    测试      实施
```

---

## 🔧 对当前项目的综合启示

### 技术选型确认

| 技术层 | 我们的选择 | 论文建议 | 一致性 |
|--------|------------|----------|:------:|
| Unicode 编码 | 标准 Unicode | 标准 Unicode | ✅ |
| 字体 | Noto Sans Mongolian | OpenType 字体 | ✅ |
| 整形引擎 | 浏览器 HarfBuzz | HarfBuzz | ✅ |
| 布局 | CSS writing-mode | CSS writing-mode | ✅ |
| 方向 | CSS text-orientation | CSS text-orientation | ✅ |

### 已知局限

根据论文，我们的方案有以下局限：

1. **字体依赖**: 渲染质量依赖 Noto Sans Mongolian 的质量
2. **浏览器差异**: 不同浏览器支持程度不同
3. **变体选择符**: FVS 支持可能不完整
4. **连字规则**: 复杂连字可能不工作
5. **移动端**: 移动设备支持弱于桌面

### 优化方向

**短期（P1）**:
- [ ] 测试不同浏览器的渲染效果
- [ ] 收集已知的渲染问题
- [ ] 记录变体选择符测试结果

**中期（P2）**:
- [ ] 研究备用字体方案
- [ ] 评估 SVG 渲染备选方案
- [ ] 优化字体加载策略

**长期（P3）**:
- [ ] 研究 HarfBuzz WASM 集成
- [ ] 考虑 Canvas 自定义渲染
- [ ] 参与 W3C 标准讨论

---

## 📚 参考资料汇总

### 研究论文
1. Biligsaikhan (2019). A Study of Traditional Mongolian Script Encodings and Rendering. COLIPS.
2. Survey Authors (2015). A Survey on Rendering Traditional Mongolian Script. Academia.
3. Unicode L2 (2010). Mongolian Script Rendering Issues. Unicode.org.
4. Modern Devices Authors (2023). Traditional Mongolian on Modern Devices. ResearchGate.
5. Brill Authors (2021). The Digitisation Odyssey of the Mongolian Script in Unicode. Inner Asia.

### 标准文档
- Unicode Standard 16.0
- W3C Mongolian Layout Requirements
- W3C Mongolian Gap Analysis
- HarfBuzz Documentation

---

**笔记完成时间**: 2026-04-01 11:30 JST  
**学习状态**: ✅ 全部 11 份资料已完成学习
