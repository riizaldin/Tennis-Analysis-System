# Training Tennis Ball Detector di Google Colab
## Split: 75% Training, 15% Validation, 10% Testing

## 📋 Langkah-langkah Lengkap

### 1. Setup Environment di Colab

```python
# Bersih & pasang versi yang cocok
!pip uninstall -y torch torchvision torchaudio ultralytics
!pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
!pip install ultralytics==8.3.3
!pip install roboflow
```

### 2. Download Dataset dari Roboflow

```python
from roboflow import Roboflow
rf = Roboflow(api_key="M4ADE509JQ3BwLY9kHR7")
project = rf.workspace("viren-dhanwani").project("tennis-ball-detection")
version = project.version(6)
dataset = version.download("yolov8")
```

### 3. Split Dataset menjadi 75%-15%-10%

Dataset dari Roboflow biasanya sudah split, tapi kita perlu split ulang:

```python
import os
import shutil
import random

def split_dataset_yolo(dataset_path, train_ratio=0.75, val_ratio=0.15, test_ratio=0.10):
    """Split YOLO dataset into 75% train, 15% val, 10% test"""
    
    print(f"Dataset path: {dataset_path}")
    
    # Paths
    train_img_dir = os.path.join(dataset_path, "train/images")
    train_label_dir = os.path.join(dataset_path, "train/labels")
    val_img_dir = os.path.join(dataset_path, "valid/images")
    val_label_dir = os.path.join(dataset_path, "valid/labels")
    test_img_dir = os.path.join(dataset_path, "test/images")
    test_label_dir = os.path.join(dataset_path, "test/labels")
    
    # Gabungkan semua data
    all_images = []
    
    if os.path.exists(train_img_dir):
        train_imgs = [f for f in os.listdir(train_img_dir) if f.endswith(('.jpg', '.png'))]
        all_images.extend([(f, train_img_dir, train_label_dir) for f in train_imgs])
    
    if os.path.exists(val_img_dir):
        val_imgs = [f for f in os.listdir(val_img_dir) if f.endswith(('.jpg', '.png'))]
        all_images.extend([(f, val_img_dir, val_label_dir) for f in val_imgs])
    
    print(f"Total images: {len(all_images)}")
    
    # Shuffle
    random.seed(42)
    random.shuffle(all_images)
    
    # Calculate split
    total = len(all_images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_files = all_images[:train_end]
    val_files = all_images[train_end:val_end]
    test_files = all_images[val_end:]
    
    print(f"\nSplit:")
    print(f"  Train: {len(train_files)} ({len(train_files)/total*100:.1f}%)")
    print(f"  Val:   {len(val_files)} ({len(val_files)/total*100:.1f}%)")
    print(f"  Test:  {len(test_files)} ({len(test_files)/total*100:.1f}%)")
    
    # Backup original
    backup_dir = os.path.join(dataset_path, "_backup_original")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"\nBacking up to {backup_dir}")
        if os.path.exists(os.path.join(dataset_path, "train")):
            shutil.copytree(os.path.join(dataset_path, "train"), os.path.join(backup_dir, "train"))
        if os.path.exists(os.path.join(dataset_path, "valid")):
            shutil.copytree(os.path.join(dataset_path, "valid"), os.path.join(backup_dir, "valid"))
    
    # Clear & recreate folders
    for folder in [train_img_dir, train_label_dir, val_img_dir, val_label_dir, test_img_dir, test_label_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
    
    # Copy files
    def copy_files(file_list, dest_img_dir, dest_label_dir, source_backup=False):
        backup_train_img = os.path.join(backup_dir, "train/images")
        backup_train_lbl = os.path.join(backup_dir, "train/labels")
        backup_val_img = os.path.join(backup_dir, "valid/images")
        backup_val_lbl = os.path.join(backup_dir, "valid/labels")
        
        for img_name, orig_img_dir, orig_label_dir in file_list:
            # Determine source from backup
            if "train" in orig_img_dir:
                src_img_dir = backup_train_img
                src_label_dir = backup_train_lbl
            else:
                src_img_dir = backup_val_img
                src_label_dir = backup_val_lbl
            
            # Copy image
            src_img = os.path.join(src_img_dir, img_name)
            dst_img = os.path.join(dest_img_dir, img_name)
            if os.path.exists(src_img):
                shutil.copy2(src_img, dst_img)
            
            # Copy label
            label_name = os.path.splitext(img_name)[0] + '.txt'
            src_label = os.path.join(src_label_dir, label_name)
            dst_label = os.path.join(dest_label_dir, label_name)
            if os.path.exists(src_label):
                shutil.copy2(src_label, dst_label)
    
    print("\nCopying files...")
    copy_files(train_files, train_img_dir, train_label_dir, source_backup=True)
    copy_files(val_files, val_img_dir, val_label_dir, source_backup=True)
    copy_files(test_files, test_img_dir, test_label_dir, source_backup=True)
    
    print(f"\n✅ Split complete!")
    print(f"  Train: {len(os.listdir(train_img_dir))} images")
    print(f"  Val:   {len(os.listdir(val_img_dir))} images")
    print(f"  Test:  {len(os.listdir(test_img_dir))} images")

# Jalankan split
split_dataset_yolo(dataset.location, train_ratio=0.75, val_ratio=0.15, test_ratio=0.10)
```

### 4. Training Model

```python
!yolo task=detect mode=train \
  model=yolov8s.pt \
  data=/content/tennis-ball-detection-6/data.yaml from ultralytics import YOLO
import os

# Load model
model = YOLO('runs/detect/tennis_ball_75_15_10/weights/best.pt')

# Gunakan ABSOLUTE PATH ke data.yaml
dataset_path = os.path.abspath('tennis-ball-detection-6')
data_yaml = os.path.join(dataset_path, 'data.yaml')

print(f"📍 Dataset path: {data_yaml}")

# Evaluasi dengan absolute path
results = model.val(
    data=data_yaml,
    split='test',
    imgsz=640
)

print("\n" + "="*60)
print("TEST SET RESULTS (10% data - unseen during training)")
print("="*60)
print(f"Precision: {results.results_dict['metrics/precision(B)']:.4f}")
print(f"Recall:    {results.results_dict['metrics/recall(B)']:.4f}")
print(f"mAP50:     {results.results_dict['metrics/mAP50(B)']:.4f}")
print(f"mAP50-95:  {results.results_dict['metrics/mAP50-95(B)']:.4f}")
print("="*60) \
  epochs=100 \
  imgsz=640 \
  batch=-1 \
  patience=20 \
  project=runs \
  name=tennis_ball_75_15_10
```

**Parameter Explanation:**
- `model=yolov8s.pt` - YOLOv8 Small (balance speed/accuracy)
- `data={dataset.location}/data.yaml` - Path ke data config
- `epochs=100` - Train 100 epoch
- `imgsz=640` - Image size 640x640
- `batch=-1` - Auto batch size (optimal untuk GPU)
- `patience=20` - Early stopping jika 20 epoch tidak ada improvement
- `project=runs` - Folder output
- `name=tennis_ball_75_15_10` - Nama experiment

### 5. Evaluasi pada Test Set (10%)

```python
from ultralytics import YOLO

# Load model terbaik
model = YOLO('runs/tennis_ball_75_15_10/weights/best.pt')

# Evaluasi pada test set
results = model.val(
    data=f'{dataset.location}/data.yaml',
    split='test',  # Test set (10% data yang belum pernah dilihat)
    imgsz=640
)

print("\n" + "="*60)
print("TEST SET RESULTS (10% data - unseen during training)")
print("="*60)
print(f"Precision: {results.results_dict['metrics/precision(B)']:.4f}")
print(f"Recall:    {results.results_dict['metrics/recall(B)']:.4f}")
print(f"mAP50:     {results.results_dict['metrics/mAP50(B)']:.4f}")
print(f"mAP50-95:  {results.results_dict['metrics/mAP50-95(B)']:.4f}")
print("="*60)
```

### 6. Download Model ke Local

```python
from google.colab import files

# Download model terbaik
files.download('runs/tennis_ball_75_15_10/weights/best.pt')

# Optional: Download last checkpoint juga
files.download('runs/tennis_ball_75_15_10/weights/last.pt')
```

## 📊 Penjelasan Split

### Kenapa 75%-15%-10%?

- **75% Training**: Data untuk model belajar pattern
- **15% Validation**: Monitor overfitting & tune hyperparameters
- **10% Testing**: Evaluasi final model (TIDAK PERNAH dilihat during training)

### Data Flow:

```
Original Dataset (100%)
    |
    ├── Training (75%)    → Model belajar dari ini
    ├── Validation (15%)  → Monitor progress, pilih model terbaik
    └── Testing (10%)     → Final evaluation (unbiased)
```

## 🎯 Tips untuk Training yang Baik

1. **Jangan melihat test set sampai akhir training**
   - Test set harus benar-benar "unseen"
   - Jangan tune hyperparameter berdasarkan test results

2. **Monitor validation metrics**
   - Jika val loss naik tapi train loss turun = overfitting
   - Gunakan early stopping (`patience=20`)

3. **Test set untuk reporting**
   - Gunakan test metrics untuk laporan final
   - Ini adalah performance "real-world" model Anda

4. **Save di Google Drive**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   
   # Copy results to Drive
   !cp -r runs/tennis_ball_75_15_10 /content/drive/MyDrive/
   ```

## 📈 Output yang Dihasilkan

Setelah training, Anda akan mendapat:

```
runs/tennis_ball_75_15_10/
├── weights/
│   ├── best.pt          # Model terbaik (berdasarkan validation)
│   └── last.pt          # Model epoch terakhir
├── results.csv          # Training metrics
├── results.png          # Training curves
├── confusion_matrix.png # Confusion matrix
└── val_batch*.jpg       # Validation predictions
```

## ⚠️ Troubleshooting

**Error: CUDA out of memory**
```python
# Kurangi batch size
!yolo task=detect mode=train ... batch=16
```

**Error: No module named 'ultralytics'**
```python
!pip install ultralytics==8.3.3
```

**Split tidak sesuai**
- Check apakah `random.seed(42)` sudah di-set
- Verify dengan print jumlah files di setiap folder

## ✅ Checklist

- [ ] Environment setup di Colab
- [ ] Dataset downloaded dari Roboflow
- [ ] Dataset di-split 75%-15%-10%
- [ ] Training completed (100 epochs atau early stop)
- [ ] Model evaluated pada test set
- [ ] Best model downloaded
- [ ] Results saved ke Google Drive

## 📞 Next Steps

Setelah training selesai:
1. Evaluasi test set metrics
2. Test inference pada video baru
3. Compare dengan model lain (yolo8_best, yolo8_best2, dll)
4. Deploy model terbaik ke aplikasi

Happy Training! 🎾🚀
