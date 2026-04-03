# 📋 蒙古文竖排修复检查清单

**参考标准**: 用户提供的正确竖排示例图片  
**修复日期**: 2026-04-01

---

## ✅ 正确的竖排标准

根据用户提供的示例，正确的传统蒙古文竖排应该是：

1. **从上到下**书写
2. **列从左到右**排列
3. 字符**垂直连贯**
4. 字符顶部朝向**左侧**

---

## 🔧 CSS 技术标准

```css
/* 必须使用以下 CSS 属性 */
.mongolian-text,
.key-char,
.mongolian-vertical {
    writing-mode: vertical-lr !important;      /* 竖排，列从左到右 */
    text-orientation: upright !important;       /* 字符保持直立 */
    -webkit-writing-mode: vertical-lr !important;
    -webkit-text-orientation: upright !important;
}
```

---

## 📁 文件修复状态

### HTML 文件

| 文件 | CSS 引用 | `.key-char` 类 | 竖排样式 | 状态 |
|------|----------|---------------|----------|------|
| `embedded-input.html` | ✅ | ✅ | ✅ | ✅ 已修复 |
| `demo_chat_keyboard_v3.html` | ✅ | ✅ | ✅ | ✅ 已修复 |
| `demo_ai_powered.html` | ✅ | ✅ | ✅ | ✅ 已修复 |
| `demo_complete_keyboard.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_full_keyboard_layout.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_input_method.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_ios_style.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_learning.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_mongolian_dialog.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_traditional_keyboard.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_ux_enhanced.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_vertical.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_vertical_final.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `demo_vertical_fixed.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |
| `ai-chat.html` | ✅ | ⏳ | ⏳ | ⏳ 待检查 |

### CSS 文件

| 文件 | 全局规则 | `.key-char` | `.mongolian-vertical` | 状态 |
|------|----------|-------------|----------------------|------|
| `mongolian-vertical.css` | ✅ | ✅ | ✅ | ✅ 已完成 |

---

## 🔍 验证步骤

### 步骤 1: 检查 HTML 结构
```bash
# 检查所有蒙古文字符是否有 .key-char 类
grep -n "<span>ᠠ\|<span>ᠡ\|<span>ᠢ" *.html
```

### 步骤 2: 检查 CSS 引用
```bash
# 检查所有 HTML 是否引用了竖排 CSS
for f in *.html; do
  grep -q 'mongolian-vertical.css' "$f" && echo "✅ $f" || echo "❌ $f"
done
```

### 步骤 3: 截图验证
```bash
# 使用 Chrome Headless 截图
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless \
  --screenshot=verify.png \
  --window-size=1920,1080 \
  file:///path/to/file.html
```

### 步骤 4: 视觉检查
- [ ] 蒙古文字符从上到下阅读
- [ ] 字符顶部朝向左侧
- [ ] 不需要歪头阅读
- [ ] 与你提供的示例图片一致

---

## 📝 修复优先级

### P0 - 核心文件（立即修复）
- [x] `embedded-input.html` ⭐ 主输入法界面
- [ ] `demo_chat_keyboard_v3.html` ⭐ 聊天界面
- [ ] `demo_ai_powered.html` ⭐ AI 增强版

### P1 - 重要文件（尽快修复）
- [ ] `demo_complete_keyboard.html`
- [ ] `demo_traditional_keyboard.html`
- [ ] `demo_vertical_final.html`

### P2 - 其他文件（计划修复）
- [ ] 其他演示文件

---

## 🎯 完成标准

所有 HTML 文件必须满足：
1. ✅ 引用 `mongolian-vertical.css`
2. ✅ 所有蒙古文字符使用 `.key-char` 类
3. ✅ CSS 中包含竖排样式（`!important`）
4. ✅ 截图验证通过（与示例一致）

---

**最后更新**: 2026-04-01 10:32 JST
