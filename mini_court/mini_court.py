import cv2
import numpy as np
import sys
sys.path.append('../')
import constants
from utils import (
    convert_meters_to_pixel_distance,
    convert_pixel_distance_to_meters,
    get_foot_position,
    get_closest_keypoint_index,
    get_closest_keypoint_index_by_zone,
    get_height_of_bbox,
    measure_xy_distance,
    get_center_of_bbox,
    measure_distance
)

class MiniCourt():
    def __init__(self,frame):
        self.drawing_rectangle_width = 150  # Reduced from 180
        self.drawing_rectangle_height = 300  # Reduced from 360
        self.buffer = 30  # Reduced from 40
        self.padding_court = 12  # Reduced from 15
        
        # Extra padding for behind baseline (players often stand behind baseline)
        self.baseline_extension = 25  # Reduced from 30

        self.set_canvas_background_box_position(frame)
        self.set_mini_court_position()
        self.set_court_drawing_key_points()
        self.set_court_lines()


    def convert_meters_to_pixels(self, meters):
        return convert_meters_to_pixel_distance(meters,
                                                constants.DOUBLE_LINE_WIDTH,
                                                self.court_drawing_width
                                            )

    def set_court_drawing_key_points(self):
        drawing_key_points = [0]*28

        # point 0 
        drawing_key_points[0] , drawing_key_points[1] = int(self.court_start_x), int(self.court_start_y)
        # point 1
        drawing_key_points[2] , drawing_key_points[3] = int(self.court_end_x), int(self.court_start_y)
        # point 2
        drawing_key_points[4] = int(self.court_start_x)
        drawing_key_points[5] = self.court_start_y + self.convert_meters_to_pixels(constants.HALF_COURT_LINE_HEIGHT*2)
        # point 3
        drawing_key_points[6] = drawing_key_points[0] + self.court_drawing_width
        drawing_key_points[7] = drawing_key_points[5] 
        # #point 4
        drawing_key_points[8] = drawing_key_points[0] +  self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[9] = drawing_key_points[1] 
        # #point 5
        drawing_key_points[10] = drawing_key_points[4] + self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[11] = drawing_key_points[5] 
        # #point 6
        drawing_key_points[12] = drawing_key_points[2] - self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[13] = drawing_key_points[3] 
        # #point 7
        drawing_key_points[14] = drawing_key_points[6] - self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[15] = drawing_key_points[7] 
        # #point 8
        drawing_key_points[16] = drawing_key_points[8] 
        drawing_key_points[17] = drawing_key_points[9] + self.convert_meters_to_pixels(constants.NO_MANS_LAND_HEIGHT)
        # # #point 9
        drawing_key_points[18] = drawing_key_points[16] + self.convert_meters_to_pixels(constants.SINGLE_LINE_WIDTH)
        drawing_key_points[19] = drawing_key_points[17] 
        # #point 10
        drawing_key_points[20] = drawing_key_points[10] 
        drawing_key_points[21] = drawing_key_points[11] - self.convert_meters_to_pixels(constants.NO_MANS_LAND_HEIGHT)
        # # #point 11
        drawing_key_points[22] = drawing_key_points[20] +  self.convert_meters_to_pixels(constants.SINGLE_LINE_WIDTH)
        drawing_key_points[23] = drawing_key_points[21] 
        # # #point 12
        drawing_key_points[24] = int((drawing_key_points[16] + drawing_key_points[18])/2)
        drawing_key_points[25] = drawing_key_points[17] 
        # # #point 13
        drawing_key_points[26] = int((drawing_key_points[20] + drawing_key_points[22])/2)
        drawing_key_points[27] = drawing_key_points[21] 

        self.drawing_key_points=drawing_key_points

    def set_court_lines(self):
        self.lines = [
            (0, 2),
            (4, 5),
            (6,7),
            (1,3),
            
            (0,1),
            (8,9),
            (10,11),
            (10,11),
            (2,3)
        ]

    def set_mini_court_position(self):
        self.court_start_x = self.start_x + self.padding_court
        self.court_start_y = self.start_y + self.padding_court
        self.court_end_x = self.end_x - self.padding_court
        self.court_end_y = self.end_y - self.padding_court
        self.court_drawing_width = self.court_end_x - self.court_start_x

    def set_canvas_background_box_position(self,frame):
        frame= frame.copy()

        self.end_x = frame.shape[1] - self.buffer
        self.end_y = self.buffer + self.drawing_rectangle_height
        self.start_x = self.end_x - self.drawing_rectangle_width
        self.start_y = self.end_y - self.drawing_rectangle_height

    def draw_court(self,frame):
        for i in range(0, len(self.drawing_key_points),2):
            x = int(self.drawing_key_points[i])
            y = int(self.drawing_key_points[i+1])
            cv2.circle(frame, (x,y),5, (0,0,255),-1)

        # draw Lines
        for line in self.lines:
            start_point = (int(self.drawing_key_points[line[0]*2]), int(self.drawing_key_points[line[0]*2+1]))
            end_point = (int(self.drawing_key_points[line[1]*2]), int(self.drawing_key_points[line[1]*2+1]))
            cv2.line(frame, start_point, end_point, (0, 0, 0), 2)

        # Draw net
        net_start_point = (self.drawing_key_points[0], int((self.drawing_key_points[1] + self.drawing_key_points[5])/2))
        net_end_point = (self.drawing_key_points[2], int((self.drawing_key_points[1] + self.drawing_key_points[5])/2))
        cv2.line(frame, net_start_point, net_end_point, (255, 0, 0), 2)

        return frame

    def draw_background_rectangle(self,frame):
        shapes = np.zeros_like(frame,np.uint8)
        # Draw the rectangle
        cv2.rectangle(shapes, (self.start_x, self.start_y), (self.end_x, self.end_y), (255, 255, 255), cv2.FILLED)
        out = frame.copy()
        alpha=0.5
        mask = shapes.astype(bool)
        out[mask] = cv2.addWeighted(frame, alpha, shapes, 1 - alpha, 0)[mask]

        return out

    def draw_mini_court(self,frames):
        output_frames = []
        for frame in frames:
            frame = self.draw_background_rectangle(frame)
            frame = self.draw_court(frame)
            output_frames.append(frame)
        return output_frames

    def get_start_point_of_mini_court(self):
        return (self.court_start_x,self.court_start_y)
    def get_width_of_mini_court(self):
        return self.court_drawing_width
    def get_court_drawing_keypoints(self):
        return self.drawing_key_points

    def get_mini_court_coordinates(self,
                                   object_position,
                                   closest_key_point, 
                                   closest_key_point_index, 
                                   player_height_in_pixels,
                                   player_height_in_meters
                                   ):
        
        distance_from_keypoint_x_pixels, distance_from_keypoint_y_pixels = measure_xy_distance(object_position, closest_key_point)

        # Conver pixel distance to meters
        distance_from_keypoint_x_meters = convert_pixel_distance_to_meters(distance_from_keypoint_x_pixels,
                                                                           player_height_in_meters,
                                                                           player_height_in_pixels
                                                                           )
        distance_from_keypoint_y_meters = convert_pixel_distance_to_meters(distance_from_keypoint_y_pixels,
                                                                                player_height_in_meters,
                                                                                player_height_in_pixels
                                                                          )
        
        # Convert to mini court coordinates
        mini_court_x_distance_pixels = self.convert_meters_to_pixels(distance_from_keypoint_x_meters)
        mini_court_y_distance_pixels = self.convert_meters_to_pixels(distance_from_keypoint_y_meters)
        closest_mini_coourt_keypoint = ( self.drawing_key_points[closest_key_point_index*2],
                                        self.drawing_key_points[closest_key_point_index*2+1]
                                        )
        
        mini_court_player_position = (closest_mini_coourt_keypoint[0]+mini_court_x_distance_pixels,
                                      closest_mini_coourt_keypoint[1]+mini_court_y_distance_pixels
                                        )

        return  mini_court_player_position

    def convert_bounding_boxes_to_mini_court_coordinates(self,player_boxes, ball_boxes, original_court_key_points ):
        player_heights = {
            1: constants.PLAYER_1_HEIGHT_METERS,
            2: constants.PLAYER_2_HEIGHT_METERS
        }

        output_player_boxes= []
        output_ball_boxes= []
        
        # Ensure all arrays have the same length
        min_frames = min(len(player_boxes), len(ball_boxes), len(original_court_key_points))
        
        if len(player_boxes) != min_frames or len(ball_boxes) != min_frames or len(original_court_key_points) != min_frames:
            print(f"Warning: Frame count mismatch - Player: {len(player_boxes)}, Ball: {len(ball_boxes)}, Court: {len(original_court_key_points)}")
            print(f"Using minimum frame count: {min_frames}")

        for frame_num in range(min_frames):
            player_bbox = player_boxes[frame_num]
            # Get court keypoints for this specific frame
            court_keypoints_frame = original_court_key_points[frame_num]
            
            # Check if ball exists in this frame
            ball_box = ball_boxes[frame_num].get(1, None)
            
            output_player_bboxes_dict = {}
            output_ball_dict = {}
            
            # Find closest player to ball if ball exists
            closest_player_id_to_ball = None
            if ball_box is not None:
                ball_position = get_center_of_bbox(ball_box)
                if player_bbox:  # Check if there are players in frame
                    closest_player_id_to_ball = min(player_bbox.keys(), key=lambda x: measure_distance(ball_position, get_center_of_bbox(player_bbox[x])))

            for player_id, bbox in player_bbox.items():
                foot_position = get_foot_position(bbox)

                # Get The closest keypoint using zone-based selection to prevent incorrect net mapping
                closest_key_point_index = get_closest_keypoint_index_by_zone(foot_position, court_keypoints_frame, [0, 1, 2, 3, 12, 13])
                closest_key_point = (float(court_keypoints_frame[closest_key_point_index*2]), 
                                     float(court_keypoints_frame[closest_key_point_index*2+1]))

                # Get Player height in pixels
                frame_index_min = max(0, frame_num-20)
                frame_index_max = min(len(player_boxes), frame_num+50)
                bboxes_heights_in_pixels = [get_height_of_bbox(player_boxes[i][player_id]) for i in range (frame_index_min,frame_index_max) if player_id in player_boxes[i]]
                max_player_height_in_pixels = max(bboxes_heights_in_pixels) if bboxes_heights_in_pixels else get_height_of_bbox(bbox)

                mini_court_player_position = self.get_mini_court_coordinates(foot_position,
                                                                            closest_key_point, 
                                                                            closest_key_point_index, 
                                                                            max_player_height_in_pixels,
                                                                            player_heights[player_id]
                                                                            )
                
                output_player_bboxes_dict[player_id] = mini_court_player_position

                # Process ball only once for the closest player
                if ball_box is not None and closest_player_id_to_ball == player_id:
                    # Get The closest keypoint using zone-based selection
                    closest_key_point_index = get_closest_keypoint_index_by_zone(ball_position, court_keypoints_frame, [0, 1, 2, 3, 12, 13])
                    closest_key_point = (float(court_keypoints_frame[closest_key_point_index*2]), 
                                        float(court_keypoints_frame[closest_key_point_index*2+1]))
                    
                    mini_court_ball_position = self.get_mini_court_coordinates(ball_position,
                                                                            closest_key_point, 
                                                                            closest_key_point_index, 
                                                                            max_player_height_in_pixels,
                                                                            player_heights[player_id]
                                                                            )
                    output_ball_dict = {1: mini_court_ball_position}
            
            output_player_boxes.append(output_player_bboxes_dict)
            output_ball_boxes.append(output_ball_dict)

        return output_player_boxes , output_ball_boxes
    
    def draw_points_on_mini_court(self,frames,postions, color=(0,255,0)):
        """
        Draw player/ball positions on mini court.
        Positions are clipped to visible area with extended baseline zones.
        """
        # Extended boundaries for drawing (allow some space beyond baselines)
        min_x = self.court_start_x - 10
        max_x = self.court_end_x + 10
        min_y = self.court_start_y - self.baseline_extension  # Allow space above top baseline
        max_y = self.court_end_y + self.baseline_extension    # Allow space below bottom baseline
        
        for frame_num, frame in enumerate(frames):
            for _, position in postions[frame_num].items():
                x, y = position
                
                # Clip to extended boundaries for visibility
                x = max(min_x, min(x, max_x))
                y = max(min_y, min(y, max_y))
                
                x = int(x)
                y = int(y)
                cv2.circle(frame, (x,y), 5, color, -1)
        return frames
    
    def calculate_player_stats(self, player_mini_court_positions, ball_mini_court_positions, fps=24):
        """
        Calculate player and ball statistics in km/h.
        
        Args:
            player_mini_court_positions: List of dicts with player positions per frame
            ball_mini_court_positions: List of dicts with ball positions per frame  
            fps: Frames per second of the video
            
        Returns:
            player_stats: Dict with player statistics
            ball_stats: Dict with ball statistics
        """
        player_stats = {}
        ball_stats = {'speeds': [], 'shot_speeds': []}
        
        # Calculate player speeds
        for player_id in [1, 2]:
            speeds = []
            positions = []
            frame_indices = []
            
            # Collect all positions for this player
            for frame_num, frame_positions in enumerate(player_mini_court_positions):
                if player_id in frame_positions:
                    positions.append(frame_positions[player_id])
                    frame_indices.append(frame_num)
            
            # Calculate speed between consecutive detected frames
            for i in range(1, len(positions)):
                prev_pos = positions[i-1]
                curr_pos = positions[i]
                
                # Check frame gap (if frames are not consecutive)
                frame_gap = frame_indices[i] - frame_indices[i-1]
                if frame_gap == 0:
                    continue
                
                # Distance in mini court pixels
                dx = curr_pos[0] - prev_pos[0]
                dy = curr_pos[1] - prev_pos[1]
                distance_pixels = np.sqrt(dx**2 + dy**2)
                
                # Convert to meters (mini court width = 10.97m real court width)
                distance_meters = (distance_pixels / self.court_drawing_width) * constants.DOUBLE_LINE_WIDTH
                
                # Convert to km/h (account for frame gaps)
                time_seconds = frame_gap / fps
                speed_mps = distance_meters / time_seconds  # meters per second
                speed_kmh = speed_mps * 3.6  # convert to km/h
                
                # Filter unrealistic speeds (player max speed ~35 km/h for tennis sprint)
                if 0 < speed_kmh < 40:
                    speeds.append(speed_kmh)
            
            player_stats[player_id] = {
                'speeds': speeds,
                'avg_speed': np.mean(speeds) if speeds else 0,
                'max_speed': np.max(speeds) if speeds else 0
            }
        
        # Calculate ball speeds (shot speed)
        ball_positions = []
        ball_frame_indices = []
        
        for frame_num, frame_positions in enumerate(ball_mini_court_positions):
            if 1 in frame_positions:  # Ball is tracked as ID 1
                ball_positions.append(frame_positions[1])
                ball_frame_indices.append(frame_num)
        
        # Calculate ball speed between consecutive detected frames
        for i in range(1, len(ball_positions)):
            prev_pos = ball_positions[i-1]
            curr_pos = ball_positions[i]
            
            # Check frame gap
            frame_gap = ball_frame_indices[i] - ball_frame_indices[i-1]
            if frame_gap == 0:
                continue
            
            dx = curr_pos[0] - prev_pos[0]
            dy = curr_pos[1] - prev_pos[1]
            distance_pixels = np.sqrt(dx**2 + dy**2)
            
            # Convert to meters
            distance_meters = (distance_pixels / self.court_drawing_width) * constants.DOUBLE_LINE_WIDTH
            
            # Convert to km/h
            time_seconds = frame_gap / fps
            speed_mps = distance_meters / time_seconds
            speed_kmh = speed_mps * 3.6
            
            # Filter unrealistic speeds (professional tennis ball max ~250 km/h)
            if 0 < speed_kmh < 300:
                ball_stats['speeds'].append(speed_kmh)
                
                # If speed is significant (> 20 km/h), consider it a shot
                if speed_kmh > 20:
                    ball_stats['shot_speeds'].append(speed_kmh)
        
        ball_stats['avg_speed'] = np.mean(ball_stats['speeds']) if ball_stats['speeds'] else 0
        ball_stats['max_speed'] = np.max(ball_stats['speeds']) if ball_stats['speeds'] else 0
        ball_stats['avg_shot_speed'] = np.mean(ball_stats['shot_speeds']) if ball_stats['shot_speeds'] else 0
        ball_stats['max_shot_speed'] = np.max(ball_stats['shot_speeds']) if ball_stats['shot_speeds'] else 0
        ball_stats['total_shots'] = len(ball_stats['shot_speeds'])
        
        return player_stats, ball_stats
    
    def draw_player_stats(self, frames, player_stats, ball_stats):
        """
        Draw player statistics below the mini court.
        
        Args:
            frames: List of video frames
            player_stats: Dict with player statistics
            ball_stats: Dict with ball statistics
        """
        for frame in frames:
            # Stats box position (below mini court)
            stats_start_y = self.end_y + 10
            stats_x = self.start_x
            
            # Background for stats (increased height for ball stats)
            stats_height = 140
            stats_width = self.drawing_rectangle_width
            
            # Draw semi-transparent background
            overlay = frame.copy()
            cv2.rectangle(overlay, 
                         (stats_x, stats_start_y), 
                         (stats_x + stats_width, stats_start_y + stats_height),
                         (255, 255, 255), 
                         -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Draw border
            cv2.rectangle(frame, 
                         (stats_x, stats_start_y), 
                         (stats_x + stats_width, stats_start_y + stats_height),
                         (0, 0, 0), 
                         2)
            
            # Text settings
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.35
            font_thickness = 1
            line_height = 16
            
            y_offset = stats_start_y + 15
            
            # Title
            cv2.putText(frame, "PLAYER STATISTICS", 
                       (stats_x + 5, y_offset),
                       font, 0.4, (0, 0, 0), 2)
            y_offset += line_height + 3
            
            # Player 1 stats
            p1_avg = player_stats.get(1, {}).get('avg_speed', 0)
            p1_max = player_stats.get(1, {}).get('max_speed', 0)
            
            cv2.putText(frame, f"Player 1 (Bottom)", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 100, 0), font_thickness)
            y_offset += line_height
            
            cv2.putText(frame, f"  Avg: {p1_avg:.1f} km/h", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 0, 0), font_thickness)
            y_offset += line_height
            
            cv2.putText(frame, f"  Max: {p1_max:.1f} km/h", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 0, 0), font_thickness)
            y_offset += line_height + 2
            
            # Player 2 stats
            p2_avg = player_stats.get(2, {}).get('avg_speed', 0)
            p2_max = player_stats.get(2, {}).get('max_speed', 0)
            
            cv2.putText(frame, f"Player 2 (Top)", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (100, 0, 0), font_thickness)
            y_offset += line_height
            
            cv2.putText(frame, f"  Avg: {p2_avg:.1f} km/h", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 0, 0), font_thickness)
            y_offset += line_height
            
            cv2.putText(frame, f"  Max: {p2_max:.1f} km/h", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 0, 0), font_thickness)
            y_offset += line_height + 2
            
            # Ball stats
            ball_avg_shot = ball_stats.get('avg_shot_speed', 0)
            ball_max_shot = ball_stats.get('max_shot_speed', 0)
            total_shots = ball_stats.get('total_shots', 0)
            
            cv2.putText(frame, f"Ball (Shots: {total_shots})", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 100, 100), font_thickness)
            y_offset += line_height
            
            cv2.putText(frame, f"  Avg: {ball_avg_shot:.1f} km/h", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 0, 0), font_thickness)
            y_offset += line_height
            
            cv2.putText(frame, f"  Max: {ball_max_shot:.1f} km/h", 
                       (stats_x + 5, y_offset),
                       font, font_scale, (0, 0, 0), font_thickness)
            
        return frames

