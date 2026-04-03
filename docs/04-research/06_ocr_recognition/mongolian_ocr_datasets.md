# OCR 数据集调研

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [OCR 数据集类型](#ocr-数据集类型)
3. [公开数据集清单](#公开数据集清单)
4. [数据集构建方法](#数据集构建方法)
5. [数据标注工具](#数据标注工具)
6. [数据增强技术](#数据增强技术)
7. [质量评估](#质量评估)
8. [使用指南](#使用指南)
9. [参考资料](#参考资料)

---

## 概述

### 为什么需要 OCR 数据集

蒙古文 OCR (光学字符识别) 面临独特挑战：
- **竖排文本**: 大多数 OCR 引擎针对横排优化
- **连写特性**: 字母连接方式复杂
- **FVS 变体**: 同一字符多种字形
- **数据稀缺**: 公开标注数据极少

**高质量数据集是训练准确 OCR 模型的基础。**

### 数据集规模对比

| 语言 | 数据集 | 图像数 | 标注类型 |
|------|--------|--------|---------|
| 中文 | CTW | 10,000 | 检测 + 识别 |
| 中文 | Total-Text | 1,255 | 弯曲文本 |
| 阿拉伯文 | APTI | 40,000 | 打印体 |
| 西里尔文 | SynTH | 100,000 | 合成数据 |
| **传统蒙古文** | **无公开大规模数据集** | **-** | **-** |

**机会**: 构建首个传统蒙古文 OCR 数据集

---

## OCR 数据集类型

### 按任务分类

#### 1. 文本检测数据集

标注文本区域位置 (bounding box 或多边形)。

```json
{
  "image": "page_001.jpg",
  "annotations": [
    {
      "text": "ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ",
      "bbox": [x1, y1, x2, y2],
      "language": "traditional_mongolian"
    }
  ]
}
```

**用途**: 训练文本检测模型 (DBNet, EAST, PSENet)

#### 2. 文本识别数据集

标注文本内容和位置。

```json
{
  "image": "word_001.png",
  "text": "ᠮᠣᠩᠭᠣᠯ",
  "script": "traditional_mongolian"
}
```

**用途**: 训练文本识别模型 (CRNN, TRBA, SVTR)

#### 3. 端到端数据集

同时包含检测和识别标注。

```json
{
  "image": "page_001.jpg",
  "lines": [
    {
      "polygon": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],
      "text": "ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ ᠪᠣᠯ ᠳᠡᠯᠬᠢᠶᠡᠨ ᠬᠠᠮᠤᠭ ᠦᠨᠳᠦᠰᠦᠨ ᠦ ᠨᠢᠭᠡ ᠬᠡᠯᠡ ᠪᠣᠯᠤᠮᠳᠠᠢ᠃"
    }
  ]
}
```

**用途**: 训练端到端模型 (Mask TextSpotter, TextDragon)

### 按数据来源分类

#### 1. 合成数据 (Synthetic)

通过渲染引擎生成。

**优点**:
- ✅ 规模可控
- ✅ 标注自动准确
- ✅ 成本低

**缺点**:
- ❌ 与真实图像有差距
- ❌ 缺少噪声/变形

**工具**:
```python
# 使用 PIL 渲染蒙古文
from PIL import Image, ImageDraw, ImageFont

def render_mongolian_text(text, font_path, size=(400, 100)):
    image = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 24)
    
    # 竖排渲染
    draw.text((50, 20), text, font=font, fill='black', 
              direction='tt', features=['+vert'])
    
    return image
```

#### 2. 真实数据 (Real)

从真实文档扫描/拍照。

**优点**:
- ✅ 真实分布
- ✅ 包含噪声/变形

**缺点**:
- ❌ 标注成本高
- ❌ 规模有限

#### 3. 半合成数据 (Semi-synthetic)

真实背景 + 合成文本。

```python
# 将合成文本粘贴到真实背景
def create_semi_synthetic(background_img, text_img):
    # 随机选择背景区域
    # 应用透视变换
    # 调整亮度和对比度
    # 添加噪声
    return composite_image
```

---

## 公开数据集清单

### 传统蒙古文数据集

#### 1. MongolianDoc (假设，需创建)

```yaml
名称：MongolianDoc
规模：10,000 页
来源：蒙古国政府公文
标注类型：检测 + 识别
许可证：CC BY 4.0
状态：规划中
```

**内容**:
- 现代打印体文档
- 竖排文本
- 包含表格/图片混合

#### 2. ClassicalMongolian-OCR (假设)

```yaml
名称：ClassicalMongolian-OCR
规模：5,000 页
来源：古典文献 (18-19 世纪)
标注类型：识别
许可证：研究用
状态：学术项目
```

**内容**:
- 手写体为主
- 古典正字法
- 质量参差不齐

### 相关数据集 (可借用)

#### 1. UD Mongolian (文本语料)

```yaml
用途：语言模型训练
规模：89,456 词
来源：UD Treebank
```

#### 2. tugstugi/mongolian-corpus

```yaml
用途：词表构建
规模：500 万词
来源：网络爬虫
许可证：MIT
```

---

## 数据集构建方法

### 构建流程

```
1. 语料收集
   ↓
2. 文本规范化
   ↓
3. 图像采集/合成
   ↓
4. 标注 (自动/人工)
   ↓
5. 质量审核
   ↓
6. 划分训练/验证/测试集
   ↓
7. 发布
```

### 语料收集

#### 来源 1: 政府公文

```python
# 爬取蒙古国政府网站
import requests
from bs4 import BeautifulSoup

def scrape_mongolian_gov(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取蒙古文内容
    mongolian_text = []
    for p in soup.find_all('p', {'lang': 'mn'}):
        text = p.get_text()
        if is_traditional_mongolian(text):
            mongolian_text.append(text)
    
    return mongolian_text
```

#### 来源 2: 数字图书馆

```python
# IIIF 图像采集
def fetch_iiif_images(base_url, manifest_id):
    manifest = requests.get(f"{base_url}/{manifest_id}/manifest").json()
    
    images = []
    for canvas in manifest['sequences'][0]['canvases']:
        image_url = canvas['images'][0]['resource']['@id']
        images.append(image_url)
    
    return images
```

#### 来源 3: 新闻网站

```python
# 蒙古国新闻网站
news_sites = [
    'montsame.mn',
    'news.mn',
    'gogo.mn'
]
```

### 图像合成

#### 使用 FontForge 渲染

```python
# 批量合成蒙古文图像
import os
from PIL import Image, ImageDraw, ImageFont

class MongolianOCRSynthesizer:
    def __init__(self, font_paths):
        self.fonts = [ImageFont.truetype(fp, 24) for fp in font_paths]
    
    def synthesize(self, text, output_dir, n_samples=100):
        for i in range(n_samples):
            # 随机选择字体
            font = random.choice(self.fonts)
            
            # 渲染文本
            img = self.render_text(text, font)
            
            # 添加噪声
            img = self.add_noise(img)
            
            # 保存
            img.save(f"{output_dir}/{i:05d}.png")
    
    def render_text(self, text, font):
        # 计算文本尺寸
        bbox = font.getbbox(text)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        # 创建图像
        img = Image.new('RGB', (width + 20, height + 20), 'white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), text, font=font, fill='black')
        
        return img
    
    def add_noise(self, img):
        # 随机旋转
        angle = random.uniform(-5, 5)
        img = img.rotate(angle, expand=True)
        
        # 调整亮度
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.8, 1.2))
        
        # 添加高斯噪声
        import numpy as np
        img_array = np.array(img)
        noise = np.random.normal(0, 5, img_array.shape)
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
```

### 标注格式

#### COCO 格式 (检测)

```json
{
  "images": [
    {"id": 1, "file_name": "00001.jpg", "width": 800, "height": 600}
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "bbox": [x, y, width, height],
      "segmentation": [[x1,y1, x2,y2, x3,y3, x4,y4]],
      "iscrowd": 0
    }
  ],
  "categories": [
    {"id": 1, "name": "mongolian_text"}
  ]
}
```

#### LMDB 格式 (识别)

```python
# 创建 LMDB 数据库
import lmdb
import pickle

def create_lmdb_dataset(image_paths, labels, output_path):
    env = lmdb.open(output_path, map_size=1099511627776)
    
    with env.begin(write=True) as txn:
        for i, (img_path, label) in enumerate(zip(image_paths, labels)):
            # 读取图像
            with open(img_path, 'rb') as f:
                img_data = f.read()
            
            # 写入图像
            txn.put(f'image-{i:09d}'.encode(), img_data)
            
            # 写入标签
            label_key = f'label-{i:09d}'.encode()
            txn.put(label_key, label.encode())
    
    env.close()
```

---

## 数据标注工具

### 1. LabelImg (检测)

```
URL: https://github.com/heartexlabs/labelImg
特点:
- 矩形框标注
- 支持 VOC/COCO 格式
- 桌面应用
```

### 2. LabelMe (多边形)

```
URL: https://github.com/wkentaro/labelme
特点:
- 多边形标注
- 支持竖排文本
- JSON 格式输出
```

### 3. CVAT (在线)

```
URL: https://cvat.org/
特点:
- Web 界面
- 多人协作
- 自动标注辅助
- 支持视频
```

### 4. 蒙古文专用标注工具 (建议开发)

```python
# 简化的蒙古文 OCR 标注工具
class MongolianOCRAnnotator:
    def __init__(self):
        self.current_image = None
        self.annotations = []
    
    def load_image(self, path):
        from PIL import Image
        self.current_image = Image.open(path)
    
    def add_annotation(self, polygon, text):
        self.annotations.append({
            'polygon': polygon,
            'text': text,
            'language': 'traditional_mongolian'
        })
    
    def save(self, output_path):
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'image': self.current_image.filename,
                'annotations': self.annotations
            }, f, ensure_ascii=False)
```

---

## 数据增强技术

### 几何变换

```python
import albumentations as A

transform = A.Compose([
    # 旋转
    A.Rotate(limit=15, p=0.5),
    
    # 透视变换
    A.Perspective(scale=(0.05, 0.1), p=0.3),
    
    # 弹性变形
    A.ElasticTransform(alpha=1, sigma=50, p=0.2),
    
    # 随机裁剪
    A.RandomCrop(width=300, height=100, p=0.5),
    
    # 翻转 (竖排文本慎用水平翻转)
    A.VerticalFlip(p=0.3),
])
```

### 外观变换

```python
transform = A.Compose([
    # 亮度对比度
    A.RandomBrightnessContrast(p=0.5),
    
    # 色调变化
    A.HueSaturationValue(p=0.3),
    
    # 高斯噪声
    A.IAAAdditiveGaussianNoise(p=0.3),
    
    # 模糊
    A.MotionBlur(blur_limit=5, p=0.3),
    
    #  JPEG 压缩
    A.ImageCompression(quality_lower=50, p=0.3),
])
```

### 特殊增强 (蒙古文)

```python
def mongolian_specific_augment(image):
    """
    蒙古文专用增强
    """
    from PIL import Image, ImageFilter
    
    # 模拟竖排扫描畸变
    def vertical_distortion(img):
        # 模拟扫描时的垂直拉伸
        return img.transform(
            img.size,
            Image.AFFINE,
            (1, 0, 0, 0, 1.05, 0)
        )
    
    # 模拟墨水扩散
    def ink_bleed(img):
        return img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # 应用增强
    if random.random() > 0.5:
        image = vertical_distortion(image)
    if random.random() > 0.5:
        image = ink_bleed(image)
    
    return image
```

---

## 质量评估

### 标注质量指标

```python
def evaluate_annotation_quality(annotations):
    """
    评估标注质量
    """
    metrics = {
        'completeness': 0,  # 完整率
        'accuracy': 0,      # 准确率
        'consistency': 0,   # 一致性
    }
    
    # 完整率：所有文本都有标注
    metrics['completeness'] = calculate_completeness(annotations)
    
    # 准确率：抽样人工检查
    metrics['accuracy'] = sample_and_check(annotations)
    
    # 一致性：多人标注对比
    metrics['consistency'] = calculate_inter_annotator_agreement(annotations)
    
    return metrics

def calculate_completeness(annotations):
    # 检查是否有遗漏文本区域
    pass

def sample_and_check(annotations, sample_size=100):
    # 随机抽样人工检查
    pass

def calculate_inter_annotator_agreement(annotations):
    # 计算 Kappa 系数
    pass
```

### 数据集划分

```python
from sklearn.model_selection import train_test_split

def split_dataset(images, labels, ratios=(0.8, 0.1, 0.1)):
    """
    划分训练/验证/测试集
    
    Args:
        images: 图像路径列表
        labels: 标签列表
        ratios: (train, val, test) 比例
    
    Returns:
        train_data, val_data, test_data
    """
    # 训练集 + 临时集
    train_imgs, temp_imgs, train_labels, temp_labels = train_test_split(
