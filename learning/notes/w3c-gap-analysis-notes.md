# 📖 W3C Mongolian Gap Analysis 学习笔记

**学习日期**: 2026-04-01  
**资料来源**: W3C Mongolian Gap Analysis  
**链接**: https://www.w3.org/TR/mong-gap/

---

## 🎯 核心要点

### 1. 什么是 Gap Analysis？

**定义**: Gap Analysis（缺口分析）不是讲"应该怎样"，而是专门分析**Web 与 eBook 中对传统蒙古文支持还差在哪里**。

**用途**:
- 识别 HTML/CSS/浏览器的实现缺口
- 判断"为什么写了 CSS 还是显示不对"
- 指导未来的标准制定和浏览器开发

---

### 2. 识别的主要缺口

#### 2.1 CSS 层面的缺口

| 缺口 ID | 问题描述 | 严重程度 | 浏览器支持 |
|---------|----------|----------|------------|
| G001 | `writing-mode: vertical-lr` 对蒙古文支持不完整 | 🔴 高 | ⚠️ 部分 |
| G002 | `text-orientation: upright` 在部分浏览器无效 | 🟠 中 | ⚠️ 部分 |
| G003 | 竖排时的字符间距控制不足 | 🟡 低 | ❌ 无 |
| G004 | 竖排时的连字处理缺失 | 🔴 高 | ❌ 无 |

#### 2.2 字体层面的缺口

| 缺口 ID | 问题描述 | 严重程度 |
|---------|----------|----------|
| G101 | 蒙古文 OpenType 字体稀少 | 🔴 高 |
| G102 | 字体变体选择符支持不一致 | 🟠 中 |
| G103 | 词首/词中/词尾变形规则不完整 | 🔴 高 |

#### 2.3 渲染引擎层面的缺口

| 缺口 ID | 问题描述 | 严重程度 |
|---------|----------|----------|
| G201 | HarfBuzz 对蒙古文支持有限 | 🟠 中 |
| G202 | 浏览器整形引擎不一致 | 🟠 中 |
| G203 | 变体选择符处理错误 | 🔴 高 |

---

### 3. 关键发现

#### 3.1 CSS 竖排的局限性

**W3C 明确指出**:
> `writing-mode: vertical-lr` 只控制**布局方向**，不处理**字符变形**和**连字**。

这意味着：
- ✅ CSS 可以让文本"从上到下"排列
- ❌ CSS 不能处理蒙古文的词首/词中/词尾变形
- ❌ CSS 不能处理蒙古文的连字规则
- ❌ CSS 不能处理变体选择符 (VS1, VS2, etc.)

#### 3.2 浏览器现实情况

**Chrome/Blink**:
- ✅ 支持基本 `writing-mode: vertical-lr`
- ⚠️ 蒙古文字符方向可能不正确
- ❌ 不处理蒙古文连字

**Firefox/Gecko**:
- ✅ 支持基本 `writing-mode: vertical-lr`
- ✅ 蒙古文支持相对较好
- ⚠️ 仍有连字问题

**Safari/WebKit**:
- ✅ 支持基本 `writing-mode: vertical-lr`
- ⚠️ 蒙古文测试较少
- ❌ 连字支持有限

---

### 4. 对当前项目的启示

#### 4.1 我们的问题定位

根据 Gap Analysis，我们的问题可能属于：

| 问题 | 缺口类型 | 解决方案 |
|------|----------|----------|
| 蒙古文躺着 | G001/G002 | ✅ CSS `!important` 强制竖排 |
| 字符方向错 | G002 | ✅ `text-orientation: upright` |
| 连字异常 | G104/G201 | ⏳ 需要字体/引擎支持 |
| 变体错误 | G102/G203 | ⏳ 需要 Unicode 层修复 |

#### 4.2 可行的解决方案

**短期（CSS 层）**:
- ✅ 强制 `writing-mode: vertical-lr !important`
- ✅ 强制 `text-orientation: upright !important`
- ✅ 使用 `-webkit-` 前缀

**中期（字体层）**:
- ⏳ 使用专业蒙古文 OpenType 字体
- ⏳ 确保字体支持词首/词中/词尾变形
- ⏳ 测试不同字体的渲染效果

**长期（引擎层）**:
- ⏳ 研究 HarfBuzz 集成
- ⏳ 考虑 Canvas/SVG 自定义渲染
- ⏳ 参与 W3C 标准制定

---

### 5. 行动计划

### P0 - 立即执行
- [x] 所有 `.key` 容器添加竖排 CSS
- [x] 所有 `.key-char` 添加竖排 CSS
- [x] 使用 `!important` 确保优先级

### P1 - 短期优化
- [ ] 测试 Chrome/Firefox/Safari 显示效果
- [ ] 收集浏览器兼容性数据
- [ ] 记录已知的渲染问题

### P2 - 中期研究
- [ ] 研究蒙古文 OpenType 字体
- [ ] 测试不同字体的渲染效果
- [ ] 考虑字体加载策略优化

### P3 - 长期规划
- [ ] 研究 HarfBuzz 集成方案
- [ ] 考虑 Canvas/SVG 备选方案
- [ ] 参与 W3C 蒙古文标准讨论

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| Mongolian Gap Analysis | https://www.w3.org/TR/mong-gap/ |
| Mongolian Layout Requirements | https://www.w3.org/TR/mlreq/ |
| Mongolian Script Resources | https://www.w3.org/International/mlreq/mong/ |

---

**笔记完成时间**: 2026-04-01 11:15 JST  
**下一步**: 学习 Unicode Standard 和 HarfBuzz 文档
