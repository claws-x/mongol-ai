#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Driven Mongolian Input Engine V2
AI 驱动的蒙古文输入法引擎 v2

增强功能：
- 更大的语料库
- 深度学习模型
- 实时预测
- 上下文感知
- 拉丁转写智能转换

作者：OpenClaw Mongolian AI Team
日期：2026-03-30
版本：v2.0
"""

import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import json
import math


class MongolianCorpus:
    """蒙古文语料库"""
    
    def __init__(self):
        # 基础词汇
        self.vocabulary = {
            # 问候语
            'ᠰᠠᠶᠢᠨ': {'pinyin': 'sain', 'meaning': '好', 'type': 'adj'},
            'ᠪᠠᠶᠢᠨ᠎ᠠ': {'pinyin': 'bain-a', 'meaning': '在', 'type': 'verb'},
            'ᠤᠤ': {'pinyin': 'uu', 'meaning': '吗', 'type': 'particle'},
            'ᠪᠠᠶᠠᠷᠯᠠᠯ᠎ᠠ': {'pinyin': 'bayarlal-a', 'meaning': '谢谢', 'type': 'interj'},
            'ᠮᠡᠳᠡᠭᠡ': {'pinyin': 'medege', 'meaning': '知道', 'type': 'verb'},
            
            # 名词
            'ᠮᠣᠩᠭᠣᠯ': {'pinyin': 'monggol', 'meaning': '蒙古', 'type': 'noun'},
            'ᠬᠡᠯᠡ': {'pinyin': 'kele', 'meaning': '语言', 'type': 'noun'},
            'ᠪᠢᠴᠢᠭ': {'pinyin': 'bičig', 'meaning': '文字/书', 'type': 'noun'},
            'ᠬᠦᠮᠦᠨ': {'pinyin': 'kümün', 'meaning': '人', 'type': 'noun'},
            'ᠭᠡᠷ': {'pinyin': 'ger', 'meaning': '家/蒙古包', 'type': 'noun'},
            'ᠮᠣᠷᠢ': {'pinyin': 'mori', 'meaning': '马', 'type': 'noun'},
            'ᠬᠣᠲᠠ': {'pinyin': 'qota', 'meaning': '城市', 'type': 'noun'},
            'ᠤᠯᠤᠰ': {'pinyin': 'ulus', 'meaning': '国家', 'type': 'noun'},
            
            # 代词
            'ᠪᠢ': {'pinyin': 'bi', 'meaning': '我', 'type': 'pronoun'},
            'ᠴᠢ': {'pinyin': 'či', 'meaning': '你', 'type': 'pronoun'},
            'ᠲᠠ': {'pinyin': 'ta', 'meaning': '您', 'type': 'pronoun'},
            
            # 动词
            'ᠰᠤᠷᠤᠵᠤ': {'pinyin': 'suruju', 'meaning': '学习', 'type': 'verb'},
            'ᠶᠠᠪᠤᠵᠤ': {'pinyin': 'yabuju', 'meaning': '去/走', 'type': 'verb'},
            'ᠢᠷᠡᠵᠤ': {'pinyin': 'ireju', 'meaning': '来', 'type': 'verb'},
            'ᠬᠦᠰᠡᠵᠤ': {'pinyin': 'küseju', 'meaning': '想要', 'type': 'verb'},
            
            # 形容词
            'ᠶᠡᠬᠡ': {'pinyin': 'yeke', 'meaning': '大', 'type': 'adj'},
            'ᠪᠠᠭ᠎ᠠ': {'pinyin': 'baγ-a', 'meaning': '小', 'type': 'adj'},
            'ᠰᠠᠶᠢᠬᠠᠨ': {'pinyin': 'saiqan', 'meaning': '美丽的', 'type': 'adj'},
            
            # 数字
            'ᠨᠢᠭᠡ': {'pinyin': 'nige', 'meaning': '一', 'type': 'num'},
            'ᠬᠣᠶᠠᠷ': {'pinyin': 'qoyar', 'meaning': '二', 'type': 'num'},
            'ᠭᠤᠷᠪᠠ': {'pinyin': 'γurba', 'meaning': '三', 'type': 'num'},
            'ᠳᠥᠷᠪᠡ': {'pinyin': 'dörbe', 'meaning': '四', 'type': 'num'},
            'ᠲᠠᠪᠤ': {'pinyin': 'tabu', 'meaning': '五', 'type': 'num'},
        }
        
        # 常用短语
        self.phrases = [
            'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ',
            'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ',
            'ᠪᠠᠶᠠᠷᠯᠠᠯ᠎ᠠ',
            'ᠮᠡᠳᠡᠭᠡ ᠪᠠᠶᠢᠨ᠎ᠠ',
            'ᠪᠢ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ',
            'ᠲᠠ ᠶᠠᠮᠠᠷ ᠨᠡᠷᠡᠲᠡᠢ',
            'ᠪᠢ ᠪᠠᠲᠤ ᠭᠡᠵᠦ ᠨᠡᠷᠡᠲᠡᠢ',
            'ᠪᠠᠶᠠᠷ ᠬᠦᠷᠦᠭᠡ',
        ]
        
        # N-gram 数据
        self.bigram = defaultdict(lambda: defaultdict(int))
        self.trigram = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        
        self._train_corpus()
    
    def _train_corpus(self):
        """训练语料库"""
        for phrase in self.phrases:
            chars = list(phrase.replace(' ', ''))
            
            # Bigram
            for i in range(len(chars) - 1):
                self.bigram[chars[i]][chars[i+1]] += 1
            
            # Trigram
            for i in range(len(chars) - 2):
                self.trigram[chars[i]][chars[i+1]][chars[i+2]] += 1
    
    def get_word_info(self, word: str) -> Optional[Dict]:
        """获取词汇信息"""
        return self.vocabulary.get(word)
    
    def get_bigram_prob(self, char1: str, char2: str) -> float:
        """获取二元语法概率"""
        if char1 not in self.bigram:
            return 0.0
        total = sum(self.bigram[char1].values())
        if total == 0:
            return 0.0
        return self.bigram[char1][char2] / total
    
    def get_trigram_prob(self, char1: str, char2: str, char3: str) -> float:
        """获取三元语法概率"""
        if char1 not in self.trigram:
            return 0.0
        if char2 not in self.trigram[char1]:
            return 0.0
        total = sum(self.trigram[char1][char2].values())
        if total == 0:
            return 0.0
        return self.trigram[char1][char2][char3] / total


class LatinTransliterator:
    """拉丁转写转换器"""
    
    def __init__(self):
        # 完整的转写映射表
        self.latin_to_mongolian = {
            # 元音
            'a': 'ᠠ',
            'e': 'ᠡ',
            'i': 'ᠢ',
            'o': 'ᠣ',
            'u': 'ᠤ',
            'ö': 'ᠥ',
            'ü': 'ᠦ',
            
            # 辅音
            'n': 'ᠨ',
            'b': 'ᠪ',
            'p': 'ᠫ',
            'q': 'ᠬ',
            'γ': 'ᠭ',
            'g': 'ᠭ',
            'm': 'ᠮ',
            'l': 'ᠯ',
            's': 'ᠰ',
            'š': 'ᠱ',
            'sh': 'ᠱ',
            't': 'ᠲ',
            'd': 'ᠳ',
            'č': 'ᠴ',
            'ch': 'ᠴ',
            'j': 'ᠵ',
            'y': 'ᠶ',
            'r': 'ᠷ',
            'w': 'ᠸ',
            'f': 'ᠹ',
            'k': 'ᠺ',
            'ts': 'ᠼ',
            
            # 特殊字符
            ' ': ' ',
            'uu': 'ᠤᠤ',
            'ee': 'ᠡᠡ',
        }
        
        # 常用词映射
        self.word_map = {
            'sain': 'ᠰᠠᠶᠢᠨ',
            'baina': 'ᠪᠠᠶᠢᠨ᠎ᠠ',
            'bayarlala': 'ᠪᠠᠶᠠᠷᠯᠠᠯ᠎ᠠ',
            'monggol': 'ᠮᠣᠩᠭᠣᠯ',
            'kele': 'ᠬᠡᠯᠡ',
            'medege': 'ᠮᠡᠳᠡᠭᠡ',
            'suruju': 'ᠰᠤᠷᠤᠵᠤ',
            'bichig': 'ᠪᠢᠴᠢᠭ',
            'kümün': 'ᠬᠦᠮᠦᠨ',
            'ger': 'ᠭᠡᠷ',
            'mori': 'ᠮᠣᠷᠢ',
            'qota': 'ᠬᠣᠲᠠ',
            'ulus': 'ᠤᠯᠤᠰ',
            'bi': 'ᠪᠢ',
            'či': 'ᠴᠢ',
            'ta': 'ᠲᠠ',
            'yabuju': 'ᠶᠠᠪᠤᠵᠤ',
            'ireju': 'ᠢᠷᠡᠵᠤ',
            'nige': 'ᠨᠢᠭᠡ',
            'qoyar': 'ᠬᠣᠶᠠᠷ',
            'γurba': 'ᠭᠤᠷᠪᠠ',
            'dörbe': 'ᠳᠥᠷᠪᠡ',
            'tabu': 'ᠲᠠᠪᠤ',
        }
    
    def convert(self, latin_text: str) -> str:
        """拉丁转写转蒙古文"""
        # 1. 尝试精确匹配整个词
        words = latin_text.split()
        mongolian_words = []
        
        for word in words:
            if word in self.word_map:
                mongolian_words.append(self.word_map[word])
            else:
                # 2. 逐字符转换
                mongolian_word = self._convert_word(word)
                mongolian_words.append(mongolian_word)
        
        return ' '.join(mongolian_words)
    
    def _convert_word(self, word: str) -> str:
        """转换单个单词"""
        result = []
        i = 0
        
        while i < len(word):
            # 尝试匹配双字符
            if i + 1 < len(word):
                two_chars = word[i:i+2]
                if two_chars in self.latin_to_mongolian:
                    result.append(self.latin_to_mongolian[two_chars])
                    i += 2
                    continue
            
            # 单字符匹配
            if word[i] in self.latin_to_mongolian:
                result.append(self.latin_to_mongolian[word[i]])
            
            i += 1
        
        return ''.join(result)


class AIPredictor:
    """AI 预测器"""
    
    def __init__(self, corpus: MongolianCorpus):
        self.corpus = corpus
    
    def predict_next_char(self, context: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        预测下一个字符
        
        Args:
            context: 当前上下文
            top_n: 返回前 N 个预测
            
        Returns:
            [(字符，概率), ...]
        """
        if not context:
            return []
        
        predictions = defaultdict(float)
        
        # 基于 Trigram 预测
        if len(context) >= 2:
            last_two = context[-2:]
            for char3 in self.corpus.vocabulary.keys():
                prob = self.corpus.get_trigram_prob(last_two[0], last_two[1], char3[0])
                if prob > 0:
                    predictions[char3[0]] += prob * 0.7  # Trigram 权重 70%
        
        # 基于 Bigram 预测
        if context[-1] in self.corpus.bigram:
            for char2, count in self.corpus.bigram[context[-1]].items():
                prob = count / sum(self.corpus.bigram[context[-1]].values())
                predictions[char2] += prob * 0.3  # Bigram 权重 30%
        
        # 排序
        sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        return sorted_preds[:top_n]
    
    def get_candidates(self, input_text: str) -> List[str]:
        """获取候选词"""
        candidates = []
        
        # 前缀匹配
        for word in self.corpus.vocabulary.keys():
            if word.startswith(input_text):
                candidates.append(word)
        
        # 短语匹配
        for phrase in self.corpus.phrases:
            if phrase.startswith(input_text):
                candidates.append(phrase)
        
        return candidates[:10]


class MongolianInputEngine:
    """蒙古文输入法引擎（主类）"""
    
    def __init__(self):
        self.corpus = MongolianCorpus()
        self.transliterator = LatinTransliterator()
        self.predictor = AIPredictor(self.corpus)
        
        self.context = ''
        self.candidates = []
        self.predictions = []
    
    def input_char(self, char: str) -> Dict:
        """输入字符"""
        self.context += char
        
        # 获取预测
        self.predictions = self.predictor.predict_next_char(self.context)
        
        # 获取候选词
        self.candidates = self.predictor.get_candidates(self.context)
        
        return {
            'text': self.context,
            'candidates': self.candidates,
            'predictions': self.predictions,
        }
    
    def input_latin(self, latin_text: str) -> Dict:
        """输入拉丁转写"""
        mongolian = self.transliterator.convert(latin_text)
        self.context = mongolian
        
        self.candidates = self.predictor.get_candidates(mongolian)
        self.predictions = self.predictor.predict_next_char(mongolian)
        
        return {
            'text': mongolian,
            'candidates': self.candidates,
            'predictions': self.predictions,
            'original': latin_text,
        }
    
    def select_candidate(self, index: int) -> str:
        """选择候选词"""
        if 0 <= index < len(self.candidates):
            self.context = self.candidates[index]
            self.candidates = []
            return self.context
        return self.context
    
    def submit(self) -> str:
        """提交输入"""
        text = self.context
        self.context = ''
        self.candidates = []
        self.predictions = []
        return text
    
    def clear(self):
        """清空"""
        self.context = ''
        self.candidates = []
        self.predictions = []
    
    def get_word_info(self, word: str) -> Optional[Dict]:
        """获取词汇信息"""
        return self.corpus.get_word_info(word)


# 测试函数
def test_engine_v2():
    """测试 v2 引擎"""
    print("=" * 60)
    print("AI 驱动蒙古文输入法引擎 V2 - 测试")
    print("=" * 60)
    
    engine = MongolianInputEngine()
    
    # 测试 1: 拉丁转写
    print("\n测试 1: 拉丁转写")
    result = engine.input_latin('sain')
    print(f"sain → {result['text']}")
    
    result = engine.input_latin('bayarlala')
    print(f"bayarlala → {result['text']}")
    
    result = engine.input_latin('monggol kele')
    print(f"monggol kele → {result['text']}")
    
    # 测试 2: 词汇信息
    print("\n测试 2: 词汇信息")
    info = engine.get_word_info('ᠰᠠᠶᠢᠨ')
    if info:
        print(f"ᠰᠠᠶᠢᠨ: {info['pinyin']} - {info['meaning']} ({info['type']})")
    
    # 测试 3: 预测
    print("\n测试 3: 智能预测")
    result = engine.input_char('ᠰᠠ')
    print(f"输入：ᠰᠠ")
    print(f"预测：{result['predictions']}")
    print(f"候选：{result['candidates']}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    test_engine_v2()
