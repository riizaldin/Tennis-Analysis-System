# 🔍 QUICK REFERENCE: Dataset Locations

## TL;DR - No Conflict!

```
Court Keypoints:  training/Court-Keypoints/  ✅
Ball Detection:   training/tennis-ball-detection-6/  ✅
                  ↑ Different folders = No conflict!
```

---

## Where is Each Dataset?

### 1. Court Keypoints Dataset
```
Location: training/Court-Keypoints/
Images:   training/data/images/
Format:   JSON (14 keypoints per image)
Model:    ResNet50
Output:   Court-Keypoints/exps/skripsi_resnet50/model_best.pt
```

### 2. Ball Detection Dataset
```
Location: training/tennis-ball-detection-6/
Images:   tennis-ball-detection-6/{train,valid,test}/images/
Format:   YOLO TXT (bounding boxes)
Model:    YOLOv8s
Output:   runs/detect/tennis_ball_improved_v6/weights/best.pt
```

---

## Which Notebook Uses Which Dataset?

| Notebook | Dataset | Path |
|----------|---------|------|
| `tennis-court_keypoints_training.ipynb` | Court Keypoints | `Court-Keypoints/` |
| `tennis_ball_detector.ipynb` | Ball Detection | `tennis-ball-detection-6/` |

---

## Path Variables in Code

### Court Keypoints:
```python
# In Court-Keypoints/dataset_resnet.py
data_path = '../data'  # → training/data/
train_json = os.path.join(data_path, 'data_train.json')
```

### Ball Detection:
```python
# In tennis_ball_detector.ipynb
dataset = version.download("yolov8")  # → tennis-ball-detection-6/
stratified_split(dataset.location, ...)  # Works on tennis-ball-detection-6/
```

---

## Checklist Before Running

### Before Court Keypoints Training:
- [ ] Check `training/data/data_train.json` exists
- [ ] Check `training/data/images/` has images
- [ ] Run from `training/Court-Keypoints/`
- [ ] Output will go to `Court-Keypoints/exps/`

### Before Ball Detection Training:
- [ ] Check `training/tennis-ball-detection-6/` exists
- [ ] Check `tennis-ball-detection-6/train/images/` has images
- [ ] Run `tennis_ball_detector.ipynb`
- [ ] Output will go to `runs/detect/`

---

## Safety Check Commands

```python
# Check both datasets exist
import os

court_exists = os.path.exists('training/Court-Keypoints/')
ball_exists = os.path.exists('training/tennis-ball-detection-6/')

print(f"Court Keypoints Dataset: {'✅' if court_exists else '❌'}")
print(f"Ball Detection Dataset:  {'✅' if ball_exists else '❌'}")
```

---

## Expected Output Paths

| Task | Model File | Location |
|------|-----------|----------|
| Court Keypoints | `model_best.pt` | `training/Court-Keypoints/exps/skripsi_resnet50/` |
| Ball Detection | `best.pt` | `training/runs/detect/tennis_ball_improved_v6/weights/` |

---

## When to Use Which?

### Use Court Keypoints Dataset When:
- Training court line detection
- Detecting 14 keypoints on court
- Working with ResNet50
- File: `tennis-court_keypoints_training.ipynb`

### Use Ball Detection Dataset When:
- Training ball detection
- Detecting tennis ball bounding boxes
- Working with YOLOv8s
- File: `tennis_ball_detector.ipynb` ← **YOU ARE HERE**

---

## Final Verdict

**Question:** Will splitting ball detection dataset conflict with court keypoints?

**Answer:** ❌ **NO!** They are in completely separate folders:
- Court: `Court-Keypoints/` and `data/`
- Ball: `tennis-ball-detection-6/`

**Safe to proceed with split!** ✅
