# report_generator.py

import os
import subprocess
import shutil
import platform


class ReportGenerator:
    
    def __init__(self, visual_data, speech_segments, full_transcript):
        self.visual_data = visual_data
        self.speech_segments = speech_segments
        self.full_transcript = full_transcript
        self.output_video = "meeting_video_captions.mp4"
        self.output_report = "Detailed_Meeting_Report.html"

    def generate_report(self):
        print("Generating detailed documented report with summaries and transcript...")
        html = "<html><body style='font-family:Arial; padding:40px; line-height:1.6;'>"
        html += "<h1 style='color:#2c3e50;'>Meeting Documentation Report</h1>"
        
        # Section 1: Full Transcript 
        html += "<h2 style='border-bottom: 2px solid #2c3e50;'>1. Full Meeting Transcript</h2>"
        html += f"<p style='background:#f9f9f9; padding:15px;'>{self.full_transcript}</p>"
        
        # Section 2: Segmented Summaries and Interactions [cite: 32, 37, 38]
        html += "<h2 style='border-bottom: 2px solid #2c3e50;'>2. Key Moments and Summaries</h2>"
        for m in self.visual_data:
            ts = f"{int(m['timestamp']//3600):02d}:{int((m['timestamp']%3600)//60):02d}:{int(m['timestamp']%60):02d}"
            html += f"<div style='margin-bottom:20px; border-left:5px solid #3498db; padding-left:15px;'>"
            html += f"<strong>Timestamp:</strong> {ts}<br>"
            html += f"<strong>Interaction:</strong> Screen/Content Change<br>"
            html += f"<strong>Summary of Discussion:</strong> {m['summary']}"
            html += "</div>"
            
        with open(self.output_report, "w", encoding="utf-8") as f:
            f.write(html + "</body></html>")

    import platform
    
    def burn_captions(self, video_in):
        print("Burning synchronized captions into video...")
    
    # Determine default font path based on Operating System 
        system = platform.system()
        if system == "Windows":
          font_path = "C\\:/Windows/Fonts/arial.ttf"
        elif system == "Darwin": # macOS
          font_path = "/Library/Fonts/Arial.ttf"
        else: # Linux
          font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

        filters = []
        for s in self.speech_segments:
           start, end = s['start'], s['end']
           txt = s['text'].replace("'", "").replace(":", "-").strip()
           if txt:
            # Explicitly include the fontfile path in the drawtext filter
             filters.append(
                f"drawtext=fontfile='{font_path}':text='{txt}':fontcolor=yellow:fontsize=24:"
                f"box=1:boxcolor=black@0.6:x=(w-text_w)/2:y=h-80:enable='between(t,{start},{end})'"
            )

        with open("filters.txt", "w", encoding="utf-8") as f: 
           f.write(",".join(filters))
    
        cmd = [
        'ffmpeg', '-y', '-i', video_in, 
        '-filter_complex_script', 'filters.txt', 
        '-c:v', 'libx264', '-preset', 'ultrafast', '-c:a', 'copy', 
        self.output_video
        ]
    
        try:
        # Added error handling for troubleshooting 
             result = subprocess.run(cmd, capture_output=True, text=True)
             if result.returncode != 0:
                print(f"FFMPEG Error: {result.stderr}")
             else:
              print(f"Success! Final video: {self.output_video}")
        finally:
             if os.path.exists("filters.txt"): 
                os.remove("filters.txt")
