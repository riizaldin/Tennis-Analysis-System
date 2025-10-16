# 🎾 Tennis Analysis Web App

Beautiful web interface for analyzing tennis videos using AI-powered computer vision models.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

---

## ✨ Features

### 🎯 Core Capabilities
- **Court Keypoints Detection** - 14 points with 99.29% accuracy
- **Player Tracking** - 2 players with consistent IDs
- **Ball Detection** - Trajectory with interpolation
- **Mini Court View** - Top-down visualization
- **Video Export** - Download analyzed video

### 🎨 User Interface
- Drag & drop video upload
- Real-time progress tracking
- Interactive parameter adjustment
- Sample frames preview
- Statistics dashboard
- Responsive design

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements_streamlit.txt
```

### 2️⃣ Run the App

**Option A: Using Script (Easiest)**
```powershell
.\run_streamlit.ps1
```

**Option B: Manual Command**
```powershell
streamlit run streamlit_app.py
```

### 3️⃣ Open Browser

App will automatically open at: **http://localhost:8501**

---

## 📦 Required Models

Make sure these model files exist:

```
tennis_analysis/
├── models/
│   └── yolo8_best.pt                     ← Ball detection
├── training/
│   └── Court-Keypoints/
│       └── exps/
│           └── skripsi_resnet50/
│               └── model_best.pt          ← Court keypoints
└── yolov8x.pt                             ← Player detection
```

**If models are missing:** The app will show which models are needed and allow you to specify custom paths.

---

## 🎮 How to Use

### Step 1: Upload Video
- Click "Choose a tennis video..."
- Select MP4, AVI, MOV, or MKV file
- Max size: 200MB

### Step 2: Configure (Sidebar)
```
🤖 Models:
   - Court Keypoints Model path
   - Ball Detection Model path
   - Player Detection Model path

🎯 Detection:
   - Ball Confidence: 0.15 (default)
   - Player Confidence: 0.2 (default)

📊 Options:
   ✅ Show Court Keypoints
   ✅ Show Player Boxes
   ✅ Show Ball Trajectory
   ✅ Show Mini Court
   ✅ Interpolate Ball
```

### Step 3: Analyze
- Click "🚀 Start Analysis"
- Wait for processing
- Download processed video

---

## 📊 App Tabs

### 📹 Video Analysis
Upload, configure, and analyze videos with real-time progress.

### ℹ️ About Models
Details about each AI model:
- **Court Keypoints**: ResNet50, 99.29% accuracy
- **Ball Detection**: YOLOv8s, 75%+ mAP@50
- **Player Tracking**: YOLOv8x + BoT-SORT

### 📊 Statistics
Model comparison, training config, and dataset information.

---

## ⚙️ Configuration Tips

### For HD Video (Best Quality)
```
Ball Confidence: 0.15
Player Confidence: 0.2
Interpolate: Yes
All visualizations: Yes
FPS: 24
```

### For Fast Processing
```
Ball Confidence: 0.20
Player Confidence: 0.25
Interpolate: No
Mini Court: No
FPS: 15
```

### For Low Quality Video
```
Ball Confidence: 0.10
Player Confidence: 0.15
Interpolate: Yes
```

---

## 🔧 Troubleshooting

### Port Already in Use
```powershell
streamlit run streamlit_app.py --server.port 8502
```

### Models Not Found
Check sidebar and update model paths to correct locations.

### Slow Processing
- Reduce FPS to 15
- Disable mini court
- Use shorter video clips
- Close other applications

### Clear Cache
```powershell
streamlit cache clear
```

---

## 🎓 For Thesis/Demo

### What to Demonstrate:
1. **Easy Upload** - Drag & drop interface
2. **Real-time Progress** - Processing transparency
3. **Multiple Visualizations** - Court, players, ball, mini court
4. **Parameter Control** - Adjust settings on-the-fly
5. **Download Results** - Export processed video
6. **Statistics** - Show model performance

### Sample Videos:
- Professional match (HD quality)
- Amateur match (robustness test)
- Different lighting conditions
- Various court types

---

## 📦 Deployment Options

### Local (Current)
```powershell
streamlit run streamlit_app.py
```

### Network
```powershell
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### Streamlit Cloud (Free)
1. Push to GitHub
2. Deploy at share.streamlit.io
3. Get public URL

### Docker
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements_streamlit.txt
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## 📸 Screenshot

```
┌────────────────────────────────────────────────────────────┐
│  🎾 Tennis Analysis System                                 │
│  Automated Court, Player, and Ball Detection with AI      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  📹 Video Analysis  │  ℹ️ About Models  │  📊 Statistics   │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Choose a tennis video...                        │    │
│  │  [Drag and drop or click to browse]              │    │
│  └──────────────────────────────────────────────────┘    │
│                                                            │
│  Duration: 30.0s  │  Frames: 750  │  FPS: 25  │  1920×1080│
│                                                            │
│  ┌─────────────────────────────────────────────────┐     │
│  │          🚀 Start Analysis                       │     │
│  └─────────────────────────────────────────────────┘     │
│                                                            │
│  ⚙️ Configuration                                          │
│  ├─ 🤖 Models                                             │
│  ├─ 🎯 Detection Parameters                              │
│  ├─ 📊 Processing Options                                │
│  └─ 💾 Output Options                                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Metrics

- **Court Detection Accuracy**: 99.29%
- **Ball Detection Rate**: 70-80%
- **Processing Speed**: ~1 minute for 30s video
- **Max Upload Size**: 200MB
- **Supported Formats**: MP4, AVI, MOV, MKV

---

## 📝 Tech Stack

- **Frontend**: Streamlit
- **Computer Vision**: OpenCV
- **Deep Learning**: PyTorch, Ultralytics
- **Models**: ResNet50, YOLOv8s, YOLOv8x
- **Tracking**: BoT-SORT
- **Language**: Python 3.9+

---

## 🆘 Support

### Check Documentation
- `STREAMLIT_APP_GUIDE.md` - Detailed guide
- `README.md` - Main project README

### Common Issues
- Models not found → Check paths
- Port in use → Use different port
- Slow processing → Adjust parameters
- Upload failed → Check file size/format

### Debug Mode
```powershell
streamlit run streamlit_app.py --logger.level=debug
```

---

## ✅ Checklist

### Before Running:
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Model files exist
- [ ] Test videos prepared

### Before Demo:
- [ ] App tested with sample videos
- [ ] All features working
- [ ] Screenshots taken
- [ ] Backup plan ready

---

## 🎉 Success!

Your Tennis Analysis Web App is ready!

**Features**:
- ✅ Beautiful UI
- ✅ Easy to use
- ✅ Real-time processing
- ✅ Multiple AI models
- ✅ Export results
- ✅ Production-ready

**Perfect for**:
- Thesis demonstration
- User testing
- Presentation to advisors
- Public deployment

---

## 📄 License

This project is part of a thesis research project.

---

## 🤝 Contributing

This is a thesis project. For questions or suggestions, please contact the author.

---

## 🙏 Acknowledgments

- **Streamlit** - Web framework
- **Ultralytics** - YOLO models
- **OpenCV** - Computer vision
- **PyTorch** - Deep learning

---

**Enjoy analyzing tennis videos! 🎾🚀**
