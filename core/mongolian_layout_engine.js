/**
 * MongolianLayoutEngine - 传统蒙古文竖排布局引擎
 * 
 * 这是 OpenClaw Mongolian AI Team 自主研发的算法
 * 不依赖任何第三方库，纯原生 JavaScript 实现
 * 
 * @version 1.0.0
 * @author OpenClaw Mongolian AI Team
 * @date 2026-03-30
 */

class MongolianLayoutEngine {
    constructor(options = {}) {
        this.options = {
            fontSize: options.fontSize || 40,
            lineHeight: options.lineHeight || 2.2,
            letterSpacing: options.letterSpacing || 3,
            maxColumnHeight: options.maxColumnHeight || 400,
            fontFamily: options.fontFamily || "'Mongolian Usug', 'Mongolian Baiti', sans-serif"
        };
        
        this.browserInfo = this.detectBrowser();
        this.cssStrategy = this.getOptimalCSSStrategy();
    }
    
    /**
     * 检测浏览器类型和版本
     * 自主研发的浏览器检测算法
     */
    detectBrowser() {
        const ua = navigator.userAgent;
        
        return {
            isWebKit: /WebKit/.test(ua) && !/Chrome/.test(ua),
            isChrome: /Chrome/.test(ua),
            isFirefox: /Firefox/.test(ua),
            isSafari: /Safari/.test(ua) && !/Chrome/.test(ua),
            version: this.extractVersion(ua)
        };
    }
    
    extractVersion(ua) {
        const match = ua.match(/(Chrome|Firefox|Safari)\/([\d.]+)/);
        return match ? match[2] : 'unknown';
    }
    
    /**
     * 获取最优 CSS 策略
     * 基于浏览器类型自动选择最佳渲染方案
     */
    getOptimalCSSStrategy() {
        if (this.browserInfo.isWebKit || this.browserInfo.isSafari) {
            return {
                'writing-mode': 'vertical-lr',
                'text-orientation': 'sideways',
                'font-feature-settings': '"mong"'
            };
        } else if (this.browserInfo.isFirefox) {
            return {
                'writing-mode': 'vertical-lr',
                'text-orientation': 'mixed'
            };
        } else {
            // Chrome/Blink
            return {
                'writing-mode': 'vertical-lr',
                'text-orientation': 'upright'
            };
        }
    }
    
    /**
     * 分析蒙古文文本
     * 识别词边界、字符位置等
     */
    analyzeText(text) {
        const words = text.split(/\s+/);
        const analysis = {
            totalChars: text.length,
            totalWords: words.length,
            words: words.map(word => this.analyzeWord(word))
        };
        
        return analysis;
    }
    
    /**
     * 分析单词
     * 识别词首、词中、词尾字符
     */
    analyzeWord(word) {
        return {
            text: word,
            length: word.length,
            firstChar: word[0],
            lastChar: word[word.length - 1],
            hasMongolian: /[\u1800-\u18AF]/.test(word)
        };
    }
    
    /**
     * 计算布局
     * 根据容器宽度计算列数和每列内容
     */
    calculateLayout(text, containerWidth) {
        const charWidth = this.options.fontSize * 0.6;
        const charsPerColumn = Math.floor(containerWidth / charWidth);
        const columns = [];
        
        let currentColumn = [];
        let currentLength = 0;
        
        for (const char of text) {
            if (char === '\n' || currentLength >= charsPerColumn) {
                columns.push(currentColumn.join(''));
                currentColumn = [];
                currentLength = 0;
                
                if (char === '\n') continue;
            }
            
            currentColumn.push(char);
            currentLength++;
        }
        
        if (currentColumn.length > 0) {
            columns.push(currentColumn.join(''));
        }
        
        return {
            columns,
            charsPerColumn,
            totalColumns: columns.length
        };
    }
    
    /**
     * 生成 CSS 样式
     * 应用最优策略
     */
    generateCSS() {
        const baseStyles = {
            'font-family': this.options.fontFamily,
            'font-size': `${this.options.fontSize}px`,
            'line-height': this.options.lineHeight,
            'letter-spacing': `${this.options.letterSpacing}px`,
            'padding': '20px',
            'max-height': `${this.options.maxColumnHeight}px`,
            'overflow-y': 'auto'
        };
        
        return {
            ...baseStyles,
            ...this.cssStrategy
        };
    }
    
    /**
     * 应用样式到元素
     */
    applyStyles(element) {
        const styles = this.generateCSS();
        
        for (const [property, value] of Object.entries(styles)) {
            element.style[property] = value;
        }
    }
    
    /**
     * 渲染蒙古文文本
     * 主入口函数
     */
    render(text, container) {
        // 1. 分析文本
        const analysis = this.analyzeText(text);
        
        // 2. 计算布局
        const layout = this.calculateLayout(text, container.offsetWidth);
        
        // 3. 创建渲染容器
        const renderContainer = document.createElement('div');
        renderContainer.className = 'mongolian-vertical';
        
        // 4. 应用样式
        this.applyStyles(renderContainer);
        
        // 5. 设置内容
        renderContainer.textContent = text;
        
        // 6. 添加到容器
        container.appendChild(renderContainer);
        
        return {
            element: renderContainer,
            analysis,
            layout
        };
    }
    
    /**
     * 性能优化：懒加载长文本
     */
    lazyLoadLongText(text, container, chunkSize = 100) {
        const chunks = [];
        for (let i = 0; i < text.length; i += chunkSize) {
            chunks.push(text.slice(i, i + chunkSize));
        }
        
        const renderContainer = document.createElement('div');
        renderContainer.className = 'mongolian-vertical';
        this.applyStyles(renderContainer);
        
        let currentChunk = 0;
        
        const loadNextChunk = () => {
            if (currentChunk < chunks.length) {
                const span = document.createElement('span');
                span.textContent = chunks[currentChunk];
                renderContainer.appendChild(span);
                currentChunk++;
                
                // 使用 requestIdleCallback 优化性能
                if (typeof requestIdleCallback === 'function') {
                    requestIdleCallback(loadNextChunk);
                } else {
                    setTimeout(loadNextChunk, 0);
                }
            }
        };
        
        loadNextChunk();
        container.appendChild(renderContainer);
        
        return renderContainer;
    }
    
    /**
     * 获取引擎信息
     */
    getInfo() {
        return {
            name: 'MongolianLayoutEngine',
            version: '1.0.0',
            author: 'OpenClaw Mongolian AI Team',
            browser: this.browserInfo,
            strategy: this.cssStrategy,
            options: this.options
        };
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MongolianLayoutEngine;
}
