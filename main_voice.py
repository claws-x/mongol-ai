#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙古文 AI 助手 - 语音输入版
Mongolian AI Assistant - Voice Input Version

用法:
    python3 main_voice.py           # 交互模式（支持语音）
    python3 main_voice.py --voice   # 强制语音模式
    python3 main.py                 # 纯文字模式
"""

import sys
import argparse
from pathlib import Path

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent))

from core.mongolian_text import MongolianTextProcessor
from core.chat_engine import MongolianChatEngine

# 尝试导入语音模块
try:
    from modules.voice_input import VoiceInput, SimpleVoiceInput
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️  语音模块未加载，将使用文字输入")


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔════════════════════════════════════════════════════════╗
║                                                        ║
║      🐎 传统蒙古文 AI 助手 (语音版) 🐎                  ║
║      Mongolian AI Assistant - Voice Input              ║
║                                                        ║
║      ᠮᠣᠩᠭᠣᠯ AI ᠲᠠᠨᠢᠯᠴᠠᠭᠤᠯᠠᠭᠴᠢ                        ║
║                                                        ║
║      🎤 支持语音输入 | 文字输出                        ║
║      🎤 Voice Input | Text Output                      ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
    """
    print(banner)


def interactive_mode(use_voice: bool = False):
    """
    交互模式
    
    Args:
        use_voice: 是否启用语音输入
    """
    print_banner()
    
    # 初始化引擎
    engine = MongolianChatEngine()
    processor = MongolianTextProcessor()
    
    # 初始化语音输入
    if use_voice and VOICE_AVAILABLE:
        voice_input = SimpleVoiceInput()  # 使用简化版
        print("✅ 语音输入已启用（简化版）")
    else:
        voice_input = None
        print("💬 文字输入模式")
    
    print("\n💡 使用说明:")
    print("  - 说话或输入蒙古文/中文进行对话")
    print("  - 输入 '/help' 查看帮助")
    print("  - 输入 '/clear' 清空对话历史")
    print("  - 输入 '/voice' 切换语音模式")
    print("  - 输入 '/quit' 退出程序")
    print()
    
    # 显示欢迎消息
    welcome = engine.chat("ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨᠤᠤ")
    print(f"🤖 AI: {welcome}\n")
    
    while True:
        try:
            # 获取用户输入
            if voice_input:
                user_input = voice_input.listen()
            else:
                user_input = input("📝 您：").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() in ['/quit', '/exit', '/q']:
                goodbye = engine.chat("再见", bilingual=True)
                print(f"\n{goodbye}")
                print("\n👋 ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ! 再见!")
                break
            
            elif user_input.lower() == '/clear':
                engine.clear_history()
                print("✅ 对话历史已清空")
                continue
            
            elif user_input.lower() == '/help':
                print("\n" + "=" * 50)
                print("帮助菜单")
                print("=" * 50)
                print("/help    - 显示帮助")
                print("/clear   - 清空对话历史")
                print("/history - 查看对话历史")
                print("/voice   - 切换语音模式")
                print("/analyze - 分析输入文本")
                print("/quit    - 退出程序")
                print("=" * 50)
                continue
            
            elif user_input.lower() == '/voice':
                if voice_input:
                    voice_input = None
                    print("🔇 已切换到文字输入模式")
                else:
                    if VOICE_AVAILABLE:
                        voice_input = SimpleVoiceInput()
                        print("🔊 已切换到语音输入模式")
                    else:
                        print("⚠️  语音模块不可用")
                continue
            
            elif user_input.lower() == '/history':
                history = engine.get_history()
                if history:
                    print("\n" + "=" * 50)
                    print("对话历史")
                    print("=" * 50)
                    for msg in history[-10:]:
                        role = "👤" if msg['role'] == 'user' else "🤖"
                        preview = msg['content'][:80].replace('\n', ' ')
                        print(f"{role} {preview}...")
                    print("=" * 50)
                else:
                    print("暂无对话历史")
                continue
            
            # 正常对话
            response = engine.chat(user_input, bilingual=True)
            print(f"\n🤖 AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ! 再见!")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}\n")


def main():
    parser = argparse.ArgumentParser(
        description='传统蒙古文 AI 助手 - 语音输入版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 main_voice.py              # 交互模式（文字）
  python3 main_voice.py --voice      # 语音模式
  python3 main_voice.py --text "..." # 单次对话
        """
    )
    
    parser.add_argument('--voice', '-v', action='store_true',
                       help='启用语音输入')
    parser.add_argument('--text', '-t', type=str, help='单次对话文本')
    
    args = parser.parse_args()
    
    if args.text:
        # 单次对话模式
        engine = MongolianChatEngine()
        response = engine.chat(args.text, bilingual=True)
        print(response)
    else:
        # 交互模式
        interactive_mode(use_voice=args.voice)


if __name__ == '__main__':
    main()
