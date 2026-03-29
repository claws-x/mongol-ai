#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙古文 AI 助手 - 命令行界面
Mongolian AI Assistant - CLI

用法：
    python3 main.py              # 交互模式
    python3 main.py --text "..." # 单次对话
    python3 main.py --translate "..." # 翻译模式
"""

import sys
import argparse
from pathlib import Path

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent))

from core.mongolian_text import MongolianTextProcessor
from core.chat_engine import MongolianChatEngine


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔════════════════════════════════════════════════════════╗
║                                                        ║
║      🐎 传统蒙古文 AI 助手 🐎                           ║
║      Mongolian AI Assistant                            ║
║                                                        ║
║      ᠮᠣᠩᠭᠣᠯ AI ᠲᠠᠨᠢᠯᠴᠠᠭᠤᠯᠠᠭᠴᠢ                        ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
    """
    print(banner)


def interactive_mode():
    """交互模式"""
    print_banner()
    
    # 初始化引擎
    engine = MongolianChatEngine()
    processor = MongolianTextProcessor()
    
    print("💡 使用说明:")
    print("  - 输入蒙古文或中文进行对话")
    print("  - 输入 '/help' 查看帮助")
    print("  - 输入 '/clear' 清空对话历史")
    print("  - 输入 '/quit' 退出程序")
    print()
    print(engine.chat("ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠤᠤ"))
    print()
    
    while True:
        try:
            # 获取用户输入
            user_input = input("📝 您：").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("\n" + engine.chat("再见", bilingual=True))
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
                print("/analyze - 分析输入文本")
                print("/translate - 翻译模式")
                print("/quit    - 退出程序")
                print("=" * 50)
                continue
            
            elif user_input.lower() == '/history':
                history = engine.get_history()
                if history:
                    print("\n" + "=" * 50)
                    print("对话历史")
                    print("=" * 50)
                    for msg in history[-10:]:
                        role = "👤" if msg['role'] == 'user' else "🤖"
                        print(f"{role} {msg['content'][:100]}")
                    print("=" * 50)
                else:
                    print("暂无对话历史")
                continue
            
            elif user_input.lower() == '/analyze':
                last_msg = engine.get_history()[-1] if engine.get_history() else None
                if last_msg:
                    analysis = processor.analyze_text(last_msg['content'])
                    print("\n" + "=" * 50)
                    print("文本分析")
                    print("=" * 50)
                    print(f"包含蒙古文：{'✅' if analysis['is_mongolian'] else '❌'}")
                    print(f"蒙古文内容：{analysis['mongolian_content']}")
                    print(f"转写：{analysis['transliteration']}")
                    print(f"字符统计：{analysis['character_count']}")
                    print("=" * 50)
                continue
            
            # 正常对话
            response = engine.chat(user_input, bilingual=True)
            print(f"\n🤖 AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ! 再见!")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}\n")


def single_chat(text: str):
    """单次对话模式"""
    engine = MongolianChatEngine()
    response = engine.chat(text, bilingual=True)
    print(response)


def translate_mode(text: str, from_lang: str = 'mn', to_lang: str = 'zh'):
    """翻译模式"""
    engine = MongolianChatEngine()
    result = engine.translate(text, from_lang, to_lang)
    print(f"原文：{text}")
    print(f"翻译：{result}")


def main():
    parser = argparse.ArgumentParser(
        description='传统蒙古文 AI 助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 main.py                      # 交互模式
  python3 main.py --text "你好"         # 单次对话
  python3 main.py --translate "谢谢"    # 翻译
        """
    )
    
    parser.add_argument('--text', '-t', type=str, help='单次对话文本')
    parser.add_argument('--translate', type=str, help='翻译文本')
    parser.add_argument('--from', dest='from_lang', type=str, default='mn',
                       help='源语言 (mn=蒙古文，zh=中文)')
    parser.add_argument('--to', dest='to_lang', type=str, default='zh',
                       help='目标语言')
    
    args = parser.parse_args()
    
    if args.text:
        single_chat(args.text)
    elif args.translate:
        translate_mode(args.translate, args.from_lang, args.to_lang)
    else:
        interactive_mode()


if __name__ == '__main__':
    main()
