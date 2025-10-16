import torch
import torchvision.transforms as transforms
import cv2
from torchvision import models
from torchvision.models import ResNet50_Weights
import numpy as np
import pickle
import os

class CourtLineDetector:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # Fix deprecation warning
        self.model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 14*2) 
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image):
        """Predict keypoints for a single frame"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_tensor = self.transform(image_rgb).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
        
        keypoints = outputs.squeeze().cpu().numpy()
        original_h, original_w = image.shape[:2]
        keypoints[::2] *= original_w / 224.0
        keypoints[1::2] *= original_h / 224.0

        return keypoints
    
    def predict_video(self, video_frames, read_from_stub=False, stub_path=None):
        """Predict keypoints for all frames with caching"""
        # Try to load from cache
        if read_from_stub and stub_path and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                print(f"Loading court keypoints from cache: {stub_path}")
                return pickle.load(f)
        
        print(f"Detecting court keypoints in {len(video_frames)} frames...")
        all_keypoints = []
        
        # Batch processing for speed
        batch_size = 8
        for i in range(0, len(video_frames), batch_size):
            batch_frames = video_frames[i:i+batch_size]
            
            # Process batch
            batch_tensors = []
            for frame in batch_frames:
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_tensor = self.transform(image_rgb)
                batch_tensors.append(image_tensor)
            
            # Stack and predict
            batch_tensor = torch.stack(batch_tensors).to(self.device)
            with torch.no_grad():
                outputs = self.model(batch_tensor)
            
            # Process outputs
            for j, output in enumerate(outputs):
                keypoints = output.cpu().numpy()
                frame = batch_frames[j]
                original_h, original_w = frame.shape[:2]
                keypoints[::2] *= original_w / 224.0
                keypoints[1::2] *= original_h / 224.0
                all_keypoints.append(keypoints)
            
            if (i+batch_size) % 100 == 0:
                print(f"Processed {min(i+batch_size, len(video_frames))}/{len(video_frames)} frames")
        
        # Save to cache
        if stub_path:
            os.makedirs(os.path.dirname(stub_path), exist_ok=True)
            with open(stub_path, 'wb') as f:
                pickle.dump(all_keypoints, f)
            print(f"Saved court keypoints to: {stub_path}")
        
        return all_keypoints

    def draw_keypoints(self, image, keypoints):
        """Draw keypoints on a single image"""
        for i in range(0, len(keypoints), 2):
            x = int(keypoints[i])
            y = int(keypoints[i+1])
            cv2.putText(image, str(i//2), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
        return image
    
    def draw_keypoints_on_video(self, video_frames, all_keypoints):
        """Draw keypoints on all video frames"""
        output_video_frames = []
        for frame, keypoints in zip(video_frames, all_keypoints):
            frame = self.draw_keypoints(frame.copy(), keypoints)
            output_video_frames.append(frame)
        return output_video_frames