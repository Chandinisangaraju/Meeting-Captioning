# video_processor.py

import cv2
import os
import json

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.temp_dir = 'temp_videos'
        self.key_moments = []
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def process_video(self):
        print("--- Starting Content Change & Interaction Detection ---")
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        prev_frame = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            # Convert to grayscale for change detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Requirement: Detect content changes (slides/transitions) [cite: 27]
                diff = cv2.absdiff(prev_frame, gray)
                non_zero_count = cv2.countNonZero(cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1])
                
                # If a significant change is detected (thresholding logic)
                if non_zero_count > 100000: 
                    timestamp_sec = frame_count / fps
                    timestamp_str = f"{int(timestamp_sec // 60):02d}:{int(timestamp_sec % 60):02d}"
                    
                    # Requirement: Extract frames for every screen and click 
                    frame_filename = f"moment_{frame_count}.jpg"
                    frame_path = os.path.join(self.temp_dir, frame_filename)
                    cv2.imwrite(frame_path, frame)
                    
                    # Requirement: Document interaction (transitions/slides) 
                    self.key_moments.append({
                        "timestamp": timestamp_str,
                        "type": "Content_Change",
                        "frame_path": frame_path,
                        "description": "Screen content transition or interaction detected."
                    })
            
            prev_frame = gray
            frame_count += 30 # Processing every 30th frame for efficiency [cite: 50]

        cap.release() 
        # Save results to JSON for the ReportGenerator to use [cite: 35]
        with open('key_moments.json', 'w') as f:
            json.dump(self.key_moments, f)
        print(f"Video Processing Complete. Saved {len(self.key_moments)} moments.")