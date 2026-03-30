#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Auto-Learning System - AI 自动学习系统
Self-Driving AI for Mongolian Language Learning

功能：
- 自动语料收集
- 智能模型更新
- 用户行为分析
- 个性化推荐
- A/B 测试框架
- 性能自动优化

作者：OpenClaw Mongolian AI Team
日期：2026-03-30
版本：v4.0
"""

import json
import math
import random
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from datetime import datetime, timedelta


class AutoCorpusCollector:
    """自动语料收集器"""
    
    def __init__(self):
        self.corpus = []
        self.user_interactions = []
        self.error_corrections = []
    
    def collect_from_input(self, input_text: str, output_text: str):
        """从用户输入收集语料"""
        self.corpus.append({
            'input': input_text,
            'output': output_text,
            'timestamp': datetime.now().isoformat(),
            'type': 'input_output_pair',
        })
    
    def collect_correction(self, wrong: str, correct: str):
        """收集纠错数据"""
        self.error_corrections.append({
            'wrong': wrong,
            'correct': correct,
            'timestamp': datetime.now().isoformat(),
        })
    
    def collect_interaction(self, user_action: str, ai_response: str, feedback: Optional[str] = None):
        """收集交互数据"""
        self.user_interactions.append({
            'user_action': user_action,
            'ai_response': ai_response,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat(),
        })
    
    def get_training_data(self, limit: int = 1000) -> List[Dict]:
        """获取训练数据"""
        # 优先使用纠错数据
        training_data = self.error_corrections[:limit // 2]
        
        # 补充交互数据
        training_data.extend(self.user_interactions[:limit // 2])
        
        return training_data
    
    def export_corpus(self, filepath: str):
        """导出语料库"""
        data = {
            'corpus': self.corpus,
            'corrections': self.error_corrections,
            'interactions': self.user_interactions,
            'export_time': datetime.now().isoformat(),
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class IntelligentModelUpdater:
    """智能模型更新器"""
    
    def __init__(self):
        self.model_version = '1.0.0'
        self.last_update = datetime.now()
        self.update_history = []
        self.performance_metrics = defaultdict(list)
    
    def evaluate_performance(self, predictions: List[Tuple[str, str]]) -> Dict:
        """
        评估模型性能
        
        Args:
            predictions: [(预测，实际), ...]
        """
        if not predictions:
            return {'accuracy': 0.0}
        
        correct = sum(1 for pred, actual in predictions if pred == actual)
        accuracy = correct / len(predictions)
        
        self.performance_metrics['accuracy'].append(accuracy)
        
        return {
            'accuracy': accuracy,
            'total': len(predictions),
            'correct': correct,
        }
    
    def should_update(self) -> bool:
        """判断是否需要更新模型"""
        # 距离上次更新超过 24 小时
        if datetime.now() - self.last_update > timedelta(hours=24):
            return True
        
        # 性能下降超过 10%
        if len(self.performance_metrics['accuracy']) >= 2:
            recent = self.performance_metrics['accuracy'][-1]
            previous = self.performance_metrics['accuracy'][-2]
            if previous - recent > 0.1:
                return True
        
        return False
    
    def update_model(self, new_data: List[Dict]) -> Dict:
        """更新模型"""
        # 模拟模型更新
        self.model_version = f"{float(self.model_version) + 0.1:.1f}"
        self.last_update = datetime.now()
        
        self.update_history.append({
            'version': self.model_version,
            'data_size': len(new_data),
            'timestamp': datetime.now().isoformat(),
        })
        
        return {
            'success': True,
            'new_version': self.model_version,
            'data_used': len(new_data),
        }


class UserBehaviorAnalyzer:
    """用户行为分析器"""
    
    def __init__(self):
        self.user_profiles = {}
        self.typing_patterns = defaultdict(list)
        self.error_patterns = defaultdict(int)
    
    def analyze_typing_speed(self, user_id: str, inputs: List[Dict]) -> Dict:
        """分析打字速度"""
        if not inputs:
            return {'wpm': 0, 'accuracy': 0}
        
        total_chars = sum(len(inp.get('text', '')) for inp in inputs)
        total_time = len(inputs) * 10  # 假设每次输入 10 秒
        
        wpm = (total_chars / 5) / (total_time / 60)  # 词/分钟
        accuracy = 0.85  # 模拟值
        
        self.user_profiles[user_id] = {
            'typing_speed': wpm,
            'accuracy': accuracy,
            'total_inputs': len(inputs),
        }
        
        return {
            'wpm': wpm,
            'accuracy': accuracy,
        }
    
    def detect_error_patterns(self, user_id: str, errors: List[Dict]) -> List[str]:
        """检测错误模式"""
        common_errors = []
        
        for error in errors:
            pattern = f"{error.get('wrong', '')} -> {error.get('correct', '')}"
            self.error_patterns[pattern] += 1
        
        # 找出最常见的错误
        for pattern, count in sorted(self.error_patterns.items(), key=lambda x: x[1], reverse=True)[:5]:
            if count >= 3:
                common_errors.append(pattern)
        
        return common_errors
    
    def generate_recommendations(self, user_id: str) -> List[str]:
        """生成个性化推荐"""
        recommendations = []
        
        profile = self.user_profiles.get(user_id, {})
        
        # 基于打字速度推荐
        if profile.get('typing_speed', 0) < 20:
            recommendations.append('建议练习常用词汇')
        
        # 基于准确率推荐
        if profile.get('accuracy', 0) < 0.8:
            recommendations.append('建议学习语法规则')
        
        return recommendations


class ABTestFramework:
    """A/B 测试框架"""
    
    def __init__(self):
        self.tests = {}
        self.results = defaultdict(lambda: {'a': [], 'b': []})
    
    def create_test(self, test_id: str, variant_a: Dict, variant_b: Dict):
        """创建 A/B 测试"""
        self.tests[test_id] = {
            'variant_a': variant_a,
            'variant_b': variant_b,
            'started_at': datetime.now().isoformat(),
            'status': 'running',
        }
    
    def assign_variant(self, test_id: str, user_id: str) -> str:
        """分配变体"""
        # 简单的哈希分配
        hash_value = hash(f"{test_id}_{user_id}") % 2
        return 'a' if hash_value == 0 else 'b'
    
    def record_result(self, test_id: str, variant: str, metric: float):
        """记录结果"""
        self.results[test_id][variant].append(metric)
    
    def get_winner(self, test_id: str) -> Optional[str]:
        """确定获胜者"""
        if test_id not in self.results:
            return None
        
        a_avg = sum(self.results[test_id]['a']) / len(self.results[test_id]['a']) if self.results[test_id]['a'] else 0
        b_avg = sum(self.results[test_id]['b']) / len(self.results[test_id]['b']) if self.results[test_id]['b'] else 0
        
        return 'a' if a_avg > b_avg else 'b'


class PerformanceAutoOptimizer:
    """性能自动优化器"""
    
    def __init__(self):
        self.metrics = {
            'response_time': [],
            'memory_usage': [],
            'prediction_accuracy': [],
        }
        self.optimization_history = []
    
    def monitor(self, metric_name: str, value: float):
        """监控指标"""
        if metric_name in self.metrics:
            self.metrics[metric_name].append(value)
            
            # 保留最近 100 个数据点
            if len(self.metrics[metric_name]) > 100:
                self.metrics[metric_name] = self.metrics[metric_name][-100:]
    
    def detect_bottleneck(self) -> Optional[str]:
        """检测性能瓶颈"""
        if not self.metrics['response_time']:
            return None
        
        avg_response = sum(self.metrics['response_time']) / len(self.metrics['response_time'])
        
        if avg_response > 500:  # 超过 500ms
            return 'response_time'
        
        return None
    
    def optimize(self, bottleneck: str) -> Dict:
        """自动优化"""
        optimizations = {
            'response_time': '启用缓存 + 减少计算',
            'memory_usage': '清理未使用数据',
            'prediction_accuracy': '更新模型',
        }
        
        self.optimization_history.append({
            'bottleneck': bottleneck,
            'action': optimizations.get(bottleneck, '未知'),
            'timestamp': datetime.now().isoformat(),
        })
        
        return {
            'success': True,
            'bottleneck': bottleneck,
            'action': optimizations.get(bottleneck),
        }


class AIDrivenSystem:
    """AI 驱动系统（主类）"""
    
    def __init__(self):
        self.corpus_collector = AutoCorpusCollector()
        self.model_updater = IntelligentModelUpdater()
        self.user_analyzer = UserBehaviorAnalyzer()
        self.ab_test = ABTestFramework()
        self.optimizer = PerformanceAutoOptimizer()
        
        self.system_stats = {
            'total_inputs': 0,
            'total_corrections': 0,
            'model_updates': 0,
            'ab_tests_running': 0,
        }
    
    def process_input(self, user_id: str, input_text: str) -> Dict:
        """处理用户输入（AI 驱动）"""
        start_time = datetime.now()
        
        # 1. 自动学习
        self.corpus_collector.collect_from_input(input_text, '')
        self.system_stats['total_inputs'] += 1
        
        # 2. 用户行为分析
        typing_speed = self.user_analyzer.analyze_typing_speed(
            user_id, 
            [{'text': input_text}]
        )
        
        # 3. 性能监控
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        self.optimizer.monitor('response_time', response_time)
        
        # 4. 模型更新检查
        if self.model_updater.should_update():
            training_data = self.corpus_collector.get_training_data()
            update_result = self.model_updater.update_model(training_data)
            self.system_stats['model_updates'] += 1
        
        return {
            'input': input_text,
            'typing_speed': typing_speed,
            'response_time': response_time,
            'model_version': self.model_updater.model_version,
        }
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            'stats': self.system_stats,
            'model_version': self.model_updater.model_version,
            'last_update': self.model_updater.last_update.isoformat(),
            'performance': {
                'avg_response_time': sum(self.optimizer.metrics['response_time']) / len(self.optimizer.metrics['response_time']) if self.optimizer.metrics['response_time'] else 0,
            },
        }


# 测试函数
def test_ai_driven_system():
    """测试 AI 驱动系统"""
    print("=" * 60)
    print("AI 驱动系统 V4 - 测试")
    print("=" * 60)
    
    system = AIDrivenSystem()
    
    # 测试 1: 处理输入
    print("\n测试 1: 处理用户输入")
    result = system.process_input('user123', 'ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ')
    print(f"输入：ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ")
    print(f"响应时间：{result['response_time']:.2f}ms")
    
    # 测试 2: 系统状态
    print("\n测试 2: 系统状态")
    status = system.get_system_status()
    print(f"状态：{json.dumps(status, indent=2, ensure_ascii=False)}")
    
    # 测试 3: A/B 测试
    print("\n测试 3: A/B 测试")
    system.ab_test.create_test('prediction_algo', {'name': 'v1'}, {'name': 'v2'})
    variant = system.ab_test.assign_variant('prediction_algo', 'user123')
    print(f"分配变体：{variant}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    test_ai_driven_system()
