# 🎾 Streamlit Tennis Analysis - Quick Reference

## 🚀 Quick Start

```powershell
cd c:\KULIAH\SKRIPSI\tennis_analysis
streamlit run streamlit_app.py
```

Browser akan otomatis buka di: **http://localhost:8501**

## ⚙️ Sidebar Settings (Konfigurasi)

### 📂 Model Paths (Jangan diubah kecuali perlu)
- Court: `models/keypoints_model.pth`
- Ball: `models/yolo8_best.pt`  
- Player: `yolov8x.pt`

### 🎯 Detection Parameters
| Parameter | Range | Default | Keterangan |
|-----------|-------|---------|------------|
| Ball Confidence | 0.05 - 0.50 | 0.15 | Lower = more detections |

### 📊 Processing Options

| Option | Default | Gunakan Kapan? |
|--------|---------|----------------|
| **Enable Moving Camera** | ✅ ON | Video handheld, zoom, multi-angle |
| Show Court Keypoints | ✅ ON | Lihat 14 titik lapangan |
| Show Player Boxes | ✅ ON | Kotak merah/biru di pemain |
| Show Ball | ✅ ON | Lingkaran kuning di bola |
| Show Mini Court | ✅ ON | Tactical view kiri atas |
| Interpolate Ball | ✅ ON | Smooth ball trajectory |

### 💾 Output Options
- Format: MP4 (H.264) - recommended
- FPS: 24 (default) - sesuaikan dengan video input

## 🎬 Workflow

1. **Upload Video**
   - Klik "Choose a tennis video..."
   - Pilih file MP4/AVI/MOV
   - Lihat info: duration, frames, FPS, resolution

2. **Configure (Optional)**
   - Adjust settings di sidebar jika perlu
   - Default settings sudah optimal

3. **Start Analysis**
   - Klik tombol "🚀 Start Analysis"
   - Tunggu progress bar (10% → 100%)
   - Lihat status updates

4. **Download Results**
   - Klik "⬇️ Download Processed Video"
   - Save ke komputer

## 📊 Understanding Results

### Metrics Explained

**Total Frames**: 1247
- Jumlah frame yang diproses

**Ball Detection: 72.3%**
- Persentase frame dengan bola terdeteksi
- 70-80% = good (expected)
- <60% = coba adjust confidence

**Player Frames: 1247**
- Frame dengan pemain terdeteksi
- Should be close to total frames

**Court Frames: 1247 ↗️ Moving**
- Frames dengan court keypoints
- ↗️ Moving = moving camera mode
- → Static = static camera mode

## 🎯 Moving Camera vs Static Camera

### When to use **Moving Camera** (ON):
✅ Video handheld (smartphone, GoPro)
✅ Zoom in/out during rally
✅ Multi-angle highlights
✅ Camera follows ball/player
✅ Practice videos
✅ Drone footage

### When to use **Static Camera** (OFF):
✅ Professional broadcast
✅ Fixed wide angle
✅ Security camera (CCTV)
✅ Need quick results
✅ Computational resources limited

## ⚡ Performance Tips

| Video Length | Moving Camera | Static Camera |
|--------------|---------------|---------------|
| <100 frames  | Fast (~15s)   | Very Fast (~5s) |
| 100-500 frames | Medium (~1min) | Fast (~5s) |
| >500 frames  | Slow (2-3min) | Fast (~5s) |

**Tip**: Test dengan static camera dulu, switch ke moving jika hasil kurang akurat.

## 🐛 Troubleshooting

### Error: "Missing model files"
**Solution**: 
- Check file paths di sidebar
- Pastikan files exist: `models/keypoints_model.pth`, `models/yolo8_best.pt`, `yolov8x.pt`

### Ball detection too low (<50%)
**Solutions**:
1. Lower ball confidence (try 0.10)
2. Enable interpolation (should be ON)
3. Check lighting in video

### Player boxes tidak muncul
**Solutions**:
1. Check "Show Player Bounding Boxes" di sidebar
2. Pastikan full court visible in video
3. Enable moving camera if camera moves

### Mini court tidak akurat
**Solutions**:
1. Enable moving camera detection
2. Check court keypoints visible (green dots)
3. Verify full court in frame

### Processing terlalu lambat
**Solutions**:
1. Disable moving camera → use static
2. Reduce output FPS (24 → 15)
3. Process shorter video clip first

## 🎨 Visualization Guide

### Court Keypoints (Green Circles)
- 14 points marking court lines
- Net posts, baselines, service lines

### Player Boxes
- **Red box**: Player 1 (closer to bottom)
- **Blue box**: Player 2 (closer to top)
- ID consistent through video

### Ball (Yellow Circle)
- Small filled circle = ball center
- Larger outline = detection area
- May appear/disappear (interpolated)

### Mini Court (Top-left overlay)
- Tactical bird's-eye view
- Red/blue dots = players
- Yellow dot = ball
- Shows court positioning

## 📁 Output Files

Downloaded video includes:
- ✅ Original video quality
- ✅ All annotations drawn
- ✅ Court keypoints (if enabled)
- ✅ Player boxes (if enabled)
- ✅ Ball tracking (if enabled)
- ✅ Mini court overlay (if enabled)

Filename format: `tennis_analysis_[original_name].mp4`

## 🎓 For Skripsi Presentation

### Recommended Settings for Demo:
```
✅ Enable Moving Camera: ON
✅ Show Court Keypoints: ON
✅ Show Player Boxes: ON
✅ Show Ball: ON
✅ Show Mini Court: ON
✅ Interpolate Ball: ON
Ball Confidence: 0.15
Output FPS: 24
```

### Demo Flow:
1. Show video upload
2. Explain sidebar settings (briefly)
3. Highlight "Enable Moving Camera" feature
4. Click "Start Analysis"
5. Explain progress (court → players → ball → draw)
6. Show results metrics
7. Show sample frames
8. Download and play output video

### Key Talking Points:
- ✨ Moving camera support (unique feature)
- 🎯 99.29% court detection accuracy
- 🎾 75%+ ball detection mAP@50
- 👥 Automatic 2-player tracking
- 📊 Real-time mini court

## ⌨️ Keyboard Shortcuts

In browser:
- `Ctrl + R` - Refresh app
- `Ctrl + -` / `Ctrl + +` - Zoom out/in
- `F11` - Fullscreen

## 📞 Support Files

- `STREAMLIT_FINAL_VERSION.md` - Complete documentation
- `MOVING_CAMERA_FEATURE.md` - Moving camera explained
- `STREAMLIT_FIXES.md` - Bug fixes log
- `streamlit_app_backup.py` - Previous version backup

---

**🎉 Ready to analyze tennis videos!**

*Last updated: Final version with moving camera support*
