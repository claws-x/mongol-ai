#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙古文 AI 对话引擎
Mongolian AI Chat Engine

功能：
- 蒙古文对话
- 上下文管理
- 翻译辅助
- 文化知识
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 支持直接运行和模块导入
try:
    from .mongolian_text import MongolianTextProcessor
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from mongolian_text import MongolianTextProcessor


class MongolianChatEngine:
    """蒙古文对话引擎"""
    
    # 系统提示词
    SYSTEM_PROMPT = """
你是一位传统蒙古文 AI 助手，名为"蒙古助手" (Mongolian Assistant)。

你的特点：
1. 使用传统蒙古文（回鹘式蒙古文）交流
2. 了解蒙古历史文化、风俗习惯
3. 可以帮助学习蒙古文
4. 支持双语模式（蒙古文 + 中文）

回答原则：
- 优先使用蒙古文回复
- 复杂内容提供中文翻译
- 保持友好、专业的语气
- 尊重蒙古传统文化

常用问候：
- ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠤᠤ (你好)
- ᠪᠠᠶᠠᠷᠲᠠᠢ (谢谢)
- ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ (再见)
"""
    
    # 预定义回复（蒙古文 + 中文）
    PREDEFINED_RESPONSES = {
        'greeting': {
            'mongolian': 'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠤᠤ！ᠪᠢ ᠮᠣᠩᠭᠣᠯ AI ᠲᠠᠨᠢᠯᠴᠠᠭᠤᠯᠠᠭᠴᠢ ᠪᠠᠶᠢᠨ᠎ᠠ᠃ ᠲᠠᠨᠳ ᠲᠤᠰᠠᠯᠠᠭ᠎ᠠ ᠪᠠᠶᠢᠭ᠎ᠠ ᠤᠤ？',
            'chinese': '你好！我是蒙古 AI 助手。有什么可以帮您？',
        },
        'thanks': {
            'mongolian': 'ᠪᠠᠶᠠᠷᠲᠠᠢ！ᠮᠢᠨᠦ ᠲᠤᠰᠠᠯᠠᠭ᠎ᠠ ᠪᠣᠯᠤᠭᠰᠠᠨᠳᠠ ᠪᠠᠶᠠᠷᠯᠠᠭ᠎ᠠ ᠪᠠᠶᠢᠨ᠎ᠠ᠃',
            'chinese': '谢谢！很高兴能帮助您。',
        },
        'bye': {
            'mongolian': 'ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ！ᠳᠠᠷᠤᠢ ᠤᠳᠠ ᠤᠴᠢᠷᠠᠯᠴᠢᠶ᠎ᠠ᠃',
            'chinese': '再见！下次再聊。',
        },
        'help': {
            'mongolian': 'ᠪᠢ ᠲᠠᠨᠳ ᠳᠠᠷᠠᠬᠢ ᠮᠡᠳᠡᠭᠡᠯᠡᠯᠦᠦᠳᠡ ᠲᠤᠰᠠᠯᠠᠭ᠎ᠠ ᠪᠣᠯᠤᠭᠰᠠᠨᠳᠠ ᠪᠣᠯᠨᠠ：\n1. ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠬᠤ\n2. ᠮᠣᠩᠭᠣᠯ ᠲᠦᠬᠡ ᠲᠥᠷᠥᠭᠡ\n3. ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ ᠰᠤᠷᠤᠬᠤ\n4. ᠣᠷᠴᠢᠯᠠᠭᠰᠠᠨ ᠠᠰᠤᠭᠤᠯᠲᠠ',
            'chinese': '我可以在以下方面帮助您：\n1. 学习蒙古语\n2. 了解蒙古文化\n3. 学习蒙古文\n4. 回答问题',
        },
        'unknown': {
            'mongolian': 'ᠤᠴᠢᠷᠠᠯᠲᠠᠢ，ᠪᠢ ᠡᠨᠡ ᠠᠰᠤᠭᠤᠯᠲᠠᠳᠠ ᠬᠠᠷᠢᠤᠴᠠᠭᠤᠯᠠᠭᠰᠠᠨ ᠦᠭᠡᠢ᠃ ᠪᠣᠯ ᠨᠥᠭᠥᠭᠡᠯ ᠠᠰᠤᠭᠤᠨ᠎ᠠ ᠪᠢᠴᠢ ᠶᠠᠭᠤ ᠪᠣᠯᠤᠭᠰᠠᠨ ᠤᠤ？',
            'chinese': '抱歉，这个问题我还不太了解。您可以换个问题问我吗？',
        },
    }
    
    def __init__(self, data_dir: str = None):
        self.processor = MongolianTextProcessor()
        self.conversation_history = []
        self.max_history = 10
        
        # 加载语料数据
        if data_dir:
            self.corpus_dir = Path(data_dir)
            self.training_data = self._load_corpus()
        else:
            self.corpus_dir = None
            self.training_data = []
    
    def _load_corpus(self) -> List[Dict]:
        """加载蒙古文语料库"""
        corpus = []
        
        if self.corpus_dir and self.corpus_dir.exists():
            # 加载传统蒙古文数据
            for jsonl_file in self.corpus_dir.glob('traditional_mongolian_*.jsonl'):
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            corpus.append(record)
                        except:
                            continue
        
        return corpus
    
    def _detect_intent(self, user_input: str) -> str:
        """
        检测用户意图
        
        Args:
            user_input: 用户输入
            
        Returns:
            str: 意图类型
        """
        input_lower = user_input.lower()
        
        # 问候
        if any(word in input_lower for word in ['ᠰᠠᠶᠢᠨ', 'ᠮᠡᠨᠳᠡ', '你好', 'hello', 'hi']):
            return 'greeting'
        
        # 感谢
        if any(word in input_lower for word in ['ᠪᠠᠶᠠᠷᠲᠠᠢ', '谢谢', 'thank']):
            return 'thanks'
        
        # 告别
        if any(word in input_lower for word in ['ᠪᠠᠶᠠᠷ', '再见', 'bye', 'goodbye']):
            return 'bye'
        
        # 求助
        if any(word in input_lower for word in ['ᠲᠤᠰᠠᠯᠠᠭ᠎ᠠ', '帮助', 'help', '怎么']):
            return 'help'
        
        return 'unknown'
    
    def _generate_response(self, intent: str, user_input: str) -> Dict[str, str]:
        """
        生成回复
        
        Args:
            intent: 用户意图
            user_input: 用户输入
            
        Returns:
            dict: 回复内容
        """
        # 使用预定义回复
        if intent in self.PREDEFINED_RESPONSES:
            return self.PREDEFINED_RESPONSES[intent]
        
        # 对于未知意图，使用通用回复
        return self.PREDEFINED_RESPONSES['unknown']
    
    def chat(self, user_input: str, bilingual: bool = True) -> str:
        """
        对话主函数
        
        Args:
            user_input: 用户输入
            bilingual: 是否双语模式
            
        Returns:
            str: AI 回复
        """
        # 分析输入
        is_mongolian = self.processor.is_mongolian(user_input)
        intent = self._detect_intent(user_input)
        
        # 生成回复
        response = self._generate_response(intent, user_input)
        
        # 格式化输出
        if bilingual:
            output = f"{response['mongolian']}\n\n{response['chinese']}"
        else:
            output = response['mongolian'] if is_mongolian else response['chinese']
        
        # 保存对话历史
        self._add_to_history('user', user_input)
        self._add_to_history('assistant', output)
        
        return output
    
    def _add_to_history(self, role: str, content: str):
        """添加对话到历史"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # 限制历史记录长度
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
    
    def get_history(self) -> List[Dict]:
        """获取对话历史"""
        return self.conversation_history
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def translate(self, text: str, from_lang: str = 'mn', to_lang: str = 'zh') -> str:
        """
        翻译功能（简化版）
        
        Args:
            text: 待翻译文本
            from_lang: 源语言 (mn=蒙古文，zh=中文)
            to_lang: 目标语言
            
        Returns:
            str: 翻译结果
        """
        if from_lang == 'mn' and to_lang == 'zh':
            # 蒙古文转中文（查词典）
            words = text.split()
            translations = []
            for word in words:
                translation = self.processor.lookup_word(word)
                translations.append(translation if translation else word)
            return ' '.join(translations)
        
        elif from_lang == 'zh' and to_lang == 'mn':
            # 中文转蒙古文（反向查词典）
            reverse_dict = {v: k for k, v in self.processor.COMMON_WORDS.items()}
            words = text.split()
            translations = []
            for word in words:
                translation = reverse_dict.get(word, word)
                translations.append(translation)
            return ' '.join(translations)
        
        return text
    
    def get_word_info(self, word: str) -> Optional[Dict]:
        """
        获取词汇信息
        
        Args:
            word: 蒙古文单词
            
        Returns:
            dict: 词汇信息
        """
        meaning = self.processor.lookup_word(word)
        if meaning:
            return {
                'word': word,
                'meaning': meaning,
                'transliteration': self.processor.transliterate(word),
            }
        return None


# 测试函数
def test_chat_engine():
    """测试对话引擎"""
    print("=" * 60)
    print("蒙古文 AI 对话引擎 - 测试")
    print("=" * 60)
    
    engine = MongolianChatEngine()
    
    # 测试对话
    test_inputs = [
        "ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠤᠤ",
        "你好",
        "ᠪᠠᠶᠠᠷᠲᠠᠢ",
        "谢谢",
        "ᠲᠤᠰᠠᠯᠠᠭ᠎ᠠ",
        "再见",
    ]
    
    for input_text in test_inputs:
        print(f"\n用户：{input_text}")
        response = engine.chat(input_text, bilingual=True)
        print(f"AI: {response}")
        print("-" * 60)


if __name__ == '__main__':
    test_chat_engine()
