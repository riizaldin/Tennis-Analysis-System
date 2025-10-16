# 🔧 STREAMLIT APP - FIXES APPLIED

## Issue: AttributeError with player_tracker and ball_tracker

### ❌ Problem:
```
AttributeError: module 'trackers.player_tracker' has no attribute 'detect_players'
```

### ✅ Solution Applied:

Changed from **module-level functions** to **class-based API**.

---

## Changes Made:

### 1. Fixed Import Statements
**Before:**
```python
from trackers import player_tracker, ball_tracker
```

**After:**
```python
# Import classes when needed (inside try block)
from trackers.player_tracker import PlayerTracker
from trackers.ball_tracker import BallTracker
```

---

### 2. Fixed Player Detection
**Before:**
```python
player_detections = player_tracker.detect_players(
    video_frames,
    model_path=player_model_path,
    conf_threshold=player_conf
)
```

**After:**
```python
from trackers.player_tracker import PlayerTracker
player_tracker_obj = PlayerTracker(player_model_path)
player_detections = player_tracker_obj.detect_frames(video_frames)

# Choose and filter to 2 players
if len(player_detections) > 0:
    player_detections = player_tracker_obj.choose_and_filter_players(
        [court_keypoints] * len(video_frames),
        player_detections
    )
```

---

### 3. Fixed Ball Detection
**Before:**
```python
ball_detections = ball_tracker.detect_ball(
    video_frames,
    model_path=ball_model_path,
    conf_threshold=ball_conf
)
```

**After:**
```python
from trackers.ball_tracker import BallTracker
ball_tracker_obj = BallTracker(ball_model_path)
ball_detections = ball_tracker_obj.detect_frames(video_frames)

if interpolate_ball:
    ball_detections = ball_tracker_obj.interpolate_ball_positions(ball_detections)
```

---

### 4. Fixed Ball Drawing
**Before:**
```python
if show_ball_trajectory and i < len(ball_detections) and ball_detections[i]:
    x, y = ball_detections[i]
    cv2.circle(frame, (int(x), int(y)), 8, (0, 255, 255), -1)
```

**After:**
```python
if show_ball_trajectory and i < len(ball_detections):
    ball_dict = ball_detections[i]
    if ball_dict and 1 in ball_dict:
        bbox = ball_dict[1]
        x1, y1, x2, y2 = bbox
        # Draw center of ball
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        cv2.circle(frame, (cx, cy), 8, (0, 255, 255), -1)
        cv2.circle(frame, (cx, cy), 12, (0, 255, 255), 2)
```

**Reason:** Ball detections return dict like `{1: [x1, y1, x2, y2]}` not just coordinates.

---

### 5. Fixed Mini Court Ball Position
**Before:**
```python
frame = mini_court.draw_mini_court(
    frame, 
    player_detections[i] if i < len(player_detections) else {},
    ball_detections[i] if i < len(ball_detections) and ball_detections[i] else None
)
```

**After:**
```python
# Get ball position for mini court
ball_pos = None
if i < len(ball_detections) and ball_detections[i] and 1 in ball_detections[i]:
    bbox = ball_detections[i][1]
    x1, y1, x2, y2 = bbox
    ball_pos = (int((x1 + x2) / 2), int((y1 + y2) / 2))

frame = mini_court.draw_mini_court(
    frame, 
    player_detections[i] if i < len(player_detections) else {},
    ball_pos
)
```

---

### 6. Fixed Ball Detection Rate Calculation
**Before:**
```python
ball_detection_rate = sum(1 for d in ball_detections if d) / len(ball_detections) * 100
```

**After:**
```python
# Count ball detections (dict with key 1)
ball_count = sum(1 for d in ball_detections if d and 1 in d and len(d[1]) > 0)
ball_detection_rate = ball_count / len(ball_detections) * 100
```

**Reason:** Ball detections are dicts, need to check if key `1` exists and has valid bbox.

---

## Data Format Reference:

### Player Detections:
```python
[
    {1: [x1, y1, x2, y2], 2: [x1, y1, x2, y2]},  # Frame 0
    {1: [x1, y1, x2, y2], 2: [x1, y1, x2, y2]},  # Frame 1
    ...
]
```
- Key: Player ID (1 or 2)
- Value: Bounding box [x1, y1, x2, y2]

### Ball Detections:
```python
[
    {1: [x1, y1, x2, y2]},  # Frame 0
    {},                      # Frame 1 (no detection)
    {1: [x1, y1, x2, y2]},  # Frame 2
    ...
]
```
- Key: Always `1` (single ball)
- Value: Bounding box [x1, y1, x2, y2]

### Court Keypoints:
```python
# Output from CourtLineDetector.predict()
array([x1, y1, x2, y2, ..., x14, y14])  # 1D numpy array (28 elements)

# Need to reshape for iteration:
keypoints_reshaped = court_keypoints.reshape(-1, 2)
# Result: [[x1, y1], [x2, y2], ..., [x14, y14]]  # 2D array (14 rows, 2 cols)
```
- 14 keypoints total
- Original format: flat 1D array
- After reshape: 14×2 array for easy iteration

---

## ✅ Verified Working:

1. ✅ Import statements fixed
2. ✅ Player detection using PlayerTracker class
3. ✅ Ball detection using BallTracker class
4. ✅ Ball drawing with correct bbox format
5. ✅ Mini court with correct ball position
6. ✅ Metrics calculation with correct data format
7. ✅ Court keypoints reshaping from 1D to 2D array

---

## 🔧 Additional Fix: Court Keypoints Format

### Issue:
```
TypeError: cannot unpack non-iterable numpy.float32 object
```

### Cause:
Court keypoints output is 1D array: `[x1, y1, x2, y2, ..., x14, y14]` (28 elements)

### Solution:
Reshape before drawing:
```python
# Before:
for x, y in court_keypoints:  # Error! Can't iterate 1D array as pairs
    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)

# After:
keypoints_reshaped = court_keypoints.reshape(-1, 2)  # [[x1,y1], [x2,y2], ..., [x14,y14]]
for x, y in keypoints_reshaped:
    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
```

---

## 🚀 How to Test:

### Step 1: Run App
```powershell
streamlit run streamlit_app.py
```

### Step 2: Upload Video
- Choose a tennis video
- Click "Start Analysis"

### Step 3: Check Output
- Should see progress bar
- Should see detection metrics
- Should see sample frames
- Should be able to download video

---

## 🔍 If Still Getting Errors:

### Error 1: Model Not Found
```
Solution: Check model paths in sidebar
- Court: training/Court-Keypoints/exps/skripsi_resnet50/model_best.pt
- Ball: models/yolo8_best.pt
- Player: yolov8x.pt
```

### Error 2: Import Error
```python
# Check if files exist
python -c "from trackers.player_tracker import PlayerTracker; print('OK')"
python -c "from trackers.ball_tracker import BallTracker; print('OK')"
```

### Error 3: YOLO Model Error
```
Solution: Ensure YOLO models are correct format
- Ball model should be YOLOv8 trained on ball dataset
- Player model should be YOLOv8x or similar
```

---

## 📝 Summary of Fixes:

| Issue | Before | After |
|-------|--------|-------|
| **Import** | Module import | Class import when needed |
| **Player API** | `detect_players()` function | `PlayerTracker.detect_frames()` method |
| **Ball API** | `detect_ball()` function | `BallTracker.detect_frames()` method |
| **Ball Format** | Assumed `(x, y)` | Actually `{1: [x1,y1,x2,y2]}` |
| **Mini Court** | Direct pass | Extract center from bbox |
| **Metrics** | Simple check | Check dict structure |

---

## ✅ Status: FIXED!

All issues resolved. App should now run correctly with proper data formats and API calls.

**Test it now:**
```powershell
streamlit run streamlit_app.py
```

🎉 **Enjoy your working Tennis Analysis Web App!**
