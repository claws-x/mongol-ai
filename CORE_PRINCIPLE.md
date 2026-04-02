# 🐎 蒙古文 AI 助手 - 核心宗旨

**版本**: v1.0  
**创建日期**: 2026-04-01  
**优先级**: 🔴 **最高优先级 (P0)**

---

## ⭐ 核心宗旨

> **蒙古文必须竖排显示，无论静态还是动态。**
> 
> **Traditional Mongolian text must be displayed vertically, whether static or dynamic.**

这是本项目的**核心遵旨**，所有技术决策、代码实现、功能设计都必须服从这一原则。

---

## 📋 竖排原则详解

### 1. 适用范围

| 场景 | 是否适用 | 说明 |
|------|----------|------|
| 静态文本展示 | ✅ **必须竖排** | SVG/CSS 均可 |
| 动态输入内容 | ✅ **必须竖排** | 推荐 CSS 方案 |
| 键盘按键字符 | ✅ **必须竖排** | 推荐 CSS 方案 |
| 聊天对话消息 | ✅ **必须竖排** | 推荐 CSS 方案 |
| 输入框内容 | ✅ **必须竖排** | 必须 CSS 方案 |
| 按钮标签 | ✅ **必须竖排** | SVG/CSS 均可 |
| 标题/标签 | ✅ **必须竖排** | SVG/CSS 均可 |
| 短语建议 | ✅ **必须竖排** | 推荐 CSS 方案 |
| 示例文本 | ✅ **必须竖排** | SVG/CSS 均可 |

**结论**: **所有蒙古文，100% 竖排，无例外。**

---

### 2. 技术方案

#### 方案 A: CSS 竖排（推荐用于动态内容）

```css
.mongolian-text {
    writing-mode: vertical-lr !important;
    text-orientation: upright !important;
    -webkit-writing-mode: vertical-lr !important;
    -webkit-text-orientation: upright !important;
}
```

**适用场景**:
- ✅ 输入框
- ✅ 键盘按键
- ✅ 聊天对话
- ✅ 动态内容
- ✅ 需要复制/粘贴的场景

**优点**:
- 原生文本支持
- 完整的输入/复制功能
- 响应式设计友好
- 性能优秀

---

#### 方案 B: SVG 竖排（推荐用于静态展示）

```svg
<text writing-mode="vertical-lr" text-orientation="upright">
    ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ
</text>
```

**适用场景**:
- ✅ Logo 和标题
- ✅ 静态文本展示
- ✅ 高质量打印输出
- ✅ 艺术设计
- ✅ 复杂图表中的文本

**优点**:
- 高质量矢量渲染
- 精确的布局控制
- 不依赖浏览器 CSS 支持
- 缩放不失真

---

### 3. 技术决策流程

```
需要显示蒙古文？
    ↓
是静态展示还是动态内容？
    ├─→ 静态展示 → 使用 SVG 方案 ✅
    └─→ 动态内容 → 使用 CSS 方案 ✅
    ↓
验证竖排效果
    ↓
确认字符方向正确（顶部朝左）
    ↓
完成 ✅
```

---

### 4. 验证标准

#### 视觉验证
- [ ] 蒙古文**从上到下**阅读
- [ ] 字符顶部朝向**左侧**
- [ ] 不需要歪头阅读
- [ ] 列从左到右排列

#### 技术验证
```javascript
// 检查 CSS 方案
const style = window.getComputedStyle(element);
if (style.writingMode !== 'vertical-lr') {
    console.error('❌ 违反竖排宗旨！');
}

// 检查 SVG 方案
const text = svgElement.querySelector('text');
if (text.getAttribute('writing-mode') !== 'vertical-lr') {
    console.error('❌ 违反竖排宗旨！');
}
```

---

### 5. 禁止事项

❌ **绝对禁止**的行为：

1. ❌ 使用横向显示蒙古文
2. ❌ 使用 `writing-mode: horizontal-tb`
3. ❌ 使用 `transform: rotate(90deg)` 代替竖排
4. ❌ 在未验证竖排效果的情况下发布
5. ❌ 为了性能/兼容性牺牲竖排效果

**违反后果**: 🔴 **严重错误，必须立即修复**

---

### 6. 代码审查清单

在提交任何代码前，必须检查：

#### HTML 审查
- [ ] 所有蒙古文元素是否应用了竖排类名
- [ ] 是否引用了 `mongolian-vertical.css`
- [ ] SVG 文本是否设置 `writing-mode="vertical-lr"`

#### CSS 审查
- [ ] 竖排样式是否使用 `!important`
- [ ] 是否包含 `-webkit-` 前缀
- [ ] `text-orientation` 是否设置为 `upright`

#### 功能审查
- [ ] 输入框是否竖排
- [ ] 键盘按键是否竖排
- [ ] 聊天消息是否竖排
- [ ] 所有蒙古文是否竖排

---

### 7. 测试要求

#### 必须测试的场景

| 场景 | 测试内容 | 通过标准 |
|------|----------|----------|
| 输入框 | 输入蒙古文 | 从上到下显示 |
| 键盘 | 点击按键 | 字符竖排显示 |
| 聊天 | 发送消息 | 消息竖排显示 |
| 短语 | 点击建议 | 插入竖排文本 |
| 复制 | 复制蒙古文 | 保持竖排格式 |
| 粘贴 | 粘贴蒙古文 | 竖排显示 |
| 打印 | 打印页面 | 保持竖排效果 |
| 移动端 | 手机浏览 | 竖排正常显示 |

---

### 8. 浏览器兼容性

#### 最低支持要求

| 浏览器 | 最低版本 | 竖排支持 |
|--------|----------|----------|
| Chrome | 110+ | ✅ 完全支持 |
| Firefox | 100+ | ✅ 完全支持 |
| Safari | 16+ | ✅ 完全支持 |
| Edge | 110+ | ✅ 完全支持 |
| iOS Safari | 16+ | ✅ 完全支持 |
| Android Chrome | 110+ | ✅ 完全支持 |

**注意**: 对于不支持竖排的旧浏览器，应显示友好提示。

---

### 9. 字体要求

#### 推荐字体

```css
font-family: 'Noto Sans Mongolian', 'Mongolian Baiti', 'Microsoft Mongolian Baiti', sans-serif;
```

#### 字体加载

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mongolian&display=swap" rel="stylesheet">
```

---

### 10. 违规处理

#### 违规等级

| 等级 | 描述 | 处理 |
|------|------|------|
| 🔴 P0 | 横向显示蒙古文 | 立即修复，阻止发布 |
| 🟠 P1 | 竖排但字符方向错误 | 尽快修复 |
| 🟡 P2 | 竖排但间距/布局问题 | 计划修复 |

#### 处理流程

```
发现违规
    ↓
记录问题（截图 + 代码位置）
    ↓
创建 Issue（标记为 P0）
    ↓
立即修复
    ↓
验证修复效果
    ↓
关闭 Issue
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `PROJECT_RULES.md` | 项目规则（包含 RULE-001） |
| `mongolian-vertical.css` | 竖排 CSS 样式表 |
| `VERTICAL_FIX_COMPLETE.md` | 竖排修复完整报告 |
| `IMPROVEMENT_PLAN.md` | 改善计划 |
| `learning/final-learning-report.md` | 技术学习报告 |

---

## ✅ 承诺

**本项目所有成员承诺**：

1. ✅ 所有蒙古文 100% 竖排显示
2. ✅ 不使用任何横向显示方案
3. ✅ 在代码审查中严格检查竖排效果
4. ✅ 在测试中验证所有蒙古文竖排
5. ✅ 发现违规立即修复

---

**核心宗旨不可违背！**

**蒙古文必须竖起来，无论静态还是动态！**

---

**创建时间**: 2026-04-01 12:15 JST  
**最后更新**: 2026-04-01 12:15 JST  
**下次审查**: 每次代码提交前
