#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音输入模块 - 支持用户语音说话
Voice Input Module - Speech to Text

使用 macOS 自带语音识别或 Google Speech Recognition
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path
from typing import Optional


class VoiceInput:
    """语音输入处理器"""
    
    def __init__(self, language: str = 'zh-CN'):
        """
        初始化语音输入
        
        Args:
            language: 语言代码 (zh-CN=中文，mn=蒙古文)
        """
        self.language = language
        self.is_macos = sys.platform == 'darwin'
        
        # 蒙古语语音支持有限，暂时用中文识别
        if language == 'mn':
            print("⚠️  蒙古语语音识别支持有限，将使用中文识别")
            self.language = 'zh-CN'
    
    def listen_macos(self, duration: int = 10) -> Optional[str]:
        """
        使用 macOS 自带语音识别
        
        Args:
            duration: 录音时长（秒）
            
        Returns:
            str: 识别的文本，失败返回 None
        """
        if not self.is_macos:
            return None
        
        print(f"🎤 正在录音... (最多 {duration} 秒，说完按 Ctrl+C)")
        
        try:
            # 使用 macOS say 命令的逆向方案 - 使用系统录音
            # macOS 没有内置 STT，使用临时方案
            
            # 方案 1: 使用系统音频录制
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_file.close()
            
            # 使用 rec 或 arecord 录制（需要安装）
            try:
                # 尝试使用 sox 的 rec 命令
                result = subprocess.run(
                    ['rec', '-r', '16000', '-c', '1', temp_file.name, 'trim', '0', str(duration)],
                    capture_output=True,
                    timeout=duration + 5
                )
                
                if result.returncode == 0:
                    # 使用 Google Speech API 识别（需要网络连接）
                    text = self._recognize_with_google(temp_file.name)
                    os.unlink(temp_file.name)
                    return text
            except FileNotFoundError:
                print("⚠️  'rec' 命令未找到，请安装 sox: brew install sox")
            except Exception as e:
                print(f"⚠️  录音失败：{e}")
            finally:
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
            
            # 方案 2: 降级到文本输入
            print("💡 降级到文本输入模式")
            return None
            
        except KeyboardInterrupt:
            print("\n⏹️  录音已停止")
            return None
        except Exception as e:
            print(f"❌ 语音输入错误：{e}")
            return None
    
    def _recognize_with_google(self, audio_file: str) -> Optional[str]:
        """
        使用 Google Speech Recognition API
        
        需要安装：pip3 install SpeechRecognition pyaudio
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            str: 识别结果
        """
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            
            # 使用 Google 免费 API
            text = recognizer.recognize_google(audio, language=self.language)
            return text
            
        except ImportError:
            print("⚠️  需要安装语音识别库：pip3 install SpeechRecognition pyaudio")
            return None
        except Exception as e:
            print(f"⚠️  识别失败：{e}")
            return None
    
    def listen_keyboard(self) -> str:
        """
        键盘输入（语音不可用时的降级方案）
        
        Returns:
            str: 用户输入的文本
        """
        try:
            user_input = input("🎤 您 (语音/文字): ").strip()
            return user_input
        except KeyboardInterrupt:
            return ""
    
    def listen(self, use_voice: bool = True) -> str:
        """
        监听用户输入（语音或文字）
        
        Args:
            use_voice: 是否尝试语音输入
            
        Returns:
            str: 用户输入
        """
        if use_voice:
            # 尝试语音输入
            text = self.listen_macos()
            if text:
                print(f"👂 识别结果：{text}")
                return text
            else:
                # 降级到键盘输入
                return self.listen_keyboard()
        else:
            return self.listen_keyboard()


class SimpleVoiceInput:
    """
    简化版语音输入
    使用 macOS 听写功能（需要用户手动触发）
    """
    
    def __init__(self):
        self.is_macos = sys.platform == 'darwin'
    
    def listen_with_macos_dictation(self) -> str:
        """
        使用 macOS 系统听写
        
        使用方法：
        1. 按 Fn 键两次（或设置的听写快捷键）
        2. 说话
        3. 文本会自动输入到输入框
        
        由于 macOS 限制，我们无法直接调用系统听写，
        所以提供一个提示，让用户使用系统听写后粘贴
        """
        print("\n" + "=" * 60)
        print("🎤 macOS 听写模式")
        print("=" * 60)
        print("\n使用方法:")
        print("1. 按 Fn 键两次（或 Ctrl+Ctrl 启动听写）")
        print("2. 对着麦克风说话")
        print("3. 听写完成后，文本会自动输入")
        print("\n或者直接在下方输入文字...")
        print("=" * 60)
        
        try:
            user_input = input("\n📝 输入：").strip()
            return user_input
        except KeyboardInterrupt:
            return ""
    
    def listen(self) -> str:
        """监听输入"""
        return self.listen_with_macos_dictation()


def test_voice_input():
    """测试语音输入"""
    print("=" * 60)
    print("语音输入模块 - 测试")
    print("=" * 60)
    
    voice = VoiceInput(language='zh-CN')
    
    print("\n请选择输入方式:")
    print("1. 语音输入（需要麦克风）")
    print("2. 文字输入")
    
    choice = input("\n选择 (1/2): ").strip()
    
    if choice == '1':
        print("\n🎤 请说话...")
        text = voice.listen(use_voice=True)
    else:
        text = voice.listen_keyboard()
    
    if text:
        print(f"\n✅ 您输入了：{text}")
    else:
        print("\n❌ 未检测到输入")


if __name__ == '__main__':
    test_voice_input()
