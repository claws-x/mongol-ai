#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙古文 NLP 工具链测试
Mongolian NLP Toolkit Test
"""

import sys
sys.path.insert(0, '..')

from mongolian_tokenizer import MongolianTokenizer
from mongolian_pos_tagger import MongolianPOSTagger
from mongolian_parser import MongolianParser


def test_full_pipeline():
    """测试完整 NLP 流程"""
    print("=" * 60)
    print("蒙古文 NLP 工具链完整测试")
    print("=" * 60)
    
    # 测试句子
    sentences = [
        "ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ？",
        "ᠪᠢ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ᠃",
        "ᠢᠮᠤ ᠰᠤᠷᠭᠠᠭᠤᠯᠢ ᠳ᠋ᠡᠭᠡ ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠰᠤᠷᠤᠬᠤ ᠪᠣᠯ ᠰᠠᠶᠢᠨ᠃",
        "ᠪᠠᠶᠠᠷᠲᠠᠢ！",
    ]
    
    # 初始化 NLP 工具
    tokenizer = MongolianTokenizer()
    tagger = MongolianPOSTagger()
    parser = MongolianParser()
    
    for i, sentence in enumerate(sentences, 1):
        print(f"\n{'='*60}")
        print(f"句子 {i}: {sentence}")
        print(f"{'='*60}")
        
        # 1. 分词
        print("\n1️⃣ 分词:")
        tokens = tokenizer.tokenize(sentence)
        print(f"   {' | '.join(tokens)}")
        
        # 2. 词性标注
        print("\n2️⃣ 词性标注:")
        tagged = tagger.tag(tokens)
        for word, pos in tagged:
            pos_name = tagger.POS_TAGS.get(pos, '未知')
            print(f"   {word} - {pos} ({pos_name})")
        
        # 3. 句法分析
        print("\n3️⃣ 句法分析:")
        tree = parser.parse(tagged)
        print(parser.visualize(tree))
        
        # 4. 句子结构
        print("\n4️⃣ 句子结构:")
        for token in tree:
            dep_name = token.dep.value
            head_idx = token.head - 1
            if head_idx >= 0 and head_idx < len(tree):
                head_word = tree[head_idx].text
                print(f"   {token.text} --[{dep_name}]--> {head_word}")
            else:
                print(f"   {token.text} --[{dep_name}]--> ROOT")


if __name__ == '__main__':
    test_full_pipeline()
