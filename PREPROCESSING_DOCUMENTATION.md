# 📊 PREPROCESSING PROCESSES - Tennis Analysis System

## Overview
Dokumentasi lengkap semua tahap preprocessing yang terjadi dalam sistem analisis tenis ini.

---

## 🎬 1. VIDEO PREPROCESSING

### 1.1 Video Loading (`utils/video_utils.py`)
```python
def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
```

**Proses:**
- ✅ Baca file video dengan OpenCV
- ✅ Ekstrak semua frame menjadi list numpy arrays
- ✅ Format: BGR color space (default OpenCV)
- ✅ Shape: (height, width, 3)

**Output:**
- List of frames: `[frame1, frame2, ..., frameN]`
- Setiap frame: numpy array (H×W×3)

---

## 🎾 2. COURT KEYPOINTS DETECTION PREPROCESSING

### 2.1 Color Space Conversion
```python
image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

**Proses:**
- ✅ Convert dari BGR (OpenCV default) ke RGB
- ✅ Diperlukan karena PyTorch model di-train dengan RGB
- ✅ Reorder channels: [B, G, R] → [R, G, B]

### 2.2 Image Transformation Pipeline
```python
self.transform = transforms.Compose([
    transforms.ToPILImage(),           # Step 1
    transforms.Resize((224, 224)),     # Step 2
    transforms.ToTensor(),             # Step 3
    transforms.Normalize(              # Step 4
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    )
])
```

**Proses Detail:**

#### Step 1: ToPILImage()
- Convert numpy array → PIL Image
- Tetap RGB format
- Diperlukan untuk resize operations

#### Step 2: Resize((224, 224))
- **Input**: Original frame size (misal: 1920×1080)
- **Output**: 224×224 pixels
- **Method**: Bilinear interpolation (default)
- **Reason**: ResNet50 membutuhkan input 224×224

**Impact pada Keypoints:**
```
Original:  x, y in (1920×1080)
Resized:   x, y in (224×224)
Scale:     x *= 224/1920, y *= 224/1080
```

#### Step 3: ToTensor()
- Convert PIL Image → PyTorch Tensor
- Shape: (H, W, C) → (C, H, W)
- Type: uint8 [0-255] → float32 [0.0-1.0]
- Formula: `pixel_value / 255.0`

#### Step 4: Normalize (ImageNet Stats)
```python
mean = [0.485, 0.456, 0.406]  # R, G, B channels
std = [0.229, 0.224, 0.225]   # R, G, B channels
```

**Formula per channel:**
```
normalized_value = (pixel_value - mean) / std
```

**Example:**
```
Input pixel (R channel):  0.8 (after ToTensor)
Normalized: (0.8 - 0.485) / 0.229 = 1.376
```

**Why ImageNet normalization?**
- ResNet50 di-train dengan ImageNet dataset
- ImageNet mean/std adalah statistik dari 1.2M images
- Transfer learning membutuhkan normalisasi yang sama

### 2.3 Batch Processing
```python
batch_tensors = []
for frame in batch_frames:
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_tensor = self.transform(image_rgb)
    batch_tensors.append(image_tensor)

batch_tensor = torch.stack(batch_tensors)  # (batch_size, 3, 224, 224)
```

**Proses:**
- ✅ Process 8 frames sekaligus (batch_size=8)
- ✅ Stack menjadi 4D tensor: (B, C, H, W)
- ✅ Efficient GPU utilization

### 2.4 Post-Processing (Coordinate Rescaling)
```python
keypoints = outputs.squeeze().cpu().numpy()  # (28,) - [x1,y1,...,x14,y14]
original_h, original_w = image.shape[:2]

# Scale back dari 224x224 ke ukuran original
keypoints[::2] *= original_w / 224.0   # x coordinates
keypoints[1::2] *= original_h / 224.0  # y coordinates
```

**Proses:**
- ✅ Model output: koordinat dalam 224×224 space
- ✅ Scale back ke ukuran original frame
- ✅ `keypoints[::2]` = x coords (index 0, 2, 4, ...)
- ✅ `keypoints[1::2]` = y coords (index 1, 3, 5, ...)

---

## 👥 3. PLAYER DETECTION PREPROCESSING

### 3.1 YOLO Preprocessing (Built-in)
```python
self.model = YOLO('yolov8x')
results = self.model.predict(frame, conf=0.25)
```

**YOLO Internal Preprocessing:**
1. **Resize**: Auto-resize ke 640×640 (YOLOv8 default)
2. **Letterboxing**: Add padding untuk maintain aspect ratio
3. **Normalization**: pixel / 255.0
4. **Channel ordering**: BGR → RGB (automatic)
5. **Tensor conversion**: (H, W, C) → (C, H, W)

**No manual preprocessing needed!** YOLO handles it internally.

### 3.2 Player Filtering
```python
# Ambil detections dari 10 frames pertama
num_frames_to_analyze = min(10, len(player_detection))

# Calculate average bbox untuk setiap track_id
for track_id, bboxes in all_detections.items():
    if len(bboxes) >= 3:  # Min 3 appearances
        avg_bbox = [
            sum(b[0] for b in bboxes) / len(bboxes),  # avg x1
            sum(b[1] for b in bboxes) / len(bboxes),  # avg y1
            sum(b[2] for b in bboxes) / len(bboxes),  # avg x2
            sum(b[3] for b in bboxes) / len(bboxes)   # avg y2
        ]
```

**Proses:**
- ✅ Ambil 10 frames pertama untuk robust selection
- ✅ Filter tracks yang appear minimal 3× (reduce noise)
- ✅ Average bounding boxes untuk smooth detection
- ✅ Kurangi false positives

### 3.3 Player Selection Criteria
```python
# Aspect ratio filter
aspect_ratio = bbox_width / bbox_height
if 1.2 <= aspect_ratio <= 5.0:  # Valid player shape

# Area filter  
area = bbox_width * bbox_height
if area > 0.15 * max_area:  # At least 15% of largest detection

# Distance from court center
distance = euclidean_distance(player_center, court_center)
```

**Filters:**
1. **Aspect Ratio**: 1.2-5.0 (eliminasi objek non-manusia)
2. **Area**: >15% dari largest detection (eliminasi small objects)
3. **Distance**: Proximity ke court center (pilih on-court players)
4. **Y-position**: Bottom player vs top player separation

### 3.4 Player ID Normalization
```python
# Sort by Y position (bottom-to-top)
sorted_players = sorted(chosen_players, 
                       key=lambda x: avg_detections[x][3],  # y2 coord
                       reverse=True)  # Descending (bottom first)

# Assign IDs
player_1 = sorted_players[0]  # Bottom player (higher Y)
player_2 = sorted_players[1]  # Top player (lower Y)
```

**Proses:**
- ✅ Normalize arbitrary track IDs → consistent IDs (1, 2)
- ✅ Player 1 = bottom player (near baseline)
- ✅ Player 2 = top player (opposite side)

---

## 🎾 4. BALL DETECTION PREPROCESSING

### 4.1 YOLO Detection
```python
self.model = YOLO('models/yolo8_best6.pt')  # Custom trained
results = self.model.predict(frame, conf=0.15)  # Lower confidence
```

**YOLO Preprocessing (same as player):**
- Resize to 640×640
- Letterboxing
- Normalization
- RGB conversion

**Configuration:**
- **conf=0.15**: Lower threshold karena ball kecil & fast
- **Custom model**: Trained khusus untuk tennis ball

### 4.2 Ball Interpolation
```python
df_ball_detections = pd.DataFrame(ball_detections, 
                                 columns=['x1', 'y1', 'x2', 'y2'])
df_ball_detections = df_ball_detections.interpolate()
df_ball_detections = df_ball_detections.bfill()
```

**Proses:**
- ✅ Convert detections → pandas DataFrame
- ✅ **Interpolate**: Fill missing frames (ball not detected)
- ✅ **Backfill**: Fill initial NaN values
- ✅ Result: Smooth ball trajectory

**Example:**
```
Frame:     1    2    3    4    5    6
Detection: X    -    -    X    X    -
After:     X   X/2  X/2   X    X   X(bf)
           ↑   ↑____↑    ↑    ↑    ↑
        detected interpolated detected backfilled
```

---

## 📐 5. MINI COURT PREPROCESSING

### 5.1 Coordinate Transformation
```python
# Transform dari court coordinates → mini court coordinates
def convert_meters_to_pixels(self, meters_x, meters_y, ...)
def convert_bounding_boxes_to_mini_court_coordinates(...)
```

**Proses:**
1. **Calculate player position** (x, y) dari bounding box
2. **Map ke court coordinates** using keypoints homography
3. **Scale to mini court** (proportional scaling)
4. **Draw on mini court** (visualization)

### 5.2 Homography Transformation
```python
# Get transformation matrix dari court keypoints
court_width = measure_distance(kp[0], kp[2])  # meters
court_height = measure_distance(kp[0], kp[1])  # meters

# Scale factor
scale_x = mini_court_width / court_width
scale_y = mini_court_height / court_height
```

---

## 📊 6. TRAINING DATA PREPROCESSING

### 6.1 Data Loading (`dataset_resnet.py`)
```python
# Read image
img = cv2.imread(img_path)  # BGR format

# Get original dimensions
original_h, original_w = img.shape[:2]

# Convert to RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

### 6.2 Keypoints Normalization
```python
kps = np.array(item['kps'], dtype=np.float32)  # (14, 2)
kps_normalized = kps.copy()

# Scale coordinates dari original size → 224x224
kps_normalized[:, 0] = kps[:, 0] * 224.0 / original_w  # x
kps_normalized[:, 1] = kps[:, 1] * 224.0 / original_h  # y

# Flatten to [x1, y1, x2, y2, ..., x14, y14]
kps_flat = kps_normalized.flatten().astype(np.float32)  # (28,)
```

**Ground Truth Format:**
```json
{
    "id": "image_001",
    "kps": [
        [x1, y1],   // Keypoint 0
        [x2, y2],   // Keypoint 1
        ...
        [x14, y14]  // Keypoint 13
    ]
}
```

### 6.3 Data Augmentation (Training Only)
```python
self.transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    # No augmentation untuk maintain keypoint accuracy
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225])
])
```

**Note:** No rotation/flip augmentation untuk preserve keypoint positions!

---

## 🔄 7. CACHING MECHANISM

### 7.1 Pickle Serialization
```python
# Save detections
with open(stub_path, 'wb') as f:
    pickle.dump(detections, f)

# Load detections
with open(stub_path, 'rb') as f:
    detections = pickle.load(f)
```

**Benefits:**
- ✅ Avoid re-running expensive detections
- ✅ Fast loading (~100× faster)
- ✅ Consistent results across runs

**Cache Files:**
```
tracker_stubs/
├── player_detections_input_video5.pkl
├── ball_detections_input_video5.pkl
└── court_keypoints_input_video5.pkl
```

---

## 📈 SUMMARY: Complete Preprocessing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    VIDEO INPUT                               │
│                  (1920×1080 BGR)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────┐      ┌────────┐     ┌──────────┐
    │COURT   │      │PLAYER  │     │  BALL    │
    │KEYPTS  │      │DETECT  │     │ DETECT   │
    └───┬────┘      └───┬────┘     └────┬─────┘
        │               │                │
        │ BGR→RGB       │ Auto YOLO      │ Auto YOLO
        │ Resize 224²   │ Resize 640²    │ Resize 640²
        │ Normalize     │ Track IDs      │ conf=0.15
        │ ImageNet      │ Filter+Norm    │ Interpolate
        ▼               ▼                ▼
    ┌────────┐      ┌────────┐     ┌──────────┐
    │14 KPs  │      │2 Players│    │Ball Traj │
    │(x,y)×14│      │ID: 1,2  │    │Smoothed  │
    └───┬────┘      └───┬────┘     └────┬─────┘
        │               │                │
        └───────────────┼────────────────┘
                        ▼
              ┌──────────────────┐
              │  MINI COURT      │
              │  Homography      │
              │  Visualization   │
              └──────────────────┘
```

---

## 🎯 Key Preprocessing Techniques

| Component | Technique | Purpose |
|-----------|-----------|---------|
| **Court Keypoints** | ImageNet Normalization | Transfer learning compatibility |
| **Court Keypoints** | Resize 224×224 | ResNet50 input requirement |
| **Court Keypoints** | Coordinate Rescaling | Map predictions to original size |
| **Player Detection** | Multi-frame Averaging | Robust player selection |
| **Player Detection** | Aspect Ratio Filter | Remove false positives |
| **Player Detection** | ID Normalization | Consistent player tracking |
| **Ball Detection** | Linear Interpolation | Smooth missing detections |
| **Ball Detection** | Backfill | Handle initial frames |
| **All Components** | Caching (Pickle) | Performance optimization |
| **Training** | Keypoint Normalization | Scale-invariant learning |

---

## 📝 For Thesis (BAB III - Metodologi)

Gunakan dokumentasi ini untuk menjelaskan tahap preprocessing di BAB III dengan detail:

1. **Ekstraksi Frame dari Video**
2. **Preprocessing Deteksi Court Keypoints** (Color conversion, Resize, Normalization)
3. **Preprocessing Deteksi Player** (YOLO auto-preprocessing, Filtering, Normalization)
4. **Preprocessing Deteksi Ball** (YOLO detection, Interpolation)
5. **Transformasi Koordinat ke Mini Court**

Setiap tahap bisa dijelaskan dengan gambar flowchart dan formula matematis! 📊
