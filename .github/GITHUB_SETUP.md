# GitHub 仓库设置指南

## 📋 待完成设置

请按以下步骤在 GitHub 仓库页面操作：

---

## 1. 添加仓库描述和主题

**操作位置**: 仓库首页右侧 "About" 区域

### 描述 (About)
```
传统蒙古文 AI 助手 - 竖排渲染引擎、NLP 工具链、移动端优化。让蒙古文在 AI 时代焕发新生。
```

### Topics (标签)
点击 "Manage topics" 添加以下标签：

```
mongolian
mongolian-script
nlp
vertical-writing
input-method
ai
open-source
mobile-first
mongolia
inner-mongolia
web-fonts
rendering-engine
javascript
python
```

---

## 2. 设置 GitHub Pages

**操作位置**: Settings → Pages

### 配置步骤

1. **Source**: Deploy from a branch
2. **Branch**: 选择 `main`
3. **Folder**: 选择 `/ (root)`
4. 点击 **Save**

### 预期结果

等待 2-3 分钟后，你的网站将在以下地址可用：

```
https://claws-x.github.io/mongol-ai/
```

### 访问演示页面

部署成功后，可以访问：

- **主页**: https://claws-x.github.io/mongol-ai/
- **AI 聊天**: https://claws-x.github.io/mongol-ai/demos/input/ai-chat.html
- **完整键盘**: https://claws-x.github.io/mongol-ai/demos/keyboard/demo_complete_keyboard.html
- **综合测试**: https://claws-x.github.io/mongol-ai/demos/tests/demo-comprehensive-test.html

---

## 3. 保护 main 分支

**操作位置**: Settings → Branches → Add branch protection rule

### 配置规则

**Branch name pattern**: `main`

✅ **Require a pull request before merging**
- ✅ Require approvals: `1`
- ❌ Dismiss pull request reviews on push (可选)

✅ **Do not allow bypassing the above settings**

✅ **Include administrators** (可选，但推荐)

✅ **Require conversation resolution before merging** (推荐)

### 效果

- 不能直接 push 到 main
- 必须通过 Pull Request
- 至少需要 1 人审批
- 所有评论必须解决后才能合并

---

## 4. 启用 GitHub Discussions

**操作位置**: Settings → General → Features

### 配置步骤

1. 找到 "Discussions"
2. ✅ 勾选 "Set up discussions"
3. 点击 **Save**

### 讨论分类建议

创建后可添加以下分类：

- 📢 **Announcements** - 官方公告
- 💡 **Ideas** - 功能建议
- ❓ **Q&A** - 问答
- 🗨️ **General** - 一般讨论
- 🌍 **International** - 多语言交流

---

## 5. 配置 Issue 模板 (可选)

**操作位置**: Issues → Set up templates → Get started

### 建议模板

#### Bug Report
```markdown
---
name: Bug Report
about: 报告问题
title: '[BUG] 简短描述'
labels: bug
---

**问题描述**
清晰简洁地描述问题

**复现步骤**
1. 打开 '...'
2. 点击 '....'
3. 看到错误 '....'

**期望行为**
清晰简洁地描述期望发生什么

**截图**
如适用，添加截图

**环境:**
- 设备：[e.g. iPhone 14, MacBook Pro]
- 系统：[e.g. iOS 16, macOS 13]
- 浏览器：[e.g. Chrome 112, Safari 16]

**其他信息**
添加其他上下文信息
```

#### Feature Request
```markdown
---
name: Feature Request
about: 功能建议
title: '[FEATURE] 简短描述'
labels: enhancement
---

**功能描述**
清晰简洁地描述建议的功能

**问题关联**
如适用，关联相关 Issue

**实现建议**
描述期望的实现方式

**替代方案**
描述考虑过的替代方案

**其他信息**
添加其他上下文信息
```

---

## 6. 设置 Issue 表单 (可选进阶)

**操作位置**: Settings → Issues → Forms

可以创建自定义表单引导用户提交更有效的 Issue。

---

## 7. 添加项目看板 (可选)

**操作位置**: Projects → New project

### 建议看板列

```
📋 Backlog (待办)
🔄 In Progress (进行中)
✅ Done (已完成)
🐛 Bugs (缺陷)
🎯 v5.3 (下一版本)
```

---

## 8. 配置 Insights (可选)

**操作位置**: Insights

### 可追踪指标

- **Traffic** - 访问量和独立访客
- **Clones** - 克隆次数
- **Code frequency** - 代码提交频率
- **Dependency graph** - 依赖关系
- **Security advisories** - 安全公告

---

## 9. 设置 Milestones (可选)

**操作位置**: Issues → Milestones → New milestone

### 建议 Milestone

#### v5.3 - 移动端优化 (2026-04-10)
- 响应式布局
- 触摸优化
- PWA 支持

#### v6.0 - PWA 发布 (2026-04-24)
- 离线支持
- 安装到主屏幕
- 推送通知

#### v7.0 - NLP 增强 (2026-05-15)
- 词典扩展到 1000+ 词
- 准确率提升到 90%+
- 预训练模型

---

## ✅ 设置检查清单

完成后勾选：

- [ ] 添加仓库描述
- [ ] 添加 15 个 Topics
- [ ] 启用 GitHub Pages (等待部署成功)
- [ ] 保护 main 分支
- [ ] 启用 Discussions
- [ ] 创建 Issue 模板
- [ ] 创建项目看板
- [ ] 设置 Milestones

---

## 🎉 完成后的效果

### 仓库首页
- ✅ 清晰的描述和标签
- ✅ 完善的 README
- ✅ 徽章展示 (License/Stars/Issues)

### 功能完整
- ✅ GitHub Pages 在线演示
- ✅ Discussions 社区讨论
- ✅ Issues 问题追踪
- ✅ Projects 项目管理

### 开发流程规范
- ✅ 分支保护
- ✅ PR 审查
- ✅ Issue 模板
- ✅ Milestones 里程碑

---

## 📞 需要帮助？

如有问题，参考：
- [GitHub Docs](https://docs.github.com/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [保护分支文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

**创建时间**: 2026-04-03  
**适用版本**: v5.2.0+
