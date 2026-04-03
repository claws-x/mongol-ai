# 浏览器兼容性测试

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [浏览器支持矩阵](#浏览器支持矩阵)
3. [核心功能兼容性](#核心功能兼容性)
4. [测试方法](#测试方法)
5. [已知问题](#已知问题)
6. [降级方案](#降级方案)
7. [自动化测试](#自动化测试)
8. [测试报告模板](#测试报告模板)
9. [参考资料](#参考资料)
10. [交叉引用](#交叉引用)

---

## 概述

### 测试目的

浏览器兼容性测试旨在确保传统蒙古文竖排功能在各种浏览器环境中能够正确显示和交互。由于蒙古文竖排依赖于 CSS Writing Modes 等现代 Web 标准，不同浏览器的实现差异可能影响用户体验。

### 测试范围

| 测试维度 | 描述 |
|----------|------|
| 桌面浏览器 | Chrome, Firefox, Safari, Edge |
| 移动浏览器 | iOS Safari, Android Chrome, Samsung Internet |
| 操作系统 | Windows, macOS, Linux, iOS, Android |
| 功能点 | 竖排渲染、字形显示、输入、混排 |

### 测试优先级

```
P0 (必须通过): 主流桌面浏览器竖排渲染
P1 (应该通过): 主流移动浏览器竖排渲染
P2 (建议通过): 旧版本浏览器降级显示
P3 (可选): 小众浏览器支持
```

---

## 浏览器支持矩阵

### 桌面浏览器

| 浏览器 | 最低版本 | writing-mode | text-orientation | 蒙古文渲染 | 综合评分 |
|--------|----------|--------------|------------------|------------|----------|
| **Chrome** | 48+ | ✅ 完全 | ✅ 完全 | ✅ 良好 | ⭐⭐⭐⭐⭐ |
| **Firefox** | 41+ | ✅ 完全 | ✅ 完全 | ✅ 良好 | ⭐⭐⭐⭐⭐ |
| **Safari** | 10+ | ✅ 完全 | ✅ 完全 | ✅ 优秀 | ⭐⭐⭐⭐⭐ |
| **Edge** | 12+ (EdgeHTML) | ✅ 完全 | ✅ 完全 | ✅ 良好 | ⭐⭐⭐⭐ |
| **Edge** | 79+ (Chromium) | ✅ 完全 | ✅ 完全 | ✅ 良好 | ⭐⭐⭐⭐⭐ |
| **Opera** | 35+ | ✅ 完全 | ✅ 完全 | ✅ 良好 | ⭐⭐⭐⭐ |
| **Brave** | 1.0+ | ✅ 完全 | ✅ 完全 | ✅ 良好 | ⭐⭐⭐⭐⭐ |

### 移动浏览器

| 浏览器 | 最低版本 | 平台 | writing-mode | text-orientation | 输入支持 | 综合评分 |
|--------|----------|------|--------------|------------------|----------|----------|
| **iOS Safari** | 10+ | iOS | ✅ 完全 | ✅ 完全 | ⚠️ 有限 | ⭐⭐⭐⭐ |
| **Android Chrome** | 48+ | Android | ✅ 完全 | ✅ 完全 | ⚠️ 有限 | ⭐⭐⭐⭐ |
| **Samsung Internet** | 5.0+ | Android | ✅ 完全 | ✅ 完全 | ⚠️ 有限 | ⭐⭐⭐ |
| **Firefox Mobile** | 41+ | Android | ✅ 完全 | ✅ 完全 | ❌ 无 | ⭐⭐⭐ |
| **Chrome iOS** | 48+ | iOS | ✅ 完全 | ✅ 完全 | ⚠️ 有限 | ⭐⭐⭐⭐ |

### 旧版本浏览器

| 浏览器 | 版本范围 | 支持情况 | 建议方案 |
|--------|----------|----------|----------|
| IE 11 | 全部 | ❌ 不支持 | 降级为横排 |
| Chrome | <48 | ❌ 不支持 | 降级为横排 |
| Firefox | <41 | ❌ 不支持 | 降级为横排 |
| Safari | <10 | ❌ 不支持 | 降级为横排 |
| Android Browser | 4.x | ❌ 不支持 | 降级为横排 |

---

## 核心功能兼容性

### 1. writing-mode: vertical-lr

**功能描述**: 竖排布局，从左到右

| 浏览器 | 支持状态 | 备注 |
|--------|----------|------|
| Chrome 48+ | ✅ 完全支持 | 无已知问题 |
| Firefox 41+ | ✅ 完全支持 | 无已知问题 |
| Safari 10+ | ✅ 完全支持 | 渲染质量优秀 |
| Edge 79+ | ✅ 完全支持 | Chromium 内核 |
| iOS Safari 10+ | ✅ 完全支持 | 与桌面 Safari 一致 |
| Android Chrome 48+ | ✅ 完全支持 | 与桌面 Chrome 一致 |

**测试代码**:
```html
<div style="writing-mode: vertical-lr; font-family: 'Noto Sans Mongolian';">
  ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ
</div>
```

**预期结果**: 文本从上到下排列，列从左到右排列

### 2. text-orientation: upright

**功能描述**: 字符直立方向（顶部朝左）

| 浏览器 | 支持状态 | 备注 |
|--------|----------|------|
| Chrome 48+ | ✅ 完全支持 | 蒙古文字符正确旋转 |
| Firefox 41+ | ✅ 完全支持 | 蒙古文字符正确旋转 |
| Safari 10+ | ✅ 完全支持 | 渲染质量最佳 |
| Edge 79+ | ✅ 完全支持 | 与 Chrome 一致 |
| iOS Safari 10+ | ✅ 完全支持 | 与桌面 Safari 一致 |

**测试代码**:
```html
<div style="writing-mode: vertical-lr; text-orientation: upright; font-family: 'Noto Sans Mongolian';">
  ᠮᠣᠩᠭᠣᠯ
</div>
```

**预期结果**: 蒙古文字符顶部朝左，保持直立

### 3. 蒙古文字体渲染

**测试字体**:
- Noto Sans Mongolian (Google)
- Microsoft Baiti (Windows 自带)
- Mongolian Baiti (旧版)

| 浏览器 | Noto Sans | Microsoft Baiti | 备注 |
|--------|-----------|-----------------|------|
| Chrome (Win) | ✅ 优秀 | ✅ 良好 | Noto 渲染更清晰 |
| Firefox (Win) | ✅ 优秀 | ✅ 良好 | 与 Chrome 相似 |
| Safari (macOS) | ✅ 优秀 | ❌ 无 | macOS 无 Baiti |
| Edge (Win) | ✅ 优秀 | ✅ 良好 | 与 Chrome 相似 |
| iOS Safari | ✅ 优秀 | ❌ 无 | 需嵌入字体 |
| Android Chrome | ✅ 优秀 | ❌ 无 | 需嵌入字体 |

**建议**: 使用 Web Fonts 嵌入 Noto Sans Mongolian 确保跨平台一致性

### 4. 输入框竖排

**功能描述**: `<input>` 和 `<textarea>` 的竖排支持

| 浏览器 | input 支持 | textarea 支持 | 备注 |
|--------|-----------|---------------|------|
| Chrome | ⚠️ 部分 | ⚠️ 部分 | 光标定位有问题 |
| Firefox | ⚠️ 部分 | ⚠️ 部分 | 滚动方向混乱 |
| Safari | ⚠️ 部分 | ⚠️ 部分 | 相对较好 |
| Edge | ⚠️ 部分 | ⚠️ 部分 | 与 Chrome 一致 |
| iOS Safari | ❌ 不支持 | ❌ 不支持 | 键盘遮挡 |
| Android Chrome | ❌ 不支持 | ❌ 不支持 | 键盘遮挡 |

**测试代码**:
```html
<input type="text" style="writing-mode: vertical-lr; font-family: 'Noto Sans Mongolian';" placeholder="ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ">
<textarea style="writing-mode: vertical-lr; font-family: 'Noto Sans Mongolian';" rows="5"></textarea>
```

**已知问题**:
- 光标位置不准确
- 虚拟键盘遮挡输入区域
- 滚动方向与预期不符
- 自动换行异常

### 5. 文本混排

**功能描述**: 蒙古文与拉丁文/数字混排

| 浏览器 | 蒙 - 拉混排 | 蒙 - 数混排 | 备注 |
|--------|-----------|-----------|------|
| Chrome | ✅ 良好 | ✅ 良好 | 方向切换正确 |
| Firefox | ✅ 良好 | ✅ 良好 | 与 Chrome 相似 |
| Safari | ✅ 优秀 | ✅ 优秀 | 渲染质量最佳 |
| Edge | ✅ 良好 | ✅ 良好 | 与 Chrome 一致 |

**测试代码**:
```html
<div style="writing-mode: vertical-lr; text-orientation: upright;">
  ᠮᠣᠩᠭᠣᠯ Unicode U+1820 ᠦᠰᠦᠭ 12345
</div>
```

---

## 测试方法

### 手动测试流程

#### 步骤 1: 准备测试环境

```bash
# 安装测试浏览器
# macOS
brew install --cask google-chrome firefox microsoft-edge

# Windows
# 手动下载各浏览器安装包

# 准备测试设备
# - Windows 10/11 PC
# - macOS PC
# - iPhone (iOS 14+)
# - Android Phone (Android 8+)
```

#### 步骤 2: 创建测试页面

```html
<!DOCTYPE html>
<html lang="mn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>蒙古文浏览器兼容性测试</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mongolian&display=swap" rel="stylesheet">
  <style>
    .test-section {
      margin: 20px;
      padding: 20px;
      border: 1px solid #ccc;
    }
    .vertical-text {
      writing-mode: vertical-lr;
      text-orientation: upright;
      font-family: 'Noto Sans Mongolian', sans-serif;
      font-size: 24px;
      line-height: 2;
    }
  </style>
</head>
<body>
  <h1>浏览器兼容性测试</h1>
  
  <div class="test-section">
    <h2>测试 1: 基础竖排</h2>
    <div class="vertical-text">
      ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ ᠪᠣᠯ ᠮᠣᠩᠭᠣᠯ ᠦᠨᠳᠦᠰᠦᠲᠡᠨ ᠦ ᠭᠡᠭᠦᠨ ᠦᠭᠡᠢ ᠡᠴᠦᠰ ᠬᠣᠶᠢᠭᠤᠷᠠᠳᠤ ᠦᠭᠡᠢ ᠪᠣᠯᠬᠤ ᠨᠢᠭᠡᠳᠦᠭᠰᠡᠨ ᠪᠡᠯᠭᠡ ᠮᠥᠴᠢᠨ ᠪᠢᠴᠢᠭ ᠦᠰᠦᠭ ᠮᠥᠨ ᠪᠣᠯᠤᠨ᠎ᠠ᠃
    </div>
  </div>
  
  <div class="test-section">
    <h2>测试 2: 混排</h2>
    <div class="vertical-text">
      ᠮᠣᠩᠭᠣᠯ Unicode U+1820 ᠦᠰᠦᠭ 12345
    </div>
  </div>
  
  <div class="test-section">
    <h2>测试 3: 输入框</h2>
    <input type="text" class="vertical-text" placeholder="ᠮᠣᠩᠭᠣᠯ ᠦᠰᠦᠭ">
  </div>
</body>
</html>
```

#### 步骤 3: 执行测试

1. 在各浏览器中打开测试页面
2. 检查竖排方向是否正确
3. 检查字形渲染是否清晰
4. 检查混排是否合理
5. 测试输入框功能
6. 记录问题和截图

#### 步骤 4: 记录结果

使用以下模板记录测试结果：

```markdown
## 测试结果 - [浏览器名称] [版本]

**测试日期**: YYYY-MM-DD  
**操作系统**: [OS 名称] [版本]  
**设备**: [设备型号]

### 通过项
- [ ] writing-mode: vertical-lr
- [ ] text-orientation: upright
- [ ] 字体渲染
- [ ] 混排显示

### 问题项
- [ ] 输入框竖排
- [ ] 其他：[描述]

### 截图
[附上截图]

### 备注
[其他观察]
```

### 自动化测试

#### 使用 Selenium

```python
# test_browser_compatibility.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_vertical_rendering(browser_name):
    """测试竖排渲染"""
    driver = getattr(webdriver, browser_name)()
    
    try:
        driver.get('file:///path/to/test_page.html')
        
        # 检查竖排元素是否存在
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'vertical-text'))
        )
        
        # 获取计算样式
        styles = driver.execute_script("""
            return window.getComputedStyle(arguments[0]);
        """, element)
        
        writing_mode = styles['writing-mode']
        text_orientation = styles['text-orientation']
        
        print(f"{browser_name}: writing-mode={writing_mode}, text-orientation={text_orientation}")
        
        assert writing_mode == 'vertical-lr', f"writing-mode 错误：{writing_mode}"
        assert text_orientation == 'upright', f"text-orientation 错误：{text_orientation}"
        
        print(f"✅ {browser_name} 测试通过")
        
    except Exception as e:
        print(f"❌ {browser_name} 测试失败：{e}")
    finally:
        driver.quit()

# 运行测试
for browser in ['Chrome', 'Firefox', 'Safari', 'Edge']:
    test_vertical_rendering(browser)
```

#### 使用 Playwright

```javascript
// test-compatibility.js
const { chromium, firefox, webkit } = require('playwright');

async function testBrowser(browserType, browserName) {
  const browser = await browserType.launch();
  const page = await browser.newPage();
  
  try {
    await page.goto('file:///path/to/test_page.html');
    
    // 检查样式
    const styles = await page.evaluate(() => {
      const element = document.querySelector('.vertical-text');
      const computed = window.getComputedStyle(element);
      return {
        writingMode: computed.writingMode,
        textOrientation: computed.textOrientation
      };
    });
    
    console.log(`${browserName}:`, styles);
    
    if (styles.writingMode === 'vertical-lr' && styles.textOrientation === 'upright') {
      console.log(`✅ ${browserName} 测试通过`);
    } else {
      console.log(`❌ ${browserName} 测试失败`);
    }
    
    // 截图
    await page.screenshot({ path: `${browserName}-screenshot.png` });
    
  } catch (error) {
    console.log(`❌ ${browserName} 测试失败：`, error);
  } finally {
    await browser.close();
  }
}

// 运行测试
(async () => {
  await testBrowser(chromium, 'Chrome');
  await testBrowser(firefox, 'Firefox');
  await testBrowser(webkit, 'Safari');
})();
```

---

## 已知问题

### 问题 1: 输入框光标定位错误

**影响浏览器**: Chrome, Firefox, Edge  
**严重程度**: 中  
**描述**: 在竖排输入框中，光标位置与实际输入位置不匹配

**临时解决方案**:
```css
input[type="text"], textarea {
  writing-mode: horizontal-tb;