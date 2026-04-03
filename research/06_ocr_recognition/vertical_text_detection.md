# 竖排文本检测

**版本**: v1.0  
**创建时间**: 2026-04-03  
**状态**: 高优先级  
**相关文档**: [[../02_vertical_writing/unicode_control_codes.md]], [[../03_font_rendering/ligature_rules.md]]

---

## 1. 竖排 OCR 技术挑战

### 1.1 传统蒙古文的竖排特性

传统蒙古文是世界上少数仍在使用**竖排书写**的文字系统之一：

```
书写方向：从上到下
列顺序：从左到右

列 1    列 2    列 3
ᠮᠣᠩ     ᠬᠡᠯᠡ    ᠪᠣᠯ
ᠭᠣᠯ     ᠪᠣᠯ    ᠳᠡᠯᠬᠢ
        ᠳᠡᠢ
```

**OCR 挑战**:
1. 文本方向与常规 OCR 假设相反
2. 字符连写导致边界模糊
3. 词间间隔不规则
4. 字形变体多 (FVS 控制)

### 1.2 与横排文字的差异

| 特性 | 横排文字 (中文/英文) | 竖排蒙古文 |
|------|---------------------|------------|
| 阅读方向 | 左→右，上→下 | 上→下，左→右 |
| 字符连接 | 独立或有限连写 | 词内强制连写 |
| 词边界 | 空格明确 | 空格 + 字形变化 |
| 行高 | 固定 | 随词长变化 |
| 列宽 | 可变 | 相对固定 |

### 1.3 图像预处理挑战

#### 1.3.1 旋转校正

```python
import cv2
import numpy as np

def detect_text_orientation(image):
    """
    检测文本方向 (横排/竖排)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 使用 Sobel 算子检测边缘
    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    
    # 计算梯度方向直方图
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    angle = np.arctan2(grad_y, grad_x) * 180 / np.pi
    
    # 竖排文本：垂直边缘占主导
    vertical_edges = np.abs(angle) > 45
    horizontal_edges = np.abs(angle) <= 45
    
    vertical_ratio = np.sum(magnitude[vertical_edges]) / np.sum(magnitude)
    
    if vertical_ratio > 0.6:
        return "vertical"
    else:
        return "horizontal"

# 测试
image = cv2.imread("mongolian_vertical.jpg")
orientation = detect_text_orientation(image)
print(f"文本方向：{orientation}")
```

#### 1.3.2 图像旋转

```python
def rotate_for_ocr(image, orientation="vertical"):
    """
    旋转图像以适应横排 OCR 引擎
    """
    if orientation == "vertical":
        # 逆时针旋转 90 度
        rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return rotated
    return image

# 处理流程
image = cv2.imread("mongolian_vertical.jpg")
orientation = detect_text_orientation(image)
rotated = rotate_for_ocr(image, orientation)

# 现在可以用标准 OCR 处理
# 但需要注意：字符顺序需要还原
```

### 1.4 连写分割挑战

蒙古文词内字母连写，OCR 需要识别：
- 词内连写边界 (不应分割)
- 词间边界 (应分割)

```python
def segment_mongolian_words(image):
    """
    分割蒙古文词 (竖排)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 二值化
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 水平投影 (竖排文本的列间分隔)
    horizontal_projection = np.sum(binary, axis=1)
    
    # 检测列边界
    columns = []
    start = None
    for i, value in enumerate(horizontal_projection):
        if value > 0 and start is None:
            start = i
        elif value == 0 and start is not None:
            columns.append((start, i))
            start = None
    
    # 垂直投影 (词间分隔)
    words_per_column = []
    for col_start, col_end in columns:
        column_image = binary[col_start:col_end, :]
        vertical_projection = np.sum(column_image, axis=0)
        
        # 检测词边界
        words = []
        start = None
        for i, value in enumerate(vertical_projection):
            if value > 0 and start is None:
                start = i
            elif value == 0 and start is not None:
                words.append((start, i))
                start = None
        
        words_per_column.append(words)
    
    return columns, words_per_column
```

---

## 2. PaddleOCR/Tesseract 适配

### 2.1 PaddleOCR 适配

#### 2.1.1 安装和配置

```bash
pip install paddlepaddle paddleocr
```

#### 2.1.2 竖排文本检测

```python
from paddleocr import PaddleOCR
import cv2

# 初始化 OCR (使用英文模型，需替换为蒙古文模型)
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',  # 需替换为蒙古文模型
    det_model_dir='./models/mongolian_det',
    rec_model_dir='./models/mongolian_rec',
    cls_model_dir='./models/angle_cls'
)

# 读取图像
image_path = "mongolian_vertical.jpg"
image = cv2.imread(image_path)

# 旋转图像 (竖排转横排)
image_rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

# OCR 识别
result = ocr.ocr(image_rotated, cls=True)

# 还原坐标 (旋转后的坐标转回原图坐标)
height, width = image.shape[:2]
for line in result:
    for box, text in line:
        # 坐标转换 (逆时针旋转 90 度的逆变换)
        # (x, y) -> (y, width - x)
        original_box = [
            [box[0][1], width - box[0][0]],
            [box[1][1], width - box[1][0]],
            [box[2][1], width - box[2][0]],
            [box[3][1], width - box[3][0]]
        ]
        print(f"文本：{text}, 位置：{original_box}")
```

#### 2.1.3 自定义检测模型训练

```python
# 使用 PaddleOCR 训练竖排检测模型
# det_db.yml 配置
"""
Global:
  debug: false
  use_gpu: true
  epoch_num: 1200
  log_smooth_window: 20
  print_batch_step: 10
  save_model_dir: ./output/mongolian_det
  save_epoch_step: 200
  
Architecture:
  model_type: det
  algorithm: DB
  Transform:
  Backbone:
    name: MobileNetV3
    scale: 0.5
    model_name: small
  Head:
    name: DBHead
    k: 50
  
Loss:
  name: DBLoss
  
Optimizer:
  name: Adam
  beta1: 0.9
  beta2: 0.999
  lr:
    name: Poly
    learning_rate: 0.001
  regularizer:
    name: 'L2'
    factor: 0.00001

Train:
  dataset:
    name: SimpleDataSet
    data_dir: ./train_data/mongolian_det/
    label_file_list:
      - ./train_data/mongolian_det/train.txt
    ratio_list: [1.0]
    transforms:
      - DecodeImage:
          img_mode: BGR
          channel_first: False
      - DetLabelEncode:
      - DetAugmentation:
          - EastRandomCrop:
              size: [640, 640]
      - NormalizeImage:
          std: [0.229, 0.224, 0.225]
          mean: [0.485, 0.456, 0.406]
          scale: 1./255.
          order: 'hwc'
      - ResizeImage:
          resize_short: 640
      - AugmentData:
      - MakeBorderMap:
          shrink_ratio: 0.4
      - MakeShrinkMap:
          shrink_ratio: 0.4
      - Permute:
          to_rgb: True
          channel_first: True
  
  loader:
    shuffle: true
    batch_size_per_card: 16
    drop_last: true
    num_workers: 8
"""

# 训练命令
# python tools/train.py -c configs/det/det_db.yml
```

### 2.2 Tesseract 适配

#### 2.2.1 安装蒙古文语言包

```bash
# Tesseract 默认不支持蒙古文
# 需自定义训练

# 安装 Tesseract
brew install tesseract  # macOS
# 或
sudo apt install tesseract-ocr  # Linux

# 查看支持的语言
tesseract --list-langs
```

#### 2.2.2 自定义训练 (Tesseract 4+)

```bash
# 1. 准备训练数据
# - 图像文件 (.tif)
# - 标注文件 (.box)

# 2. 生成 box 文件
tesseract mongolian.train.tif mongolian batch.nochop makebox

# 3. 编辑 box 文件 (修正边界框和字符标签)

# 4. 生成字体列表
echo "Mongolian 0 0 0 0 0" > fontlist

# 5. 生成字体特征文件
text2image --font=Mongolian \
           --outputbase=mongolian \
           --testdata_dir=./tesseract-ocr/tessdata \
           --fontconfig_tmpdir=/tmp

# 6. 生成训练数据
generate_traineddata mongolian

# 7. 编译模型
combine_lang_model \
  --input_dir ./tesseract-ocr/tessdata \
  --lang mongolian \
  --scriptlist mongolian.script \
  --output_dir ./tesseract-ocr/tessdata
```

#### 2.2.3 使用 Tesseract

```python
import pytesseract
from PIL import Image
import cv2

# 加载图像
image = cv2.imread("mongolian_vertical.jpg")

# 旋转 (竖排转横排)
image_rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

# 转换为 PIL Image
pil_image = Image.fromarray(cv2.cvtColor(image_rotated, cv2.COLOR_BGR2RGB))

# OCR 识别
custom_config = r'--oem 3 --psm 6 -l mong'  # mong 是自定义的蒙古文语言包
text = pytesseract.image_to_string(pil_image, config=custom_config)

print(text)
```

### 2.3 模型对比

| 框架 | 竖排支持 | 蒙古文支持 | 训练难度 | 推理速度 |
|------|----------|------------|----------|----------|
| PaddleOCR | ★★★☆☆ | 需自定义 | ★★☆☆☆ | 快 |
| Tesseract | ★★☆☆☆ | 需自定义 | ★★★☆☆ | 中 |
| EasyOCR | ★★☆☆☆ | 需自定义 | ★★☆☆☆ | 中 |
| 自研模型 | ★★★★★ | 完全定制 | ★★★★☆ | 可优化 |

---

## 3. 检测算法设计

### 3.1 两阶段检测流程

```
阶段 1: 文本区域检测
  ↓
阶段 2: 字符识别和序列解码
```

#### 3.1.1 阶段 1: 文本区域检测

**目标**: 检测图像中的竖排文本列

**算法选择**:
- DBNet (Differentiable Binarization)
- EAST (Efficient and Accurate Scene Text Detector)
- CRAFT (Character Region Awareness for Text Detection)

**DBNet 适配竖排**:

```python
import torch
import torch.nn as nn

class DBNetVertical(DBNet):
    """
    适配竖排文本的 DBNet
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 调整 anchor 比例以适应竖排文本
        self.anchor_ratios = [0.5, 1.0, 2.0]  # 增加高宽比
    
    def forward(self, x):
        # 标准 DBNet 前向传播
        features = self.backbone(x)
        features = self.neck(features)
        probability_map = self.head(features)
        
        # 后处理：调整二值化阈值
        binary_map = self.binarize(probability_map)
        
        return probability_map, binary_map
    
    def binarize(self, probability_map, threshold=0.3):
        """
        可微二值化
        """
        return (probability_map > threshold).float()
```

#### 3.1.2 阶段 2: 序列识别

**CRNN (Convolutional Recurrent Neural Network)**:

```python
class CRNNVertical(nn.Module):
    """
    竖排文本识别网络
    """
    
    def __init__(self, num_classes, nc=1, n_rnn=256, leaky_reluf=False):
        super().__init__()
        
        # CNN 特征提取
        self.conv = nn.Sequential(
            nn.Conv2d(nc, 64, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(128, 256, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1), (2, 1)),  # 只压缩高度
            
            nn.Conv2d(256, 512, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(512),
            nn.Conv2d(512, 512, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(512),
            nn.MaxPool2d((2, 1), (2, 1)),
            
            nn.Conv2d(512, 512, 2, 1, 0),
            nn.ReLU(inplace=True),
        )
        
        # RNN 序列建模
        self.rnn = nn.LSTM(512, n_rnn, bidirectional=True, batch_first=True)
        
        # 分类头
        self.fc = nn.Linear(n_rnn * 2, num_classes)
    
    def forward(self, x):
        # CNN 特征
        features = self.conv(x)  # [B, 512, H, W]
        
        # 转换为序列 (竖排：按列扫描)
        b, c, h, w = features.size()
        features = features.view(b, c, h * w).permute(0, 2, 1)  # [B, W*H, C]
        
        # RNN 序列建模
        rnn_out, _ = self.rnn(features)  # [B, W*H, 2*n_rnn]
        
        # 分类
        output = self.fc(rnn_out)  # [B, W*H, num_classes]
        
        return output
```

### 3.2 后处理算法

#### 3.2.1 文本行分组

```python
def group_text_lines(boxes, threshold=10):
    """
    将检测框分组为文本列
    
    Args:
        boxes: 检测框列表 [(x1, y1, x2, y2), ...]
        threshold: 分组阈值 (像素)
    
    Returns:
        columns: 列列表 [[box1, box2, ...], ...]
    """
    # 按 x 坐标排序
    boxes_sorted = sorted(boxes, key=lambda b: b[0])
    
    columns = []
    current_column = [boxes_sorted[0]]
    
    for box in boxes_sorted[1:]:
        # 计算与当前列的平均 x 距离