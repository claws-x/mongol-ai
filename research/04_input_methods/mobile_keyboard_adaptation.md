# 移动端键盘适配

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [移动端键盘布局设计](#移动端键盘布局设计)
3. [iOS 键盘适配](#ios-键盘适配)
4. [Android 键盘适配](#android-键盘适配)
5. [自定义键盘实现](#自定义键盘实现)
6. [FVS 选择器设计](#fvs-选择器设计)
7. [竖排输入优化](#竖排输入优化)
8. [性能优化](#性能优化)
9. [测试清单](#测试清单)
10. [参考资料](#参考资料)

---

## 概述

### 为什么需要移动端键盘适配

**市场现状**:

| 平台 | 传统蒙古文键盘 | 竖排支持 | 预测输入 |
|------|--------------|---------|---------|
| iOS 原生 | ❌ 无 | ❌ | - |
| Android GBoard | ❌ 无 | ❌ | - |
| Menksoft | ⚠️ 西里尔为主 | ⚠️ | ⚠️ 基础 |
| 开源项目 | ❌ 无 | ❌ | ❌ |

**机会**: 首个移动优先的传统蒙古文虚拟键盘

### 设计原则

```
原则 1: 拇指友好
常用键放在拇指自然区域

原则 2: FVS 便捷访问
变体选择符一键可达

原则 3: 竖排兼容
键盘布局适配竖排显示

原则 4: 预测集成
智能预测减少击键

原则 5: 跨平台一致
iOS/Android 体验统一
```

### 技术选型

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|---------|
| 系统键盘扩展 | 全局可用 | 开发复杂 | 长期方案 |
| Web 自定义键盘 | 开发简单 | 仅限 Web | 短期方案 |
| Hybrid (React Native) | 跨平台 | 性能折中 | 推荐 |

---

## 移动端键盘布局设计

### 标准布局 (36 键)

```
┌─────────────────────────────────────────────────────────┐
│  ᠠ  ᠡ  ᠢ  ᠣ  ᠤ  ᠥ  ᠦ  ᠧ  ᠨ  ᠩ              [⌫]         │
│   ᠪ  ᠭ  ᠳ  ᠴ  ᠵ  ᠶ  ᠺ  ᠯ  ᠰ  ᠱ  ᠲ              [⏎]      │
│    [123]  ᠷ  ᠸ  ᠹ  ᠼ  ᠽ  ᠾ  ᠿ  ,  .  ?  [🌐]           │
│                    [Space: ᠭᠣᠯ]                         │
└─────────────────────────────────────────────────────────┘
```

### 优化布局 (带 FVS 快捷键)

```
┌─────────────────────────────────────────────────────────┐
│  ᠠ  ᠡ  ᠢ  ᠣ  ᠤ  ᠥ  ᠦ  ᠧ  ᠨ  ᠩ              [⌫]         │
│   ᠪ  ᠭ  ᠳ  ᠴ  ᠵ  ᠶ  ᠺ  ᠯ  ᠰ  ᠱ  ᠲ              [⏎]      │
│  [FVS]  ᠷ  ᠸ  ᠹ  ᠼ  ᠽ  ᠾ  ᠿ  ,  .  ?  [🌐]            │
│                    [Space: ᠭᠣᠯ]                         │
└─────────────────────────────────────────────────────────┘

FVS 长按菜单:
┌─────────────┐
│  FVS1 (᠎)   │
│  FVS2 (᠏)   │
│  FVS3 (᠐)   │
│  NNBSP ( )  │
└─────────────┘
```

### 频率优化布局

基于词频统计将高频字母放在易按位置:

```javascript
const letterFrequency = {
  'ᠠ': 0.142,  // 最高频，放在中央
  'ᠨ': 0.118,
  'ᠭ': 0.095,
  'ᠳ': 0.087,
  'ᠪ': 0.076,
  'ᠯ': 0.072,
  'ᠶ': 0.068,
  'ᠰ': 0.065,
  'ᠲ': 0.061,
  'ᠢ': 0.058,
  // ... 其他字母
};

// 热力图优化布局
const optimizedLayout = [
  ['ᠨ', 'ᠠ', 'ᠢ', 'ᠣ', 'ᠤ', 'ᠥ', 'ᠦ', 'ᠭ', 'ᠪ', 'ᠯ'],
  ['ᠰ', 'ᠲ', 'ᠳ', 'ᠴ', 'ᠵ', 'ᠶ', 'ᠺ', 'ᠸ', 'ᠹ', 'ᠼ'],
  ['FVS', 'ᠷ', 'ᠽ', 'ᠾ', 'ᠿ', ',', '.', '?', '🌐']
];
```

---

## iOS 键盘适配

### Custom Keyboard Extension

```swift
// KeyboardViewController.swift
import UIKit

class KeyboardViewController: UIInputViewController {
    
    @IBOutlet var nextKeyboardButton: UIButton!
    
    // 键盘按钮数组
    var keyboardButtons: [UIButton] = []
    
    // 蒙古文字母
    let mongolianLetters = [
        "ᠠ", "ᠡ", "ᠢ", "ᠣ", "ᠤ", "ᠥ", "ᠦ", "ᠧ",
        "ᠨ", "ᠩ", "ᠪ", "ᠭ", "ᠳ", "ᠴ", "ᠵ", "ᠶ",
        "ᠺ", "ᠯ", "ᠰ", "ᠱ", "ᠲ", "ᠷ", "ᠸ", "ᠹ",
        "ᠼ", "ᠽ", "ᠾ", "ᠿ"
    ]
    
    override func updateViewConstraints() {
        super.updateViewConstraints()
        
        // 添加自定义键盘视图
        setupKeyboard()
    }
    
    func setupKeyboard() {
        let buttonWidth = (view.bounds.width - 60) / 10
        let buttonHeight: CGFloat = 50
        
        for (index, letter) in mongolianLetters.enumerated() {
            let button = UIButton(type: .system)
            button.setTitle(letter, for: .normal)
            button.titleLabel?.font = UIFont.systemFont(ofSize: 24)
            button.frame = CGRect(
                x: 10 + (index % 10) * (buttonWidth + 5),
                y: 20 + (index / 10) * (buttonHeight + 5),
                width: buttonWidth,
                height: buttonHeight
            )
            
            button.addTarget(self, action: #selector(keyPressed(_:)), for: .touchUpInside)
            view.addSubview(button)
            keyboardButtons.append(button)
        }
    }
    
    @objc func keyPressed(_ sender: UIButton) {
        guard let proxy = textDocumentProxy as? UITextDocumentProxy else { return }
        
        // 插入蒙古文字符
        proxy.insertText(sender.title(for: .normal) ?? "")
        
        // 触觉反馈
        UIImpactFeedbackGenerator(style: .light).impactOccurred()
    }
    
    // FVS 长按菜单
    func showFVSPopup(for button: UIButton) {
        let alertController = UIAlertController(
            title: "选择变体",
            message: nil,
            preferredStyle: .actionSheet
        )
        
        alertController.addAction(UIAlertAction(title: "FVS1 (᠎)", style: .default) { _ in
            self.textDocumentProxy?.insertText("\u{180B}")
        })
        
        alertController.addAction(UIAlertAction(title: "FVS2 (᠏)", style: .default) { _ in
            self.textDocumentProxy?.insertText("\u{180C}")
        })
        
        alertController.addAction(UIAlertAction(title: "FVS3 (᠐)", style: .default) { _ in
            self.textDocumentProxy?.insertText("\u{180D}")
        })
        
        alertController.addAction(UIAlertAction(title: "取消", style: .cancel))
        
        present(alertController, animated: true)
    }
}
```

### Info.plist 配置

```xml
<!-- Info.plist -->
<key>NSExtension</key>
<dict>
    <key>NSExtensionPointIdentifier</key>
    <string>com.apple.keyboard-service</string>
    <key>NSExtensionPrincipalClass</key>
    <string>$(PRODUCT_MODULE_NAME).KeyboardViewController</string>
</dict>

<key>PrimaryLanguage</key>
<string>mn-MN</string>

<key>KeyboardName</key>
<string>传统蒙古文</string>
```

---

## Android 键盘适配

### InputMethodService 实现

```kotlin
// MongolianIME.kt
package com.mongolian.keyboard

import android.inputmethodservice.InputMethodService
import android.inputmethodservice.Keyboard
import android.inputmethodservice.KeyboardView
import android.view.KeyEvent
import android.view.View
import android.widget.Button

class MongolianIME : InputMethodService(), KeyboardView.OnKeyboardActionListener {
    
    private lateinit var keyboardView: KeyboardView
    private lateinit var keyboard: Keyboard
    
    // 蒙古文字母
    private val mongolianLetters = arrayOf(
        "ᠠ", "ᠡ", "ᠢ", "ᠣ", "ᠤ", "ᠥ", "ᠦ", "ᠧ",
        "ᠨ", "ᠩ", "ᠪ", "ᠭ", "ᠳ", "ᠴ", "ᠵ", "ᠶ",
        "ᠺ", "ᠯ", "ᠰ", "ᠱ", "ᠲ", "ᠷ", "ᠸ", "ᠹ",
        "ᠼ", "ᠽ", "ᠾ", "ᠿ"
    )
    
    override fun onCreateInputView(): View {
        keyboardView = layoutInflater.inflate(R.layout.keyboard_view, null) as KeyboardView
        
        // 加载自定义键盘布局
        keyboard = Keyboard(this, R.xml.mongolian_keyboard)
        keyboardView.keyboard = keyboard
        keyboardView.setOnKeyboardActionListener(this)
        
        return keyboardView
    }
    
    override fun onKey(primaryCode: Int, keyCodes: IntArray?) {
        val inputConnection = currentInputConnection
        
        when (primaryCode) {
            Keyboard.KEYCODE_DELETE -> {
                inputConnection.deleteSurroundingText(1, 0)
            }
            Keyboard.KEYCODE_SHIFT -> {
                // 切换大小写 (蒙古文不需要，保留给数字/符号)
            }
            Keyboard.KEYCODE_MODE_CHANGE -> {
                // 切换到数字/符号键盘
            }
            Keyboard.KEYCODE_DONE -> {
                inputConnection.sendKeyEvent(KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_ENTER))
            }
            else -> {
                // 插入蒙古文字符
                val code = Character.toChars(primaryCode)
                inputConnection.commitText(String(code), 1)
            }
        }
    }
    
    // 其他必需实现的方法...
    override fun onPress(primaryCode: Int) {}
    override fun onRelease(primaryCode: Int) {}
    override fun onText(text: CharSequence?) {}
    override fun swipeDown() {}
    override fun swipeLeft() {}
    override fun swipeRight() {}
    override fun swipeUp() {}
}
```

### 键盘布局 XML

```xml
<!-- res/xml/mongolian_keyboard.xml -->
<Keyboard xmlns:android="http://schemas.android.com/apk/res/android"
    android:keyWidth="10%p"
    android:keyHeight="60dp"
    android:horizontalGap="0px"
    android:verticalGap="0px">
    
    <!-- 第一行 -->
    <Row>
        <Key android:codes="5888" android:keyLabel="ᠠ" android:keyEdgeFlags="left"/>
        <Key android:codes="5889" android:keyLabel="ᠡ"/>
        <Key android:codes="5890" android:keyLabel="ᠢ"/>
        <Key android:codes="5891" android:keyLabel="ᠣ"/>
        <Key android:codes="5892" android:keyLabel="ᠤ"/>
        <Key android:codes="5893" android:keyLabel="ᠥ"/>
        <Key android:codes="5894" android:keyLabel="ᠦ"/>
        <Key android:codes="5895" android:keyLabel="ᠧ"/>
        <Key android:codes="5928" android:keyLabel="ᠨ"/>
        <Key android:codes="5929" android:keyLabel="ᠩ" android:keyEdgeFlags="right"/>
    </Row>
    
    <!-- 第二行 -->
    <Row>
        <Key android:codes="5930" android:keyLabel="ᠪ" android:keyEdgeFlags="left"/>
        <Key android:codes="5932" android:keyLabel="ᠭ"/>
        <Key android:codes="5939" android:keyLabel="ᠳ"/>
        <Key android:codes="5940" android:keyLabel="ᠴ"/>
        <Key android:codes="5941" android:keyLabel="ᠵ"/>
        <Key android:codes="5942" android:keyLabel="ᠶ"/>
        <Key android:codes="5946" android:keyLabel="ᠺ"/>
        <Key android:codes="5935" android:keyLabel="ᠯ"/>
        <Key android:codes="5936" android:keyLabel="ᠰ"/>
        <Key android:codes="5937" android:keyLabel="ᠱ" android:keyEdgeFlags="right"/>
    </Row>
    
    <!-- 第三行 -->
    <Row>
        <Key android:codes="5938" android:keyLabel="ᠲ" android:keyWidth="15%p" android:keyEdgeFlags="left"/>
        <Key android:codes="5943" android:keyLabel="ᠷ"/>
        <Key android:codes="5944" android:keyLabel="ᠸ"/>
        <Key android:codes="5945" android:keyLabel="ᠹ"/>
        <Key android:codes="5948" android:keyLabel="ᠼ"/>
        <Key android:codes="5949" android:keyLabel="ᠽ"/>
        <Key android:codes="5950" android:keyLabel="ᠾ"/>
        <Key android:codes="5951" android:keyLabel="ᠿ"/>
        <Key android:codes="-5" android:keyLabel="⌫" android:keyWidth="15%p" android:isRepeatable="true" android:keyEdgeFlags="right"/>
    </Row>
    
    <!-- 空格行 -->
    <Row android:rowEdgeFlags="bottom">
        <Key android:codes="-2" android:keyLabel="123" android:keyWidth="15%p" android:keyEdgeFlags="left"/>
        <Key android:codes="-6" android:keyLabel="FVS" android:keyWidth="15%p"/>
        <Key android:codes="32" android:keyLabel="ᠭᠣᠯ" android:keyWidth="50%p" android:isRepeatable="true"/>
        <Key android:codes="-4" android:keyLabel="⏎" android:keyWidth="20%p" android:keyEdgeFlags="right"/>
    </Row>
</Keyboard>
```

### AndroidManifest.xml 配置

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.mongolian.keyboard">
    
    <application>
        <service
            android:name=".MongolianIME"
            android:label="@string/ime_name"
            android:permission="android.permission.BIND_INPUT_METHOD"
            android:exported="true">
            <intent-filter>
                <action android:name="android.view.InputMethod" />
            </intent-filter>
            <meta-data
                android:name="android.view.im"
                android:resource="@xml/method" />
        </service>
    </application>
</manifest>
```

```xml
<!-- res/xml/method.xml -->