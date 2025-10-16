from ultralytics import YOLO
import cv2
import os
import pickle
import pandas as pd
from typing import List, Dict, Optional


class BallTracker:
    def __init__(self, model_path: str, conf: float = 0.15, ball_class_id: Optional[int] = None):
        self.model = YOLO(model_path)
        self.conf = conf
        self.ball_class_id = ball_class_id  # kalau None: ambil bbox dengan conf tertinggi

    # ---------- Inference ----------
    def detect_frame(self, frame) -> Dict[int, list]:
        """Return {1: [x1,y1,x2,y2]} or {} if none."""
        res = self.model.predict(frame, conf=self.conf, verbose=False)[0]
        best = None
        best_conf = -1.0

        for box in res.boxes:
            xyxy = box.xyxy.tolist()[0]
            cls  = int(box.cls.item()) if box.cls is not None else None
            conf = float(box.conf.item()) if box.conf is not None else 0.0

            if self.ball_class_id is not None:
                if cls == self.ball_class_id and conf > best_conf:
                    best_conf, best = conf, xyxy
            else:
                if conf > best_conf:
                    best_conf, best = conf, xyxy

        return {1: best} if best is not None else {}

    def detect_frames(self, frames: List, read_from_stub: bool = False, stub_path: Optional[str] = None):
        # cache baca
        if read_from_stub and stub_path and os.path.exists(stub_path):
            print(f"Loading ball detections from cache: {stub_path}")
            with open(stub_path, "rb") as f:
                return pickle.load(f)

        print(f"Detecting ball in {len(frames)} frames...")
        dets = [self.detect_frame(fr) for fr in frames]

        # cache tulis
        if stub_path:
            os.makedirs(os.path.dirname(stub_path), exist_ok=True)
            with open(stub_path, "wb") as f:
                pickle.dump(dets, f)
            print(f"Saved ball detections to: {stub_path}")

        return dets

    # ---------- Hit estimation ----------
    def get_ball_shot_frames(self, ball_detections: List[Dict[int, list]],
                             window: int = 5, minimum_change_frames_for_hit: int = 25) -> List[int]:
        """Heuristik: perubahan tanda delta_y yang bertahan >= minimum_change_frames_for_hit."""
        arr = [d.get(1, []) for d in ball_detections]
        if not any(len(a) == 4 for a in arr):
            return []

        df = pd.DataFrame(arr, columns=["x1", "y1", "x2", "y2"]).interpolate().bfill()
        df["mid_y"] = (df["y1"] + df["y2"]) / 2.0
        df["mid_y_rolling_mean"] = df["mid_y"].rolling(window=window, min_periods=1).mean()
        df["delta_y"] = df["mid_y_rolling_mean"].diff()
        df["ball_hit"] = 0  # init

        hits = []
        look_ahead = int(minimum_change_frames_for_hit * 1.2)

        for i in range(1, max(1, len(df) - look_ahead)):
            d0 = df["delta_y"].iloc[i]
            d1 = df["delta_y"].iloc[i + 1]
            neg2pos = (d0 < 0) and (d1 > 0)
            pos2neg = (d0 > 0) and (d1 < 0)
            if not (neg2pos or pos2neg):
                continue

            initial_sign = 1 if d0 > 0 else -1
            change_count = 0
            for j in range(i + 1, min(len(df), i + look_ahead + 1)):
                dj = df["delta_y"].iloc[j]
                if (initial_sign > 0 and dj < 0) or (initial_sign < 0 and dj > 0):
                    change_count += 1

            if change_count >= minimum_change_frames_for_hit:
                df.loc[i, "ball_hit"] = 1
                hits.append(i)

        return hits

    # ---------- Interpolation ----------
    def interpolate_ball_positions(self, ball_detections: List[Dict[int, list]]):
        """Return format konsisten: [{1:[x1,y1,x2,y2]}, ...]"""
        raw = [d.get(1, []) for d in ball_detections]
        if not any(len(r) == 4 for r in raw):
            print("Warning: No ball detections found. Returning empty detections.")
            return [{} for _ in raw]

        df = pd.DataFrame(raw, columns=["x1", "y1", "x2", "y2"]).interpolate().bfill()
        return [{1: row.tolist()} for _, row in df.iterrows()]

    # ---------- Drawing ----------
    def draw_bboxes(self, video_frames: List, ball_detections: List[Dict[int, list]]):
        out = []
        for frame, det in zip(video_frames, ball_detections):
            img = frame.copy()
            if det and 1 in det and len(det[1]) == 4:
                x1, y1, x2, y2 = map(int, det[1])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(img, "Ball", (x1, max(0, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
            out.append(img)
        return out
