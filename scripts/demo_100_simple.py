#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100 次 OpenClaw 聊天演示 - 简化版
使用基础对话功能
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.chat_engine import MongolianChatEngine

# 基础对话话题
TOPICS = [
    "ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨᠤᠤ",  # 你好
    "你好",
    "ᠪᠠᠶᠠᠷᠲᠠᠢ",  # 谢谢
    "谢谢",
    "ᠲᠤᠰᠠᠯᠠᠭ᠎ᠠ",  # 帮助
    "帮助",
    "再见",
    "ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ",  # 再见
    "OpenClaw",
    "ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ",  # 蒙古语
    "学习",
    "ᠰᠤᠷᠤᠬᠤ",  # 学习
    "AI",
    "机器人",
    "ᠲᠠᠨᠢᠯᠴᠠᠭᠤᠯᠠᠭᠴᠢ",  # 助手
    "Gitea",
    "代码",
    "ᠭᠠᠵᠠᠷ",  # 地方
    "Telegram",
    "飞书",
]

def run_demo():
    """运行 100 次聊天演示"""
    engine = MongolianChatEngine()
    
    print("=" * 70)
    print("🤖 OpenClaw 聊天演示 - 100 次对话")
    print("📅", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    print()
    
    chat_log = []
    
    for i in range(100):
        topic_idx = i % len(TOPICS)
        user_input = TOPICS[topic_idx]
        
        response = engine.chat(user_input, bilingual=True)
        
        chat_log.append({
            'round': i + 1,
            'input': user_input,
            'output': response
        })
        
        print(f"━━━ 第 {i+1:3d} 轮 ━━━")
        print(f"👤 {user_input}")
        print(f"🤖 {response[:150]}...")
        print()
        
        if (i + 1) % 10 == 0:
            print(f"\n📊 进度：{i+1}/100\n")
    
    # 保存记录
    log_file = Path(__file__).parent / 'chat_log_openclaw_100.txt'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("🤖 OpenClaw 聊天演示 - 100 次对话\n")
        f.write("📅 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 70 + "\n\n")
        
        for entry in chat_log:
            f.write(f"━━━ 第 {entry['round']:3d} 轮 ━━━\n")
            f.write(f"👤 {entry['input']}\n")
            f.write(f"🤖 {entry['output']}\n\n")
    
    print("=" * 70)
    print(f"✅ 100 轮完成！")
    print(f"📄 记录：{log_file}")
    print("=" * 70)

if __name__ == '__main__':
    run_demo()
