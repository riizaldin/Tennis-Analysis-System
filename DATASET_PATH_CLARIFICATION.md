# 📁 DATASET STRUCTURE & PATH CLARIFICATION

## Training Folder Structure

```
training/
├── Court-Keypoints/              ← COURT KEYPOINTS DATASET
│   ├── data/                     ← JSON files (images in ../data)
│   │   ├── data_train.json       (75%)
│   │   ├── data_val.json         (15%)
│   │   └── data_test.json        (10%)
│   ├── dataset_resnet.py
│   ├── trainer_resnet.py
│   ├── validator_resnet.py
│   ├── split_data.py             ← Split script for keypoints
│   └── exps/
│       └── skripsi_resnet50/
│           └── model_best.pt     ← Trained court model
│
├── tennis-ball-detection-6/      ← BALL DETECTION DATASET
│   ├── train/                    ← Will be re-split to 75%
│   │   ├── images/
│   │   └── labels/
│   ├── valid/                    ← Will be re-split to 15%
│   │   ├── images/
│   │   └── labels/
│   ├── test/                     ← Will be re-split to 10%
│   │   ├── images/
│   │   └── labels/
│   └── data.yaml                 ← YOLO config (auto-updated)
│
├── data/                         ← IMAGES FOR COURT KEYPOINTS
│   ├── images/                   (Shared by both JSONs)
│   ├── data_train.json
│   └── data_val.json
│
├── runs/                         ← Training outputs
│   └── detect/
│       └── tennis_ball_improved_v6/
│           └── weights/
│               └── best.pt       ← Trained ball model
│
├── tennis_ball_detector.ipynb    ← THIS NOTEBOOK (Ball detection)
├── tennis-court_keypoints_training.ipynb  ← Court keypoints
└── yolov8s.pt                    ← Pretrained YOLO weights
```

---

## 🎯 NO CONFLICT - Completely Separate Datasets!

| Aspect | Court Keypoints | Ball Detection |
|--------|----------------|----------------|
| **Location** | `training/Court-Keypoints/` | `training/tennis-ball-detection-6/` |
| **Data Format** | JSON files (annotations) | YOLO format (txt labels) |
| **Images** | In `training/data/images/` | In `tennis-ball-detection-6/{train,valid,test}/images/` |
| **Model Type** | ResNet50 (regression) | YOLOv8s (object detection) |
| **Output** | 14 keypoints (x,y) | Bounding boxes (x,y,w,h) |
| **Split Method** | `split_data.py` (JSON → JSON) | `stratified_split()` (move files between folders) |
| **Split Ratio** | 75-15-10 | 75-15-10 |
| **Trained Model** | `Court-Keypoints/exps/.../model_best.pt` | `runs/detect/.../best.pt` |

---

## 📊 Dataset Paths in Code

### Court Keypoints Training:
```python
# File: training/Court-Keypoints/dataset_resnet.py
data_path = '../data'  # Points to training/data/
# Reads: data_train.json, data_val.json, data_test.json
# Images: training/data/images/*.jpg
```

### Ball Detection Training:
```python
# File: training/tennis_ball_detector.ipynb
dataset = version.download("yolov8")  # Downloads to tennis-ball-detection-6/
dataset.location  # → "training/tennis-ball-detection-6"
# Images: tennis-ball-detection-6/{train,valid,test}/images/*.jpg
```

---

## ✅ Why No Conflict?

### 1. Different Directories
```
Court Keypoints: training/data/images/
Ball Detection:  training/tennis-ball-detection-6/train/images/
                                                   /valid/images/
                                                   /test/images/
```
**→ Completely separate folders!**

### 2. Different File Formats
```
Court Keypoints JSON:
{
  "file_name": "image001.jpg",
  "kps": [[x1,y1], [x2,y2], ..., [x14,y14]]
}

Ball Detection TXT:
0 0.5234 0.6123 0.0234 0.0189
↑ class x_center y_center width height
```
**→ Different annotation formats!**

### 3. Different Split Scripts
```
Court Keypoints:
- Uses split_data.py
- Modifies JSON files in-place
- Creates data_train.json, data_val.json, data_test.json

Ball Detection:
- Uses stratified_split() in notebook
- Moves image files between train/valid/test folders
- Updates data.yaml
```
**→ Different split mechanisms!**

### 4. Different Models
```
Court Keypoints:
- Model: ResNet50
- Input: 224×224 RGB
- Output: 28 values (14 x,y coordinates)
- Saves to: Court-Keypoints/exps/skripsi_resnet50/model_best.pt

Ball Detection:
- Model: YOLOv8s
- Input: 640×640 RGB
- Output: Bounding boxes [x,y,w,h,conf,class]
- Saves to: runs/detect/tennis_ball_improved_v6/weights/best.pt
```
**→ Different model architectures!**

---

## 🔍 Visual Path Verification

### When Running Court Keypoints Training:
```
training/tennis-court_keypoints_training.ipynb
    ↓
Reads: training/data/data_train.json
    ↓
Images: training/data/images/img_0001.jpg
    ↓
Model: training/Court-Keypoints/exps/skripsi_resnet50/model_best.pt
```

### When Running Ball Detection Training:
```
training/tennis_ball_detector.ipynb
    ↓
Downloads: training/tennis-ball-detection-6/
    ↓
Reads: training/tennis-ball-detection-6/train/images/*.jpg
       training/tennis-ball-detection-6/train/labels/*.txt
    ↓
Model: training/runs/detect/tennis_ball_improved_v6/weights/best.pt
```

**→ No overlap in paths!**

---

## 📋 Execution Flow (No Conflicts)

### Phase 1: Court Keypoints (Already Done ✅)
```bash
cd training/Court-Keypoints/
python split_data.py            # Split JSONs once
python main.py                  # Train ResNet50
# Result: model_best.pt (99.29% accuracy)
```

### Phase 2: Ball Detection (Current Task)
```python
# In tennis_ball_detector.ipynb
dataset = download("yolov8")              # Downloads to tennis-ball-detection-6/
stratified_split(dataset.location, ...)  # Re-splits to 75-15-10
model.train(data=f'{dataset.location}/data.yaml')  # Train YOLOv8s
# Result: runs/detect/.../best.pt
```

**→ Completely independent workflows!**

---

## 🎓 For Thesis BAB III

### Dataset Description:
```
Penelitian ini menggunakan dua dataset terpisah:

1. Dataset Court Keypoints:
   - Lokasi: training/Court-Keypoints/
   - Total: 7,160 images
   - Format: JSON annotations dengan 14 keypoints
   - Split: 75% training (5,370), 15% validation (1,074), 10% testing (716)
   - Model: ResNet50
   
2. Dataset Ball Detection:
   - Lokasi: training/tennis-ball-detection-6/
   - Total: ~1,000 images (dari Roboflow)
   - Format: YOLO annotations (bounding boxes)
   - Split: 75% training, 15% validation, 10% testing (stratified by ball size)
   - Model: YOLOv8s

Kedua dataset disimpan di direktori terpisah dan tidak ada konflik dalam 
proses preprocessing maupun training.
```

---

## ⚠️ Important Notes

### DO NOT:
- ❌ Mix court keypoints images with ball detection images
- ❌ Use same model file for both tasks
- ❌ Run split scripts on wrong dataset
- ❌ Modify Court-Keypoints/ when working on ball detection

### DO:
- ✅ Keep datasets in separate folders
- ✅ Use different model output paths
- ✅ Document both datasets separately in thesis
- ✅ Train models independently

---

## 🔧 Verification Commands

### Check Court Keypoints Dataset:
```python
import json
with open('training/data/data_train.json') as f:
    train_data = json.load(f)
print(f"Court keypoints training images: {len(train_data)}")
# Expected: ~5,370 images
```

### Check Ball Detection Dataset:
```python
from pathlib import Path
ball_train = Path('training/tennis-ball-detection-6/train/images')
print(f"Ball detection training images: {len(list(ball_train.glob('*.jpg')))}")
# Expected after split: ~750 images (75%)
```

### Check No Overlap:
```python
# Court keypoints images
court_imgs = set([img['file_name'] for img in train_data])

# Ball detection images
ball_imgs = set([img.name for img in ball_train.glob('*.jpg')])

# Check overlap
overlap = court_imgs & ball_imgs
print(f"Overlapping images: {len(overlap)}")
# Expected: 0 (no overlap!)
```

---

## 📊 Summary Table

| Feature | Court Keypoints | Ball Detection | Conflict? |
|---------|----------------|----------------|-----------|
| Directory | `Court-Keypoints/` | `tennis-ball-detection-6/` | ✅ No |
| Images | `data/images/` | `{train,valid,test}/images/` | ✅ No |
| Annotations | JSON files | TXT files | ✅ No |
| Model | ResNet50 | YOLOv8s | ✅ No |
| Output | 28 coordinates | Bounding boxes | ✅ No |
| Training script | `main.py` | `tennis_ball_detector.ipynb` | ✅ No |
| Model save path | `exps/skripsi_resnet50/` | `runs/detect/tennis_ball_improved_v6/` | ✅ No |
| Split ratio | 75-15-10 | 75-15-10 | ✅ Consistent |
| Split method | `split_data.py` | `stratified_split()` | ✅ Different scripts |

**VERDICT: ✅ NO CONFLICTS - Completely safe to train both models!**
