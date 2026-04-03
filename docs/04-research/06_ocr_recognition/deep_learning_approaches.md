# 深度学习方法

**文档版本**: 1.0  
**创建日期**: 2026-04-03  
**最后更新**: 2026-04-03  
**作者**: Mongolian AI Assistant Team  
**状态**: ✅ 完成

---

## 目录

1. [概述](#概述)
2. [OCR 技术架构](#ocr-技术架构)
3. [文本检测模型](#文本检测模型)
4. [文本识别模型](#文本识别模型)
5. [端到端模型](#端到端模型)
6. [竖排文本特殊处理](#竖排文本特殊处理)
7. [训练实践](#训练实践)
8. [部署优化](#部署优化)
9. [性能对比](#性能对比)
10. [参考资料](#参考资料)

---

## 概述

### 现代 OCR 技术栈

```
┌─────────────────────────────────────────────────────────┐
│                     输入图像                              │
│                  (竖排蒙古文)                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  文本检测 (Detection)                    │
│  DBNet / EAST / PSENet / FCENet                         │
│  输出：文本区域 bounding box / polygon                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│             文本矫正 (Rectification) [可选]              │
│  STN / Thin-Plate Spline                                │
│  输出：矫正后的文本图像                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  文本识别 (Recognition)                  │
│  CRNN / TRBA / SVTR / ABINet                            │
│  输出：Unicode 文本序列                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  后处理 (Post-processing)                │
│  语言模型校正 / FVS 恢复 / 规范化                         │
│  输出：最终识别结果                                      │
└─────────────────────────────────────────────────────────┘
```

### 蒙古文 OCR 特殊挑战

| 挑战 | 描述 | 解决方案 |
|------|------|---------|
| 竖排文本 | 主流模型针对横排优化 | 旋转图像 or 修改模型 |
| 连写 | 字母连接紧密 | 序列建模 (CTC/Attention) |
| FVS 变体 | 零宽变体选择符 | 特殊 token 处理 |
| 数据稀缺 | 标注数据少 | 合成数据 + 迁移学习 |

---

## OCR 技术架构

### 两阶段架构 (主流)

```python
import torch
import torch.nn as nn

class TwoStageOCR(nn.Module):
    def __init__(self, detector, recognizer):
        super().__init__()
        self.detector = detector
        self.recognizer = recognizer
    
    def forward(self, image):
        # 阶段 1: 检测
        detections = self.detector(image)
        
        # 阶段 2: 对每个检测区域识别
        results = []
        for det in detections:
            roi = crop_roi(image, det.bbox)
            text = self.recognizer(roi)
            results.append({
                'bbox': det.bbox,
                'text': text,
                'confidence': det.confidence
            })
        
        return results
```

### 端到端架构

```python
class EndToEndOCR(nn.Module):
    def __init__(self, backbone, decoder):
        super().__init__()
        self.backbone = backbone  # ResNet / ViT
        self.decoder = decoder     # Transformer
    
    def forward(self, image):
        # 特征提取
        features = self.backbone(image)
        
        # 同时预测检测和识别
        detections, texts = self.decoder(features)
        
        return detections, texts
```

---

## 文本检测模型

### DBNet (Differentiable Binarization)

**论文**: Real-time Scene Text Detection with Differentiable Binarization (AAAI 2020)

**特点**:
- ✅ 实时性能
- ✅ 高精度
- ✅ 适合密集文本

**架构**:
```python
import segmentation_models_pytorch as smp

class DBNet(smp.DeepLabV3Plus):
    def __init__(self):
        super().__init__(
            encoder_name='resnet18',
            encoder_weights='imagenet',
            in_channels=3,
            classes=1  # 前景/背景
        )
        
        # 可微二值化
        self.threshold = nn.Parameter(torch.ones(1))
    
    def forward(self, x):
        # 概率图
        prob_map = super().forward(x)
        
        # 二值化
        binary_map = (prob_map > self.threshold).float()
        
        return prob_map, binary_map
```

**训练**:
```python
# DBNet loss
class DBLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.bce_loss = nn.BCELoss()
        self.l1_loss = nn.L1Loss()
    
    def forward(self, prob_pred, prob_gt, binary_pred, binary_gt):
        # 概率图损失
        prob_loss = self.bce_loss(prob_pred, prob_gt)
        
        # 二值图损失
        binary_loss = self.bce_loss(binary_pred, binary_gt)
        
        # 差异损失
        diff_loss = self.l1_loss(prob_pred, binary_pred)
        
        return prob_loss + binary_loss + 0.1 * diff_loss
```

### EAST (Efficient and Accurate Scene Text Detector)

**论文**: EAST: An Efficient and Accurate Scene Text Detector (CVPR 2017)

**特点**:
- ✅ 单阶段检测
- ✅ 支持多方向文本
- ⚠️ 后处理复杂

### PSENet (Shape Robust Text Detection)

**论文**: Shape Robust Text Detection with Progressive Scale Expansion Network (CVPR 2019)

**特点**:
- ✅ 适合弯曲文本
- ✅ 鲁棒性强
- ⚠️ 速度较慢

### 蒙古文适配

```python
class MongolianDBNet(DBNet):
    """
    针对竖排蒙古文优化的 DBNet
    """
    def __init__(self):
        super().__init__()
        
        # 修改 anchor 比例 (竖排文本高宽比大)
        self.anchor_ratios = [0.2, 0.5, 1.0]  # 横排：[1, 2, 5]
    
    def rotate_image(self, image):
        """
        将竖排图像旋转 90 度，适配横排模型
        """
        return torch.rot90(image, k=1, dims=[-2, -1])
    
    def forward(self, image):
        # 旋转图像
        rotated = self.rotate_image(image)
        
        # 检测
        prob_map, binary_map = super().forward(rotated)
        
        # 旋转回原方向
        prob_map = torch.rot90(prob_map, k=3, dims=[-2, -1])
        binary_map = torch.rot90(binary_map, k=3, dims=[-2, -1])
        
        return prob_map, binary_map
```

---

## 文本识别模型

### CRNN (Convolutional Recurrent Neural Network)

**论文**: An End-to-End Trainable Neural Network for Image-based Sequence Recognition (TPAMI 2017)

**架构**:
```
CNN (特征提取) → BiLSTM (序列建模) → CTC (解码)
```

```python
class CRNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        
        # CNN  backbone
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d((2, 1), (2, 1)),  # 只压缩高度
            nn.Conv2d(256, 512, 3, padding=1),
            nn.ReLU(),
        )
        
        # BiLSTM
        self.rnn = nn.LSTM(
            input_size=512,
            hidden_size=256,
            num_layers=2,
            bidirectional=True,
            batch_first=True
        )
        
        # 分类头
        self.classifier = nn.Linear(512, num_classes)
    
    def forward(self, image):
        # CNN 特征
        features = self.cnn(image)  # [B, 512, H, W]
        
        # 转换为序列
        b, c, h, w = features.shape
        features = features.view(b, c, h * w).permute(0, 2, 1)  # [B, W, C]
        
        # RNN 序列建模
        rnn_out, _ = self.rnn(features)  # [B, W, 512]
        
        # 分类
        logits = self.classifier(rnn_out)  # [B, W, num_classes]
        
        return logits
```

**CTC 解码**:
```python
import torch.nn.functional as F

def ctc_decode(logits, blank_index=0):
    """
    CTC 贪婪解码
    """
    # softmax
    probs = F.softmax(logits, dim=-1)
    
    # 贪婪解码
    _, predictions = torch.max(probs, dim=-1)
    
    # 去除重复和 blank
    decoded = []
    for pred in predictions:
        prev = None
        text = []
        for idx in pred:
            if idx != blank_index and idx != prev:
                text.append(idx.item())
            prev = idx
        decoded.append(text)
    
    return decoded
```

### TRBA (Transformation-Based Recognition)

**论文**: On Recognizing Texts of Arbitrary Shapes with 2D Recurrence (CVPR 2020)

**架构**:
```
STN (矫正) → ResNet (特征) → BiLSTM (序列) → Attention (解码)
```

```python
class TRBA(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        
        # 空间变换网络
        self.stn = TPS_SpatialTransformer()
        
        # 特征提取
        self.resnet = ResNet(34)
        
        # 序列建模
        self.lstm = nn.LSTM(512, 256, 2, bidirectional=True)
        
        # Attention 解码
        self.attention = AttentionDecoder(512, num_classes)
    
    def forward(self, image):
        # 矫正
        corrected = self.stn(image)
        
        # 特征
        features = self.resnet(corrected)
        
        # 序列
        seq_out, _ = self.lstm(features)
        
        # Attention 解码
        text = self.attention(seq_out)
        
        return text
```

### SVTR (Scene Text Recognition with Visual Transformer)

**论文**: SVTR: Scene Text Recognition with Visual Transformer (IJCAI 2022)

**特点**:
- ✅ 纯 Transformer 架构
- ✅ 全局上下文建模
- ✅ SOTA 性能

```python
class SVTR(nn.Module):
    def __init__(self, num_classes, img_size=(32, 100)):
        super().__init__()
        
        # Patch embedding
        self.patch_embed = PatchEmbed(
            img_size=img_size,
            patch_size=(2, 2),
            in_chans=3,
            embed_dim=192
        )
        
        # Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(dim=192, num_heads=6)
            for _ in range(12)
        ])
        
        # Head
        self.head = nn.Linear(192, num_classes)
    
    def forward(self, image):
        # Patch embedding
        x = self.patch_embed(image)
        
        # Transformer
        for block in self.blocks:
            x = block(x)
        
        # 分类
        logits = self.head(x)
        
        return logits
```

### 蒙古文适配

```python
class MongolianCRNN(CRNN):
    """
    针对蒙古文优化的 CRNN
    """
    def __init__(self, num_classes=500):
        # 蒙古文字符集：~160 基本字符 + FVS + 标点
        super().__init__(num_classes)
        
        # 特殊 token
        self.fvs1_token = num_classes - 3
        self.fvs2_token = num_classes - 2
        self.fvs3_token = num_classes - 1
    
    def postprocess(self, predictions):
        """
        后处理：恢复 FVS 序列
        """
        results = []
        for pred in predictions:
            text = []
            for i, idx in enumerate(pred):
                char = self.idx_to_char[idx]
                text.append(char)
                
                # 检查 FVS
                if i + 1