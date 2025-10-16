# 🎾 Tennis Analysis System

Advanced tennis match analysis system using computer vision and deep learning for player tracking, ball detection, court line detection, and comprehensive match statistics.

## ✨ Features

- **Player Tracking**: YOLOv8-based player detection and tracking using BoT-SORT
- **Ball Detection**: Custom-trained YOLOv8s model for accurate tennis ball detection
- **Court Line Detection**: CNN-based keypoint detection for court boundary identification
- **Mini Court Visualization**: Top-down view showing player and ball positions
- **Player Statistics**: 
  - Shot speed analysis (km/h)
  - Player movement speed (km/h)
  - Average speeds per player
  - Shot count tracking
- **Streamlit Web Interface**: Interactive web application for analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- GPU recommended (CUDA-compatible) for training
- 4GB+ RAM

### Installation

1. Clone the repository:
```bash
git clone https://github.com/riizaldin/Tennis-Analysis-System.git
cd Tennis-Analysis-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download pre-trained models (if available) or train your own (see Training section)

### Usage

#### Command Line Analysis
```bash
python main.py
```

#### Web Interface
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
tennis_analysis/
├── constants/              # Constants and configuration
├── court_line_detector/    # Court line detection module
├── mini_court/            # Mini court visualization
├── trackers/              # Player and ball tracking
│   ├── player_tracker.py
│   └── ball_tracker.py
├── utils/                 # Utility functions
│   ├── bbox_utils.py
│   ├── conversions.py
│   ├── video_utils.py
│   └── player_stats_drawer_utils.py
├── training/              # Model training notebooks
│   ├── tennis_ball_detector.ipynb
│   ├── tennis_ball_training_complete.ipynb
│   └── tennis-court_keypoints_training.ipynb
├── models/                # Trained model weights
├── input_videos/          # Input video files
├── output_videos/         # Processed output videos
├── main.py               # Main analysis script
├── streamlit_app.py      # Web interface
└── requirements.txt      # Python dependencies
```

## 🎯 Training Your Own Models

### Ball Detection Model

Use the complete training pipeline notebook:

1. Open `training/tennis_ball_training_complete.ipynb`
2. Run all cells sequentially:
   - Install requirements
   - Download dataset from Roboflow
   - Stratified split (75-15-10)
   - Train YOLOv8s model
   - Evaluate and export

**Training Configuration:**
- Model: YOLOv8s
- Epochs: 150 (early stopping: 30)
- Optimizer: AdamW
- Dataset: Tennis Ball Detection v6
- Expected mAP@50: >75%

### Court Keypoints Model

Use `training/tennis-court_keypoints_training.ipynb` for training the court line detection CNN.

## 📊 Features Details

### Player Statistics
- **Shot Speed**: Calculated from ball movement between frames (km/h)
- **Player Speed**: Movement speed of each player (km/h)
- **Averages**: Average shot and player speeds throughout the match
- **Dynamic FPS**: Automatic FPS detection for accurate speed calculations

### Mini Court
- Real-time top-down visualization
- Player position tracking (color-coded)
- Ball trajectory visualization
- Scaled proportions matching real tennis court dimensions

### Moving Camera Detection
- Automatic detection of camera movement
- Switches between tracking modes for optimal performance

## 🛠️ Technical Details

### Models Used
1. **YOLOv8x**: Player detection
2. **YOLOv8s (custom)**: Ball detection (trained on 578 images)
3. **CNN Keypoints**: Court line detection (14 keypoints)
4. **BoT-SORT**: Player tracking algorithm

### Speed Calculations
- Formula: `(distance_meters / time_seconds) × 3.6 = km/h`
- Dynamic FPS detection from video metadata
- Pixel-to-meter conversion using court dimensions

## 📝 Requirements

See `requirements.txt` for complete list. Main dependencies:
- ultralytics
- opencv-python
- torch
- pandas
- streamlit
- roboflow (for training)
- tqdm

## 🎓 For Academic Use

This project was developed as part of a thesis on tennis match analysis using computer vision.

**Key Achievements:**
- mAP@50: >75% on ball detection
- Recall: >70%
- Real-time processing capability
- Accurate speed measurements

## 📄 License

[Your License Here]

## 👤 Author

**Muhammad Rizaldi**
- GitHub: [@riizaldin](https://github.com/riizaldin)

## 🙏 Acknowledgments

- Ultralytics YOLOv8
- Roboflow for dataset management
- Tennis Ball Detection Dataset v6 by Viren Dhanwani

## 📧 Contact

For questions or collaboration: [Your Email]

---

**Note**: Large files (models, videos, datasets) are not included in this repository. Download instructions and model weights will be provided separately.
