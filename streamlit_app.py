"""
Tennis Analysis System - Advanced Video Analysis with Deep Learning
Court Detection (with Moving Camera Support), Player Tracking, and Ball Detection
"""

import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from pathlib import Path
import pickle

# Import custom modules
import sys
sys.path.append(str(Path(__file__).parent))

from utils import video_utils
from court_line_detector import CourtLineDetector
from mini_court import MiniCourt

# Page config
st.set_page_config(
    page_title="Tennis Analysis System",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg", width=200)
    st.markdown("## ⚙️ Configuration")
    
    # Model selection
    st.markdown("### 🤖 Models")
    
    court_model_path = st.text_input(
        "Court Keypoints Model",
        value="models/court_keypoints_best.pt",
        help="ResNet50 model for court keypoints detection (99.29% accuracy)"
    )
    
    ball_model_path = st.text_input(
        "Ball Detection Model",
        value="models/yolo8_best2.pt",
        help="YOLOv8s model for tennis ball detection (75%+ mAP@50)"
    )
    
    player_model_path = st.text_input(
        "Player Detection Model",
        value="yolov8x.pt",
        help="YOLOv8x model for player detection"
    )
    
    st.markdown("---")
    
    # Detection parameters
    st.markdown("### 🎯 Detection Parameters")
    
    ball_conf = st.slider(
        "Ball Detection Confidence",
        min_value=0.05,
        max_value=0.5,
        value=0.15,
        step=0.05,
        help="Lower value = more detections but more false positives"
    )
    
    st.markdown("---")
    
    # Processing options
    st.markdown("### 📊 Processing Options")
    
    enable_moving_camera = st.checkbox(
        "Enable Moving Camera Detection",
        value=True,
        help="Detect court keypoints in all frames (for moving camera videos). Slower but more accurate."
    )
    
    show_court_keypoints = st.checkbox("Show Court Keypoints", value=True)
    show_player_boxes = st.checkbox("Show Player Bounding Boxes", value=True)
    show_ball = st.checkbox("Show Ball Detection", value=True)
    show_mini_court = st.checkbox("Show Mini Court", value=True)
    
    interpolate_ball = st.checkbox(
        "Interpolate Ball Position",
        value=True,
        help="Fill missing ball positions with linear interpolation"
    )
    
    st.markdown("---")
    
    # Output options
    st.markdown("### 💾 Output Options")
    
    output_format = st.selectbox(
        "Video Format",
        ["MP4 (H.264)", "AVI (XVID)"]
    )
    
    output_fps = st.number_input(
        "Output FPS",
        min_value=15,
        max_value=60,
        value=24,
        step=1
    )
    
    st.markdown("---")
    
    # Model info
    st.markdown("### 📈 Model Performance")
    st.info("""
    **Court Detection:**
    - Accuracy: 99.29%
    - Precision: 99.30%
    - Moving camera support ✓
    
    **Ball Detection:**
    - mAP@50: >75%
    - Recall: >70%
    
    **Player Tracking:**
    - YOLOv8x + BoT-SORT
    """)

# Main content
st.markdown('<div class="main-header">🎾 Tennis Analysis System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Court Detection, Player Tracking, and Ball Analysis</div>', unsafe_allow_html=True)

st.markdown("---")

# Video upload section
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose a tennis video...",
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Upload a tennis match video for analysis"
    )

with col2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**💡 Tips:**")
    st.markdown("- Use HD video for best results")
    st.markdown("- Ensure full court is visible")
    st.markdown("- Good lighting conditions")
    st.markdown("- Moving camera supported!")
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    # Save uploaded file
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    
    # Display video info
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps
    cap.release()
    
    st.success(f"✅ Video uploaded successfully! ({uploaded_file.name})")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Duration", f"{duration:.1f}s")
    with col2:
        st.metric("Frames", total_frames)
    with col3:
        st.metric("FPS", fps)
    with col4:
        st.metric("Resolution", f"{width}×{height}")
    
    st.markdown("---")
    
    # Process button
    if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
        
        # Check if models exist
        models_ok = True
        missing_models = []
        
        if not Path(court_model_path).exists():
            missing_models.append(f"Court Model: {court_model_path}")
            models_ok = False
        
        if not Path(ball_model_path).exists():
            missing_models.append(f"Ball Model: {ball_model_path}")
            models_ok = False
        
        if not Path(player_model_path).exists():
            missing_models.append(f"Player Model: {player_model_path}")
            models_ok = False
        
        if not models_ok:
            st.error("❌ Missing model files:")
            for model in missing_models:
                st.error(f"  - {model}")
            st.info("💡 Please check the model paths in the sidebar.")
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Read video frames
                status_text.text("📹 Reading video frames...")
                progress_bar.progress(10)
                
                video_frames = video_utils.read_video(video_path)
                st.info(f"✅ Loaded {len(video_frames)} frames")
                
                # Step 2: Detect court keypoints
                court_detector = CourtLineDetector(court_model_path)
                
                if enable_moving_camera:
                    status_text.text("🎯 Detecting court keypoints (moving camera mode - all frames)...")
                    progress_bar.progress(20)
                    
                    # Use predict_video for moving camera detection (batch processing)
                    court_keypoints = court_detector.predict_video(video_frames)
                    st.success(f"✅ Court keypoints detected in {len(court_keypoints)} frames (moving camera)!")
                else:
                    status_text.text("🎯 Detecting court keypoints (static camera - first frame)...")
                    progress_bar.progress(20)
                    
                    # Use predict for static camera (single frame)
                    single_keypoint = court_detector.predict(video_frames[0])
                    court_keypoints = [single_keypoint] * len(video_frames)
                    st.success("✅ Court keypoints detected (static camera)!")
                
                # Step 3: Detect players
                status_text.text("👥 Detecting players...")
                progress_bar.progress(40)
                
                from trackers.player_tracker import PlayerTracker
                player_tracker_obj = PlayerTracker(player_model_path)
                player_detections = player_tracker_obj.detect_frames(video_frames)
                
                # Choose and filter to 2 players with court keypoints
                if len(player_detections) > 0:
                    player_detections = player_tracker_obj.choose_and_filter_players(
                        court_keypoints,  # Use multi-frame or replicated keypoints
                        player_detections
                    )
                
                st.success(f"✅ Players detected in {len(player_detections)} frames")
                
                # Step 4: Detect ball
                status_text.text("🎾 Detecting ball...")
                progress_bar.progress(60)
                
                from trackers.ball_tracker import BallTracker
                ball_tracker_obj = BallTracker(ball_model_path)
                ball_detections = ball_tracker_obj.detect_frames(video_frames)
                
                if interpolate_ball:
                    status_text.text("📈 Interpolating ball positions...")
                    ball_detections = ball_tracker_obj.interpolate_ball_positions(ball_detections)
                
                ball_detected_frames = sum(1 for d in ball_detections if d and 1 in d)
                st.success(f"✅ Ball detected in {ball_detected_frames} frames")
                
                # Step 5: Initialize Mini Court and calculate stats
                status_text.text("📊 Calculating player statistics...")
                progress_bar.progress(70)
                
                # Initialize mini court
                mini_court = MiniCourt(video_frames[0])
                
                # Convert positions to mini court coordinates
                player_mini_court_detections, ball_mini_court_detections = mini_court.convert_bounding_boxes_to_mini_court_coordinates(
                    player_detections,
                    ball_detections,
                    court_keypoints
                )
                
                # Detect ball shot frames
                ball_shot_frames = ball_tracker_obj.get_ball_shot_frames(ball_detections)
                st.info(f"🎾 Detected {len(ball_shot_frames)} ball shots")
                
                # Calculate player stats
                import pandas as pd
                from copy import deepcopy
                from utils import measure_distance, convert_pixel_distance_to_meters
                import constants
                
                player_stats_data = [{
                    'frame_num': 0,
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
                    end_frame = ball_shot_frames[ball_shot_ind + 1]
                    ball_shot_time_in_seconds = (end_frame - start_frame) / fps
                    
                    # Get distance covered by ball
                    distance_covered_pixels = measure_distance(
                        ball_mini_court_detections[start_frame][1],
                        ball_mini_court_detections[end_frame][1]
                    )
                    distance_covered_meters = convert_pixel_distance_to_meters(
                        distance_covered_pixels,
                        constants.DOUBLE_LINE_WIDTH,
                        mini_court.get_width_of_mini_court()
                    )
                    
                    # Speed of ball shot in km/h
                    speed_of_ball_shot = distance_covered_meters / ball_shot_time_in_seconds * 3.6
                    
                    # Player who shot the ball
                    player_positions = player_mini_court_detections[start_frame]
                    player_shot_ball = min(
                        player_positions.keys(),
                        key=lambda player_id: measure_distance(
                            player_positions[player_id],
                            ball_mini_court_detections[start_frame][1]
                        )
                    )
                    
                    # Opponent player speed
                    opponent_player_id = 1 if player_shot_ball == 2 else 2
                    distance_covered_pixels_opponent = measure_distance(
                        player_mini_court_detections[start_frame][opponent_player_id],
                        player_mini_court_detections[end_frame][opponent_player_id]
                    )
                    distance_covered_meters_opponent = convert_pixel_distance_to_meters(
                        distance_covered_pixels_opponent,
                        constants.DOUBLE_LINE_WIDTH,
                        mini_court.get_width_of_mini_court()
                    )
                    
                    speed_of_opponent_player = distance_covered_meters_opponent / ball_shot_time_in_seconds * 3.6
                    
                    current_player_stats = deepcopy(player_stats_data[-1])
                    current_player_stats['frame_num'] = start_frame
                    current_player_stats[f'player_{player_shot_ball}_number_of_shots'] += 1
                    current_player_stats[f'player_{player_shot_ball}_total_shot_speed'] += speed_of_ball_shot
                    current_player_stats[f'player_{player_shot_ball}_last_shot_speed'] = speed_of_ball_shot
                    current_player_stats[f'player_{opponent_player_id}_total_player_speed'] += speed_of_opponent_player
                    current_player_stats[f'player_{opponent_player_id}_last_player_speed'] = speed_of_opponent_player
                    
                    player_stats_data.append(current_player_stats)
                
                # Create dataframe and merge with all frames
                player_stats_data_df = pd.DataFrame(player_stats_data)
                frames_df = pd.DataFrame({'frame_num': range(len(video_frames))})
                player_stats_data_df = pd.merge(frames_df, player_stats_data_df, on='frame_num', how='left')
                player_stats_data_df = player_stats_data_df.ffill()
                
                # Calculate averages
                player_stats_data_df['player_1_average_shot_speed'] = player_stats_data_df['player_1_total_shot_speed'] / player_stats_data_df['player_1_number_of_shots']
                player_stats_data_df['player_2_average_shot_speed'] = player_stats_data_df['player_2_total_shot_speed'] / player_stats_data_df['player_2_number_of_shots']
                player_stats_data_df['player_1_average_player_speed'] = player_stats_data_df['player_1_total_player_speed'] / player_stats_data_df['player_2_number_of_shots']
                player_stats_data_df['player_2_average_player_speed'] = player_stats_data_df['player_2_total_player_speed'] / player_stats_data_df['player_1_number_of_shots']
                
                st.success("✅ Player statistics calculated!")
                
                # Step 6: Draw annotations
                status_text.text("🎨 Drawing annotations...")
                progress_bar.progress(80)
                
                output_frames = video_frames.copy()
                
                # Draw player boxes
                if show_player_boxes:
                    output_frames = player_tracker_obj.draw_bboxes(output_frames, player_detections)
                
                # Draw ball
                if show_ball:
                    output_frames = ball_tracker_obj.draw_bboxes(output_frames, ball_detections)
                
                # Draw court keypoints
                if show_court_keypoints:
                    output_frames = court_detector.draw_keypoints_on_video(output_frames, court_keypoints)
                
                # Draw mini court
                if show_mini_court:
                    output_frames = mini_court.draw_mini_court(output_frames)
                    # Draw player positions on mini court (green)
                    output_frames = mini_court.draw_points_on_mini_court(output_frames, player_mini_court_detections, color=(0, 255, 0))
                    # Draw ball position on mini court (yellow)
                    output_frames = mini_court.draw_points_on_mini_court(output_frames, ball_mini_court_detections, color=(0, 255, 255))
                
                # Draw player stats
                from utils import draw_player_stats
                output_frames = draw_player_stats(output_frames, player_stats_data_df)
                
                # Draw frame numbers
                for i, frame in enumerate(output_frames):
                    cv2.putText(frame, f"Frame {i+1}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Step 7: Save output video
                status_text.text("💾 Saving output video...")
                progress_bar.progress(90)
                
                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                
                fourcc = cv2.VideoWriter_fourcc(*'mp4v') if output_format == "MP4 (H.264)" else cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(output_path, fourcc, output_fps, (width, height))
                
                for frame in output_frames:
                    out.write(frame)
                
                out.release()
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                st.success("🎉 Video analysis completed successfully!")
                
                # Display results
                st.markdown("---")
                st.markdown("### 📊 Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Frames", len(output_frames))
                
                with col2:
                    # Count ball detections (dict with key 1)
                    ball_count = sum(1 for d in ball_detections if d and 1 in d and len(d[1]) > 0)
                    ball_detection_rate = ball_count / len(ball_detections) * 100
                    st.metric("Ball Detection", f"{ball_detection_rate:.1f}%")
                
                with col3:
                    player_frames = sum(1 for d in player_detections if d)
                    st.metric("Player Frames", player_frames)
                
                with col4:
                    court_frames = len(court_keypoints)
                    court_mode = "Moving" if enable_moving_camera else "Static"
                    st.metric("Court Frames", court_frames, delta=court_mode)
                
                # Download button
                st.markdown("---")
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Processed Video",
                        data=f,
                        file_name=f"tennis_analysis_{uploaded_file.name}",
                        mime="video/mp4",
                        use_container_width=True,
                        type="primary"
                    )
                
                # Display sample frames
                st.markdown("### 🎬 Sample Frames")
                
                sample_indices = [0, len(output_frames)//3, 2*len(output_frames)//3, -1]
                cols = st.columns(4)
                
                for idx, col in zip(sample_indices, cols):
                    with col:
                        frame_rgb = cv2.cvtColor(output_frames[idx], cv2.COLOR_BGR2RGB)
                        frame_num = idx if idx >= 0 else len(output_frames)+idx
                        st.image(frame_rgb, caption=f"Frame {frame_num}", use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error during processing: {str(e)}")
                st.error("Please check your model paths and video file.")
                import traceback
                st.code(traceback.format_exc())
            
            finally:
                # Clean up
                if 'video_path' in locals():
                    try:
                        os.unlink(video_path)
                    except:
                        pass
else:
    st.info("👆 Upload a tennis video to start analysis")
    st.markdown("""
    ### 📝 Instructions:
    1. **Upload Video**: Choose a tennis match video (MP4, AVI, MOV)
    2. **Configure Settings**: Adjust detection parameters in the sidebar
    3. **Enable Moving Camera**: Check if your video has camera movement
    4. **Start Analysis**: Click the button to begin processing
    5. **Download Results**: Get the analyzed video with all annotations
    
    ### 🎯 Key Features:
    - **Moving Camera Support**: Detects court in all frames (not just first frame)
    - **High Accuracy**: 99.29% court detection, 75%+ ball detection
    - **Player Tracking**: Automatic 2-player detection with BoT-SORT
    - **Ball Interpolation**: Fills missing ball positions for smooth trajectory
    - **Mini Court**: Real-time tactical view overlay
    """)
