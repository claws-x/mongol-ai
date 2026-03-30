#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Driven Mongolian Input Engine
AI 驱动的蒙古文输入法引擎

基于 Unicode 标准和 AI 预测算法
实现智能蒙古文输入

作者：OpenClaw Mongolian AI Team
日期：2026-03-30
版本：v1.0
"""

import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import json


class UnicodeMongolianHandler:
    """Unicode 蒙古文编码处理器"""
    
    # Unicode 范围
    MONGOLIAN_RANGE = range(0x1800, 0x18AF + 1)
    
    # 元音字母
    VOWELS = {
        'ᠠ': 'a',  # U+1820
        'ᠡ': 'e',  # U+1821
        'ᠢ': 'i',  # U+1822
        'ᠣ': 'o',  # U+1823
        'ᠤ': 'u',  # U+1824
        'ᠥ': 'ö',  # U+1825
        'ᠦ': 'ü',  # U+1826
    }
    
    # 辅音字母
    CONSONANTS = {
        'ᠨ': 'n', 'ᠪ': 'b', 'ᠫ': 'p', 'ᠬ': 'q', 'ᠭ': 'γ',
        'ᠮ': 'm', 'ᠯ': 'l', 'ᠰ': 's', 'ᠱ': 'š', 'ᠲ': 't',
        'ᠳ': 'd', 'ᠴ': 'č', 'ᠵ': 'j', 'ᠶ': 'y', 'ᠷ': 'r',
        'ᠸ': 'w', 'ᠹ': 'f', 'ᠺ': 'k', 'ᠻ': 'ḳ', 'ᠼ': 'ts',
    }
    
    # FVS (自由变体选择符)
    FVS = {
        '\u180B': 'FVS1',
        '\u180C': 'FVS2',
        '\u180D': 'FVS3',
    }
    
    def is_mongolian_char(self, char: str) -> bool:
        """判断字符是否为蒙古文"""
        return ord(char) in self.MONGOLIAN_RANGE
    
    def extract_vowels(self, text: str) -> List[str]:
        """提取文本中的元音"""
        return [char for char in text if char in self.VOWELS]
    
    def detect_vowel_harmony(self, word: str) -> str:
        """
        检测元音和谐类型
        
        Returns:
            'positive' (阳性), 'negative' (阴性), 'neutral' (中性)
        """
        vowels = self.extract_vowels(word)
        
        positive_vowels = {'ᠠ', 'ᠣ', 'ᠤ'}
        negative_vowels = {'ᠡ', 'ᠥ', 'ᠦ'}
        
        has_positive = any(v in positive_vowels for v in vowels)
        has_negative = any(v in negative_vowels for v in vowels)
        
        if has_positive and not has_negative:
            return 'positive'
        elif has_negative and not has_positive:
            return 'negative'
        else:
            return 'neutral'
    
    def to_latin(self, mongolian_text: str) -> str:
        """蒙古文转拉丁转写"""
        result = []
        for char in mongolian_text:
            if char in self.VOWELS:
                result.append(self.VOWELS[char])
            elif char in self.CONSONANTS:
                result.append(self.CONSONANTS[char])
            else:
                result.append(char)
        return ''.join(result)


class MongolianPredictor:
    """蒙古文智能预测器"""
    
    def __init__(self):
        self.unicode_handler = UnicodeMongolianHandler()
        
        # N-gram 模型（简化版）
        self.bigram = defaultdict(lambda: defaultdict(int))
        self.trigram = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        
        # 词汇表
        self.vocabulary = self._load_vocabulary()
        
        # 训练语料（示例）
        self._train_sample_data()
    
    def _load_vocabulary(self) -> Dict[str, List[str]]:
        """加载基础词汇表"""
        return {
            'ᠰ': ['ᠰᠠᠶᠢᠨ', 'ᠰᠤᠷᠤᠵᠤ', 'ᠰᠡᠳᠬᠢᠯ'],
            'ᠪ': ['ᠪᠠᠶᠢᠨ᠎ᠠ', 'ᠪᠠᠶᠠᠷᠯᠠᠯ᠎ᠠ', 'ᠪᠢᠴᠢᠭ'],
            'ᠮ': ['ᠮᠣᠩᠭᠣᠯ', 'ᠮᠡᠳᠡᠭᠡ', 'ᠮᠣᠷᠢ'],
            'ᠬ': ['ᠬᠡᠯᠡ', 'ᠬᠦᠮᠦᠨ', 'ᠬᠣᠲᠠ'],
            'ᠤ': ['ᠤᠤ', 'ᠤᠨᠴᠢᠭ', 'ᠤᠯᠤᠰ'],
        }
    
    def _train_sample_data(self):
        """训练示例数据"""
        sample_texts = [
            'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ',
            'ᠪᠠᠶᠠᠷᠯᠠᠯ᠎ᠠ',
            'ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ',
            'ᠪᠢ ᠰᠤᠷᠤᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ',
            'ᠮᠡᠳᠡᠭᠡ ᠪᠠᠶᠢᠨ᠎ᠠ',
        ]
        
        for text in sample_texts:
            chars = list(text.replace(' ', ''))
            
            # 训练 Bigram
            for i in range(len(chars) - 1):
                self.bigram[chars[i]][chars[i+1]] += 1
            
            # 训练 Trigram
            for i in range(len(chars) - 2):
                self.trigram[chars[i]][chars[i+1]][chars[i+2]] += 1
    
    def predict_next_char(self, context: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        预测下一个字符
        
        Args:
            context: 当前输入上下文
            top_n: 返回前 N 个预测结果
            
        Returns:
            [(字符，概率), ...]
        """
        if not context:
            return []
        
        # 基于 Trigram 预测
        if len(context) >= 2:
            last_two = context[-2:]
            if last_two[0] in self.trigram and last_two[1] in self.trigram[last_two[0]]:
                predictions = self.trigram[last_two[0]][last_two[1]]
                total = sum(predictions.values())
                
                if total > 0:
                    sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
                    return [(char, count / total) for char, count in sorted_preds[:top_n]]
        
        # 基于 Bigram 预测
        if context[-1] in self.bigram:
            predictions = self.bigram[context[-1]]
            total = sum(predictions.values())
            
            if total > 0:
                sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
                return [(char, count / total) for char, count in sorted_preds[:top_n]]
        
        # 基于词汇表预测
        last_char = context[-1]
        if last_char in self.vocabulary:
            words = self.vocabulary[last_char]
            return [(word[0] if len(word) > len(context) else '᠂', 0.5) for word in words[:top_n]]
        
        return []
    
    def get_candidates(self, input_text: str) -> List[str]:
        """
        获取候选词
        
        Args:
            input_text: 输入文本（蒙古文或拉丁转写）
            
        Returns:
            候选词列表
        """
        # 如果是拉丁转写，先转换
        if not self.unicode_handler.is_mongolian_char(input_text[0]):
            input_text = self.latin_to_mongolian(input_text)
        
        # 查找匹配的词汇
        candidates = []
        for words in self.vocabulary.values():
            for word in words:
                if word.startswith(input_text):
                    candidates.append(word)
        
        return candidates[:10]
    
    def latin_to_mongolian(self, latin_text: str) -> str:
        """
        拉丁转写转蒙古文（简化版）
        
        TODO: 实现完整的转写规则
        """
        transliteration_map = {
            'sain': 'ᠰᠠᠶᠢᠨ',
            'baina': 'ᠪᠠᠶᠢᠨ᠎ᠠ',
            'uu': 'ᠤᠤ',
            'bayarlala': 'ᠪᠠᠶᠠᠷᠯᠠᠯ᠎ᠠ',
            'monggol': 'ᠮᠣᠩᠭᠣᠯ',
            'kele': 'ᠬᠡᠯᠡ',
            'medege': 'ᠮᠡᠳᠡᠭᠡ',
            'suruju': 'ᠰᠤᠷᠤᠵᠤ',
        }
        
        # 精确匹配
        if latin_text in transliteration_map:
            return transliteration_map[latin_text]
        
        # 分词匹配
        words = latin_text.split()
        mongolian_words = []
        for word in words:
            if word in transliteration_map:
                mongolian_words.append(transliteration_map[word])
            else:
                # TODO: 规则转换
                mongolian_words.append(word)
        
        return ' '.join(mongolian_words)


class MongolianCorrector:
    """蒙古文自动纠错器"""
    
    def __init__(self):
        self.unicode_handler = UnicodeMongolianHandler()
    
    def correct(self, text: str) -> str:
        """
        纠正文本错误
        
        1. 检查元音和谐
        2. 规范化 FVS
        3. 检查连写
        """
        # 1. 规范化空格
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 2. 规范化 FVS（移除多余的 FVS）
        text = self._normalize_fvs(text)
        
        # 3. 检查元音和谐（警告级别，不自动修改）
        # vowel_harmony_ok = self._check_vowel_harmony(text)
        
        return text
    
    def _normalize_fvs(self, text: str) -> str:
        """规范化 FVS 使用"""
        # 简化实现：移除孤立的 FVS
        result = []
        prev_char = None
        
        for char in text:
            if char in self.unicode_handler.FVS:
                # 如果前一个字符不是蒙古文，跳过 FVS
                if prev_char and self.unicode_handler.is_mongolian_char(prev_char):
                    result.append(char)
            else:
                result.append(char)
                prev_char = char
        
        return ''.join(result)


class AIInputEngine:
    """AI 驱动的蒙古文输入法引擎"""
    
    def __init__(self):
        self.unicode_handler = UnicodeMongolianHandler()
        self.predictor = MongolianPredictor()
        self.corrector = MongolianCorrector()
        
        # 当前输入上下文
        self.context = ''
        
        # 候选词
        self.candidates = []
    
    def input_char(self, char: str) -> Dict:
        """
        输入字符
        
        Returns:
            {
                'text': 当前文本，
                'candidates': 候选词，
                'predictions': 预测字符，
            }
        """
        # 更新上下文
        self.context += char
        
        # 获取预测
        predictions = self.predictor.predict_next_char(self.context)
        
        # 获取候选词
        self.candidates = self.predictor.get_candidates(self.context)
        
        return {
            'text': self.context,
            'candidates': self.candidates,
            'predictions': predictions,
        }
    
    def select_candidate(self, index: int) -> str:
        """选择候选词"""
        if 0 <= index < len(self.candidates):
            self.context = self.candidates[index]
            self.candidates = []
            return self.context
        return self.context
    
    def submit(self) -> str:
        """提交当前输入"""
        text = self.corrector.correct(self.context)
        self.context = ''
        self.candidates = []
        return text
    
    def clear(self):
        """清空输入"""
        self.context = ''
        self.candidates = []


# 测试函数
def test_engine():
    """测试输入法引擎"""
    print("=" * 60)
    print("AI 驱动蒙古文输入法引擎 - 测试")
    print("=" * 60)
    
    engine = AIInputEngine()
    
    # 测试 1: 输入蒙古文
    print("\n测试 1: 输入蒙古文")
    result = engine.input_char('ᠰ')
    print(f"输入：ᠰ")
    print(f"预测：{result['predictions']}")
    print(f"候选：{result['candidates']}")
    
    # 测试 2: 继续输入
    result = engine.input_char('ᠠ')
    print(f"\n输入：ᠠ")
    print(f"当前：{result['text']}")
    print(f"候选：{result['candidates']}")
    
    # 测试 3: 拉丁转写
    print("\n测试 3: 拉丁转写")
    mongolian = engine.predictor.latin_to_mongolian('sain')
    print(f"sain → {mongolian}")
    
    mongolian = engine.predictor.latin_to_mongolian('bayarlala')
    print(f"bayarlala → {mongolian}")
    
    # 测试 4: 提交
    print("\n测试 4: 提交")
    submitted = engine.submit()
    print(f"提交：{submitted}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    test_engine()
