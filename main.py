import json
import os
import sys
from input_handler import get_video_source
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
from report_generator import ReportGenerator

def run_automated_pipeline(user_input, username=None, password=None):
    """
    Main entry point for single-click execution [cite: 42-45].
    Processes local files (MP4, MOV, AVI), YouTube, and Web platforms [cite: 6-9].
    """
    try:
        # STEP 1: Get Video Source [cite: 19-25, 73]
        video_path = get_video_source(user_input, username=username, password=password)
        
        if not video_path or not os.path.exists(video_path):
            raise FileNotFoundError(f"Could not retrieve or find the video source: {user_input} [cite: 64]")

        # STEP 2: Process Visuals (Transitions/Clicks) [cite: 26-29, 32]
        vp = VideoProcessor(video_path)
        vp.process_video()
        
        with open('visual_moments.json', 'r') as f:
            visual_moments = json.load(f)
            
        # STEP 3: Process Audio (Transcription/Summary) [cite: 30-31, 33]
        ap = AudioProcessor(video_path)
        moments_with_summary, speech_segments, full_transcript = ap.process_audio(visual_moments)
        
        # STEP 4: Generate Deliverables [cite: 15, 34, 74]
        rg = ReportGenerator(moments_with_summary, speech_segments, full_transcript)
        rg.generate_report() # Generates HTML/PDF [cite: 41]
        rg.burn_captions(video_path) # Generates captioned video [cite: 40]
        
        print("\n--- ALL DELIVERABLES GENERATED SUCCESSFULLY ---")

    except Exception as e:
        print(f"--- ERROR IN PIPELINE: {e} --- [cite: 62, 80]")

if __name__ == "__main__":
    # Check if a link/path was passed via command line
    if len(sys.argv) > 1:
        meeting_input = sys.argv[1]
    else:
        # If not, ask the user directly (Simple & Intuitive UI) [cite: 54-55]
        print("=== AI Meeting Automator ===")
        meeting_input = input("Enter Video Path or URL: ").strip()
    
    # Credentials can also be requested dynamically if needed [cite: 24, 58]
    run_automated_pipeline(meeting_input)
    
