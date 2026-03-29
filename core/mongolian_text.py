#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
传统蒙古文文本处理模块
Mongolian Text Processing Module

支持：
- 传统蒙古文 Unicode 范围：U+1800 - U+18AF
- 文本规范化
- 字符验证
- 词法分析
"""

import re
from typing import List, Dict, Tuple, Optional


class MongolianTextProcessor:
    """传统蒙古文文本处理器"""
    
    # 传统蒙古文 Unicode 范围
    MONGOLIAN_RANGE = re.compile(r'[\u1800-\u18AF]+')
    
    # 蒙古文标点符号
    MONGOLIAN_PUNCTUATION = {
        '\u1800': '᠀',  # 蒙古文逗号
        '\u1801': '᠁',  # 蒙古文句号
        '\u1802': '᠂',  # 蒙古文逗号变体
        '\u1803': '᠃',  # 蒙古文冒号
        '\u1804': '᠄',  # 蒙古文破折号
        '\u1805': '᠅',  # 蒙古文连字符
    }
    
    # 常用蒙古文字符映射（简化）
    COMMON_CHARACTERS = {
        'ᠠ': 'a', 'ᠡ': 'e', 'ᠢ': 'i', 'ᠣ': 'o', 'ᠤ': 'u', 'ᠥ': 'ö', 'ᠦ': 'ü',
        'ᠨ': 'n', 'ᠪ': 'b', 'ᠭ': 'g', 'ᠬ': 'q', 'ᠮ': 'm', 'ᠯ': 'l',
        'ᠰ': 's', 'ᠲ': 't', 'ᠴ': 'č', 'ᠶ': 'y', 'ᠷ': 'r', 'ᠸ': 'w',
        'ᠹ': 'f', 'ᠺ': 'k', 'ᠻ': 'ḳ', 'ᠼ': 'ts', 'ᠽ': 'dz', 'ᠾ': 'ž',
        'ᠿ': 'ǰ', 'ᡀ': 'y', 'ᡁ': 'ng',
    }
    
    # 常用蒙古文词汇
    COMMON_WORDS = {
        'ᠮᠣᠩᠭᠣᠯ': '蒙古',
        'ᠪᠢᠴᠢᠭ': '文字/书',
        'ᠬᠡᠯᠡ': '语言',
        'ᠰᠠᠶᠢᠨ': '好',
        'ᠪᠠᠶᠠᠷᠲᠠᠢ': '谢谢',
        'ᠪᠠᠶᠢᠨ᠎ᠤᠤ': '在吗/你好',
        'ᠮᠡᠨᠳᠡ': '你好',
        'ᠲᠠᠰ': '您',
        'ᠪᠢ': '我',
        'ᠡᠴᠢ': '父亲',
        'ᠡᠬᠡ': '母亲',
        'ᠭᠡᠷ': '家/蒙古包',
        'ᠮᠣᠷᠢ': '马',
        'ᠬᠣᠨᠢ': '羊',
        'ᠲᠡᠭᠡᠭᠡᠰᠦ': '车',
        'ᠤᠳᠠ': '水',
        'ᠢᠳᠡᠭᠡ': '食物',
        'ᠠᠵᠢᠯ': '工作',
        'ᠨᠤᠲᠤᠭ': '地方/国家',
        'ᠡᠷᠲᠡ': '古代/传统',
        'ᠵᠣᠬᠢᠶᠠᠯ': '生活',
        'ᠴᠢᠨᠭᠢᠰ': '成吉思',
        'ᠬᠠᠭᠠᠨ': '汗/可汗',
    }
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    def is_mongolian(self, text: str) -> bool:
        """
        判断文本是否包含传统蒙古文
        
        Args:
            text: 输入文本
            
        Returns:
            bool: 是否包含蒙古文
        """
        matches = self.MONGOLIAN_RANGE.findall(text)
        return len(''.join(matches)) >= 3
    
    def extract_mongolian(self, text: str) -> str:
        """
        提取文本中的蒙古文部分
        
        Args:
            text: 输入文本
            
        Returns:
            str: 蒙古文部分
        """
        matches = self.MONGOLIAN_RANGE.findall(text)
        return ' '.join(matches)
    
    def normalize(self, text: str) -> str:
        """
        规范化蒙古文文本
        
        Args:
            text: 输入文本
            
        Returns:
            str: 规范化后的文本
        """
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 统一标点符号
        for code, char in self.MONGOLIAN_PUNCTUATION.items():
            text = text.replace(code, char)
        
        return text
    
    def count_characters(self, text: str) -> Dict[str, int]:
        """
        统计字符数量
        
        Args:
            text: 输入文本
            
        Returns:
            dict: 字符统计
        """
        mongolian_chars = self.extract_mongolian(text)
        
        stats = {
            'total': len(text),
            'mongolian': len(mongolian_chars.replace(' ', '')),
            'words': len(text.split())
        }
        
        return stats
    
    def transliterate(self, text: str) -> str:
        """
        蒙古文转写为拉丁字母（简化版）
        
        Args:
            text: 蒙古文文本
            
        Returns:
            str: 拉丁转写
        """
        result = text
        for mongolian, latin in self.COMMON_CHARACTERS.items():
            result = result.replace(mongolian, latin)
        return result
    
    def lookup_word(self, word: str) -> Optional[str]:
        """
        查询蒙古文词汇含义
        
        Args:
            word: 蒙古文单词
            
        Returns:
            str: 中文含义，如果未找到返回 None
        """
        return self.COMMON_WORDS.get(word)
    
    def get_common_phrases(self) -> List[Dict[str, str]]:
        """
        获取常用蒙古文短语
        
        Returns:
            list: 短语列表
        """
        phrases = [
            {'mongolian': 'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠤᠤ', 'chinese': '你好', 'pinyin': 'sain bain uu'},
            {'mongolian': 'ᠪᠠᠶᠠᠷᠲᠠᠢ', 'chinese': '谢谢', 'pinyin': 'bayartai'},
            {'mongolian': 'ᠮᠡᠨᠳᠡ', 'chinese': '你好', 'pinyin': 'mende'},
            {'mongolian': 'ᠪᠢ ᠴᠢᠮᠠᠶᠢ ᠬᠠᠢᠷᠲᠠᠢ', 'chinese': '我爱你', 'pinyin': 'bi chimayi khairtai'},
            {'mongolian': 'ᠰᠠᠶᠢᠨ ᠦᠳᠡᠬᠡ', 'chinese': '晚安', 'pinyin': 'sain udehe'},
            {'mongolian': 'ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ', 'chinese': '再见', 'pinyin': 'bayar khuruuge'},
            {'mongolian': 'ᠲᠠ ᠰᠠᠶᠢᠨ ᠤᠤ', 'chinese': '你好吗', 'pinyin': 'ta sain uu'},
            {'mongolian': 'ᠪᠢ ᠰᠠᠶᠢᠨ', 'chinese': '我很好', 'pinyin': 'bi sain'},
        ]
        return phrases
    
    def analyze_text(self, text: str) -> Dict:
        """
        分析蒙古文文本
        
        Args:
            text: 输入文本
            
        Returns:
            dict: 分析结果
        """
        result = {
            'is_mongolian': self.is_mongolian(text),
            'mongolian_content': self.extract_mongolian(text),
            'character_count': self.count_characters(text),
            'normalized': self.normalize(text),
            'transliteration': self.transliterate(self.extract_mongolian(text)),
        }
        
        return result


# 测试函数
def test_mongolian_processor():
    """测试蒙古文处理器"""
    processor = MongolianTextProcessor()
    
    print("=" * 60)
    print("传统蒙古文文本处理器 - 测试")
    print("=" * 60)
    
    # 测试文本
    test_texts = [
        "ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ (蒙古文)",
        "ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠤᠤ - 你好",
        "Hello ᠮᠣᠩᠭᠣᠯ World",
        "ᠪᠠᠶᠠᠷᠲᠠᠢ - 谢谢",
    ]
    
    for text in test_texts:
        print(f"\n输入：{text}")
        analysis = processor.analyze_text(text)
        print(f"  包含蒙古文：{'✅' if analysis['is_mongolian'] else '❌'}")
        print(f"  蒙古文内容：{analysis['mongolian_content']}")
        print(f"  转写：{analysis['transliteration']}")
        print(f"  字符数：{analysis['character_count']}")
    
    # 显示常用短语
    print("\n" + "=" * 60)
    print("常用蒙古文短语")
    print("=" * 60)
    phrases = processor.get_common_phrases()
    for phrase in phrases:
        print(f"  {phrase['mongolian']}")
        print(f"    中文：{phrase['chinese']}")
        print(f"    拼音：{phrase['pinyin']}")
        print()


if __name__ == '__main__':
    test_mongolian_processor()
