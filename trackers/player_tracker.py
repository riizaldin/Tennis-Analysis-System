from ultralytics import YOLO
import cv2
import pickle
import os
import sys
import numpy as np
sys.path.append('../')
from utils import measure_distance, get_center_of_bbox



class PlayerTracker:
    def __init__ (self, model_path):
        self.model = YOLO(model_path)
        
    def choose_and_filter_players(self, court_keypoints, player_detection):
        # Check if player_detection is empty or first frame has no detections
        if not player_detection or len(player_detection) == 0:
            print("Warning: No player detections found!")
            return []
        
        # Use multiple frames (first 10) to get more robust player selection
        # This handles cases where first frame might not be representative
        num_frames_to_analyze = min(10, len(player_detection))
        
        # Collect all detections from first N frames
        all_detections = {}
        for i in range(num_frames_to_analyze):
            if player_detection[i]:
                for track_id, bbox in player_detection[i].items():
                    if track_id not in all_detections:
                        all_detections[track_id] = []
                    all_detections[track_id].append(bbox)
        
        if not all_detections:
            print("Warning: No players detected in first frames!")
            return player_detection
        
        # Calculate average bbox for each track_id
        avg_detections = {}
        for track_id, bboxes in all_detections.items():
            if len(bboxes) >= 3:  # Only consider tracks that appear in at least 3 frames
                avg_bbox = [
                    sum(b[0] for b in bboxes) / len(bboxes),  # x1
                    sum(b[1] for b in bboxes) / len(bboxes),  # y1
                    sum(b[2] for b in bboxes) / len(bboxes),  # x2
                    sum(b[3] for b in bboxes) / len(bboxes)   # y2
                ]
                avg_detections[track_id] = avg_bbox
        
        if not avg_detections:
            print("Warning: No consistent tracks found in first frames!")
            # Fallback to first frame
            avg_detections = player_detection[0]
        
        print(f"  Found {len(avg_detections)} consistent tracks in first {num_frames_to_analyze} frames")
        
        court_keypoints_first_frame = court_keypoints[0]
        chosen_player = self.choose_players(court_keypoints_first_frame, avg_detections)
        
        # Filter and normalize player IDs to 1 and 2
        filtered_player_detections = []
        for player_dict in player_detection:
            filtered_player_dict = {track_id: bbox for track_id, bbox in player_dict.items() if track_id in chosen_player}
            filtered_player_detections.append(filtered_player_dict)
        
        # Normalize IDs to 1 and 2
        normalized_detections = self.normalize_player_ids(filtered_player_detections, chosen_player, avg_detections)
        
        return normalized_detections
    
    def normalize_player_ids(self, player_detections, chosen_players, avg_detections):
        """
        Normalize player IDs to 1 and 2 based on their Y position.
        Player with higher Y (lower on screen, near bottom) = Player 1
        Player with lower Y (higher on screen, near top) = Player 2
        """
        if len(chosen_players) < 2:
            # If only one player, just map to ID 1
            if len(chosen_players) == 1:
                old_id = chosen_players[0]
                id_mapping = {old_id: 1}
            else:
                return player_detections
        else:
            # Sort players by Y position (bottom of bbox)
            # Calculate average Y position for each player
            player_y_positions = {}
            for track_id in chosen_players:
                if track_id in avg_detections:
                    # Use bottom of bbox (y2) for positioning
                    player_y_positions[track_id] = avg_detections[track_id][3]
            
            # Sort by Y position: higher Y (bottom of screen) = Player 1, lower Y (top) = Player 2
            sorted_players = sorted(player_y_positions.items(), key=lambda x: x[1], reverse=True)
            
            # Create ID mapping: bottom player -> 1, top player -> 2
            id_mapping = {
                sorted_players[0][0]: 1,  # Bottom player (higher Y)
                sorted_players[1][0]: 2   # Top player (lower Y)
            }
            
            print(f"  ID Normalization: {id_mapping[sorted_players[0][0]]} (bottom, Y={sorted_players[0][1]:.0f}) ← ID {sorted_players[0][0]}")
            print(f"  ID Normalization: {id_mapping[sorted_players[1][0]]} (top, Y={sorted_players[1][1]:.0f}) ← ID {sorted_players[1][0]}")
        
        # Apply ID mapping to all frames
        normalized_detections = []
        for player_dict in player_detections:
            normalized_dict = {}
            for old_id, bbox in player_dict.items():
                if old_id in id_mapping:
                    new_id = id_mapping[old_id]
                    normalized_dict[new_id] = bbox
            normalized_detections.append(normalized_dict)
        
        return normalized_detections
        
    def choose_players(self, court_keypoints, player_dict, debug=True):
        # If less than 2 players detected, return all
        if len(player_dict) < 2:
            if debug:
                print(f"  Only {len(player_dict)} player(s) detected, returning all")
            return list(player_dict.keys())
        
        if debug:
            print(f"  Analyzing {len(player_dict)} detected players...")
        
        candidates = []
        for track_id, bbox in player_dict.items():
            x1, y1, x2, y2 = bbox
            player_center = get_center_of_bbox(bbox)
            
            # Calculate bbox properties
            bbox_width = x2 - x1
            bbox_height = y2 - y1
            bbox_area = bbox_width * bbox_height
            aspect_ratio = bbox_height / bbox_width if bbox_width > 0 else 0
            
            # Calculate distance to closest court keypoint
            min_distance = float('inf')
            for i in range(0, len(court_keypoints), 2):
                court_keypoint = (float(court_keypoints[i]), float(court_keypoints[i+1]))
                distance = measure_distance(player_center, court_keypoint)
                if distance < min_distance:
                    min_distance = distance
            
            # Store all metrics
            candidates.append({
                'track_id': track_id,
                'distance': min_distance,
                'area': bbox_area,
                'y_position': y2,  # Bottom of bbox (players usually at bottom of frame)
                'aspect_ratio': aspect_ratio,
                'bbox': bbox
            })
            
            if debug:
                print(f"    ID {track_id}: aspect={aspect_ratio:.2f}, area={bbox_area:.0f}, dist={min_distance:.0f}, y={y2:.0f}")
        
        # Multi-stage filtering
        # Stage 1: Filter by aspect ratio (standing person should be taller than wide)
        # Tennis players typically have aspect ratio between 1.5 to 4.0
        filtered_candidates = [c for c in candidates if 1.2 <= c['aspect_ratio'] <= 5.0]
        
        if debug:
            print(f"  After aspect ratio filter (1.2-5.0): {len(filtered_candidates)} candidates")
        
        # If too few candidates after aspect ratio filter, relax the constraint
        if len(filtered_candidates) < 2:
            filtered_candidates = candidates
            if debug:
                print(f"  Relaxing aspect ratio filter, using all {len(candidates)} candidates")
        
        # Stage 2: Filter by bbox area (remove very small detections)
        if len(filtered_candidates) >= 2:
            max_area = max([c['area'] for c in filtered_candidates])
            area_threshold = max_area * 0.15
            filtered_candidates = [c for c in filtered_candidates if c['area'] > area_threshold]
            if debug:
                print(f"  After area filter (>15% of max={max_area:.0f}): {len(filtered_candidates)} candidates")
        
        # If still have less than 2, use all candidates
        if len(filtered_candidates) < 2:
            filtered_candidates = candidates
            if debug:
                print(f"  Insufficient candidates, using all {len(candidates)}")
        
        # Stage 3: Prioritize by composite score
        # Score based on: distance (lower is better), area (larger is better), y_position (higher is better for tennis)
        for candidate in filtered_candidates:
            # Normalize metrics (0-1 scale)
            max_dist = max([c['distance'] for c in filtered_candidates])
            max_area = max([c['area'] for c in filtered_candidates])
            max_y = max([c['y_position'] for c in filtered_candidates])
            min_y = min([c['y_position'] for c in filtered_candidates])
            
            # Calculate composite score (lower is better for distance, higher is better for area and y)
            distance_score = candidate['distance'] / max_dist if max_dist > 0 else 0
            area_score = candidate['area'] / max_area if max_area > 0 else 0
            
            # Y score: prefer players at bottom of frame (tennis court perspective)
            # Normalize so higher y = better (closer to bottom)
            y_normalized = (candidate['y_position'] - min_y) / (max_y - min_y) if (max_y - min_y) > 0 else 0.5
            
            # Weighted composite score (lower is better)
            # Prioritize: area (40%), distance to court (35%), y position (25%)
            candidate['score'] = ((1 - area_score) * 0.40) + (distance_score * 0.35) + ((1 - y_normalized) * 0.25)
        
        # Sort by composite score (lower is better)
        filtered_candidates.sort(key=lambda x: x['score'])
        
        if debug:
            print(f"  Final ranking by composite score:")
            for i, c in enumerate(filtered_candidates[:5]):  # Show top 5
                print(f"    {i+1}. ID {c['track_id']}: score={c['score']:.3f}")
        
        # Choose top 2 players
        chosen_players = [filtered_candidates[0]['track_id']]
        if len(filtered_candidates) > 1:
            chosen_players.append(filtered_candidates[1]['track_id'])
        
        if debug:
            print(f"  ✓ Chosen players: {chosen_players}")
        
        return chosen_players
    
    def detect_frames(self, frames, read_from_stub = False, stub_path=None):
        # Auto-detect if stub exists
        if stub_path and os.path.exists(stub_path):
            print(f"Loading player detections from cache: {stub_path}")
            with open(stub_path, 'rb') as f:
                return pickle.load(f)
        
        print(f"Detecting players in {len(frames)} frames...")
        player_detections = []
        
        for frame in frames:
            player_dict = self.detect_frame(frame)
            player_detections.append(player_dict)
        
        # Post-process: smooth tracking and fill gaps
        player_detections = self.smooth_detections(player_detections)
        
        # Save to stub if path provided
        if stub_path is not None:
            os.makedirs(os.path.dirname(stub_path), exist_ok=True)
            with open(stub_path, 'wb') as f:
                pickle.dump(player_detections, f)
            print(f"Saved player detections to: {stub_path}")
        
        return player_detections
        
    def detect_frame(self, frame):
        results = self.model.track(
            frame, 
            persist=True,
            conf=0.25,  # Balanced confidence threshold
            iou=0.4,    # IoU threshold for NMS
            tracker="botsort.yaml",  # Using BoT-SORT for better tracking
            classes=[0],  # Only detect person class
            verbose=False,  # Reduce console output
            imgsz=640  # Input image size
        )
        
        player_dict = {}
        for box in results[0].boxes:
            if box.id is not None:  # Only include tracked objects with valid ID
                track_id = int(box.id[0])
                bbox = box.xyxy[0].tolist()
                
                # Additional validation: check if bbox is reasonable
                x1, y1, x2, y2 = bbox
                width = x2 - x1
                height = y2 - y1
                
                # Filter out unrealistic detections
                if width > 10 and height > 10:  # Minimum size
                    player_dict[track_id] = bbox
        
        return player_dict
    
    def smooth_detections(self, player_detections, max_gap=5):
        """
        Smooth player detections by interpolating small gaps where tracking was lost.
        This helps maintain consistent tracking across frames.
        """
        if not player_detections:
            return player_detections
        
        # Get all unique track IDs across all frames
        all_track_ids = set()
        for frame_detections in player_detections:
            all_track_ids.update(frame_detections.keys())
        
        # For each track ID, interpolate missing frames
        for track_id in all_track_ids:
            frame_positions = []
            
            # Collect all frames where this track_id appears
            for frame_idx, frame_detections in enumerate(player_detections):
                if track_id in frame_detections:
                    frame_positions.append((frame_idx, frame_detections[track_id]))
            
            # If track appears in multiple frames, interpolate gaps
            if len(frame_positions) > 1:
                for i in range(len(frame_positions) - 1):
                    start_frame, start_bbox = frame_positions[i]
                    end_frame, end_bbox = frame_positions[i + 1]
                    gap = end_frame - start_frame - 1
                    
                    # Only interpolate small gaps
                    if 0 < gap <= max_gap:
                        # Linear interpolation of bbox coordinates
                        for frame_idx in range(start_frame + 1, end_frame):
                            alpha = (frame_idx - start_frame) / (end_frame - start_frame)
                            interpolated_bbox = [
                                start_bbox[0] + alpha * (end_bbox[0] - start_bbox[0]),
                                start_bbox[1] + alpha * (end_bbox[1] - start_bbox[1]),
                                start_bbox[2] + alpha * (end_bbox[2] - start_bbox[2]),
                                start_bbox[3] + alpha * (end_bbox[3] - start_bbox[3])
                            ]
                            player_detections[frame_idx][track_id] = interpolated_bbox
        
        return player_detections
    
    def draw_bboxes(self, video_frames, player_detections):
        output_video_frames = []
        for frame, player_dict in zip(video_frames, player_detections):
            for track_id, bbox in player_dict.items():
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Player {track_id}", (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            output_video_frames.append(frame)
        
        return output_video_frames