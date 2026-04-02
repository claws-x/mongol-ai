#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙古文词性标注器 (Mongolian POS Tagger)
Mongolian Part-of-Speech Tagger

功能：
- 基于规则的词性标注
- 基于 HMM 的词性标注（待实现）
- 基于深度学习的词性标注（待实现）

作者：Mongolian AI Team
日期：2026-04-02
版本：v1.0
"""

import json
from typing import List, Dict, Tuple
from collections import defaultdict


class MongolianPOSTagger:
    """蒙古文词性标注器"""
    
    def __init__(self):
        # 词性标签集
        self.POS_TAGS = {
            'n': '名词 (Noun)',
            'v': '动词 (Verb)',
            'adj': '形容词 (Adjective)',
            'adv': '副词 (Adverb)',
            'prep': '后置词 (Postposition)',
            'conj': '连词 (Conjunction)',
            'part': '助词 (Particle)',
            'pron': '代词 (Pronoun)',
            'num': '数词 (Numeral)',
            'interj': '感叹词 (Interjection)',
            'unk': '未知 (Unknown)',
        }
        
        # 加载词典
        self.dictionary = self._load_dictionary()
        
        # 词缀规则
        self.affix_rules = self._load_affix_rules()
    
    def _load_dictionary(self) -> Dict:
        """加载词典"""
        try:
            with open('data/mongolian_dictionary.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'ᠰᠠᠶᠢᠨ': {'pos': 'adj', 'meaning': '好'},
                'ᠪᠠᠶᠢᠨ᠎ᠠ': {'pos': 'v', 'meaning': '在'},
                'ᠮᠣᠩᠭᠣᠯ': {'pos': 'n', 'meaning': '蒙古'},
                'ᠬᠡᠯᠡ': {'pos': 'n', 'meaning': '语言'},
                'ᠪᠢᠴᠢᠭ': {'pos': 'n', 'meaning': '文字/书'},
                'ᠰᠤᠷᠤᠬᠤ': {'pos': 'v', 'meaning': '学习'},
                'ᠪᠠᠶᠠᠷᠲᠠᠢ': {'pos': 'interj', 'meaning': '谢谢'},
                'ᠮᠡᠨᠳᠡ': {'pos': 'interj', 'meaning': '你好'},
                'ᠪᠢ': {'pos': 'pron', 'meaning': '我'},
                'ᠴᠢ': {'pos': 'pron', 'meaning': '你'},
                'ᠲᠠ': {'pos': 'pron', 'meaning': '您'},
                'ᠢᠮᠤ': {'pos': 'n', 'meaning': '内蒙古大学'},
                'ᠰᠤᠷᠭᠠᠭᠤᠯᠢ': {'pos': 'n', 'meaning': '学校'},
                'ᠰᠤᠷᠭᠠᠭᠴᠢ': {'pos': 'n', 'meaning': '学生'},
                'ᠪᠠᠭᠰᠢ': {'pos': 'n', 'meaning': '老师'},
                'ᠨᠣᠮ': {'pos': 'n', 'meaning': '书'},
            }
    
    def _load_affix_rules(self) -> Dict:
        """加载词缀规则"""
        return {
            # 动词词缀
            'ᠬᠤ': 'v',  # 不定式
            'ᠵᠤ': 'v',  # 现在时
            'ᠪᠠ': 'v',  # 过去时
            
            # 名词词缀
            'ᠨ': 'n',  # 主格
            'ᠢᠶᠡᠨ': 'n',  # 宾格
            'ᠳᠤ': 'n',  # 与格
            'ᠠᠴᠠ': 'n',  # 离格
            'ᠢᠶᠠᠷ': 'n',  # 工具格
            'ᠤᠨ': 'n',  # 属格
            
            # 助词
            'ᠤᠤ': 'part',  # 疑问
            'ᠨᠢ': 'part',  # 定冠
        }
    
    def tag(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """
        词性标注
        
        Args:
            tokens: 分词结果
            
        Returns:
            [(词，词性), ...]
        """
        result = []
        
        for token in tokens:
            pos = self._tag_token(token)
            result.append((token, pos))
        
        return result
    
    def _tag_token(self, token: str) -> str:
        """标注单个词"""
        # 1. 查词典
        if token in self.dictionary:
            return self.dictionary[token]['pos']
        
        # 2. 查词缀规则
        for affix, pos in sorted(self.affix_rules.items(), key=lambda x: len(x[0]), reverse=True):
            if token.endswith(affix):
                stem = token[:-len(affix)]
                if stem and stem in self.dictionary:
                    return self.dictionary[stem]['pos']
                else:
                    return pos
        
        # 3. 基于规则猜测
        pos = self._guess_pos_by_rules(token)
        if pos:
            return pos
        
        # 4. 默认未知
        return 'unk'
    
    def _guess_pos_by_rules(self, word: str) -> Optional[str]:
        """基于规则猜测词性"""
        # 动词：以 ᠬᠤ, ᠵᠤ, ᠪᠠ 结尾
        if word.endswith('ᠬᠤ') or word.endswith('ᠵᠤ') or word.endswith('ᠪᠠ'):
            return 'v'
        
        # 形容词：以 ᠨ 结尾（部分）
        if word.endswith('ᠨ') and len(word) > 2:
            return 'adj'
        
        # 代词：短词
        if word in ['ᠪᠢ', 'ᠴᠢ', 'ᠲᠠ', 'ᠪᠢᠳ', 'ᠲᠠᠰ']:
            return 'pron'
        
        # 数词
        if word in ['ᠨᠢᠭᠡ', 'ᠬᠣᠶᠠᠷ', 'ᠭᠤᠷᠪᠠ', 'ᠳᠥᠷᠪᠡ', 'ᠲᠠᠪᠤ']:
            return 'num'
        
        # 感叹词
        if word in ['ᠪᠠᠶᠠᠷᠲᠠᠢ', 'ᠮᠡᠨᠳᠡ', 'ᠤᠴᠢᠷᠠᠯᠴᠢᠶ᠎ᠡ']:
            return 'interj'
        
        return None
    
    def tag_sentence(self, text: str) -> List[Tuple[str, str, str]]:
        """
        标注整个句子
        
        Args:
            text: 蒙古文句子
            
        Returns:
            [(词，词性，释义), ...]
        """
        # 导入分词器
        from mongolian_tokenizer import MongolianTokenizer
        tokenizer = MongolianTokenizer()
        
        # 分词
        tokens = tokenizer.tokenize(text)
        
        # 词性标注
        tagged = self.tag(tokens)
        
        # 添加释义
        result = []
        for token, pos in tagged:
            meaning = self.dictionary.get(token, {}).get('meaning', '')
            result.append((token, pos, meaning))
        
        return result


def test_pos_tagger():
    """测试词性标注器"""
    print("=" * 60)
    print("蒙古文词性标注器测试")
    print("=" * 60)
    
    tagger = MongolianPOSTagger()
    
    # 测试用例
    test_cases = [
        "ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ",
        "ᠪᠢ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ",
        "ᠢᠮᠤ ᠰᠤᠷᠭᠠᠭᠤᠯᠢ ᠳ᠋ᠡᠭᠡ ᠰᠤᠷᠭᠠᠭᠴᠢ ᠪᠠᠶᠢᠨ᠎ᠠ",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n句子 {i}: {text}")
        result = tagger.tag_sentence(text)
        for word, pos, meaning in result:
            print(f"  {word} - {pos} - {meaning}")


if __name__ == '__main__':
    test_pos_tagger()
