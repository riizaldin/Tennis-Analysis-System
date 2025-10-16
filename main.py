from utils import (read_video, 
                   save_video,
                   measure_distance,
                   draw_player_stats,
                   convert_pixel_distance_to_meters)

from trackers import PlayerTracker, BallTracker
from court_line_detector import CourtLineDetector
from mini_court import MiniCourt
import os
import cv2  
import pandas as pd
import constants
from copy import deepcopy

def main():
    #read video
    input_video_path = 'input_videos/input_video2.mp4'
    video_frames = read_video(input_video_path)
    
    print(f"Total frames: {len(video_frames)}")
    
    # Get video FPS for accurate time calculation
    cap = cv2.VideoCapture(input_video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    print(f"Video FPS: {video_fps}")
    
    # Generate unique stub paths based on video name
    video_name = os.path.splitext(os.path.basename(input_video_path))[0]
    
    #detect players (auto-detect cache)
    player_tracker = PlayerTracker(model_path='yolov8x')
    player_detections = player_tracker.detect_frames(
        video_frames, 
        read_from_stub=True,  # Not used anymore, but kept for compatibility
        stub_path=f'tracker_stubs/player_detections_{video_name}.pkl'
    )
    
    # Debug: Print player detection stats
    if player_detections:
        total_detections = sum(len(frame_dict) for frame_dict in player_detections)
        unique_ids = set()
        for frame_dict in player_detections:
            unique_ids.update(frame_dict.keys())
        print(f"Total player detections: {total_detections}")
        print(f"Unique player IDs detected: {sorted(unique_ids)}")
        print(f"First frame detections: {len(player_detections[0])} players")
    
    #detect ball (auto-detect cache)
    ball_tracker = BallTracker(model_path='models/yolo8_best2.pt')  
    ball_detections = ball_tracker.detect_frames(
        video_frames, 
        read_from_stub=True,
        stub_path=f'tracker_stubs/ball_detections_{video_name}.pkl'
    )
    
    ball_detections = ball_tracker.interpolate_ball_positions(ball_detections)
    
    # detect court lines (auto-detect cache)
    court_model_path = 'models/court_keypoints_best.pt'
    court_line_detector = CourtLineDetector(court_model_path)
    court_keypoints = court_line_detector.predict_video(
        video_frames,
        read_from_stub=True,
        stub_path=f'tracker_stubs/court_keypoints_{video_name}.pkl'
    )
    
    #choose and filter players based on court keypoints
    print(f"\nFiltering players based on court keypoints...")
    player_detections_filtered = player_tracker.choose_and_filter_players(court_keypoints, player_detections)
    
    # Debug: Print filtering results
    if player_detections_filtered:
        total_after = sum(len(frame_dict) for frame_dict in player_detections_filtered)
        unique_ids_after = set()
        for frame_dict in player_detections_filtered:
            unique_ids_after.update(frame_dict.keys())
        print(f"After filtering: {total_after} detections")
        print(f"Chosen player IDs: {sorted(unique_ids_after)}\n")
    
    player_detections = player_detections_filtered
    
    #detect ball hits
    ball_shot_frames = ball_tracker.get_ball_shot_frames(ball_detections)
    print(f"Detected ball hit frames: {ball_shot_frames}\n")
    
    
    
    # Initialize mini court
    mini_court = MiniCourt(video_frames[0])
    
    # Convert player and ball positions to mini court coordinates
    print("Converting positions to mini court coordinates...")
    player_mini_court_detections, ball_mini_court_detections = mini_court.convert_bounding_boxes_to_mini_court_coordinates(
        player_detections,
        ball_detections,
        court_keypoints
    )
    
    player_stats_data = [{
        'frame_num' : 0,
        'player_1_number_of_shots': 0,
        'player_1_total_shot_speed': 0,
        'player_1_last_shot_speed': 0,
        'player_1_total_player_speed': 0,
        'player_1_last_player_speed': 0,
        
        'player_2_number_of_shots': 0,
        'player_2_total_shot_speed': 0,
        'player_2_last_shot_speed': 0,
        'player_2_total_player_speed': 0,
        'player_2_last_player_speed': 0,
    }]
    
    for ball_shot_ind in range(len(ball_shot_frames) - 1):
        start_frame = ball_shot_frames[ball_shot_ind]
        end_frame = ball_shot_frames[ball_shot_ind+1] 
        ball_shot_time_in_seconds = (end_frame - start_frame) / video_fps  # Use actual video FPS
        
        #get distance covered by the ball
        distance_covered_pixels = measure_distance(ball_mini_court_detections[start_frame][1], ball_mini_court_detections[end_frame][1])
        distance_covered_meters = convert_pixel_distance_to_meters( distance_covered_pixels, constants.DOUBLE_LINE_WIDTH,
                                                                    mini_court.get_width_of_mini_court())
                                             
        
        #speed of ball shot in km/h
        speed_of_ball_shot = distance_covered_meters / ball_shot_time_in_seconds * 3.6  # Convert m/s to km/h
        
        #player who shot the ball
        #find player closest to ball at start_frame
        player_positions = player_mini_court_detections[start_frame]
        player_shot_ball = min(player_positions.keys(), key=lambda player_id: measure_distance(player_positions[player_id], 
                                                                                               ball_mini_court_detections[start_frame][1]))

        #opponent player speed
        opponent_player_id = 1 if player_shot_ball == 2 else 2
        distance_covered_pixels_opponent = measure_distance(player_mini_court_detections[start_frame][opponent_player_id], 
                                                          player_mini_court_detections[end_frame][opponent_player_id])
        distance_covered_meters_opponent = convert_pixel_distance_to_meters(distance_covered_pixels_opponent, 
                                                                            constants.DOUBLE_LINE_WIDTH,
                                                                            mini_court.get_width_of_mini_court())
        
        speed_of_opponent_player = distance_covered_meters_opponent / ball_shot_time_in_seconds * 3.6  # Convert m/s to km/h
        
        current_player_stats = deepcopy(player_stats_data[-1])
        current_player_stats['frame_num'] = start_frame
        current_player_stats[f'player_{player_shot_ball}_number_of_shots'] += 1
        current_player_stats[f'player_{player_shot_ball}_total_shot_speed'] += speed_of_ball_shot
        current_player_stats[f'player_{player_shot_ball}_last_shot_speed'] = speed_of_ball_shot
        
        current_player_stats[f'player_{opponent_player_id}_total_player_speed'] += speed_of_opponent_player
        current_player_stats[f'player_{opponent_player_id}_last_player_speed'] = speed_of_opponent_player
        
        player_stats_data.append(current_player_stats)
        
    player_stats_data_df = pd.DataFrame(player_stats_data) 
    frames_df = pd.DataFrame({'frame_num': range(len(video_frames))})
    player_stats_data_df = pd.merge(frames_df, player_stats_data_df, on='frame_num', how='left')
    player_stats_data_df = player_stats_data_df.ffill()
    
    player_stats_data_df['player_1_average_shot_speed'] = player_stats_data_df['player_1_total_shot_speed'] / player_stats_data_df['player_1_number_of_shots']
    player_stats_data_df['player_2_average_shot_speed'] = player_stats_data_df['player_2_total_shot_speed'] / player_stats_data_df['player_2_number_of_shots']
    player_stats_data_df['player_1_average_player_speed'] = player_stats_data_df['player_1_total_player_speed'] / player_stats_data_df['player_2_number_of_shots']
    player_stats_data_df['player_2_average_player_speed'] = player_stats_data_df['player_2_total_player_speed'] / player_stats_data_df['player_1_number_of_shots']
    
    #draw output
    output_video_frames = player_tracker.draw_bboxes(video_frames, player_detections)
    output_video_frames = ball_tracker.draw_bboxes(output_video_frames, ball_detections)
    output_video_frames = court_line_detector.draw_keypoints_on_video(output_video_frames, court_keypoints)
    
    #draw mini court
    output_video_frames = mini_court.draw_mini_court(output_video_frames)
    
    # Draw player stats on video frames
    output_video_frames = draw_player_stats(output_video_frames, player_stats_data_df)
    
    # Draw player positions on mini court (green for players)
    output_video_frames = mini_court.draw_points_on_mini_court(output_video_frames, player_mini_court_detections, color=(0, 255, 0))
    
    # Draw ball position on mini court (yellow for ball)
    output_video_frames = mini_court.draw_points_on_mini_court(output_video_frames, ball_mini_court_detections, color=(0, 255, 255))
    
    #draw frame numbers
    for i, frame in enumerate(output_video_frames):
        cv2.putText(frame, f"Frame {i+1}", (10, 30),  # Changed idx to i
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
    #save output video
    output_path = f'output_videos/output_{video_name}.avi'
    save_video(output_video_frames, output_path)
    print(f"Saved output to: {output_path}")

if __name__ == "__main__":
    main()