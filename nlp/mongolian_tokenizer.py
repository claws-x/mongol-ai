#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙古文分词器 (Mongolian Tokenizer)
Mongolian Language Tokenizer

功能：
- 基于规则的分词
- 基于统计的分词（待实现）
- 基于深度学习的分词（待实现）

作者：Mongolian AI Team
日期：2026-04-02
版本：v1.0
"""

import re
import json
from typing import List, Dict, Tuple
from collections import defaultdict


class MongolianTokenizer:
    """蒙古文分词器"""
    
    def __init__(self):
        # 蒙古文 Unicode 范围
        self.MONGOLIAN_RANGE = re.compile(r'[\u1800-\u18AF]+')
        
        # 标点符号
        self.PUNCTUATION = {
            '\u1800': '᠀',  # 逗号
            '\u1801': '᠁',  # 句号
            '\u1802': '᠂',  # 逗号变体
            '\u1803': '᠃',  # 句号变体
            '\u1804': '᠄',  # 冒号
            '\u1805': '᠅',  # 连字符
        }
        
        # 连接词
        self.CONJUNCTIONS = {
            'ᠪᠠ': '和/与',
            'ᠪᠣᠯ': '如果/成为',
            'ᠭᠡᠵᠦ': '说/称为',
            'ᠦ': '不/无',
            'ᠪᠢᠴᠢ': '包括',
        }
        
        # 助词
        self.PARTICLES = {
            'ᠤᠤ': '疑问词',
            'ᠨᠢ': '定冠词',
            'ᠢᠶᠡᠨ': '宾格',
            'ᠳᠤ': '与格',
            'ᠠᠴᠠ': '离格',
            'ᠢᠶᠠᠷ': '工具格',
            'ᠤᠨ': '属格',
        }
        
        # 加载词典（如果存在）
        self.dictionary = self._load_dictionary()
        
    def _load_dictionary(self) -> Dict:
        """加载蒙古文词典"""
        try:
            with open('data/mongolian_dictionary.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 返回基础词典
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
    
    def tokenize(self, text: str) -> List[str]:
        """
        分词主函数
        
        Args:
            text: 蒙古文文本
            
        Returns:
            分词结果列表
        """
        # 1. 检测是否包含蒙古文
        if not self.MONGOLIAN_RANGE.search(text):
            return [text]
        
        # 2. 基于规则分词
        tokens = self._rule_based_tokenize(text)
        
        # 3. 后处理
        tokens = self._post_process(tokens)
        
        return tokens
    
    def _rule_based_tokenize(self, text: str) -> List[str]:
        """
        基于规则的分词
        
        规则：
        1. 按空格分词
        2. 按标点分词
        3. 按连接词/助词分词
        """
        # 步骤 1: 按空格分割
        tokens = text.split()
        
        # 步骤 2: 分离标点
        result = []
        for token in tokens:
            # 检查是否包含标点
            has_punct = any(p in token for p in self.PUNCTUATION.keys())
            
            if has_punct:
                # 分离标点
                sub_tokens = self._split_punctuation(token)
                result.extend(sub_tokens)
            else:
                result.append(token)
        
        # 步骤 3: 分离连接词/助词
        final_result = []
        for token in result:
            if self.MONGOLIAN_RANGE.match(token):
                sub_tokens = self._split_affixes(token)
                final_result.extend(sub_tokens)
            else:
                final_result.append(token)
        
        return final_result
    
    def _split_punctuation(self, token: str) -> List[str]:
        """分离标点符号"""
        result = []
        current = ''
        
        for char in token:
            if char in self.PUNCTUATION.keys():
                if current:
                    result.append(current)
                    current = ''
                result.append(char)
            else:
                current += char
        
        if current:
            result.append(current)
        
        return result
    
    def _split_affixes(self, word: str) -> List[str]:
        """
        分离词缀（连接词/助词）
        
        蒙古语是粘着语，词缀附加在词干后
        """
        result = [word]  # 默认返回整个词
        
        # 检查常见词缀
        for affix in sorted(self.PARTICLES.keys(), key=len, reverse=True):
            if word.endswith(affix):
                stem = word[:-len(affix)]
                if stem:
                    result = [stem, affix]
                break
        
        return result
    
    def _post_process(self, tokens: List[str]) -> List[str]:
        """后处理：清理空字符串等"""
        return [t for t in tokens if t.strip()]
    
    def tokenize_with_pos(self, text: str) -> List[Tuple[str, str]]:
        """
        分词并标注词性
        
        Args:
            text: 蒙古文文本
            
        Returns:
            [(词，词性), ...]
        """
        tokens = self.tokenize(text)
        result = []
        
        for token in tokens:
            pos = self._guess_pos(token)
            result.append((token, pos))
        
        return result
    
    def _guess_pos(self, word: str) -> str:
        """猜测词性"""
        # 查词典
        if word in self.dictionary:
            return self.dictionary[word]['pos']
        
        # 基于词缀猜测
        if word in self.PARTICLES:
            return 'part'  # 助词
        
        if word in self.CONJUNCTIONS:
            return 'conj'  # 连接词
        
        # 基于词尾猜测
        if word.endswith('ᠬᠤ'):
            return 'v'  # 动词不定式
        
        if word.endswith('ᠨ'):
            return 'n'  # 名词
        
        # 默认
        return 'unk'
    
    def get_word_info(self, word: str) -> Optional[Dict]:
        """获取单词信息"""
        return self.dictionary.get(word)
    
    def add_to_dictionary(self, word: str, pos: str, meaning: str):
        """添加到词典"""
        self.dictionary[word] = {
            'pos': pos,
            'meaning': meaning
        }
    
    def save_dictionary(self, filepath: str):
        """保存词典"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.dictionary, f, ensure_ascii=False, indent=2)


def test_tokenizer():
    """测试分词器"""
    print("=" * 60)
    print("蒙古文分词器测试")
    print("=" * 60)
    
    tokenizer = MongolianTokenizer()
    
    # 测试用例
    test_cases = [
        "ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ",  # 你好吗
        "ᠪᠢ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ",  # 我在学蒙古语
        "ᠢᠮᠤ ᠰᠤᠷᠭᠠᠭᠤᠯᠢ",  # 内蒙古大学
        "ᠪᠠᠶᠠᠷᠲᠠᠢ",  # 谢谢
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {text}")
        print(f"分词：{tokenizer.tokenize(text)}")
        print(f"词性：{tokenizer.tokenize_with_pos(text)}")


if __name__ == '__main__':
    test_tokenizer()
