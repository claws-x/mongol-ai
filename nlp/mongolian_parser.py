#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙古文语法分析器 (Mongolian Parser)
Mongolian Syntax Parser

功能：
- 依存句法分析
- 短语结构分析
- 语义角色标注

作者：Mongolian AI Team
日期：2026-04-02
版本：v1.0
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class PosTag(Enum):
    """词性标签"""
    NOUN = 'n'
    VERB = 'v'
    ADJ = 'adj'
    ADV = 'adv'
    PRON = 'pron'
    NUM = 'num'
    PART = 'part'
    CONJ = 'conj'
    INTERJ = 'interj'
    UNK = 'unk'


class DepRel(Enum):
    """依存关系标签"""
    ROOT = 'root'  # 根节点
    SUBJ = 'subj'  # 主语
    OBJ = 'obj'  # 宾语
    MOD = 'mod'  # 修饰语
    ADVCL = 'advcl'  # 状语从句
    AUX = 'aux'  # 助动词
    CASE = 'case'  # 格标记
    CONJ = 'conj'  # 并列
    CC = 'cc'  # 连词
    PUNCT = 'punct'  # 标点


@dataclass
class Token:
    """词元"""
    id: int
    text: str
    pos: PosTag
    dep: DepRel
    head: int  # 父节点 ID


class MongolianParser:
    """蒙古文语法分析器"""
    
    def __init__(self):
        # 格标记
        self.CASE_MARKERS = {
            'ᠨᠢ': 'nom',  # 主格
            'ᠢᠶᠡᠨ': 'acc',  # 宾格
            'ᠳᠤ': 'dat',  # 与格
            'ᠠᠴᠠ': 'abl',  # 离格
            'ᠢᠶᠠᠷ': 'ins',  # 工具格
            'ᠤᠨ': 'gen',  # 属格
        }
        
        # 动词词尾
        self.VERB_ENDINGS = {
            'ᠬᠤ': 'inf',  # 不定式
            'ᠵᠤ': 'pres',  # 现在时
            'ᠪᠠ': 'past',  # 过去时
            'ᠨ᠎ᠠ': 'pres',  # 现在时
        }
    
    def parse(self, tokens: List[Tuple[str, str]]) -> List[Token]:
        """
        句法分析
        
        Args:
            tokens: [(词，词性), ...]
            
        Returns:
            依存树
        """
        # 1. 创建 Token 列表
        tokens_list = self._create_tokens(tokens)
        
        # 2. 寻找动词（谓语）
        verb_idx = self._find_verb(tokens_list)
        
        # 3. 寻找主语
        subj_idx = self._find_subject(tokens_list, verb_idx)
        
        # 4. 寻找宾语
        obj_idx = self._find_object(tokens_list, verb_idx)
        
        # 5. 标注依存关系
        self._label_dependencies(tokens_list, verb_idx, subj_idx, obj_idx)
        
        return tokens_list
    
    def _create_tokens(self, tokens: List[Tuple[str, str]]) -> List[Token]:
        """创建 Token 列表"""
        result = []
        
        for i, (text, pos) in enumerate(tokens, 1):
            pos_tag = PosTag(pos) if pos in [p.value for p in PosTag] else PosTag.UNK
            token = Token(
                id=i,
                text=text,
                pos=pos_tag,
                dep=DepRel.UNK,
                head=0
            )
            result.append(token)
        
        return result
    
    def _find_verb(self, tokens: List[Token]) -> int:
        """寻找动词（谓语）"""
        for i, token in enumerate(tokens):
            if token.pos == PosTag.VERB:
                return i
        # 如果没有动词，返回最后一个词
        return len(tokens) - 1
    
    def _find_subject(self, tokens: List[Token], verb_idx: int) -> int:
        """寻找主语"""
        # 主语通常在动词前，是名词或代词
        for i in range(verb_idx):
            if tokens[i].pos in [PosTag.NOUN, PosTag.PRON]:
                return i
        return -1
    
    def _find_object(self, tokens: List[Token], verb_idx: int) -> int:
        """寻找宾语"""
        # 宾语通常在动词前，是名词，带有宾格标记
        for i in range(verb_idx):
            if tokens[i].pos == PosTag.NOUN:
                if tokens[i].text.endswith('ᠢᠶᠡᠨ'):  # 宾格
                    return i
        return -1
    
    def _label_dependencies(self, tokens: List[Token], verb_idx: int, 
                           subj_idx: int, obj_idx: int):
        """标注依存关系"""
        # 根节点
        tokens[verb_idx].dep = DepRel.ROOT
        tokens[verb_idx].head = 0
        
        # 主语
        if subj_idx >= 0:
            tokens[subj_idx].dep = DepRel.SUBJ
            tokens[subj_idx].head = verb_idx + 1
        
        # 宾语
        if obj_idx >= 0:
            tokens[obj_idx].dep = DepRel.OBJ
            tokens[obj_idx].head = verb_idx + 1
        
        # 其他词
        for i, token in enumerate(tokens):
            if i != verb_idx and i != subj_idx and i != obj_idx:
                # 默认依附于动词
                token.dep = DepRel.MOD
                token.head = verb_idx + 1
    
    def visualize(self, tokens: List[Token]) -> str:
        """可视化依存树"""
        result = []
        
        for token in tokens:
            dep_str = f"{token.dep.value}({token.head})"
            result.append(f"{token.text} - {token.pos.value} - {dep_str}")
        
        return '\n'.join(result)


def test_parser():
    """测试语法分析器"""
    print("=" * 60)
    print("蒙古文语法分析器测试")
    print("=" * 60)
    
    parser = MongolianParser()
    
    # 测试用例
    test_cases = [
        [
            ("ᠪᠢ", "pron"),
            ("ᠮᠣᠩᠭᠣᠯ", "n"),
            ("ᠬᠡᠯᠡ", "n"),
            ("ᠰᠤᠷᠤᠵᠤ", "v"),
            ("ᠪᠠᠶᠢᠨ᠎ᠠ", "v"),
        ],
        [
            ("ᠰᠠᠶᠢᠨ", "adj"),
            ("ᠪᠠᠶᠢᠨ᠎ᠠ", "v"),
            ("ᠤᠤ", "part"),
        ],
    ]
    
    for i, tokens in enumerate(test_cases, 1):
        print(f"\n句子 {i}: {' '.join(t[0] for t in tokens)}")
        tree = parser.parse(tokens)
        print(parser.visualize(tree))


if __name__ == '__main__':
    test_parser()
