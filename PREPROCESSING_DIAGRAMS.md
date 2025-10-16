# 📊 PREPROCESSING VISUAL DIAGRAMS
## For Thesis BAB III - Metodologi

---

## DIAGRAM 1: COMPLETE PREPROCESSING PIPELINE

```
┌─────────────────────────────────────────────────────────────────┐
│                      INPUT VIDEO                                 │
│                  (MP4, 1920×1080, 30fps)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                   ┌────────▼────────┐
                   │ FRAME EXTRACTION│
                   │  cv2.VideoCapture│
                   │  BGR Format     │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
    ┌─────────▼──────┐ ┌───▼────┐ ┌─────▼──────┐
    │ COURT KEYPOINTS│ │PLAYER  │ │   BALL     │
    │   DETECTION    │ │TRACKING│ │ DETECTION  │
    └─────────┬──────┘ └───┬────┘ └─────┬──────┘
              │             │             │
              │             │             │
    ┌─────────▼──────────────────────────────────────┐
    │         PREPROCESSING DETAILS                  │
    └────────────────────────────────────────────────┘
              │             │             │
    ┌─────────▼──────┐ ┌───▼────┐ ┌─────▼──────┐
    │ 14 Keypoints   │ │2 Players│ │Ball Trajectory│
    │ (x,y) × 14     │ │ID: 1,2  │ │ Interpolated  │
    └─────────┬──────┘ └───┬────┘ └─────┬──────┘
              │             │             │
              └─────────────┼─────────────┘
                            │
                   ┌────────▼────────┐
                   │  MINI COURT     │
                   │  TRANSFORMATION │
                   │  Homography     │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │  OUTPUT VIDEO   │
                   │  Visualization  │
                   └─────────────────┘
```

---

## DIAGRAM 2: COURT KEYPOINTS PREPROCESSING (Detailed)

```
┌────────────────────────────────────────────────────┐
│             INPUT FRAME                            │
│         (1920×1080, BGR)                          │
└──────────────────┬─────────────────────────────────┘
                   │
         ┌─────────▼──────────┐
         │ COLOR CONVERSION   │
         │  BGR → RGB         │
         │  cv2.cvtColor()    │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  ToPILImage()      │
         │  numpy → PIL Image │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Resize(224, 224)  │
         │  Bilinear Interp   │
         │  1920×1080 → 224²  │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  ToTensor()        │
         │  [0-255] → [0-1]   │
         │  (H,W,C) → (C,H,W) │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Normalize()       │
         │  ImageNet Stats    │
         │  mean=[0.485,...]  │
         │  std=[0.229,...]   │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Tensor(3,224,224) │
         │  Normalized        │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  ResNet50 Model    │
         │  Forward Pass      │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Output (28 values)│
         │  [x1,y1,...,x14,y14]│
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │ COORDINATE RESCALE │
         │  x *= W/224        │
         │  y *= H/224        │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │ 14 KEYPOINTS       │
         │ Original Size      │
         │ (x,y) coordinates  │
         └────────────────────┘
```

---

## DIAGRAM 3: PLAYER DETECTION PREPROCESSING

```
┌────────────────────────────────────────┐
│        INPUT FRAMES (0-9)              │
│        10 frames for analysis          │
└──────────────┬─────────────────────────┘
               │
     ┌─────────▼──────────┐
     │  YOLO DETECTION    │
     │  Auto Preprocessing │
     │  • Resize 640×640  │
     │  • Letterbox       │
     │  • Normalize /255  │
     │  • BGR → RGB       │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  COLLECT ALL       │
     │  DETECTIONS        │
     │  Per Track ID      │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  FILTER: Appear≥3  │
     │  frames            │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  AVERAGE BBOXES    │
     │  Smooth detection  │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  APPLY FILTERS     │
     │  ├─ Aspect: 1.2-5  │
     │  ├─ Area: >15%     │
     │  └─ Distance check │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  SELECT 2 PLAYERS  │
     │  Best scores       │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  SORT BY Y-POSITION│
     │  Bottom → Top      │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  NORMALIZE IDs     │
     │  Player 1: Bottom  │
     │  Player 2: Top     │
     └─────────┬──────────┘
               │
     ┌─────────▼──────────┐
     │  OUTPUT            │
     │  2 Tracked Players │
     │  Consistent IDs    │
     └────────────────────┘
```

---

## DIAGRAM 4: BALL TRAJECTORY INTERPOLATION

```
FRAME:     1    2    3    4    5    6    7    8    9    10
          ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐
DETECTED: │✓│  │✗│  │✗│  │✓│  │✓│  │✗│  │✗│  │✗│  │✓│  │✗│
          └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘
            │    │    │    │    │    │    │    │    │    │
            ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼
           [x,y] NaN  NaN [x,y][x,y] NaN  NaN  NaN [x,y] NaN

                    ┌───────────────┐
                    │ df.interpolate()│
                    │ Linear Interp  │
                    └───────┬───────┘
                            ▼

FRAME:     1    2    3    4    5    6    7    8    9    10
          ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐
AFTER:    │✓│  │i│  │i│  │✓│  │✓│  │i│  │i│  │i│  │✓│  │b│
          └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘
           │    │    │    │    │    │    │    │    │    │
           ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼
          det  int  int  det  det  int  int  int  det  bfill

Legend:
✓ = Detected by YOLO
✗ = Not detected (NaN)
i = Interpolated value
b = Backfilled value
```

---

## DIAGRAM 5: IMAGE NORMALIZATION PROCESS

```
STEP 1: Original Image (BGR)
┌─────────────────────┐
│  Pixel Value Range  │
│     0 - 255         │
│  Blue, Green, Red   │
└─────────┬───────────┘
          │
STEP 2: Convert to RGB
┌─────────▼───────────┐
│  cv2.cvtColor()     │
│  BGR → RGB          │
│  [B,G,R] → [R,G,B]  │
└─────────┬───────────┘
          │
STEP 3: ToTensor()
┌─────────▼───────────┐
│  Divide by 255      │
│  Range: 0.0 - 1.0   │
│  Shape: (C,H,W)     │
└─────────┬───────────┘
          │
STEP 4: Normalize (ImageNet)
┌─────────▼───────────┐
│  Per Channel:       │
│                     │
│  R: (val - 0.485)   │
│       / 0.229       │
│                     │
│  G: (val - 0.456)   │
│       / 0.224       │
│                     │
│  B: (val - 0.406)   │
│       / 0.225       │
└─────────┬───────────┘
          │
STEP 5: Normalized Tensor
┌─────────▼───────────┐
│  Range: ~[-2, +2]   │
│  Zero-mean          │
│  Unit variance      │
│  Ready for ResNet50 │
└─────────────────────┘
```

---

## DIAGRAM 6: COORDINATE SCALING

```
ORIGINAL IMAGE                RESIZED IMAGE
1920×1080                    224×224
┌──────────────┐            ┌────┐
│              │            │    │
│              │   Resize   │    │
│      •       │  ────────► │  • │
│   (960,540)  │            │(112,112)
│              │            │    │
└──────────────┘            └────┘

SCALING FORMULA:
x_new = x_old × (224 / 1920) = x_old × 0.1167
y_new = y_old × (224 / 1080) = y_old × 0.2074

REVERSE SCALING (after prediction):
x_original = x_pred × (1920 / 224) = x_pred × 8.571
y_original = y_pred × (1080 / 224) = y_pred × 4.821
```

---

## DIAGRAM 7: BATCH PROCESSING

```
INPUT: 100 Frames
┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│1 │2 │3 │4 │5 │6 │7 │8 │9 │10│ ... 100 frames
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
    │                             Batch Size = 8
    ▼
┌──────────────────────────┐
│  Batch 1: Frames 1-8     │
│  ┌─┬─┬─┬─┬─┬─┬─┬─┐       │
│  │1│2│3│4│5│6│7│8│       │
│  └─┴─┴─┴─┴─┴─┴─┴─┘       │
│        │                 │
│  ┌─────▼──────┐          │
│  │Preprocess  │          │
│  │All frames  │          │
│  └─────┬──────┘          │
│        │                 │
│  ┌─────▼──────┐          │
│  │torch.stack │          │
│  │(8,3,224,224)│         │
│  └─────┬──────┘          │
│        │                 │
│  ┌─────▼──────┐          │
│  │GPU Forward │          │
│  │Pass Once   │          │
│  └─────┬──────┘          │
│        │                 │
│  ┌─────▼──────┐          │
│  │8 Predictions│         │
│  └────────────┘          │
└──────────────────────────┘
    │
    ▼
Repeat for Batch 2, 3, ... 13

Benefits:
✓ Faster (GPU parallelization)
✓ Efficient memory usage
✓ Better throughput
```

---

## DIAGRAM 8: PLAYER SELECTION SCORING

```
ALL DETECTED PLAYERS
┌────────────────────────────────────┐
│ ID  Aspect  Area   Dist   Y-pos   │
│ 1   1.78    9119   48     593     │ ← Bottom player
│ 2   1.43    1363   234    313     │
│ 3   2.33    2095   95     197     │ ← Top player
│ 4   2.79    998    133    133     │
│ 5   1.29    2883   322    298     │
└────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ FILTER 1: Aspect Ratio (1.2-5.0)   │
│ ✓ All pass                          │
└─────────────────────┬───────────────┘
                      ▼
┌─────────────────────────────────────┐
│ FILTER 2: Area > 15% max (>1368)   │
│ ✓ ID 1: 9119 > 1368                │
│ ✗ ID 2: 1363 < 1368 (eliminated)   │
│ ✓ ID 3: 2095 > 1368                │
│ ✗ ID 4: 998 < 1368 (eliminated)    │
│ ✓ ID 5: 2883 > 1368                │
└─────────────────────┬───────────────┘
                      ▼
┌─────────────────────────────────────┐
│ COMPOSITE SCORE CALCULATION         │
│ score = w1×aspect_score +           │
│         w2×area_score +              │
│         w3×distance_score            │
│                                      │
│ ID 1: score = 0.052 ← Best (bottom) │
│ ID 3: score = 0.661 ← 2nd (top)     │
│ ID 5: score = 0.810                 │
└─────────────────────┬───────────────┘
                      ▼
┌─────────────────────────────────────┐
│ SELECT TOP 2                        │
│ Player 1 (ID 1): Bottom, Y=593      │
│ Player 2 (ID 3): Top, Y=197         │
└─────────────────────────────────────┘
```

---

## DIAGRAM 9: MINI COURT TRANSFORMATION

```
CAMERA VIEW              COURT COORDINATES        MINI COURT
(Original Frame)         (Real-world meters)      (Visualization)

┌──────────────┐        ┌──────────────┐         ┌────────┐
│              │        │              │         │        │
│              │        │              │         │        │
│    P1 •──────┼────────┼──►Transform─┼─────────┼──► •  │
│    (x1,y1)   │        │  (mx, my)    │         │  (px,py)
│              │  Homo  │              │  Scale  │        │
│              │  graphy│              │         │        │
│    P2 •──────┼────────┼──►Transform─┼─────────┼──► •  │
│    (x2,y2)   │        │  (mx, my)    │         │  (px,py)
│              │        │              │         │        │
└──────────────┘        └──────────────┘         └────────┘
  1920×1080              23.77m × 10.97m          500×250px

Steps:
1. Get player center from bbox
2. Apply homography matrix (from keypoints)
3. Convert to court meters
4. Scale to mini court pixels
```

---

## 📝 Usage in Thesis

### For BAB III (Metodologi):
1. Use **DIAGRAM 1** untuk overview complete pipeline
2. Use **DIAGRAM 2** untuk detail court keypoints preprocessing
3. Use **DIAGRAM 3** untuk player detection flow
4. Use **DIAGRAM 4** untuk explain ball interpolation
5. Use **DIAGRAM 5** untuk normalization math
6. Use **DIAGRAM 6** untuk coordinate scaling formula

### For BAB IV (Hasil):
- Use **DIAGRAM 7** untuk explain batch processing efficiency
- Use **DIAGRAM 8** untuk player selection results
- Use **DIAGRAM 9** untuk visualization transformation

### Tips:
✅ Convert ASCII diagrams to professional flowcharts (Visio/Draw.io)
✅ Add Indonesian labels
✅ Include actual screenshots as examples
✅ Reference diagram numbers in text: "seperti pada Gambar X.X"
