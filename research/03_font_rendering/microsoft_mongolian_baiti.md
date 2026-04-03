# Microsoft Mongolian Baiti 字体分析

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [字体历史](#字体历史)
3. [技术规格](#技术规格)
4. [字形覆盖](#字形覆盖)
5. [渲染特性](#渲染特性)
6. [平台支持](#平台支持)
7. [与 Noto 对比](#与 noto 对比)
8. [使用场景](#使用场景)
9. [已知问题](#已知问题)
10. [测试报告](#测试报告)
11. [参考资料](#参考资料)
12. [交叉引用](#交叉引用)

---

## 概述

### 什么是 Microsoft Mongolian Baiti

Microsoft Mongolian Baiti 是微软公司开发的传统蒙古文字体，随 Windows Vista 及后续版本一起分发。作为最早广泛可用的蒙古文字体之一，它在蒙古文数字化早期发挥了重要作用。

### 字体地位

| 维度 | 描述 |
|------|------|
| **历史地位** | 首个大规模分发的蒙古文字体 |
| **普及程度** | Windows 用户默认拥有 |
| **当前状态** | 维护停滞，被 Noto 超越 |
| **推荐使用** | 仅作为后备字体 |

### 基本信息

| 属性 | 值 |
|------|-----|
| **字体家族** | Mongolian Baiti |
| **开发商** | Microsoft Corporation |
| **首次发布** | 2006 (Windows Vista) |
| **许可** | 微软专有字体许可 |
| **格式** | TTF |
| **字重** | Regular |
| **文件体积** | ~200KB |

---

## 字体历史

### 发展时间线

```
2006 年:
  └─ Windows Vista 发布，首次包含 Mongolian Baiti
     └─ 蒙古文 Unicode 支持初步实现

2007 年:
  └─ Windows XP SP3 提供可选安装

2009 年:
  └─ Windows 7 预装

2012 年:
  └─ Windows 8 预装
     └─ 渲染引擎改进

2015 年:
  └─ Windows 10 预装
     └─ 最后重大更新

2020 年:
  └─ 维护基本停滞
     └─ 用户转向 Noto Sans Mongolian

2023 年:
  └─ 仍包含在 Windows 11 中
     └─ 作为兼容性后备字体
```

### 设计背景

Mongolian Baiti 的设计目标：
1. 为 Windows 用户提供基本蒙古文支持
2. 覆盖蒙古文 Unicode 核心区块
3. 支持基本的连写和位置变体
4. 与 Windows 渲染引擎深度集成

**设计限制**:
- 发布时蒙古文 Unicode 标准尚未完全成熟
- 早期 HarfBuzz 等开源渲染引擎尚未普及
- 主要面向 Windows 平台，跨平台考虑有限

---

## 技术规格

### 字体度量

```
Family Name:        Mongolian Baiti
Style Name:         Regular
Version:            1.00
Units Per Em:       2048
Ascender:           1806
Descender:          -474
Line Gap:           0
X Height:           ~1024
Cap Height:         ~1434
```

### 字符映射

| Unicode 区块 | 覆盖率 | 备注 |
|-------------|--------|------|
| U+1800–U+18AF (Mongolian) | ~95% | 核心区块基本覆盖 |
| U+11660–U+1167F (Mongolian Supplement) | ~50% | 部分覆盖 |
| U+0020–U+007F (Basic Latin) | 100% | 完全覆盖 |

### 文件信息

```
文件名：MONGOLIA.TTF
文件大小：约 200KB
创建工具：Microsoft 内部工具
嵌入权限：可编辑安装
子集化：不允许
```

---

## 字形覆盖

### 字母覆盖

**元音字母** (U+1820–U+1826):

| 字符 | Unicode | 名称 | 支持 |
|------|---------|------|------|
| ᠠ | U+1820 | a | ✅ |
| ᠡ | U+1821 | e | ✅ |
| ᠢ | U+1822 | i | ✅ |
| ᠣ | U+1823 | o | ✅ |
| ᠤ | U+1824 | u | ✅ |
| ᠥ | U+1825 | ö | ✅ |
| ᠦ | U+1826 | ü | ✅ |

**辅音字母** (部分):

| 字符 | Unicode | 名称 | 支持 |
|------|---------|------|------|
| ᠭ | U+182D | ga | ✅ |
| ᠬ | U+182E | ka | ✅ |
| ᠯ | U+182F | la | ✅ |
| ᠮ | U+1830 | ma | ✅ |
| ᠨ | U+1831 | na | ✅ |
| ᠪ | U+1834 | ba | ✅ |
| ᠫ | U+1835 | pa | ✅ |
| ᠰ | U+1830 | sha | ✅ |
| ᠲ | U+1832 | ta | ✅ |

### 数字覆盖

| 字符 | Unicode | 支持 |
|------|---------|------|
| ᠐ | U+1810 | ✅ |
| ᠑ | U+1811 | ✅ |
| ᠒ | U+1812 | ✅ |
| ᠓ | U+1813 | ✅ |
| ᠔ | U+1814 | ✅ |
| ᠕ | U+1815 | ✅ |
| ᠖ | U+1816 | ✅ |
| ᠗ | U+1817 | ✅ |
| ᠘ | U+1818 | ✅ |
| ᠙ | U+1819 | ✅ |

### 标点符号

| 字符 | Unicode | 名称 | 支持 |
|------|---------|------|------|
| ᠀ | U+1800 | Hyphen | ✅ |
| ᠁ | U+1801 | En Dash | ✅ |
| ᠂ | U+1802 | Comma | ✅ |
| ᠃ | U+1803 | Full Stop | ✅ |
| ᠄ | U+1804 | Colon | ✅ |
| ᠅ | U+1805 | Four Dots | ✅ |
| ᠆ | U+1806 | Todo Mark | ✅ |

### FVS 支持

| 选择器 | Unicode | 支持程度 |
|--------|---------|----------|
| FVS1 | U+180B | ⚠️ 部分 |
| FVS2 | U+180C | ⚠️ 部分 |
| FVS3 | U+180D | ⚠️ 部分 |
| MVS | U+180E | ✅ 支持 |

**注意**: Mongolian Baiti 的 FVS 支持不完整，某些变体序列可能无法正确渲染。

---

## 渲染特性

### OpenType 特性

| 特性 | 支持 | 说明 |
|------|------|------|
| `init` | ✅ | 词首形式 |
| `medi` | ✅ | 词中形式 |
| `fina` | ✅ | 词尾形式 |
| `isol` | ✅ | 独立形式 |
| `calt` | ⚠️ | 有限的上下文替代 |
| `liga` | ⚠️ | 基本连字 |
| `rlig` | ✅ | 必需连字 |
| `ccmp` | ✅ | 字形组合 |
| `mark` | ⚠️ | 部分标记定位 |
| `mkmk` | ❌ | 不支持 |

### 连写规则

Mongolian Baiti 实现了基本连写规则：

```
常见连写:
- ga + a → 连写形式
- ma + i → 连写形式
- na + u → 连写形式

连写质量:
- 基本连写：✅ 良好
- 复杂连写：⚠️ 偶有问题
- 三字母以上：⚠️ 可能断裂
```

### 位置变体

| 位置 | 支持 | 质量 |
|------|------|------|
| 独立 | ✅ | 良好 |
| 词首 | ✅ | 良好 |
| 词中 | ✅ | 良好 |
| 词尾 | ✅ | 良好 |

**特殊情况**:
- 词尾 n 的长尾/短尾：⚠️ 需要 FVS 区分
- 词尾 b 的特殊形式：✅ 自动处理
- 双写字母：⚠️ 偶有渲染问题

---

## 平台支持

### Windows

| 版本 | 支持状态 | 备注 |
|------|----------|------|
| Windows Vista | ✅ 预装 | 首次引入 |
| Windows 7 | ✅ 预装 | 渲染改进 |
| Windows 8 | ✅ 预装 | 与 Vista 相似 |
| Windows 8.1 | ✅ 预装 | 与 8 相似 |
| Windows 10 | ✅ 预装 | 最后更新 |
| Windows 11 | ✅ 预装 | 兼容性支持 |

### macOS

| 状态 | 说明 |
|------|------|
| ❌ 不预装 | macOS 不包含 Mongolian Baiti |
| ⚠️ 可手动安装 | 可从 Windows 复制字体文件 |
| ⚠️ 渲染差异 | macOS Core Text 渲染可能与 Windows 不同 |

### Linux

| 状态 | 说明 |
|------|------|
| ❌ 不预装 | 大多数 Linux 发行版不包含 |
| ⚠️ 可手动安装 | 需手动复制字体文件 |
| ⚠️ 许可限制 | 专有字体，分发受限 |

### 移动端

| 平台 | 支持 |
|------|------|
| iOS | ❌ 不支持 |
| Android | ❌ 不支持 |
| Windows Mobile | ✅ 曾支持 (已停产) |

---

## 与 Noto 对比

### 综合对比表

| 特性 | Mongolian Baiti | Noto Sans Mongolian | 胜出 |
|------|-----------------|---------------------|------|
| **许可** | 专有 | OFL 开源 | Noto |
| **跨平台** | Windows only | 全平台 | Noto |
| **Unicode 覆盖** | ~95% | 100% | Noto |
| **FVS 支持** | 部分 | 完全 | Noto |
| **渲染质量** | 良好 | 优秀 | Noto |
| **字重选择** | 1 种 | 2 种 | Noto |
| **文件大小** | ~200KB | ~150KB | Noto |
| **维护状态** | 停滞 | 活跃 | Noto |
| **Web 支持** | 有限 | 优秀 | Noto |
| **默认安装** | Windows | 需下载 | Baiti |

### 渲染质量对比

**测试文本**:
```
ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃
```

| 评估项 | Mongolian Baiti | Noto Sans Mongolian |
|--------|-----------------|---------------------|
| 字符完整性 | ✅ | ✅ |
| 连写流畅度 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 字形美观度 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| FVS 渲染 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 竖排支持 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 何时使用 Mongolian Baiti

**推荐使用场景**:
- Windows 桌面应用，需要零字体依赖
- 内部系统，用户均为 Windows
- 向后兼容旧文档
- 快速原型，不关心跨平台

**不推荐使用场景**:
- Web 应用
- 跨平台应用
- 移动端应用
- 需要高质量渲染的场景
- 需要 FVS 完整支持的场景

---

## 使用场景

### Windows 桌面应用

```csharp
// WPF 示例
<TextBlock FontFamily="Mongolian Baiti" FontSize="24">
  ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ
</TextBlock>

// WinForms 示例
label1.Font = new Font("Mongolian Baiti", 24F);
label1.Text = "ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ";
```

### CSS 后备字体

```css
.mongolian-text {
  font-family: 'Noto Sans Mongolian', 'Mongolian Baiti', sans-serif;
}
```

**说明**: 将 Mongolian Baiti 作为 Noto 的后备，在 Noto 不可用时回退。

### 文档兼容性

```xml
<!-- Word 文档字体声明 -->
<w:rFonts w:ascii="Mongolian Baiti" w:hAnsi="Mongolian Baiti"/>
```

---

## 已知问题

### 问题 1: FVS 渲染不完整

**描述**: 某些 FVS 变体序列无法正确渲染

**影响**: 需要特定字形变体的文本显示错误

**解决**: 使用 Noto Sans Mongolian 替代

### 问题 2: 复杂连写断裂

**描述**: 三字母以上的复杂连写可能断裂

**示例**:
```
ᠮᠣᠩᠭᠣᠯᠤᠨ (monggol-un) - 可能断裂
```

**解决**: 简化文本或使用 Noto

### 问题 3: macOS 渲染差异

**描述**: 在 macOS 上手动安装后，渲染质量下降

**原因**: macOS Core Text 与 Windows Uniscribe 渲染引擎差异

**解决**: 在 macOS 上使用 Noto Sans Mongolian

### 问题 4: 竖排支持有限

**描述**: 竖排时某些字形方向不正确

**影响**: 需要 CSS text-orientation 修正

**解决**: 
```css
.mongolian-vertical {
  writing-mode: vertical-lr;
  text-orientation: upright;
  font-family: 'Noto Sans Mongolian', 'Mongolian Baiti', sans-serif;
}
```

### 问题 5: 无 Bold 字重

**描述**: 仅提供 Regular 字重

**影响**: 无法显示粗体文本

**解决**: 
```css
/* 使用 text-shadow 模拟粗体 (不推荐) */
.mongolian-bold {
  font-family: 'Mongolian Baiti';
  text-shadow: 1px 0 0 currentColor;
}

/* 或使用 Noto Sans Mongolian Bold */
.mongolian-bold {
  font-family: 'Noto Sans Mongolian';
  font-weight: 700;
}
```

---

## 测试报告

### 测试环境

| 环境 |