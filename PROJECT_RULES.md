# 🐎 蒙古文 AI 助手项目规则

**版本**: v1.0  
**创建日期**: 2026-04-01  
**最后更新**: 2026-04-01

---

## ⚠️ 核心规则（必须遵守）

### 规则 1: 所有蒙古文必须竖排显示 🔝

**规则编号**: RULE-001  
**优先级**: 🔴 **最高优先级 (P0)**  
**违反后果**: 严重 - 不符合传统蒙古文书写规范

#### 规则描述
**所有蒙古文文本必须使用竖排显示，绝对不允许横向显示。**

传统蒙古文（回鹘式蒙古文）的书写方向是**从上到下，列从左到右**。这是蒙古文的本质特征，任何横向显示都是错误的。

#### 技术要求

**CSS 标准**:
```css
/* ✅ 正确 - 使用 W3C 标准竖排 */
.mongolian-text {
    writing-mode: vertical-lr;      /* 竖排，列从左到右 */
    text-orientation: upright;      /* 字符保持直立 */
    -webkit-writing-mode: vertical-lr;
    -webkit-text-orientation: upright;
}

/* ❌ 错误 - 禁止使用横向显示 */
.mongolian-text {
    writing-mode: horizontal-tb;    /* 禁止！ */
    text-orientation: sideways;     /* 禁止！ */
}

/* ❌ 错误 - 禁止使用 rotate 旋转 */
.mongolian-text {
    transform: rotate(90deg);       /* 禁止！这是临时方案 */
}
```

#### 适用范围

| 元素类型 | 是否适用 | 说明 |
|----------|----------|------|
| 输入框文本 | ✅ 必须 | 用户输入的蒙古文 |
| 键盘按键 | ✅ 必须 | 按键上的蒙古文字符 |
| 聊天消息 | ✅ 必须 | 对话中的蒙古文 |
| 按钮标签 | ✅ 必须 | 按钮上的蒙古文 |
| 标题/标签 | ✅ 必须 | 所有蒙古文标题 |
| 短语建议 | ✅ 必须 | 建议的蒙古文短语 |
| 示例文本 | ✅ 必须 | 示例中的蒙古文 |

#### 检查清单

在提交任何 HTML/CSS 更改前，必须检查：

- [ ] 所有蒙古文元素是否应用了 `writing-mode: vertical-lr`
- [ ] 是否包含 `-webkit-` 前缀以支持 Safari/Chrome
- [ ] 是否设置了 `text-orientation: upright`
- [ ] 是否**没有**使用 `transform: rotate()`
- [ ] 是否**没有**使用 `writing-mode: horizontal-tb`

#### 验证方法

**浏览器开发者工具检查**:
```javascript
// 在 Console 中运行，检查所有蒙古文元素
document.querySelectorAll('[lang="mn"], .mongolian, [class*="mongolian"]').forEach(el => {
    const style = window.getComputedStyle(el);
    if (style.writingMode !== 'vertical-lr') {
        console.error('❌ 违反竖排规则:', el);
    } else {
        console.log('✅ 符合竖排规则:', el);
    }
});
```

**视觉检查**:
- 蒙古文字符应该**从上到下**阅读
- 字符顶部应该朝向**左侧**
- 不应该需要歪头阅读

---

### 规则 2: 必须使用标准蒙古文字体

**规则编号**: RULE-002  
**优先级**: 🟠 高优先级 (P1)

#### 字体系列
```css
font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', 'Microsoft Mongolian Baiti', sans-serif;
```

#### 字体优先级
1. Mongolian Baiti (Windows 标准)
2. Noto Sans Mongolian (Google 字体，跨平台)
3. Microsoft Mongolian Baiti (备用)
4. sans-serif (最后备用)

---

### 规则 3: Unicode 范围必须正确

**规则编号**: RULE-003  
**优先级**: 🟠 高优先级 (P1)

#### 传统蒙古文 Unicode 范围
```
U+1800 - U+18AF  (蒙古文区块)
U+11660 - U+1167F (蒙古文补充)
```

#### 禁止事项
- ❌ 禁止使用西里尔字母代替传统蒙古文
- ❌ 禁止使用拉丁字母音译代替蒙古文
- ❌ 禁止使用图片代替文本蒙古文

---

### 规则 4: 输入框必须支持竖排

**规则编号**: RULE-004  
**优先级**: 🟠 高优先级 (P1)

#### 技术要求
```css
textarea.mongolian-input {
    writing-mode: vertical-lr;
    text-orientation: upright;
    font-family: 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
    min-height: 120px;
    line-height: 1.8;
}
```

#### 注意事项
- 输入框高度必须足够显示多列文本
- 必须支持自动换列
- 滚动条应该是**水平滚动**（因为列从左到右增加）

---

### 规则 5: 键盘布局必须符合蒙古文习惯

**规则编号**: RULE-005  
**优先级**: 🟡 中优先级 (P2)

#### 键盘分类
1. **元音键盘** (7 个): ᠠ ᠡ ᠢ ᠣ ᠤ ᠥ ᠦ
2. **辅音键盘 1** (7 个): ᠨ ᠪ ᠫ ᠬ ᠭ ᠮ ᠯ
3. **辅音键盘 2** (7 个): ᠰ ᠱ ᠲ ᠳ ᠴ ᠵ ᠶ
4. **辅音键盘 3** (7 个): ᠷ ᠸ ᠹ ᠺ ᠻ ᠼ ᠽ
5. **功能键盘**: 标点符号 + 控制键

#### 按键上的蒙古文
- ✅ 必须竖排显示
- ✅ 字体大小适中 (16-22px)
- ✅ 居中对齐

---

## 📋 代码审查清单

### HTML 审查
- [ ] 所有蒙古文元素是否有 `lang="mn"` 属性
- [ ] 所有蒙古文元素是否应用了竖排类名
- [ ] 是否引用了 `mongolian-vertical.css`

### CSS 审查
- [ ] 竖排样式是否使用 `!important` (防止被覆盖)
- [ ] 是否包含 `-webkit-` 前缀
- [ ] 是否没有冲突的横向样式

### JavaScript 审查
- [ ] 动态创建的元素是否应用了竖排类
- [ ] 输入处理是否正确处理蒙古文
- [ ] 是否没有破坏竖排的 DOM 操作

---

## 🔧 修复指南

### 发现横向蒙古文时的修复步骤

**步骤 1**: 识别问题元素
```bash
grep -rn "writing-mode: horizontal" *.html
grep -rn "transform: rotate" *.html
```

**步骤 2**: 添加/修改 CSS 类
```html
<!-- ❌ 修改前 -->
<span>ᠮᠣᠩᠭᠣᠯ</span>

<!-- ✅ 修改后 -->
<span class="mongolian-vertical">ᠮᠣᠩᠭᠣᠯ</span>
```

**步骤 3**: 验证修复
- 在浏览器中打开页面
- 确认蒙古文从上到下显示
- 使用开发者工具检查 computed style

---

## 📖 参考文档

- [W3C Mongolian Layout Requirements](https://www.w3.org/TR/mlreq/)
- [W3C Vertical Text](https://www.w3.org/International/articles/vertical-text/)
- [Unicode Mongolian Block](https://unicode.org/charts/PDF/U1800.pdf)

---

## ⚖️ 违规处理

### P0 违规 (规则 1)
- 🔴 立即修复
- 🔴 阻止发布
- 🔴 需要代码审查

### P1 违规 (规则 2-4)
- 🟠 尽快修复
- 🟠 记录在案
- 🟠 下次发布前修复

### P2 违规 (规则 5)
- 🟡 计划修复
- 🟡 可延后处理

---

**所有项目成员必须遵守以上规则。**  
**违反规则 1 (竖排显示) 是零容忍的严重问题。**
