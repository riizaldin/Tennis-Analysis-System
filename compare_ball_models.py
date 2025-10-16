"""
Comprehensive comparison of all available YOLO ball detection models
Tests: yolo8_best.pt, yolo8_best2.pt, yolo8_last.pt, yolo8_last2.pt
"""

import cv2
import os
from ultralytics import YOLO
import numpy as np

def test_model_on_frames(model_path, video_path, num_frames=30, conf_threshold=0.1):
    """Test a single model on multiple frames"""
    print(f"\n{'='*80}")
    print(f"Testing Model: {model_path}")
    print(f"{'='*80}")
    
    if not os.path.exists(model_path):
        print(f"❌ Model NOT FOUND: {model_path}")
        return None
    
    # Load model
    try:
        model = YOLO(model_path)
        print(f"✓ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None
    
    # Get model info
    try:
        file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        print(f"📦 File Size: {file_size:.2f} MB")
        
        # Count parameters
        total_params = sum(p.numel() for p in model.model.parameters())
        print(f"🔢 Total Parameters: {total_params:,}")
        
        # Get model architecture type
        model_type = model.model.__class__.__name__
        print(f"🏗️  Architecture: {model_type}")
        
    except Exception as e:
        print(f"⚠️  Could not get model info: {e}")
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return None
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"🎬 Video: {os.path.basename(video_path)} ({total_frames} frames)")
    
    # Test on frames
    detections_count = 0
    confidence_scores = []
    frame_with_detections = []
    
    print(f"\n🔍 Testing on {num_frames} frames (conf={conf_threshold})...")
    
    for frame_num in range(min(num_frames, total_frames)):
        ret, frame = cap.read()
        if not ret:
            break
        
        try:
            # Run detection
            results = model.predict(frame, conf=conf_threshold, verbose=False)
            
            # Check if any tennis balls detected
            if len(results[0].boxes) > 0:
                detections_count += 1
                frame_with_detections.append(frame_num)
                
                # Get confidence scores
                for box in results[0].boxes:
                    confidence_scores.append(float(box.conf[0]))
        except Exception as e:
            print(f"⚠️  Error on frame {frame_num}: {e}")
            continue
    
    cap.release()
    
    # Calculate statistics
    detection_rate = (detections_count / num_frames) * 100 if num_frames > 0 else 0
    avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
    max_confidence = max(confidence_scores) if confidence_scores else 0
    min_confidence = min(confidence_scores) if confidence_scores else 0
    
    # Print results
    print(f"\n📊 RESULTS:")
    print(f"   Frames with detections: {detections_count}/{num_frames}")
    print(f"   Detection Rate: {detection_rate:.1f}%")
    print(f"   Total detections: {len(confidence_scores)}")
    
    if confidence_scores:
        print(f"   Confidence Scores:")
        print(f"      Average: {avg_confidence:.3f}")
        print(f"      Maximum: {max_confidence:.3f}")
        print(f"      Minimum: {min_confidence:.3f}")
        print(f"   Sample frames with detections: {frame_with_detections[:10]}")
    else:
        print(f"   ⚠️  NO DETECTIONS FOUND")
    
    return {
        'model_path': model_path,
        'file_size_mb': file_size if 'file_size' in locals() else 0,
        'total_params': total_params if 'total_params' in locals() else 0,
        'detection_rate': detection_rate,
        'detections_count': detections_count,
        'total_detections': len(confidence_scores),
        'avg_confidence': avg_confidence,
        'max_confidence': max_confidence,
        'min_confidence': min_confidence,
        'frames_tested': num_frames
    }

def print_comparison_table(results):
    """Print a comparison table of all models"""
    print(f"\n\n{'='*100}")
    print(f"{'COMPARISON SUMMARY':^100}")
    print(f"{'='*100}\n")
    
    # Sort by detection rate (descending)
    valid_results = [r for r in results if r is not None]
    sorted_results = sorted(valid_results, key=lambda x: x['detection_rate'], reverse=True)
    
    # Print header
    print(f"{'Rank':<6} {'Model':<20} {'Size(MB)':<12} {'Params':<15} {'Det.Rate':<12} {'Avg Conf':<12} {'Total Det':<12}")
    print(f"{'-'*100}")
    
    # Print each model
    for rank, result in enumerate(sorted_results, 1):
        model_name = os.path.basename(result['model_path'])
        size_str = f"{result['file_size_mb']:.2f}"
        params_str = f"{result['total_params']/1e6:.1f}M" if result['total_params'] > 0 else "N/A"
        det_rate_str = f"{result['detection_rate']:.1f}%"
        avg_conf_str = f"{result['avg_confidence']:.3f}" if result['avg_confidence'] > 0 else "N/A"
        total_det_str = str(result['total_detections'])
        
        # Add emoji indicators
        if result['detection_rate'] > 70:
            indicator = "🥇"
        elif result['detection_rate'] > 50:
            indicator = "🥈"
        elif result['detection_rate'] > 30:
            indicator = "🥉"
        elif result['detection_rate'] > 0:
            indicator = "⚠️"
        else:
            indicator = "❌"
        
        print(f"{indicator} {rank:<4} {model_name:<20} {size_str:<12} {params_str:<15} {det_rate_str:<12} {avg_conf_str:<12} {total_det_str:<12}")
    
    print(f"{'-'*100}")
    
    # Print winner
    if sorted_results:
        best = sorted_results[0]
        print(f"\n🏆 BEST PERFORMING MODEL: {os.path.basename(best['model_path'])}")
        print(f"   Detection Rate: {best['detection_rate']:.1f}%")
        print(f"   Average Confidence: {best['avg_confidence']:.3f}")
        print(f"   File Size: {best['file_size_mb']:.2f} MB")
        
        # Print worst
        if len(sorted_results) > 1:
            worst = sorted_results[-1]
            print(f"\n⚠️  WORST PERFORMING MODEL: {os.path.basename(worst['model_path'])}")
            print(f"   Detection Rate: {worst['detection_rate']:.1f}%")
            if worst['detection_rate'] == 0:
                print(f"   ❌ COMPLETELY FAILED - NO DETECTIONS")

def main():
    """Main comparison function"""
    print("="*100)
    print("TENNIS BALL DETECTION MODEL COMPARISON")
    print("="*100)
    
    # Models to test
    models = [
        'models/yolo8_best.pt',
        'models/yolo8_best2.pt',
        'models/yolo8_last.pt',
        'models/yolo8_last2.pt',
        'models/yolo8_best6.pt',
        'models/yolo8_last6.pt',
        'models/yolo8_best5.pt',
        'models/yolo8_last5.pt',
    ]
    
    # Video to test on
    video_path = 'input_videos/input_video2.mp4'
    
    # Check which models exist
    print("\n📁 Checking available models...")
    available_models = []
    for model_path in models:
        if os.path.exists(model_path):
            print(f"   ✓ Found: {model_path}")
            available_models.append(model_path)
        else:
            print(f"   ✗ Missing: {model_path}")
    
    if not available_models:
        print("\n❌ No models found! Please check the models directory.")
        return
    
    print(f"\n✓ Found {len(available_models)} models to test")
    
    # Check video exists
    if not os.path.exists(video_path):
        print(f"\n❌ Video not found: {video_path}")
        print("Available videos:")
        if os.path.exists('input_videos'):
            for f in os.listdir('input_videos'):
                if f.endswith(('.mp4', '.avi', '.mov')):
                    print(f"   - {f}")
        return
    
    print(f"✓ Using video: {video_path}")
    
    # Test each model
    results = []
    num_test_frames = 30  # Test on first 30 frames
    conf_threshold = 0.1   # Low threshold to catch any detection
    
    for model_path in available_models:
        result = test_model_on_frames(model_path, video_path, num_test_frames, conf_threshold)
        results.append(result)
    
    # Print comparison table
    print_comparison_table(results)
    
    print("\n" + "="*100)
    print("COMPARISON COMPLETE")
    print("="*100)

if __name__ == "__main__":
    main()
