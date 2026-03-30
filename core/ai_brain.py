#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Brain - 蒙古文 AI 大脑
AI Brain for Mongolian Language Processing

高级功能：
- 深度学习预测
- 上下文理解
- 语法检查
- 自动纠错
- 用户习惯学习
- 智能推荐

作者：OpenClaw Mongolian AI Team
日期：2026-03-30
版本：v3.0
"""

import json
import math
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class NeuralPredictor:
    """神经预测器（模拟）"""
    
    def __init__(self):
        # 加载预训练权重（简化版）
        self.weights = {
            'ᠰ': {'ᠠ': 0.8, 'ᠡ': 0.1, 'ᠢ': 0.05, 'ᠣ': 0.03, 'ᠤ': 0.02},
            'ᠪ': {'ᠠ': 0.7, 'ᠡ': 0.2, 'ᠢ': 0.05, 'ᠣ': 0.03, 'ᠤ': 0.02},
            'ᠮ': {'ᠣ': 0.6, 'ᠡ': 0.2, 'ᠠ': 0.1, 'ᠤ': 0.05, 'ᠥ': 0.05},
        }
    
    def predict(self, context: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        神经预测
        
        Args:
            context: 上下文
            top_n: 返回前 N 个预测
            
        Returns:
            [(字符，置信度), ...]
        """
        if not context or context[-1] not in self.weights:
            return []
        
        last_char = context[-1]
        predictions = self.weights.get(last_char, {})
        
        # 排序
        sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        return sorted_preds[:top_n]


class GrammarChecker:
    """语法检查器"""
    
    def __init__(self):
        # 元音和谐规则
        self.vowel_harmony = {
            'positive': {'ᠠ', 'ᠣ', 'ᠤ'},
            'negative': {'ᠡ', 'ᠥ', 'ᠦ'},
            'neutral': {'ᠢ'},
        }
        
        # 常见语法错误模式
        self.error_patterns = {
            'ᠪᠠᠶᠢᠨ᠎ᠠᠤᠤ': 'ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ',  # 缺少空格
            'ᠰᠠᠶᠢᠨᠪᠠᠶᠢᠨ᠎ᠠ': 'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ',  # 缺少空格
        }
    
    def check(self, text: str) -> List[Dict]:
        """
        检查语法错误
        
        Returns:
            [错误位置，错误类型，建议修正]
        """
        errors = []
        
        # 检查常见错误
        for wrong, correct in self.error_patterns.items():
            if wrong in text:
                errors.append({
                    'position': text.find(wrong),
                    'type': 'spacing',
                    'wrong': wrong,
                    'correct': correct,
                })
        
        # 检查元音和谐
        errors.extend(self._check_vowel_harmony(text))
        
        return errors
    
    def _check_vowel_harmony(self, text: str) -> List[Dict]:
        """检查元音和谐"""
        errors = []
        
        # 简化实现：检测明显的元音和谐错误
        all_vowels = set()
        for vowel_set in self.vowel_harmony.values():
            all_vowels.update(vowel_set)
        
        vowels = [char for char in text if char in all_vowels]
        
        if not vowels:
            return errors
        
        # 检测阳性 + 阴性混合
        has_positive = any(v in self.vowel_harmony['positive'] for v in vowels)
        has_negative = any(v in self.vowel_harmony['negative'] for v in vowels)
        
        if has_positive and has_negative:
            errors.append({
                'position': 0,
                'type': 'vowel_harmony',
                'message': '可能存在元音和谐错误',
            })
        
        return errors
    
    def auto_correct(self, text: str) -> str:
        """自动纠错"""
        corrected = text
        
        for wrong, correct in self.error_patterns.items():
            corrected = corrected.replace(wrong, correct)
        
        return corrected


class UserHabitLearner:
    """用户习惯学习器"""
    
    def __init__(self):
        self.user_history = []
        self.frequent_words = defaultdict(int)
        self.frequent_phrases = defaultdict(int)
        self.typing_patterns = defaultdict(list)
    
    def learn(self, input_text: str, output_text: str):
        """学习用户输入"""
        self.user_history.append({
            'input': input_text,
            'output': output_text,
            'timestamp': datetime.now().isoformat(),
        })
        
        # 统计常用词
        words = input_text.split()
        for word in words:
            self.frequent_words[word] += 1
        
        # 统计常用短语
        if len(words) > 1:
            phrase = ' '.join(words[:3])
            self.frequent_phrases[phrase] += 1
    
    def get_recommendations(self, context: str) -> List[str]:
        """基于用户习惯推荐"""
        recommendations = []
        
        # 推荐常用词
        for word, count in sorted(self.frequent_words.items(), key=lambda x: x[1], reverse=True)[:5]:
            if word.startswith(context):
                recommendations.append(word)
        
        return recommendations
    
    def get_typing_speed(self) -> float:
        """计算打字速度"""
        if len(self.user_history) < 2:
            return 0.0
        
        # 简化实现
        return len(self.user_history) * 10  # 字符/分钟


class ContextualAI:
    """上下文 AI"""
    
    def __init__(self):
        self.conversation_history = []
        self.current_topic = None
        self.formality_level = 'neutral'  # formal, neutral, informal
    
    def add_message(self, role: str, text: str):
        """添加对话到历史"""
        self.conversation_history.append({
            'role': role,
            'text': text,
            'timestamp': datetime.now().isoformat(),
        })
        
        # 检测话题
        self._detect_topic(text)
    
    def _detect_topic(self, text: str):
        """检测当前话题"""
        topic_keywords = {
            'greeting': ['ᠰᠠᠶᠢᠨ', 'ᠮᠡᠨᠳᠡ', 'ᠪᠠᠶᠠᠷᠲᠠᠢ'],
            'learning': ['ᠰᠤᠷᠤᠵᠤ', 'ᠬᠡᠯᠡ', 'ᠪᠢᠴᠢᠭ'],
            'question': ['ᠤᠤ', 'ᠶᠠᠮᠠᠷ', 'ᠬᠡᠨ'],
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text for kw in keywords):
                self.current_topic = topic
                break
    
    def get_context_aware_response(self, input_text: str) -> str:
        """基于上下文的智能回复"""
        # 基于话题回复
        if self.current_topic == 'greeting':
            return 'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ！ᠲᠠ ᠶᠠᠮᠠᠷ ᠠᠰᠤᠭᠤᠯᠲᠠᠢ？'
        elif self.current_topic == 'learning':
            return 'ᠮᠡᠳᠡᠭᠡ ᠪᠠᠶᠢᠨ᠎ᠠ！ᠪᠢ ᠲᠠᠨᠳ ᠲᠤᠰᠠᠯᠠᠭ᠎ᠠ ᠪᠣᠯᠨᠠ᠃'
        elif self.current_topic == 'question':
            return 'ᠰᠠᠶᠢᠨ ᠠᠰᠤᠭᠤᠯᠲᠠ！ᠪᠢ ᠬᠠᠷᠢᠤᠴᠠᠭᠤᠯᠠᠵᠤ ᠪᠠᠶᠢᠨ᠎ᠠ᠃'
        else:
            return 'ᠮᠡᠳᠡᠭᠡ ᠪᠠᠶᠢᠨ᠎ᠠ！'
    
    def get_conversation_summary(self) -> Dict:
        """获取对话摘要"""
        return {
            'total_messages': len(self.conversation_history),
            'current_topic': self.current_topic,
            'formality_level': self.formality_level,
        }


class MongolianAIBrain:
    """蒙古文 AI 大脑（主类）"""
    
    def __init__(self):
        self.neural_predictor = NeuralPredictor()
        self.grammar_checker = GrammarChecker()
        self.user_learner = UserHabitLearner()
        self.contextual_ai = ContextualAI()
        
        # 统计
        self.stats = {
            'predictions': 0,
            'corrections': 0,
            'learning_rate': 0.0,
        }
    
    def process_input(self, input_text: str) -> Dict:
        """
        处理用户输入
        
        Returns:
            {
                'text': 处理后的文本，
                'predictions': 预测，
                'corrections': 纠错建议，
                'recommendations': 推荐，
            }
        """
        # 1. 语法检查
        errors = self.grammar_checker.check(input_text)
        corrected_text = self.grammar_checker.auto_correct(input_text)
        
        if corrected_text != input_text:
            self.stats['corrections'] += 1
        
        # 2. AI 预测
        predictions = self.neural_predictor.predict(corrected_text)
        self.stats['predictions'] += len(predictions)
        
        # 3. 用户习惯推荐
        recommendations = self.user_learner.get_recommendations(corrected_text)
        
        # 4. 上下文理解
        self.contextual_ai.add_message('user', corrected_text)
        
        return {
            'text': corrected_text,
            'predictions': predictions,
            'corrections': errors,
            'recommendations': recommendations,
            'context': self.contextual_ai.get_conversation_summary(),
        }
    
    def generate_response(self, input_text: str) -> str:
        """生成 AI 回复"""
        # 基于上下文生成回复
        response = self.contextual_ai.get_context_aware_response(input_text)
        
        # 学习用户输入
        self.user_learner.learn(input_text, response)
        
        # 更新统计
        self.stats['learning_rate'] = self.user_learner.get_typing_speed()
        
        return response
    
    def get_stats(self) -> Dict:
        """获取 AI 统计"""
        return {
            **self.stats,
            'user_history_length': len(self.user_learner.user_history),
            'frequent_words_count': len(self.user_learner.frequent_words),
        }


# 测试函数
def test_ai_brain():
    """测试 AI 大脑"""
    print("=" * 60)
    print("蒙古文 AI 大脑 V3 - 测试")
    print("=" * 60)
    
    brain = MongolianAIBrain()
    
    # 测试 1: 语法检查
    print("\n测试 1: 语法检查")
    result = brain.process_input('ᠰᠠᠶᠢᠨᠪᠠᠶᠢᠨ᠎ᠠ')
    print(f"输入：ᠰᠠᠶᠢᠨᠪᠠᠶᠢᠨ᠎ᠠ")
    print(f"纠错：{result['corrections']}")
    
    # 测试 2: AI 预测
    print("\n测试 2: AI 预测")
    result = brain.process_input('ᠰᠠ')
    print(f"输入：ᠰᠠ")
    print(f"预测：{result['predictions']}")
    
    # 测试 3: 对话
    print("\n测试 3: 智能对话")
    response = brain.generate_response('ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ？')
    print(f"用户：ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠤ？")
    print(f"AI: {response}")
    
    # 测试 4: 统计
    print("\n测试 4: AI 统计")
    stats = brain.get_stats()
    print(f"统计：{stats}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    test_ai_brain()
