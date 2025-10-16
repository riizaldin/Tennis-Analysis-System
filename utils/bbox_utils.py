def get_center_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    center_x = int(x1 + x2) / 2
    center_y = int(y1 + y2) / 2
    return (center_x, center_y)

def measure_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5 # Euclidean distance same like pythagorean theorem

def get_foot_position(bbox):
    """Get the foot position (bottom center) of a bounding box"""
    x1, y1, x2, y2 = bbox
    return (int((x1 + x2) / 2), int(y2))

def get_height_of_bbox(bbox):
    """Get the height of a bounding box"""
    return bbox[3] - bbox[1]

def measure_xy_distance(point1, point2):
    """Measure distance in x and y separately with direction (signed distance)"""
    return point1[0] - point2[0], point1[1] - point2[1]

def get_closest_keypoint_index(point, keypoints, keypoint_indices):
    """Get the index of the closest keypoint from a list of keypoint indices"""
    import numpy as np
    
    min_distance = float('inf')
    closest_index = keypoint_indices[0]
    
    for keypoint_index in keypoint_indices:
        # Extract keypoint coordinates
        kp_x = keypoints[keypoint_index * 2]
        kp_y = keypoints[keypoint_index * 2 + 1]
        
        # Convert to float - handles both numpy types and regular Python numbers
        kp_x = float(kp_x)
        kp_y = float(kp_y)
            
        keypoint = (kp_x, kp_y)
        distance = measure_distance(point, keypoint)
        
        if distance < min_distance:
            min_distance = distance
            closest_index = keypoint_index
    
    return closest_index

def get_closest_keypoint_index_by_zone(point, keypoints, keypoint_indices):
    """
    Get the closest keypoint based on court zones to avoid incorrect net mappings.
    
    Strategy:
    - Divide court into 3 zones: TOP (near baseline), NET, BOTTOM (far baseline)
    - First filter keypoints by zone, then find closest within that zone
    - This prevents players near top baseline from being mapped to net keypoints
    
    Args:
        point: (x, y) position to match
        keypoints: Array of all court keypoints [x0, y0, x1, y1, ...]
        keypoint_indices: List of candidate keypoint indices [0, 1, 2, 3, 12, 13]
    
    Returns:
        Index of the most appropriate keypoint
    """
    import numpy as np
    
    # Get key Y positions to define zones
    # Keypoints: 0,1 = near baseline (top), 2,3 = far service line (bottom), 12,13 = net
    near_baseline_y = (float(keypoints[0*2+1]) + float(keypoints[1*2+1])) / 2
    far_service_y = (float(keypoints[2*2+1]) + float(keypoints[3*2+1])) / 2
    net_y = (float(keypoints[12*2+1]) + float(keypoints[13*2+1])) / 2
    
    point_y = point[1]
    
    # Define zone thresholds with some buffer
    # Zone 1: TOP (near baseline area) - use keypoints 0, 1
    # Zone 2: NET (net crossing area) - use keypoints 12, 13
    # Zone 3: BOTTOM (far service/baseline area) - use keypoints 2, 3
    
    top_zone_max = net_y - abs(net_y - near_baseline_y) * 0.3  # 30% before net
    bottom_zone_min = net_y + abs(far_service_y - net_y) * 0.3  # 30% after net
    
    # Determine which keypoints to consider based on Y position
    if point_y < top_zone_max:
        # TOP zone: only consider baseline keypoints 0, 1
        zone_candidates = [k for k in keypoint_indices if k in [0, 1]]
    elif point_y > bottom_zone_min:
        # BOTTOM zone: only consider far keypoints 2, 3
        zone_candidates = [k for k in keypoint_indices if k in [2, 3]]
    else:
        # NET zone: consider net keypoints and nearby baselines
        zone_candidates = [k for k in keypoint_indices if k in [12, 13]]
        # If no net keypoints available, fall back to all
        if not zone_candidates:
            zone_candidates = keypoint_indices
    
    # If no candidates in zone (shouldn't happen), use all
    if not zone_candidates:
        zone_candidates = keypoint_indices
    
    # Now find closest keypoint within the zone candidates
    min_distance = float('inf')
    closest_index = zone_candidates[0]
    
    for keypoint_index in zone_candidates:
        kp_x = float(keypoints[keypoint_index * 2])
        kp_y = float(keypoints[keypoint_index * 2 + 1])
        
        keypoint = (kp_x, kp_y)
        distance = measure_distance(point, keypoint)
        
        if distance < min_distance:
            min_distance = distance
            closest_index = keypoint_index
    
    return closest_index