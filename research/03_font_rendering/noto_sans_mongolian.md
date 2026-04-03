# Noto Sans Mongolian 字体深度分析

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [字体基本信息](#字体基本信息)
3. [字形覆盖范围](#字形覆盖范围)
4. [技术特性](#技术特性)
5. [渲染质量分析](#渲染质量分析)
6. [与其他字体对比](#与其他字体对比)
7. [Web 使用方案](#web 使用方案)
8. [性能优化](#性能优化)
9. [已知问题](#已知问题)
10. [测试用例](#测试用例)
11. [参考资料](#参考资料)
12. [交叉引用](#交叉引用)

---

## 概述

### 什么是 Noto Sans Mongolian

Noto Sans Mongolian 是 Google Noto 字体家族的一部分，专为传统蒙古文设计的开源字体。Noto 项目的目标是"没有豆腐"（No Tofu），即为所有 Unicode 字符提供高质量字体支持，避免显示缺失字符时的方框（□）。

### 为什么选择 Noto Sans Mongolian

| 优势 | 描述 | 重要性 |
|------|------|--------|
| **开源免费** | Apache 2.0 许可，可自由使用 | ⭐⭐⭐⭐⭐ |
| **Unicode 覆盖** | 完整支持蒙古文 Unicode 区块 | ⭐⭐⭐⭐⭐ |
| **跨平台一致** | Windows/macOS/Linux 渲染一致 | ⭐⭐⭐⭐⭐ |
| **高质量设计** | 专业字体设计师设计 | ⭐⭐⭐⭐ |
| **持续更新** | Google 持续维护更新 | ⭐⭐⭐⭐ |
| **Web 优化** | 提供 Web Font 版本 | ⭐⭐⭐⭐ |

### 字体获取

**官方下载**:
- Google Fonts: https://fonts.google.com/noto/specimen/Noto+Sans+Mongolian
- GitHub: https://github.com/googlefonts/noto-fonts
- Noto 项目: https://www.google.com/get/noto/

**版本信息**:
- 当前版本：2.001 (2023)
- 许可：SIL Open Font License 1.1
- 格式：TTF, OTF, WOFF, WOFF2

---

## 字体基本信息

### 技术规格

| 属性 | 值 |
|------|-----|
| **字体家族** | Noto Sans Mongolian |
| **设计师** | Google Noto Team |
| **发布年份** | 2016 (初版), 2023 (最新版) |
| **许可** | SIL Open Font License 1.1 |
| **格式** | TTF, OTF, WOFF, WOFF2 |
| **字重** | Regular (400), Bold (700) |
| **字形数量** | 256+ |
| **Unicode 版本** | 15.0 |
| **文件体积** | TTF: ~150KB, WOFF2: ~80KB |

### 字重与变体

```
Noto Sans Mongolian/
├── Regular (400)          - 标准字重
├── Bold (700)             - 粗体
└── Variable (未来)         - 可变字体 (计划中)
```

**注意**: 目前 Noto Sans Mongolian 仅提供 Regular 和 Bold 两种字重，缺少 Light、Medium、Black 等中间字重。

### 度量信息

```
Ascender:         1069
Descender:        -293
Line Gap:         0
Units Per Em:     1000
X Height:         500 (约)
Cap Height:       700 (约)
```

---

## 字形覆盖范围

### Unicode 区块支持

Noto Sans Mongolian 覆盖以下 Unicode 区块：

| Unicode 区块 | 范围 | 覆盖度 | 说明 |
|-------------|------|--------|------|
| **Mongolian** | U+1800–U+18AF | ✅ 100% | 传统蒙古文核心区块 |
| **Mongolian Supplement** | U+11660–U+1167F | ✅ 100% | 蒙古文补充区块 |
| **Basic Latin** | U+0020–U+007F | ✅ 100% | 拉丁字母、数字、标点 |

### 蒙古文字符覆盖

**字母表覆盖** (U+1820–U+1842):

```
✅ 元音字母 (7 个):
   U+1820 ᠠ a
   U+1821 ᠡ e
   U+1822 ᠢ i
   U+1823 ᠣ o
   U+1824 ᠤ u
   U+1825 ᠥ ö
   U+1826 ᠦ ü

✅ 辅音字母 (约 20 个):
   U+182D ᠭ ga
   U+182E ᠬ ka
   U+182F ᠯ la
   U+1830 ᠮ ma
   U+1831 ᠨ na
   U+1834 ᠪ ba
   U+1835 ᠫ pa
   U+1836 ᠬ qa
   ... (完整覆盖)

✅ 数字 (U+1810–U+1819):
   ᠐ ᠑ ᠒ ᠓ ᠔ ᠕ ᠖ ᠗ ᠘ ᠙ (0-9)

✅ 标点符号 (U+1800–U+180A):
   ᠀ ᠁ ᠂ ᠃ ᠄ ᠅ ᠆ ᠇ ᠈ ᠉

✅ 控制字符 (FVS):
   U+180B FVS1
   U+180C FVS2
   U+180D FVS3
   U+180E MVS
```

### 缺失字符

目前 Noto Sans Mongolian 的覆盖已经相当完整，但以下字符可能需要注意：

| 字符 | Unicode | 状态 | 备注 |
|------|---------|------|------|
| 一些历史变体 | U+18B0+ | ⚠️ 部分 | 古蒙古文变体 |
| 托忒文 | U+18B0–U+18FF | ⚠️ 部分 | 西蒙古文 |
| 阿礼噶礼 | U+18B0+ | ❌ 缺失 | 藏文转写系统 |

---

## 技术特性

### OpenType 特性

Noto Sans Mongolian 支持以下 OpenType 特性：

```
特性标签          描述                   蒙古文应用
-----------------------------------------------------------------
ccmp              字形组合/分解          ✅ 用于连写
liga              标准连字               ✅ 用于常见连写
rlig              必需连字               ✅ 用于位置变体
calt              上下文替代             ✅ 用于词中位置
locl              本地化形式             ⚠️ 有限支持
mark              标记定位               ✅ 用于附加符号
mkmk              标记到标记定位         ✅ 用于多层标记
```

### 字形变体支持

蒙古文的一个关键特性是字形根据位置变化（词首、词中、词尾、独立）：

```
位置类型          说明                    Noto 支持
-----------------------------------------------------------------
独立形式          单字母词                ✅ 完全支持
词首形式          单词开头的字母          ✅ 完全支持
词中形式          单词中间的字母          ✅ 完全支持
词尾形式          单词结尾的字母          ✅ 完全支持
```

**示例**: 字母 "ga" (ᠭ) 的不同位置形式

```
独立：ᠭ
词首：ᠭᠠ (ga)
词中：ᠠᠭᠠ (aga)
词尾：ᠠᠭ (ag)
```

### FVS (Free Variation Selector) 支持

Noto Sans Mongolian 支持 FVS 来选择特定字形变体：

```
基础字符 + FVS1 = 变体 1
基础字符 + FVS2 = 变体 2
基础字符 + FVS3 = 变体 3

示例:
ᠭᠠ (ga) - 标准形式
ᠭ︀ᠠ (ga+FVS1) - 变体 1
ᠭ︁ᠠ (ga+FVS2) - 变体 2
```

**注意**: FVS 的正确渲染需要字体和渲染引擎的共同支持。

---

## 渲染质量分析

### 桌面浏览器渲染

| 浏览器 | 渲染引擎 | 质量评分 | 备注 |
|--------|----------|----------|------|
| Chrome | Blink/HarfBuzz | ⭐⭐⭐⭐⭐ | 优秀，连写正确 |
| Firefox | Gecko/HarfBuzz | ⭐⭐⭐⭐⭐ | 优秀，与 Chrome 相似 |
| Safari | Core Text | ⭐⭐⭐⭐ | 良好，偶有连写问题 |
| Edge | Blink/HarfBuzz | ⭐⭐⭐⭐⭐ | 与 Chrome 一致 |

### 移动端渲染

| 平台 | 浏览器 | 渲染质量 | 备注 |
|------|--------|----------|------|
| iOS 14+ | Safari | ⭐⭐⭐⭐ | 良好，字体加载快 |
| Android 8+ | Chrome | ⭐⭐⭐⭐⭐ | 优秀 |
| Android 8+ | Samsung Internet | ⭐⭐⭐⭐ | 良好 |

### 渲染测试

**测试文本**:
```
ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃
```

**检查项目**:
- [ ] 所有字符正确显示
- [ ] 连写正确（无断裂）
- [ ] 字形位置变体正确
- [ ] FVS 变体正确
- [ ] 标点符号位置正确
- [ ] 竖排时字符方向正确

---

## 与其他字体对比

### 对比 Microsoft Baiti

| 特性 | Noto Sans Mongolian | Microsoft Baiti | 胜出 |
|------|---------------------|-----------------|------|
| **许可** | OFL (开源) | 专有 | Noto |
| **跨平台** | 优秀 | Windows only | Noto |
| **字形数量** | 256+ | 200+ | Noto |
| **渲染质量** | 优秀 | 良好 | Noto |
| **Web 支持** | 优秀 | 有限 | Noto |
| **字重选择** | 2 种 | 1 种 | Noto |
| **文件大小** | ~150KB | ~200KB | Noto |
| **FVS 支持** | 完全 | 部分 | Noto |

**结论**: Noto Sans Mongolian 在各方面都优于 Microsoft Baiti，推荐作为首选字体。

### 对比 Mongolian Baiti

| 特性 | Noto Sans Mongolian | Mongolian Baiti | 胜出 |
|------|---------------------|-----------------|------|
| **Unicode 覆盖** | 完整 | 不完整 | Noto |
| **渲染质量** | 优秀 | 一般 | Noto |
| **维护状态** | 活跃 | 停滞 | Noto |
| **Web 优化** | 是 | 否 | Noto |

### 对比其他开源字体

| 字体 | 项目 | 状态 | 与 Noto 对比 |
|------|------|------|-------------|
| Noto Sans Mongolian | Google | ✅ 活跃 | 基准 |
| Mongol Usug | 社区项目 | ⚠️ 停滞 | Noto 更完整 |
| Free Mongolian | 社区项目 | ⚠️ 有限 | Noto 更专业 |

---

## Web 使用方案

### Google Fonts 嵌入

```html
<!DOCTYPE html>
<html lang="mn">
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mongolian:wght@400;700&display=swap" rel="stylesheet">
  <style>
    .mongolian-text {
      font-family: 'Noto Sans Mongolian', sans-serif;
      font-weight: 400;
    }
    .mongolian-bold {
      font-family: 'Noto Sans Mongolian', sans-serif;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <p class="mongolian-text">ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ</p>
  <p class="mongolian-bold">ᠮᠣᠩᠭᠣᠯ ᠠᠢ ᠲᠡᠭᠦᠰᠯᠡᠯ</p>
</body>
</html>
```

### 自托管方案

```css
@font-face {
  font-family: 'Noto Sans Mongolian';
  src: url('/fonts/NotoSansMongolian-Regular.woff2') format('woff2'),
       url('/fonts/NotoSansMongolian-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Noto Sans Mongolian';
  src: url('/fonts/NotoSansMongolian-Bold.woff2') format('woff2'),
       url('/fonts/NotoSansMongolian-Bold.woff') format('woff');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

.mongolian-text {
  font-family: 'Noto Sans Mongolian', sans-serif;
}
```

**文件下载**:
```bash
# 从 Google Fonts 下载
wget https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansMongolian/NotoSansMongolian-Regular.ttf
wget https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansMongolian/NotoSansMongolian-Bold.ttf

# 转换为 Web 字体格式
fonttools ttLib.woff2 compress NotoSansMongolian-Regular.ttf
fonttools ttLib.woff2 compress NotoSansMongolian-Bold.ttf
```

### 性能优化

```css
/* 使用 font-display: swap 避免 FOIT */
@font-face {
  font-family: 'Noto Sans Mongolian';
  src: url('NotoSansMongolian.woff2') format('woff2');
  font-display: swap;
}

/* 预加载关键字体 */
<link rel="preload" href="/fonts/NotoSansMongolian-Regular.woff2" as="font" type="font/woff2" crossorigin>

/* 使用 WOFF2 格式 (比 TTF 小 30-50%) */
```

---

## 性能优化

### 字体子集化

对于特定项目，可以创建字体子集以减少文件大小：

```bash
# 使用 pyftsubset 创建子集
pyftsubset NotoSansMongolian-Regular.ttf \
  --unicodes=U+1800-18AF,U+11660-1167F \
  --output-file=NotoSansMongolian-subset.woff2