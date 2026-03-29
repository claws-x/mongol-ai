# 传统蒙古文竖排显示算法研究

## 一、问题定义

**核心问题**：如何在 Web 浏览器中正确显示传统蒙古文竖排文本？

**需求**：
1. 从上到下书写
2. 列从左到右排列
3. 保持蒙古文字符的正确形态（词首、词中、词尾）
4. 支持手写体字体
5. 跨浏览器兼容（Chrome、Firefox、Safari）

---

## 二、传统蒙古文文字特性研究

### 2.1 文字基本特征

1. **书写方向**：
   - 垂直方向：从上到下
   - 水平方向：列从左到右

2. **字符形态**：
   - 词首形式（Initial form）
   - 词中形式（Medial form）
   - 词尾形式（Final form）
   - 独立形式（Isolated form）

3. **连写特性**：
   - 传统蒙古文是连写文字
   - 字符之间通过连接符连接
   - 形态根据位置自动变化

### 2.2 Unicode 编码

- **编码范围**：U+1800 - U+18AF
- **编码标准**：Unicode Mongolian block
- **问题**：Unicode 编码不区分词首/词中/词尾形态，需要字体和渲染引擎处理

---

## 三、现有技术方案调研

### 3.1 CSS Writing Modes 方案

**标准**：W3C CSS Writing Modes Level 3

```css
writing-mode: vertical-lr;
text-orientation: sideways;
```

**优点**：
- 标准化方案
- 浏览器原生支持

**缺点**：
- WebKit 需要额外设置
- 对蒙古文连写支持不完整
- 字体依赖性强

### 3.2 字体渲染方案

**字体**：
- Mongolian Baiti（Windows 自带）
- Noto Sans Mongolian（Google）
- Mongolian Usug（手写体）

**问题**：
- 不同字体渲染效果不同
- 部分字体不支持竖排
- 词形变化依赖字体

### 3.3 JavaScript 渲染方案

**思路**：使用 Canvas 或 SVG 手动渲染每个字符

**优点**：
- 完全控制渲染过程
- 可以处理特殊形态

**缺点**：
- 性能问题
- 文本选择困难
- 可访问性差

---

## 四、我们的算法设计

### 4.1 核心思想

**"三层渲染架构"**：

```
┌─────────────────────────────────┐
│   应用层：蒙古文 AI 助手          │
├─────────────────────────────────┤
│   渲染层：MongolianLayoutEngine │
├─────────────────────────────────┤
│   基础层：Browser + Font        │
└─────────────────────────────────┘
```

### 4.2 MongolianLayoutEngine 算法

```javascript
class MongolianLayoutEngine {
    // 1. 文本分析
    analyzeText(text) {
        // 识别词边界
        // 识别每个字符的位置（词首/词中/词尾）
        // 生成形态映射表
    }
    
    // 2. 布局计算
    calculateLayout(text, containerWidth) {
        // 计算每列高度
        // 计算列间距
        // 生成布局树
    }
    
    // 3. 渲染优化
    optimizeRendering() {
        // 懒加载长文本
        // 缓存已渲染内容
        // 预加载字体
    }
}
```

### 4.3 自适应浏览器策略

```javascript
function getOptimalCSS(browser) {
    const strategies = {
        'webkit': {
            'writing-mode': 'vertical-lr',
            'text-orientation': 'sideways',
            'font-feature-settings': '"mong"'
        },
        'gecko': {
            'writing-mode': 'vertical-lr',
            'text-orientation': 'mixed'
        },
        'blink': {
            'writing-mode': 'vertical-lr',
            'text-orientation': 'upright'
        }
    };
    
    return strategies[browser] || strategies['blink'];
}
```

### 4.4 字体回退链

```css
font-family: 
    'Mongolian Usug',           /* 首选：手写体 */
    'Mongolian Baiti',          /* 备选：印刷体 */
    'Noto Sans Mongolian',      /* 备选：Google 字体 */
    'Microsoft Uighur',         /* 备选：系统字体 */
    sans-serif;                 /* 最后回退 */
```

---

## 五、创新点

### 5.1 智能词形识别算法

```javascript
function identifyGlyphForm(char, position, prevChar, nextChar) {
    // 基于上下文识别字符形态
    // 考虑前一个字符和后一个字符
    // 返回正确的字形变体
}
```

### 5.2 动态列宽调整

```javascript
function adjustColumnWidth(text, maxWidth) {
    // 根据文本长度动态调整列宽
    // 保持视觉平衡
    // 避免过长的列
}
```

### 5.3 跨浏览器兼容层

```javascript
class BrowserCompatLayer {
    detectBrowser() {
        // 检测浏览器类型和版本
    }
    
    applyOptimalStyles() {
        // 应用最适合当前浏览器的样式
    }
    
    fallbackIfNeeded() {
        // 必要时使用回退方案
    }
}
```

---

## 六、测试计划

### 6.1 功能测试

- [ ] 基础竖排显示
- [ ] 词形变化正确
- [ ] 连写效果正确
- [ ] 手写体显示
- [ ] 印刷体显示

### 6.2 兼容性测试

- [ ] Chrome (Blink)
- [ ] Firefox (Gecko)
- [ ] Safari (WebKit)
- [ ] Edge (Blink)

### 6.3 性能测试

- [ ] 短文本（<100 字符）
- [ ] 中文本（100-1000 字符）
- [ ] 长文本（>1000 字符）
- [ ] 滚动性能

---

## 七、下一步行动

1. **实现 MongolianLayoutEngine 核心算法**
2. **创建浏览器检测模块**
3. **开发字体加载优化**
4. **编写测试用例**
5. **性能优化**

---

## 八、参考资料

1. W3C CSS Writing Modes: https://www.w3.org/TR/css-writing-modes-3/
2. Unicode Mongolian: https://unicode.org/charts/PDF/U1800.pdf
3. Onon 输入法文档：http://ime.onon.cn
4. 蒙古文排版需求：https://www.w3.org/TR/mlreq/

---

**版本**：v1.0  
**创建**：2026-03-30  
**作者**：OpenClaw Mongolian AI Team
