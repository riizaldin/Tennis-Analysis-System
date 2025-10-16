# 🎾 Streamlit App - Final Version with Moving Camera Support

## ✅ What's Implemented

### 1. **Complete Original Structure Restored**
- ✅ Sidebar dengan semua konfigurasi
- ✅ Wide layout untuk tampilan profesional
- ✅ 3-column video upload dengan info box
- ✅ Progress bar dengan status updates
- ✅ Sample frames display (4 frames)
- ✅ Download button untuk hasil

### 2. **Moving Camera Detection Integrated**
```python
if enable_moving_camera:
    # Detect court in ALL frames
    court_keypoints = court_detector.predict_video(video_frames)
    st.success(f"✅ Court detected in {len(court_keypoints)} frames (moving camera)!")
else:
    # Detect first frame only
    single_keypoint = court_detector.predict(video_frames[0])
    court_keypoints = [single_keypoint] * len(video_frames)
    st.success("✅ Court keypoints detected (static camera)!")
```

**Features:**
- Checkbox di sidebar: "Enable Moving Camera Detection"
- Default: **ON** (value=True)
- Help text menjelaskan trade-off speed vs accuracy
- Status message berbeda untuk moving vs static

### 3. **Per-Frame Keypoints Drawing**
```python
for i, frame in enumerate(output_frames):
    # Draw keypoints from corresponding frame
    if show_court_keypoints and i < len(court_keypoints):
        keypoints_reshaped = court_keypoints[i].reshape(-1, 2)
        for x, y in keypoints_reshaped:
            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
```

### 4. **Player Filtering with Multi-Frame Keypoints**
```python
# Choose and filter to 2 players with court keypoints
if len(player_detections) > 0:
    player_detections = player_tracker_obj.choose_and_filter_players(
        court_keypoints,  # List of keypoints (one per frame)
        player_detections
    )
```

### 5. **All Bug Fixes Included**
✅ **Fix #1**: PlayerTracker class-based API
```python
from trackers.player_tracker import PlayerTracker
player_tracker_obj = PlayerTracker(player_model_path)
player_detections = player_tracker_obj.detect_frames(video_frames)
```

✅ **Fix #2**: BallTracker class-based API
```python
from trackers.ball_tracker import BallTracker
ball_tracker_obj = BallTracker(ball_model_path)
ball_detections = ball_tracker_obj.detect_frames(video_frames)
```

✅ **Fix #3**: Ball detection format (dict with key 1)
```python
if ball_dict and 1 in ball_dict:
    bbox = ball_dict[1]
    x1, y1, x2, y2 = bbox
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
```

✅ **Fix #4**: Court keypoints reshape
```python
keypoints_reshaped = court_keypoints[i].reshape(-1, 2)
```

## 📊 Sidebar Configuration

### 🤖 Models
- Court Keypoints Model: `models/keypoints_model.pth`
- Ball Detection Model: `models/yolo8_best.pt`
- Player Detection Model: `yolov8x.pt`

### 🎯 Detection Parameters
- **Ball Detection Confidence**: 0.05 - 0.50 (default: 0.15)

### 📊 Processing Options
- ✅ **Enable Moving Camera Detection** (NEW!)
- ✅ Show Court Keypoints
- ✅ Show Player Bounding Boxes
- ✅ Show Ball Detection
- ✅ Show Mini Court
- ✅ Interpolate Ball Position

### 💾 Output Options
- Video Format: MP4 (H.264) / AVI (XVID)
- Output FPS: 15-60 (default: 24)

### 📈 Model Performance (Info Box)
```
Court Detection:
- Accuracy: 99.29%
- Precision: 99.30%
- Moving camera support ✓

Ball Detection:
- mAP@50: >75%
- Recall: >70%

Player Tracking:
- YOLOv8x + BoT-SORT
```

## 🎯 Analysis Results Display

4 Metrics:
1. **Total Frames**: Jumlah frame yang diproses
2. **Ball Detection**: Persentase deteksi bola (%)
3. **Player Frames**: Jumlah frame dengan pemain
4. **Court Frames**: Jumlah frame + mode (Moving/Static)

Example:
```
Total Frames: 1247
Ball Detection: 72.3%
Player Frames: 1247
Court Frames: 1247 ↗️ Moving
```

## 🔄 Processing Workflow

```
1. Upload Video (MP4/AVI/MOV)
   ↓
2. Read Video Frames (10%)
   ↓
3. Detect Court Keypoints (20%)
   - Moving Camera: detect_video() → all frames
   - Static Camera: predict() → replicate
   ↓
4. Detect Players (40%)
   - YOLOv8x detection
   - Filter with court keypoints
   ↓
5. Detect Ball (60%)
   - YOLOv8s detection
   - Optional interpolation
   ↓
6. Draw Annotations (80%)
   - Court keypoints (green circles)
   - Player boxes (red/blue)
   - Ball (yellow circle)
   - Mini court overlay
   ↓
7. Save Output Video (90%)
   ↓
8. Display Results (100%)
   - 4 metrics
   - 4 sample frames
   - Download button
```

## 📝 Key Code Changes from Original

### Before (Original without moving camera):
```python
# Detect only first frame
court_keypoints = court_detector.predict(video_frames[0])

# Use same keypoints for all frames
for i, frame in enumerate(output_frames):
    if show_court_keypoints:
        keypoints_reshaped = court_keypoints.reshape(-1, 2)
        for x, y in keypoints_reshaped:
            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
```

### After (With moving camera support):
```python
# Conditional detection
if enable_moving_camera:
    court_keypoints = court_detector.predict_video(video_frames)
else:
    single_keypoint = court_detector.predict(video_frames[0])
    court_keypoints = [single_keypoint] * len(video_frames)

# Use per-frame keypoints
for i, frame in enumerate(output_frames):
    if show_court_keypoints and i < len(court_keypoints):
        keypoints_reshaped = court_keypoints[i].reshape(-1, 2)
        for x, y in keypoints_reshaped:
            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
```

## 🚀 How to Run

```powershell
# Activate virtual environment
cd c:\KULIAH\SKRIPSI\tennis_analysis
.\.venv\Scripts\Activate.ps1

# Install streamlit if not installed
pip install streamlit

# Run the app
streamlit run streamlit_app.py
```

App will open in browser at: http://localhost:8501

## 🎓 Perfect for Skripsi

### Why This Version is Best:

1. **Complete Feature Set** ✨
   - All original features intact
   - Moving camera support added
   - Professional sidebar layout

2. **User-Friendly** 👥
   - Clear instructions
   - Helpful tooltips
   - Real-time progress updates

3. **Flexible** 🔧
   - Moving camera ON/OFF
   - Configurable parameters
   - Multiple visualization options

4. **Accurate** 🎯
   - Moving camera for better accuracy
   - Per-frame court detection
   - Improved player filtering

5. **Professional** 💼
   - Wide layout
   - Model performance display
   - Sample frames preview
   - Clean download workflow

## 📚 Documentation

Related files:
- `STREAMLIT_FIXES.md` - Bug fixes applied
- `MOVING_CAMERA_FEATURE.md` - Moving camera explanation
- `streamlit_app_backup.py` - Backup of previous version
- `STREAMLIT_APP_GUIDE.md` - Complete usage guide

## ✅ Testing Checklist

Before presentation:
- [ ] Test with static camera video (broadcast)
- [ ] Test with moving camera video (handheld)
- [ ] Verify all checkboxes work
- [ ] Check sample frames display correctly
- [ ] Test download button
- [ ] Verify moving/static indicator in results

## 🎉 Ready for Demo!

Streamlit app sekarang:
- ✅ Struktur original yang profesional
- ✅ Moving camera detection terintegrasi
- ✅ Semua bug fixes included
- ✅ Ready untuk presentasi skripsi
- ✅ User-friendly dan informative

**Perfect untuk demonstrasi dan evaluasi! 🎓**
