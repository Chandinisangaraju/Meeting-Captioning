# video_processor.py

import cv2
import json

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.key_moments = []

    def process_video(self):
        print("Creating report markers every 5 seconds...")
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = total_frames / fps

        # Loop through the video in 5-second steps
        for second in range(0, int(duration_sec), 5):
            self.key_moments.append({"timestamp": float(second)})
            print(f"  [MARKER] Added moment at {second}s")
        
        cap.release()
        
        with open('visual_moments.json', 'w') as f:
            json.dump(self.key_moments, f)