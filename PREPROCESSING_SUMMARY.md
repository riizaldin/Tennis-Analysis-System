# 📋 PREPROCESSING SUMMARY - Quick Reference

## ✅ Tahap-Tahap Preprocessing dalam Kode

### 1️⃣ **VIDEO LOADING**
```python
frames = read_video('input_video.mp4')
```
- Load video → list of frames
- Format: BGR (OpenCV default)
- Shape: (H, W, 3)

---

### 2️⃣ **COURT KEYPOINTS PREPROCESSING**

#### A. Color Space Conversion
```python
image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```
- BGR → RGB (PyTorch requirement)

#### B. Image Transformations
```python
transforms.Compose([
    ToPILImage(),              # numpy → PIL
    Resize((224, 224)),        # Resize ke ResNet50 input size
    ToTensor(),                # PIL → Tensor, [0-255] → [0.0-1.0]
    Normalize(                 # ImageNet normalization
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])
```

**Formula Normalization:**
```
normalized = (pixel - mean) / std
```

#### C. Coordinate Rescaling (Post-processing)
```python
keypoints[::2] *= original_w / 224.0   # x coords
keypoints[1::2] *= original_h / 224.0  # y coords
```
- Scale dari 224×224 → original size

---

### 3️⃣ **PLAYER DETECTION PREPROCESSING**

#### A. YOLO Auto-Preprocessing (Built-in)
- Resize: 640×640
- Letterboxing (maintain aspect ratio)
- Normalization: /255.0
- BGR → RGB

#### B. Multi-Frame Filtering
```python
# Ambil 10 frames pertama
num_frames_to_analyze = 10

# Average bboxes untuk smooth detection
avg_bbox = [sum(x)/len(x) for x in zip(*bboxes)]
```

#### C. Player Selection Filters
1. **Aspect Ratio**: 1.2 ≤ ratio ≤ 5.0
2. **Area**: > 15% dari largest detection
3. **Distance**: Proximity ke court center
4. **Consistency**: Appear ≥ 3 frames

#### D. ID Normalization
```python
# Sort by Y position (bottom to top)
player_1 = bottom_player  # Higher Y
player_2 = top_player     # Lower Y
```

---

### 4️⃣ **BALL DETECTION PREPROCESSING**

#### A. YOLO Detection
```python
results = model.predict(frame, conf=0.15)
```
- Lower confidence (0.15) untuk ball kecil

#### B. Interpolation
```python
df = pd.DataFrame(detections)
df = df.interpolate()     # Fill missing frames
df = df.bfill()          # Backfill initial NaN
```

**Example:**
```
Frame:  1   2   3   4   5
Before: ✓   ✗   ✗   ✓   ✓
After:  ✓  (i) (i)  ✓   ✓
```

---

### 5️⃣ **MINI COURT TRANSFORMATION**

```python
# Transform coordinates
player_pos = get_center_of_bbox(bbox)
court_pos = transform_to_court(player_pos, keypoints)
mini_court_pos = scale_to_mini_court(court_pos)
```

- Bounding box → player center
- Player position → court coordinates
- Court → mini court scaling

---

### 6️⃣ **TRAINING DATA PREPROCESSING**

```python
# Image
img = cv2.imread(path)              # Load BGR
img_rgb = cv2.cvtColor(img, BGR2RGB) # Convert RGB
img_tensor = transform(img_rgb)     # Resize + Normalize

# Keypoints
kps[:, 0] *= 224.0 / original_w    # Scale x
kps[:, 1] *= 224.0 / original_h    # Scale y
kps_flat = kps.flatten()           # (14,2) → (28,)
```

---

### 7️⃣ **CACHING**

```python
# Save
pickle.dump(detections, file)

# Load
detections = pickle.load(file)
```

- Avoid re-computation
- ~100× faster loading

---

## 📊 Preprocessing by Component

| Component | Input | Preprocessing | Output |
|-----------|-------|---------------|--------|
| **Video** | MP4 file | Extract frames | List[ndarray] BGR |
| **Court** | BGR frame | RGB→Resize(224²)→Normalize | 14 keypoints (x,y) |
| **Player** | BGR frame | YOLO(640²)→Filter→Normalize | 2 players (bbox) |
| **Ball** | BGR frame | YOLO(640²)→Interpolate | Ball trajectory |
| **Mini Court** | Positions | Homography transform | Mini court coords |

---

## 🔢 Important Numbers

### Image Sizes
- **Original Frame**: 1920×1080 (or video size)
- **Court Detection**: 224×224 (ResNet50)
- **YOLO Detection**: 640×640 (YOLOv8)
- **Mini Court**: Custom (misal 500×250)

### Normalization Values (ImageNet)
- **Mean**: [0.485, 0.456, 0.406] (RGB)
- **Std**: [0.229, 0.224, 0.225] (RGB)

### Detection Thresholds
- **Player conf**: 0.25 (default YOLO)
- **Ball conf**: 0.15 (lower, karena small object)
- **Player filter**: Aspect 1.2-5.0, Area >15%

### Batch Processing
- **Court keypoints**: batch_size = 8
- **YOLO**: single frame (real-time)

---

## 🎯 Key Formulas

### 1. Pixel Normalization
```
normalized = (pixel / 255.0 - mean) / std
```

### 2. Coordinate Scaling
```
scaled_x = original_x * target_size / original_size
```

### 3. Linear Interpolation
```
interpolated = start + (end - start) * t
where t = current_frame / total_frames
```

### 4. Bounding Box Center
```
center_x = (x1 + x2) / 2
center_y = (y1 + y2) / 2
```

### 5. Aspect Ratio
```
aspect_ratio = bbox_width / bbox_height
```

---

## 🔄 Complete Flow

```
VIDEO
  ↓
FRAME EXTRACTION (BGR)
  ↓
┌─────────────┬──────────────┬────────────┐
│             │              │            │
COURT KPs     PLAYERS        BALL
│             │              │
BGR→RGB       YOLO Auto      YOLO Auto
Resize 224²   Resize 640²    Resize 640²
Normalize     Filter         Interpolate
ImageNet      ID Norm        
│             │              │
14 KPs        2 Players      Ball Traj
└─────────────┴──────────────┴────────────┘
                      ↓
              MINI COURT TRANSFORM
                      ↓
              VISUALIZATION
```

---

## 📝 For Documentation (BAB III)

Jelaskan preprocessing dalam urutan ini:

1. **Ekstraksi Frame**
   - Video → frames
   - OpenCV VideoCapture
   
2. **Preprocessing Court Keypoints**
   - Color conversion (BGR→RGB)
   - Resize (original→224×224)
   - Normalization (ImageNet stats)
   - Coordinate rescaling (224×224→original)

3. **Preprocessing Player Detection**
   - YOLO automatic preprocessing
   - Multi-frame averaging
   - Filtering (aspect, area, distance)
   - ID normalization

4. **Preprocessing Ball Detection**
   - YOLO detection
   - Trajectory interpolation
   - Backfill missing frames

5. **Coordinate Transformation**
   - Player position extraction
   - Homography to court coordinates
   - Scaling to mini court

---

## 💡 Tips untuk Thesis

✅ **Gunakan diagram flowchart** untuk setiap tahap  
✅ **Include formula matematis** (normalization, scaling)  
✅ **Explain WHY** setiap preprocessing diperlukan  
✅ **Show before/after examples** (visual comparison)  
✅ **Mention ImageNet transfer learning** (justify normalization)  
✅ **Discuss interpolation benefits** (smooth trajectory)

---

**File lengkap**: `PREPROCESSING_DOCUMENTATION.md`
