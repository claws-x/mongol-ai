# 🐎 传统蒙古文 AI 助手 - Mongolian AI Assistant

## 项目目标

开发一款支持**传统蒙古文**（回鹘式蒙古文）的 AI 助手工具，实现：
- ✅ 蒙古文输入/输出
- ✅ 蒙古文对话聊天
- ✅ 蒙古文文本处理
- ✅ 蒙古文 - 中文/英文翻译

---

## 技术架构

```
mongolian-ai-assistant/
├── core/           # 核心功能模块
│   ├── mongolian_text.py      # 蒙古文文本处理
│   ├── mongolian_input.py     # 蒙古文输入处理
│   └── chat_engine.py         # 对话引擎
├── ui/             # 用户界面
│   ├── cli.py                 # 命令行界面
│   └── web.py                 # Web 界面（可选）
├── models/         # AI 模型集成
│   └── llm_integration.py     # 大模型集成
├── data/           # 语料数据
│   └── mongolian_corpus.jsonl # 蒙古文训练数据
├── tests/          # 测试文件
└── main.py         # 主程序入口
```

---

## 传统蒙古文 Unicode

**Unicode 范围**: U+1800 - U+18AF

示例：
```
ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ (蒙古文)
ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠤᠤ (你好)
ᠪᠠᠶᠠᠷᠲᠠᠢ (谢谢)
```

---

## 快速开始

```bash
cd mongolian-ai-assistant
python3 main.py
```

---

## 功能特性

### 1. 蒙古文对话
- 支持传统蒙古文输入
- AI 用蒙古文回复
- 双语模式（蒙古文 + 中文）

### 2. 蒙古文处理
- 文本规范化
- 字符编码转换
- 词汇分析

### 3. 翻译功能
- 蒙古文 ↔ 中文
- 蒙古文 ↔ 英文

### 4. 学习辅助
- 词汇解释
- 语法帮助
- 文化背景

---

## 依赖安装

```bash
pip3 install -r requirements.txt
```

---

## 数据来源

使用之前抓取的蒙古文训练数据：
- 西里尔蒙古文：1,190 条
- 传统蒙古文：5,108 条

路径：`../mongolian-llm-data/output/`

---

## 开发状态

- [x] 项目结构创建
- [ ] 蒙古文文本处理模块
- [ ] 对话引擎集成
- [ ] 命令行界面
- [ ] Web 界面（可选）
- [ ] 测试用例

---

**作者**: OpenClaw AI Team  
**创建**: 2026-03-29  
**许可证**: MIT
