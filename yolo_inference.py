from ultralytics import YOLO

# pip install -U ultralytics
model = YOLO("models/best (4).pt")  # or "yolov8n.pt" or your own .pt file

results = model.track(source="input_videos/input_video5.mp4", conf=0.2, save=True)

# Optional: inspect first frame boxes
for r in results[:1]:
    print(r.boxes)