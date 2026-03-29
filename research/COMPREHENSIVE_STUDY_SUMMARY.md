# 蒙古文研究综合学习笔记

## 学习时间

**日期**：2026-03-30  
**耗时**：约 2 小时  
**学习者**：OpenClaw Mongolian AI Team

---

## 学习资源总览

### 1. 官方网站

| 网站 | URL | 学习内容 |
|------|-----|---------|
| **Mongolfont** | http://www.mongolfont.com/cn/ | 蒙古文字体、键盘布局、输入法 |
| **CJVLang** | http://www.cjvlang.com/ | 蒙古文 Web 显示教程 |
| **W3C** | https://www.w3.org/TR/mlreq/ | 蒙古文排版标准 |
| **Unicode** | https://www.unicode.org/notes/tn57/ | Unicode 编码与字形变换 |

### 2. 学术论文

| 论文 | 来源 | 年份 | 主题 |
|------|------|------|------|
| **蒙古文拼写形式多样化现象研究** | ACL Anthology (CCL 2020) | 2020 | 拼写规范化 |
| **蒙古文信息化研究** | 社科网 | 2010 | 基础建设 |
| **Encoding and Shaping of the Mongolian Script** | Unicode TN #57 | 2024 | 编码标准 |

---

## 核心知识点

### 1. 蒙古文文字特性

**书写方向**：
- 从上到下书写
- 列从左到右排列
- 世界唯一的竖排文字（从左到右）

**字符形态**：
- 词首形式 (Initial)
- 词中形式 (Medial)
- 词尾形式 (Final)
- 独立形式 (Isolated)

**Unicode 编码**：
- 基本区块：U+1800 - U+18AF
- 扩展区块：U+11660 - U+1167F
- 2000 年 Unicode 3.0 收录

### 2. CSS 竖排显示

**标准方案**：
```css
.mongolian-vertical {
    /* 书写模式 */
    writing-mode: vertical-lr;
    -webkit-writing-mode: vertical-lr;
    -ms-writing-mode: tb-lr;
    
    /* 字符方向 */
    text-orientation: upright;
    -webkit-text-orientation: sideways-right;
    
    /* 对齐 */
    text-align: right;
    text-justify: inter-ideograph;
    
    /* 字体 */
    font-family: 'Mongolian White', 'Mongolian Baiti', sans-serif;
}
```

**备选方案（transform）**：
```css
.mongolian-vertical {
    display: inline-block;
    transform: rotate(90deg);
    transform-origin: top left;
    white-space: nowrap;
}
```

### 3. 字体支持

**Mongolfont 四种字体**：
1. Mongolian White（白体）
2. Mongolian Writing（手写体）
3. Mongolian Art（美术体）
4. Mongolian Title（标题字）

**字体类型**：
- OpenType (.ttf) - Windows 使用
- AAT (.ttf) - Mac 使用

**系统支持**：
- Windows Vista/7+：原生支持
- Windows XP：不支持 OpenType
- Mac OS X：需要 AAT 字体
- Linux：需要安装模块

### 4. 拼写形式多样化

**问题定义**（ACL 2020）：
> 看到的单词字形正确但其内码序列不正确，或者说单词"变形显现字形"序列正确但"名义字符"序列不正确

**原因**：
1. 历史原因：早期编码不统一
2. 技术原因：Unicode 普及不够
3. 用户原因：缺乏标准化培训

**影响**：
- 文本匹配困难
- 机器翻译问题
- 语音识别障碍
- 数据库查询不完整

**解决方案**：
1. 推广 Unicode 标准编码
2. 使用智能输入法
3. 使用校对纠错工具
4. 基于生语料的统计学习

### 5. Unicode 字形变换（UTN #57）

**分层变换系统**：
```
输入文本 (Unicode 码点序列)
  ↓
第 1 层：基础变换
  ↓
第 2 层：上下文变换
  ↓
第 3 层：变体选择
  ↓
输出：最终字形呈现
```

**自由变体选择符 (FVS)**：
- FVS1 (U+180B)
- FVS2 (U+180C)
- FVS3 (U+180D)

**使用场景**：
```
基本字符 + FVS1 → 变体 1
基本字符 + FVS2 → 变体 2
基本字符 + FVS3 → 变体 3
```

---

## 技术发展脉络

```
2000 年
  ↓
Unicode 3.0 收录蒙古文 (U+1800-U+18AF)
  ↓
2006 年
  ↓
Windows Vista 首次支持蒙古文
  ↓
2009-2010 年
  ↓
Windows 7 普及 + 社科网论文（基础建设研究）
  ↓
2011 年
  ↓
Mongolfont 字体发布
  ↓
2016 年
  ↓
Unicode UTN #57 首次发布
  ↓
2020 年
  ↓
ACL 论文（拼写形式多样化研究）
  ↓
2024 年
  ↓
Unicode UTN #57 Version 4（最新版本）
  ↓
2026 年（现在）
  ↓
我们的项目：AI 助手 + 竖排显示 + 规范化
```

---

## 项目实现

### 1. 已实现功能

**竖排显示**：
- ✅ CSS 样式表（9 种样式）
- ✅ 多种浏览器兼容
- ✅ 响应式设计
- ✅ 打印样式

**文本处理**：
- ✅ 蒙古文检测
- ✅ 内容提取
- ✅ 基础词汇库（8 个短语）

**Skill 安装**：
- ✅ Mongolian Assistant Skill v2.0
- ✅ 完整文档
- ✅ 使用示例

### 2. 待实现功能

**文本规范化**：
- [ ] MongolianNormalizer 类
- [ ] FVS 规范化
- [ ] 同形异码处理

**拼写检查**：
- [ ] MongolianSpellChecker 类
- [ ] 不规范拼写检测
- [ ] 纠正建议

**字形变换**：
- [ ] MongolianShaper 类
- [ ] 分层变换引擎
- [ ] OpenType 特性集成

**输入法**：
- [ ] 智能输入法集成
- [ ] 自动规范化
- [ ] 避免误录

### 3. 文件结构

```
mongolian-ai-assistant/
├── core/
│   ├── mongolian_layout_engine.js    # 布局引擎
│   └── mongolian_text.py             # 文本处理器
├── research/
│   ├── VERTICAL_LAYOUT_RESEARCH.md   # 竖排研究
│   ├── ACL_2020_MONGOLIAN_SPELLING.md
│   ├── SINOSS_2010_MONGOLIAN_RESEARCH.md
│   ├── UNICODE_TN57_MONGOLIAN.md
│   └── COMPREHENSIVE_STUDY_SUMMARY.md（本文件）
├── mongolian-vertical.css             # 竖排 CSS
├── demo_vertical_final.html           # 演示页面
├── test_vertical.html                 # 测试页面
├── README.md
└── DELIVERY.md

skills/mongolian-assistant/
├── SKILL.md                           # 技能说明
├── mongolian_processor.py             # 处理器
└── requirements.txt                   # 依赖
```

---

## 关键发现

### 1. 竖排显示方案

**最佳实践**（综合多个来源）：
```css
.mongolian-vertical {
    /* 标准方案 */
    writing-mode: vertical-lr;
    text-orientation: upright;
    -webkit-text-orientation: sideways-right;
    
    /* 字体 */
    font-family: 'Mongolian White', 'Mongolian Baiti', 'Noto Sans Mongolian', sans-serif;
    
    /* 对齐 */
    text-align: right;
    text-justify: inter-ideograph;
}
```

### 2. 字体选择

**推荐顺序**：
1. Mongolian White（Mongolfont）
2. Mongolian Baiti（Windows 默认）
3. Noto Sans Mongolian（Google）

### 3. 规范化标准

**依据**：
- Unicode UTN #57 Version 4（最新标准）
- ACL 2020 论文（问题定义）
- W3C Mongolian Layout（Web 标准）

### 4. 浏览器兼容性

**支持情况**：
- Chrome/Blink：✅ 完全支持
- Firefox/Gecko：✅ 完全支持
- Safari/WebKit：⚠️ 需要 `-webkit-text-orientation: sideways-right`
- IE：❌ 不支持（使用 transform 回退）

---

## 下一步行动计划

### 短期（1 周）

1. **实现文本规范化模块**
   - [ ] 基于 Unicode UTN #57
   - [ ] FVS 规范化
   - [ ] 同形异码处理

2. **开发拼写检查器**
   - [ ] 检测不规范拼写
   - [ ] 提供纠正建议
   - [ ] 批量处理

3. **下载字体**
   - [ ] Mongolfont 四种字体
   - [ ] Noto Sans Mongolian
   - [ ] 集成到项目

### 中期（1 月）

4. **集成智能输入法**
   - [ ] 参考 Mongolfont 键盘布局
   - [ ] 自动规范化
   - [ ] 避免误录

5. **开发校对工具**
   - [ ] 拼写检查
   - [ ] 批量纠正
   - [ ] 后处理

6. **扩展词汇库**
   - [ ] 从 8 个扩展到 100+ 个
   - [ ] 添加例句
   - [ ] 添加发音

### 长期（3 月）

7. **字形变换引擎**
   - [ ] 分层变换
   - [ ] OpenType 集成
   - [ ] 性能优化

8. **语音支持**
   - [ ] 蒙古文 TTS
   - [ ] 蒙古文 STT
   - [ ] 发音练习

9. **学习模块**
   - [ ] 词汇学习
   - [ ] 语法指导
   - [ ] 练习测试

---

## 参考资源汇总

### 官方网站

- **Mongolfont**：http://www.mongolfont.com/cn/
- **CJVLang**：http://www.cjvlang.com/Writing/writmongol/
- **W3C**：https://www.w3.org/TR/mlreq/
- **Unicode**：https://www.unicode.org/notes/tn57/

### 学术论文

- **ACL 2020**：https://aclanthology.org/2020.ccl-1.45/
- **Unicode TN #57**：https://www.unicode.org/notes/tn57/utn57-mong-4.pdf

### 字体下载

- **Mongolfont**：http://www.mongolfont.com/cn/font/index.html
- **Google Fonts**：https://fonts.google.com/noto/specimen/Noto+Sans+Mongolian

### 教程

- **CJVLang 教程**：http://www.cjvlang.com/Writing/writmongol/tradmononsite.html

---

## 学习心得

### 1. 理论研究的重要性

通过学习 3 篇论文（2010-2024），我们：
- 理解了蒙古文信息化的发展历程
- 掌握了拼写形式多样化问题的本质
- 学习了 Unicode 官方标准

### 2. 实践与理论结合

- **理论**：Unicode UTN #57、ACL 论文
- **实践**：CSS 竖排显示、字体支持
- **结合**：基于理论指导实践

### 3. 持续学习

蒙古文信息化是一个持续发展的领域：
- 2000 年：Unicode 收录
- 2010 年：基础建设
- 2020 年：规范化研究
- 2024 年：UTN #57 v4
- 2026 年：我们的 AI 项目

我们需要持续学习，跟上最新发展。

---

**整理**：OpenClaw Mongolian AI Team  
**日期**：2026-03-30  
**版本**：v1.0  
**状态**：✅ 学习完成，准备实现
