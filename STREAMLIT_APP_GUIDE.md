# 🎾 Tennis Analysis Streamlit Web App

## Beautiful Web Interface for Tennis Video Analysis

---

## 📸 Features

### 🎯 Main Features:
1. **Court Keypoints Detection** - Detects 14 keypoints on tennis court
2. **Player Tracking** - Tracks 2 players with consistent IDs
3. **Ball Detection** - Detects tennis ball with trajectory interpolation
4. **Mini Court Visualization** - Top-down view of player positions
5. **Real-time Configuration** - Adjust detection parameters on-the-fly
6. **Video Export** - Download analyzed video

### 🎨 UI Features:
- **Drag & Drop Upload** - Easy video upload
- **Real-time Progress** - See processing status
- **Interactive Sidebar** - Adjust all parameters
- **Sample Frames Preview** - Quick result preview
- **Statistics Dashboard** - Model performance metrics
- **Responsive Design** - Works on desktop and tablet

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install Streamlit dependencies
pip install -r requirements_streamlit.txt
```

### Step 2: Run the App
```powershell
# Run Streamlit app
streamlit run streamlit_app.py
```

### Step 3: Open Browser
The app will automatically open at:
```
http://localhost:8501
```

---

## 📁 Required Files

### Model Files:
```
tennis_analysis/
├── models/
│   └── yolo8_best.pt                    ← Ball detection model
├── training/
│   └── Court-Keypoints/
│       └── exps/
│           └── skripsi_resnet50/
│               └── model_best.pt         ← Court keypoints model
├── yolov8x.pt                            ← Player detection model
└── streamlit_app.py                      ← This app
```

### If Models are Missing:
The app will show an error and tell you which models are missing.

---

## 🎮 How to Use

### 1. Upload Video
- Click **"Choose a tennis video..."**
- Select MP4, AVI, MOV, or MKV file
- Max size: 200MB (for best performance)

### 2. Configure Parameters (Sidebar)
```
🤖 Models:
- Court Keypoints Model: Path to ResNet50 model
- Ball Detection Model: Path to YOLO ball model
- Player Detection Model: Path to YOLO player model

🎯 Detection Parameters:
- Ball Detection Confidence: 0.05-0.5 (default: 0.15)
- Player Detection Confidence: 0.1-0.5 (default: 0.2)

📊 Processing Options:
✅ Show Court Keypoints
✅ Show Player Bounding Boxes
✅ Show Ball Trajectory
✅ Show Mini Court
✅ Interpolate Ball Position

💾 Output Options:
- Video Format: MP4 or AVI
- Output FPS: 15-60 (default: 24)
```

### 3. Start Analysis
- Click **"🚀 Start Analysis"** button
- Wait for processing (progress bar shows status)
- View results and download video

---

## 📊 App Sections

### Tab 1: Video Analysis
```
┌─────────────────────────────────────┐
│  📹 Upload Video                    │
│  ⚙️  Configure Parameters           │
│  🚀 Start Analysis                  │
│  📊 View Results                    │
│  ⬇️  Download Processed Video      │
└─────────────────────────────────────┘
```

### Tab 2: About Models
```
┌─────────────────────────────────────┐
│  🎯 Court Keypoints Model           │
│     - Architecture: ResNet50        │
│     - Accuracy: 99.29%              │
│                                     │
│  🎾 Ball Detection Model            │
│     - Architecture: YOLOv8s         │
│     - mAP@50: >75%                  │
│                                     │
│  👥 Player Tracking Model           │
│     - Architecture: YOLOv8x         │
│     - Tracker: BoT-SORT             │
└─────────────────────────────────────┘
```

### Tab 3: Statistics
```
┌─────────────────────────────────────┐
│  📊 Model Comparison Table          │
│  ⚙️  Training Configuration         │
│  📁 Dataset Split Information       │
└─────────────────────────────────────┘
```

---

## ⚙️ Configuration Guide

### Optimal Settings for Different Videos:

#### High Quality Video (HD, Good Lighting):
```
Ball Confidence: 0.15
Player Confidence: 0.2
Interpolate Ball: Yes
All Visualizations: Yes
```

#### Lower Quality Video (SD, Low Light):
```
Ball Confidence: 0.10
Player Confidence: 0.15
Interpolate Ball: Yes
Mini Court: Optional
```

#### Fast Processing (Quick Preview):
```
Ball Confidence: 0.20
Player Confidence: 0.25
Interpolate Ball: No
Show Mini Court: No
Output FPS: 15
```

---

## 🎨 UI Components

### Progress Indicators:
```
📹 Reading video frames...           [10%]
🎯 Detecting court keypoints...      [20%]
👥 Detecting players...              [40%]
🎾 Detecting ball...                 [60%]
📈 Interpolating ball positions...   [70%]
🎨 Drawing annotations...            [80%]
💾 Saving output video...            [90%]
✅ Analysis complete!                [100%]
```

### Metrics Display:
```
┌──────────────┬──────────────┬──────────────┐
│ Total Frames │ Ball Detect  │ Player Frames│
│     250      │    75.2%     │     248      │
└──────────────┴──────────────┴──────────────┘
```

---

## 🔧 Troubleshooting

### Problem 1: Models Not Found
```
❌ Missing model files:
  - Court Model: training/Court-Keypoints/exps/skripsi_resnet50/model_best.pt

Solution:
1. Check model path in sidebar
2. Ensure model file exists
3. Train model if not available
```

### Problem 2: Video Processing Error
```
❌ Error during processing: [error message]

Common causes:
- Video format not supported
- Video file corrupted
- Insufficient memory
- Model loading failed

Solution:
1. Try different video format (MP4 recommended)
2. Reduce video resolution
3. Check error details in app
```

### Problem 3: Slow Processing
```
⏱️ Processing taking too long?

Solutions:
1. Reduce output FPS (15 instead of 24)
2. Disable mini court visualization
3. Use smaller video file
4. Ensure GPU is being used (if available)
```

### Problem 4: Port Already in Use
```
❌ Port 8501 is already in use

Solution:
streamlit run streamlit_app.py --server.port 8502
```

---

## 💡 Tips for Best Results

### Video Requirements:
✅ Full court visible
✅ HD quality (1920×1080 or higher)
✅ Good lighting
✅ Stable camera (not shaky)
✅ Clear court lines
✅ Ball visible (not too small)

### Processing Tips:
✅ Start with default parameters
✅ Adjust confidence if too many false positives
✅ Use interpolation for smoother ball trajectory
✅ Enable mini court for better visualization
✅ Export at 24 FPS for smooth playback

### Performance Tips:
✅ Close other applications
✅ Use GPU if available
✅ Process shorter clips first (test)
✅ Increase confidence for faster processing
✅ Disable unnecessary visualizations

---

## 🎓 For Thesis/Presentation

### Demo Workflow:
1. **Prepare Sample Videos** (30-60 seconds each)
2. **Test Different Settings** (show parameter effects)
3. **Save Results** (download processed videos)
4. **Take Screenshots** (for thesis documentation)
5. **Record Demo** (screen recording for presentation)

### What to Show:
✅ Upload interface (easy to use)
✅ Real-time progress (transparency)
✅ Sample frames (quality results)
✅ Statistics tab (model performance)
✅ Download feature (practical output)

### Talking Points:
- "Web-based interface for easy access"
- "Real-time parameter adjustment"
- "Integrated 3 AI models seamlessly"
- "99.29% court detection accuracy"
- "Production-ready deployment"

---

## 📦 Deployment Options

### Option 1: Local Deployment (Current)
```powershell
streamlit run streamlit_app.py
# Access: http://localhost:8501
```

### Option 2: Network Deployment
```powershell
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
# Access: http://[YOUR_IP]:8501
```

### Option 3: Streamlit Cloud (Free Hosting)
```
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Deploy app
5. Get public URL
```

### Option 4: Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements_streamlit.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## 🎬 Demo Videos Recommendation

### Good Test Videos:
1. **Professional Match** - HD quality, full court view
2. **Amateur Match** - Lower quality, testing robustness
3. **Training Session** - Multiple balls, stress test
4. **Slow Motion** - High FPS, detailed analysis

### Video Sources:
- YouTube (download with proper licensing)
- Personal recordings
- Open datasets (e.g., Tennis Video Dataset)
- Synthetic videos (for edge cases)

---

## 📊 Expected Output

### Processed Video Contains:
✅ **Court Keypoints** (14 green dots)
✅ **Player Bounding Boxes** (red/blue boxes with IDs)
✅ **Ball Detection** (yellow circle with trajectory)
✅ **Mini Court** (top-right corner, top-down view)

### Statistics Shown:
✅ Total Frames Processed
✅ Ball Detection Rate (%)
✅ Player Detection Frames
✅ Processing Time
✅ Video Resolution
✅ FPS Information

---

## 🔒 Security Notes

### For Public Deployment:
⚠️ **Do NOT** deploy with API keys exposed
⚠️ **Do NOT** allow unlimited file uploads
⚠️ **Implement** file size limits
⚠️ **Validate** file types strictly
⚠️ **Add** rate limiting
⚠️ **Use** authentication if needed

### Current Implementation:
✅ Local files only
✅ 200MB size limit (configurable)
✅ Allowed extensions: mp4, avi, mov, mkv
✅ Temporary file cleanup
✅ No database (stateless)

---

## 📈 Future Enhancements

### Potential Features:
1. **Batch Processing** - Multiple videos at once
2. **Live Camera** - Real-time analysis
3. **Shot Classification** - Forehand/backhand detection
4. **Rally Analysis** - Count shots per rally
5. **Speed Calculation** - Ball speed estimation
6. **Heatmaps** - Player movement patterns
7. **Export Statistics** - CSV/JSON export
8. **Comparison Mode** - Compare 2 videos side-by-side

---

## 🆘 Support

### If You Encounter Issues:

1. **Check Console Output**
   ```powershell
   # Run with verbose logging
   streamlit run streamlit_app.py --logger.level=debug
   ```

2. **Check Model Files**
   ```python
   # Verify model exists
   from pathlib import Path
   print(Path("models/yolo8_best.pt").exists())
   ```

3. **Check Video File**
   ```python
   # Test video loading
   import cv2
   cap = cv2.VideoCapture("your_video.mp4")
   print(f"Frames: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
   ```

4. **Clear Cache**
   ```powershell
   # Clear Streamlit cache
   streamlit cache clear
   ```

---

## ✅ Checklist Before Demo

### Pre-Demo:
- [ ] All models trained and saved
- [ ] Test videos prepared (3-5 videos)
- [ ] Streamlit app tested with each video
- [ ] Screenshots taken for thesis
- [ ] Demo script prepared
- [ ] Backup plan (recorded demo video)

### During Demo:
- [ ] Close unnecessary applications
- [ ] Ensure good internet (if cloud deployment)
- [ ] Have sample videos ready
- [ ] Show parameter adjustment
- [ ] Demonstrate download feature
- [ ] Explain statistics tab

### After Demo:
- [ ] Save processed videos
- [ ] Document any issues
- [ ] Gather feedback
- [ ] Update thesis with results

---

## 🎯 Success Metrics

### For Thesis:
✅ **Functionality**: All features working correctly
✅ **Accuracy**: 99.29% court detection, 75%+ ball detection
✅ **Performance**: <5 minutes for 1-minute video
✅ **Usability**: Easy to use interface
✅ **Reliability**: Consistent results across videos

---

## 📝 Summary

**Streamlit Web App Features:**
- ✅ Beautiful, professional UI
- ✅ Easy video upload
- ✅ Real-time progress tracking
- ✅ Interactive parameter adjustment
- ✅ Multiple visualization options
- ✅ Download processed videos
- ✅ Model statistics and comparison
- ✅ Responsive design

**Ready for:**
- ✅ Thesis demonstration
- ✅ Presentation to advisors
- ✅ User testing
- ✅ Public deployment (with security)

**Enjoy your Tennis Analysis Web App! 🎾🚀**
