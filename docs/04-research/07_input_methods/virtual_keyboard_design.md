# 虚拟键盘设计文档

**版本**: v1.0  
**创建时间**: 2026-04-03  
**最后更新**: 2026-04-03  
**状态**: ✅ 完成

---

## 📋 概述

本文档定义蒙古文虚拟键盘的设计规范，包括布局、交互、竖排适配、移动端优化等核心内容。

### 设计目标

1. **竖排优先**: 键盘布局适配竖排输入场景
2. **移动优化**: 针对手机/平板优化触摸体验
3. **标准兼容**: 符合蒙古国国家标准 GB/T 26224-2010
4. **智能预测**: 支持词频预测、自动校正
5. **可定制**: 支持用户自定义布局

---

## 🎹 键盘布局

### 标准布局 (横排)

```
┌─────────────────────────────────────────────────────────┐
│  ᠬ ᠭ ᠮ ᠯ ᠰ ᠱ ᠲ ᠳ ᠴ ᠵ ᠶ ᠷ ᠸ ᠹ ᠺ ᠻ ᠼ ᠽ ᠾ ᠿ           │
│  ᠠ ᠡ ᠢ ᠣ ᠤ ᠥ ᠦ ᠨ ᠪ ᠫ ᠬ ᠭ ᠭ ᠯ ᠰ ᠱ ᠲ ᠳ ᠴ ᠵ           │
│  Q W E R T Y U I O P [ ]                                │
│  A S D F G H J K L ; '                                  │
│  Z X C V B N M , . /                                    │
│                      [Space]                            │
└─────────────────────────────────────────────────────────┘
```

### 竖排布局 (移动端)

```
┌─────────┐
│ ᠬ ᠠ Q   │
│ ᠭ ᠡ W   │
│ ᠮ ᠢ E   │
│ ᠯ ᠣ R   │
│ ᠰ ᠤ T   │
│ ᠱ ᠥ Y   │
│ ᠲ ᠦ U   │
│ ᠳ ᠨ I   │
│ ᠴ ᠪ O   │
│ ᠵ ᠫ P   │
│         │
│ [␣]     │
└─────────┘
```

### 布局标准

**蒙古国国家标准 GB/T 26224-2010**:

| 区域 | 键位 | 说明 |
|------|------|------|
| 元音区 | ᠠ ᠡ ᠢ ᠣ ᠤ ᠥ ᠦ | 7 个基本元音 |
| 辅音区 | ᠨ ᠪ ᠫ ᠬ ᠭ ᠮ ᠯ ᠰ ᠱ ᠲ ᠳ ᠴ ᠵ ᠶ ᠷ | 15 个基本辅音 |
| 扩展区 | ᠸ ᠹ ᠺ ᠻ ᠼ ᠽ ᠾ ᠿ | 8 个扩展辅音 |
| 控制区 | FVS1 FVS2 FVS3 ZWJ ZWNJ | 5 个控制符 |
| 数字区 | 0-9 | 阿拉伯数字 |
| 符号区 | ， 。 ？ ！ ： ； | 标点符号 |

---

## 🎨 UI 设计

### 横排键盘组件

```tsx
import React, { useState } from 'react';

interface KeyProps {
    label: string;
    code: string;
    onPress: (code: string) => void;
    width?: number;
    isSpecial?: boolean;
}

const Key: React.FC<KeyProps> = ({ 
    label, 
    code, 
    onPress, 
    width = 1,
    isSpecial = false 
}) => {
    return (
        <button
            className={`key ${isSpecial ? 'special' : ''}`}
            style={{ flex: width }}
            onClick={() => onPress(code)}
        >
            <span className="key-label">{label}</span>
        </button>
    );
};

interface MongolianKeyboardProps {
    onKeyPress: (char: string) => void;
    layout?: 'horizontal' | 'vertical';
}

const MongolianKeyboard: React.FC<MongolianKeyboardProps> = ({
    onKeyPress,
    layout = 'horizontal'
}) => {
    const vowels = ['ᠠ', 'ᠡ', 'ᠢ', 'ᠣ', 'ᠤ', 'ᠥ', 'ᠦ'];
    const consonants = [
        'ᠨ', 'ᠪ', 'ᠫ', 'ᠬ', 'ᠭ', 'ᠮ', 'ᠯ', 'ᠰ', 'ᠱ',
        'ᠲ', 'ᠳ', 'ᠴ', 'ᠵ', 'ᠶ', 'ᠷ'
    ];
    const extended = ['ᠸ', 'ᠹ', 'ᠺ', 'ᠻ', 'ᠼ', 'ᠽ', 'ᠾ', 'ᠿ'];
    const control = ['FVS1', 'FVS2', 'FVS3', 'ZWJ', 'ZWNJ'];

    const handleKeyPress = (key: string) => {
        if (key.startsWith('FVS')) {
            const fvsMap: Record<string, string> = {
                'FVS1': '\u180B',
                'FVS2': '\u180C',
                'FVS3': '\u180D'
            };
            onKeyPress(fvsMap[key]);
        } else if (key === 'ZWJ') {
            onKeyPress('\u200D');
        } else if (key === 'ZWNJ') {
            onKeyPress('\u200C');
        } else {
            onKeyPress(key);
        }
    };

    if (layout === 'vertical') {
        return (
            <div className="keyboard-vertical">
                <div className="keyboard-column">
                    {consonants.map(char => (
                        <Key
                            key={char}
                            label={char}
                            code={char}
                            onPress={handleKeyPress}
                        />
                    ))}
                </div>
                <div className="keyboard-column">
                    {vowels.map(char => (
                        <Key
                            key={char}
                            label={char}
                            code={char}
                            onPress={handleKeyPress}
                        />
                    ))}
                </div>
                <div className="keyboard-column">
                    <Key label="␣" code=" " onPress={handleKeyPress} width={3} />
                </div>
            </div>
        );
    }

    return (
        <div className="keyboard-horizontal">
            {/* 扩展辅音行 */}
            <div className="keyboard-row">
                {extended.map(char => (
                    <Key
                        key={char}
                        label={char}
                        code={char}
                        onPress={handleKeyPress}
                    />
                ))}
            </div>

            {/* 元音行 */}
            <div className="keyboard-row">
                {vowels.map(char => (
                    <Key
                        key={char}
                        label={char}
                        code={char}
                        onPress={handleKeyPress}
                    />
                ))}
            </div>

            {/* 辅音行 */}
            <div className="keyboard-row">
                {consonants.map(char => (
                    <Key
                        key={char}
                        label={char}
                        code={char}
                        onPress={handleKeyPress}
                    />
                ))}
            </div>

            {/* 控制符行 */}
            <div className="keyboard-row">
                {control.map(key => (
                    <Key
                        key={key}
                        label={key}
                        code={key}
                        onPress={handleKeyPress}
                        isSpecial
                    />
                ))}
            </div>

            {/* 空格行 */}
            <div className="keyboard-row">
                <Key label="␣" code=" " onPress={handleKeyPress} width={10} />
            </div>
        </div>
    );
};

export default MongolianKeyboard;
```

### 竖排键盘样式

```css
.keyboard-vertical {
    display: flex;
    flex-direction: row;
    gap: 4px;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 8px;
    max-height: 400px;
    overflow-y: auto;
}

.keyboard-column {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.keyboard-vertical .key {
    width: 48px;
    height: 48px;
    font-size: 20px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.1s;
}

.keyboard-vertical .key:active {
    background: #007AFF;
    color: white;
    transform: scale(0.95);
}

.keyboard-vertical .key.special {
    background: #e5e5e5;
    font-size: 14px;
}

/* 横排键盘样式 */
.keyboard-horizontal {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 8px;
}

.keyboard-row {
    display: flex;
    gap: 4px;
    justify-content: center;
}

.keyboard-horizontal .key {
    height: 44px;
    font-size: 18px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.1s;
}

.keyboard-horizontal .key:active {
    background: #007AFF;
    color: white;
    transform: scale(0.95);
}
```

---

## 📱 移动端优化

### 触摸优化

```tsx
import React, { useRef, useCallback } from 'react';

interface TouchKeyProps {
    label: string;
    code: string;
    onPress: (code: string) => void;
    onLongPress?: (code: string) => void;
}

const TouchKey: React.FC<TouchKeyProps> = ({
    label,
    code,
    onPress,
    onLongPress
}) => {
    const touchTimer = useRef<NodeJS.Timeout | null>(null);
    const isLongPress = useRef(false);

    const handleTouchStart = useCallback(() => {
        isLongPress.current = false;
        touchTimer.current = setTimeout(() => {
            isLongPress.current = true;
            if (onLongPress) {
                onLongPress(code);
                // 触觉反馈
                if (navigator.vibrate) {
                    navigator.vibrate(50);
                }
            }
        }, 500);
    }, [code, onLongPress]);

    const handleTouchEnd = useCallback(() => {
        if (touchTimer.current) {
            clearTimeout(touchTimer.current);
            touchTimer.current = null;
        }

        if (!isLongPress.current) {
            onPress(code);
            // 轻触反馈
            if (navigator.vibrate) {
                navigator.vibrate(10);
            }
        }
    }, [code, onPress]);

    const handleTouchCancel = useCallback(() => {
        if (touchTimer.current) {
            clearTimeout(touchTimer.current);
            touchTimer.current = null;
        }
    }, []);

    return (
        <button
            className="touch-key"
            onTouchStart={handleTouchStart}
            onTouchEnd={handleTouchEnd}
            onTouchCancel={handleTouchCancel}
            onMouseDown={handleTouchStart}
            onMouseUp={handleTouchEnd}
            onMouseLeave={handleTouchCancel}
        >
            <span className="key-label">{label}</span>
        </button>
    );
};

export default TouchKey;
```

### 小屏适配

```css
/* 小屏幕优化 */
@media (max-width: 375px) {
    .keyboard-vertical {
        gap: 2px;
        padding: 4px;
    }

    .keyboard-vertical .key {
        width: 40px;
        height: 40px;
        font-size: 16px;
    }

    .keyboard-column {
        gap: 2px;
    }
}

/* 大屏幕优化 */
@media (min-width: 768px) {
    .keyboard-vertical {
        gap: 6px;
        padding: 12px;
    }

    .keyboard-vertical .key {
        width: 56px;
        height: 56px;
        font-size: 24px;
    }
}

/* 横屏模式 */
@media (orientation: landscape) and (max-height: 500px) {
    .keyboard-vertical {
        flex-direction: row;
        max-height: 100%;
    }

    .keyboard-column {
        flex: 1;
    }
}
```

### 输入框集成

```tsx
import React, { useState, useRef, useEffect } from 'react';
import MongolianKeyboard from './MongolianKeyboard';
import MongolianInput from './MongolianInput';

interface MongolianInputWithKeyboardProps {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
}

const MongolianInputWithKeyboard: React.FC<MongolianInputWithKeyboardProps> = ({
    value,
    onChange,
    placeholder
}) => {
    const [showKeyboard, setShowKeyboard] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);
    const keyboardRef = useRef<HTMLDivElement>(null);

    // 点击外部关闭键盘
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (
                keyboardRef.current &&
                !keyboardRef.current.contains(event.target as Node) &&
                inputRef.current &&
                !inputRef.current.contains(event.target as Node)
            ) {
                setShowKeyboard(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleKeyPress = (char: string) => {
        const newValue = value + char;
        onChange(newValue);
    };

    const handleBackspace = () => {
        const newValue = value.slice(0, -1);
        onChange(newValue);
    };

    return (
        <div className="mongolian-input-with-keyboard">
            <div
                className="input-area"
                onClick={() => setShowKeyboard(true)}
                ref={inputRef}
            >
                <MongolianInput
                    value={value}
                    onChange={onChange}
                    placeholder={placeholder}
                    readOnly
                />
            </div>

            {showKeyboard && (
                <div className="keyboard-container" ref={keyboardRef}>
                    <div className="keyboard-header">
                        <span>蒙古文键盘</span>
                        <button onClick={() => setShowKeyboard(false)}>
                            ✕
                        </button>
                    </div>
                    <MongolianKeyboard onKeyPress={handleKeyPress} />
                    <div className="keyboard-footer">
                        <button onClick={handleBackspace}>⌫</button>
                        <button onClick={() => onChange(value + ' ')}>␣</button>
                        <button onClick={() => setShowKeyboard(false)}>✓</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MongolianInputWithKeyboard;
```

---

## 🧠 智能预测

### 词频预测

```python
from collections import defaultdict
from typing import List, Tuple, Dict
import json

class MongolianPredictiveText:
    def __init__(self, corpus_path: str = None):
        self.unigram = defaultdict(int)
        self.bigram = defaultdict(lambda: defaultdict(int))
        self.trigram = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.total_words = 0
        
        if corpus_path:
            self.load_corpus(corpus_path)
    
    def load_corpus(self, path: str):
        """加载语料库"""
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().split()
                for i, word in enumerate(words):
                    self.unigram[word] += 1
                    self.total_words += 1
                    
                    if i > 0:
                        self.bigram[words[i-1]][word] += 1
                    
                    if i > 1:
                        self.tr