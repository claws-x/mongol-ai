#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100 次 OpenClaw 主题聊天演示
Automated 100 Chat Demo - OpenClaw Topics
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.chat_engine import MongolianChatEngine

# OpenClaw 相关话题（蒙古文 + 中文）
OPENCLAW_TOPICS = [
    ("ᠲᠠ OpenClaw ᠢ ᠮᠡᠳᠡᠬᠦ ᠤᠤ", "你知道 OpenClaw 吗"),
    ("OpenClaw ᠶᠢᠨ ᠬᠡᠷᠡᠭᠰᠢᠯ ᠶᠠᠮᠠᠷ ᠪᠡᠨ", "OpenClaw 是做什么的"),
    ("ᠪᠢ OpenClaw ᠢ ᠬᠡᠷᠬᠢᠶᠡᠯᠡᠬᠦ ᠪᠣᠯᠲᠠᠢ", "我想使用 OpenClaw"),
    ("OpenClaw ᠶᠢᠨ ᠳᠠᠭᠠᠤᠬᠤ ᠬᠡᠷᠡᠭᠰᠢᠯ", "OpenClaw 的主要功能"),
    ("ᠬᠡᠷᠬᠢᠶᠡᠯᠡᠭᠴᠢᠳᠡ OpenClaw ᠢ ᠬᠡᠷᠬᠢᠶᠡᠯᠡᠬᠦ", "如何使用 OpenClaw"),
    ("OpenClaw ᠶᠢᠨ AI Agent", "OpenClaw 的 AI 助手"),
    ("OpenClaw ᠶᠢᠨ Telegram Bot", "OpenClaw 的电报机器人"),
    ("OpenClaw ᠶᠢᠨ Feishu Bot", "OpenClaw 的飞书机器人"),
    ("OpenClaw ᠶᠢᠨ Gitea", "OpenClaw 的 Gitea 代码管理"),
    ("OpenClaw ᠶᠢᠨ CI/CD", "OpenClaw 的持续集成"),
    ("OpenClaw ᠶᠢᠨ Mongolian AI", "OpenClaw 的蒙古文 AI"),
    ("OpenClaw ᠶᠢᠨ Voice Input", "OpenClaw 的语音输入"),
    ("OpenClaw ᠶᠢᠨ Text Processing", "OpenClaw 的文本处理"),
    ("OpenClaw ᠶᠢᠨ Chat Engine", "OpenClaw 的对话引擎"),
    ("OpenClaw ᠶᠢᠨ Vocabulary", "OpenClaw 的词汇库"),
    ("ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ OpenClaw ᠳ᠋ᠡᠭᠡ", "蒙古语在 OpenClaw 中"),
    ("OpenClaw ᠶᠢᠨ ᠮᠥᠷᠥᠭᠡᠳᠡᠯ", "OpenClaw 的未来"),
    ("OpenClaw ᠶᠢᠨ ᠬᠥᠭᠵᠢᠭᠤᠯᠦᠯᠲᠡ", "OpenClaw 的发展"),
    ("OpenClaw ᠶᠢᠨ ᠭᠠᠵᠠᠷ ᠳᠡᠭᠡᠷᠬᠢ ᠨᠥᠯᠥᠭᠡ", "OpenClaw 在本地运行"),
    ("OpenClaw ᠶᠢᠨ ᠠᠶᠤᠯᠭ᠎ᠠ", "OpenClaw 的安装"),
    ("OpenClaw ᠶᠢᠨ ᠲᠣᠬᠢᠷᠠᠭᠤᠯᠤᠯᠲᠠ", "OpenClaw 的配置"),
    ("OpenClaw ᠶᠢᠨ Plugin", "OpenClaw 的插件系统"),
    ("OpenClaw ᠶᠢᠨ Skill", "OpenClaw 的技能"),
    ("OpenClaw ᠶᠢᠨ Memory", "OpenClaw 的记忆功能"),
    ("OpenClaw ᠶᠢᠨ Session", "OpenClaw 的会话管理"),
    ("OpenClaw ᠶᠢᠨ Tool", "OpenClaw 的工具调用"),
    ("OpenClaw ᠶᠢᠨ Browser", "OpenClaw 的浏览器控制"),
    ("OpenClaw ᠶᠢᠨ Canvas", "OpenClaw 的画布功能"),
    ("OpenClaw ᠶᠢᠨ Message", "OpenClaw 的消息发送"),
    ("OpenClaw ᠶᠢᠨ TTS", "OpenClaw 的语音合成"),
    ("OpenClaw ᠶᠢᠨ STT", "OpenClaw 的语音识别"),
    ("OpenClaw ᠶᠢᠨ Subagent", "OpenClaw 的子代理"),
    ("OpenClaw ᠶᠢᠨ Main Agent", "OpenClaw 的主代理"),
    ("OpenClaw ᠶᠢᠨ Specialist", "OpenClaw 的专家代理"),
    ("OpenClaw ᠶᠢᠨ News Agent", "OpenClaw 的新闻代理"),
    ("OpenClaw ᠶᠢᠨ Math Agent", "OpenClaw 的数学代理"),
    ("OpenClaw ᠶᠢᠨ iOS Agent", "OpenClaw 的 iOS 开发代理"),
    ("OpenClaw ᠶᠢᠨ ECH Agent", "OpenClaw 的 ECH 嵌入式代理"),
    ("OpenClaw ᠶᠢᠨ Paper Agent", "OpenClaw 的论文阅读代理"),
    ("OpenClaw ᠶᠢᠨ Language Agent", "OpenClaw 的语言学习代理"),
    ("OpenClaw ᠶᠢᠨ Workflow", "OpenClaw 的工作流"),
    ("OpenClaw ᠶᠢᠨ Automation", "OpenClaw 的自动化"),
    ("OpenClaw ᠶᠢᠨ Integration", "OpenClaw 的集成"),
    ("OpenClaw ᠶᠢᠨ API", "OpenClaw 的接口"),
    ("OpenClaw ᠶᠢᠨ Webhook", "OpenClaw 的 Webhook"),
    ("OpenClaw ᠶᠢᠨ Cron", "OpenClaw 的定时任务"),
    ("OpenClaw ᠶᠢᠨ Log", "OpenClaw 的日志"),
    ("OpenClaw ᠶᠢᠨ Debug", "OpenClaw 的调试"),
    ("OpenClaw ᠶᠢᠨ Test", "OpenClaw 的测试"),
    ("OpenClaw ᠶᠢᠨ Deploy", "OpenClaw 的部署"),
]

def run_demo():
    """运行 100 次聊天演示"""
    engine = MongolianChatEngine()
    
    print("=" * 70)
    print("🤖 OpenClaw 主题聊天演示 - 100 次对话")
    print("📅 时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    print()
    
    # 保存聊天记录
    chat_log = []
    
    for i in range(100):
        # 选择话题（循环使用）
        topic_idx = i % len(OPENCLAW_TOPICS)
        mn_topic, zh_topic = OPENCLAW_TOPICS[topic_idx]
        
        # 交替使用蒙古文和中文
        if i % 2 == 0:
            user_input = mn_topic
        else:
            user_input = zh_topic
        
        # 获取 AI 回复
        response = engine.chat(user_input, bilingual=True)
        
        # 记录
        chat_log.append({
            'round': i + 1,
            'input_mn': mn_topic,
            'input_zh': zh_topic,
            'input_actual': user_input,
            'output': response
        })
        
        # 输出
        print(f"━━━ 第 {i+1:3d} 轮 ━━━")
        print(f"👤 用户：{user_input}")
        print(f"🤖 AI: {response[:200]}...")
        print()
        
        # 每 10 轮显示统计
        if (i + 1) % 10 == 0:
            print(f"\n📊 进度：{i+1}/100 轮\n")
    
    # 保存聊天记录
    log_file = Path(__file__).parent / 'chat_log_100.txt'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("🤖 OpenClaw 主题聊天演示 - 100 次对话记录\n")
        f.write("📅 时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 70 + "\n\n")
        
        for entry in chat_log:
            f.write(f"━━━ 第 {entry['round']:3d} 轮 ━━━\n")
            f.write(f"👤 用户：{entry['input_actual']}\n")
            f.write(f"🤖 AI: {entry['output']}\n\n")
    
    print("=" * 70)
    print("✅ 100 轮对话完成！")
    print(f"📄 聊天记录已保存到：{log_file}")
    print("=" * 70)


if __name__ == '__main__':
    run_demo()
