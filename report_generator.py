# report_generator.py

import os
import subprocess
from datetime import timedelta

class ReportGenerator:
    def __init__(self, processed_moments):
        # We merge them immediately to avoid FFMPEG overload
        self.data = self.merge_moments(processed_moments)
        self.output_report = "Meeting_Documentation_Report.html"
        self.output_video = "meeting_video_captions.mp4"
        self.ffmpeg_path = r"D:\FFMPEG\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"

    def ensure_seconds(self, ts):
        if isinstance(ts, (int, float)): return float(ts)
        if isinstance(ts, str) and ":" in ts:
            parts = ts.split(':')
            return float(parts[0]) * 60 + float(parts[1]) if len(parts) == 2 else float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        return float(ts)

    def merge_moments(self, moments):
        """Reduces 1,200+ tiny moments into meaningful segments so FFMPEG doesn't crash."""
        if not moments: return []
        merged = []
        current = moments[0].copy()
        
        for next_m in moments[1:]:
            # If the summary is the same or it's within 2 seconds, merge them
            if next_m['summary'] == current['summary'] or (self.ensure_seconds(next_m['timestamp']) - self.ensure_seconds(current['timestamp']) < 2.0):
                continue 
            else:
                merged.append(current)
                current = next_m.copy()
        merged.append(current)
        return merged

    def generate_pdf_report(self):
        """Generates the HTML report."""
        print(f"-> Generating Report with {len(self.data)} merged segments...")
        html = "<html><body style='font-family:sans-serif;margin:40px;'><h1>Meeting Report</h1>"
        for m in self.data:
            ts = str(timedelta(seconds=int(self.ensure_seconds(m['timestamp']))))
            html += f"<div style='margin-bottom:30px;'><h3>Time: {ts}</h3><p>{m.get('summary', '')}</p></div>"
        with open(self.output_report, "w", encoding="utf-8") as f: f.write(html + "</body></html>")
        print(f"-> Report saved.")

    def burn_in_captions(self, video_input_path):
        """Forces HIGH VISIBILITY captions onto the video."""
        print(f"-> Burning {len(self.data)} Optimized Captions...")
        
        filter_script = "final_filters.txt"
        filters = []
        
        # 1. Add a 'Proof of Life' caption that stays for the first 5 seconds
        filters.append("drawtext=text='CAPTIONS ACTIVE':fontcolor=red:fontsize=40:x=20:y=20:enable='between(t,0,5)'")

        for i, m in enumerate(self.data):
            start = self.ensure_seconds(m['timestamp'])
            end = self.ensure_seconds(self.data[i+1]['timestamp']) if i+1 < len(self.data) else start + 4
            
            # Clean text for FFMPEG
            txt = m.get('summary', 'Meeting Detail').replace("'", "").replace(":", "-").replace("\n", " ")
            
            # Bright Yellow text, Large Font, Black Box
            cmd = (f"drawtext=text='{txt}':fontcolor=yellow:fontsize=30:box=1:boxcolor=black@0.8:"
                   f"x=(w-text_w)/2:y=h-100:enable='between(t,{start},{end})'")
            filters.append(cmd)

        with open(filter_script, "w", encoding="utf-8") as f:
            f.write(",".join(filters))

        # We use -c:v libx264 to FORCE re-encoding so the text is burned into the pixels
        command = [
            self.ffmpeg_path, '-y', '-i', video_input_path,
            '-filter_complex_script', filter_script,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23', '-c:a', 'copy',
            self.output_video
        ]

        try:
            print("-> FFMPEG is re-encoding the video. Please wait...")
            subprocess.run(command, check=True, capture_output=True)
            print(f"-> SUCCESS! Verify '{self.output_video}' now.")
        except subprocess.CalledProcessError as e:
            print(f"!! FFMPEG Error: {e.stderr.decode()}")
        finally:
            if os.path.exists(filter_script): os.remove(filter_script)