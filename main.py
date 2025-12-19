# main_app.py 
from input_handler import get_video_source
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
from report_generator import ReportGenerator
import json
import os

def run_automated_pipeline(user_input, username=None, password=None):
    """
    Main entry point for single-click execution[cite: 42, 45].
    Processes local files (MP4, MOV, AVI), YouTube, and Web platforms [cite: 6-9].
    """
    try:
        # STEP 1: Get Video Source [cite: 73]
        # Supports cloud links and private company videos with credentials [cite: 22-24]
        video_path = get_video_source(user_input, username=username, password=password)
        
        if not video_path or not os.path.exists(video_path):
            raise FileNotFoundError(f"Could not retrieve or find the video source: {user_input} [cite: 64]")

        # STEP 2: Process Visuals (Transitions/Clicks) [cite: 32]
        # Detects and documents every interaction [cite: 32]
        vp = VideoProcessor(video_path)
        vp.process_video()
        
        # Load the documented interactions [cite: 13, 37]
        with open('visual_moments.json', 'r') as f:
            visual_moments = json.load(f)
            
        # STEP 3: Process Audio (Transcription/Summary) [cite: 31, 33]
        # Summarizes key points for each segment [cite: 33, 38]
        ap = AudioProcessor(video_path)
        moments_with_summary, speech_segments, full_transcript = ap.process_audio(visual_moments)
        
        # STEP 4: Generate Deliverables [cite: 15, 74]
        rg = ReportGenerator(moments_with_summary, speech_segments, full_transcript)
        
        # Generate the documented report (PDF/HTML) [cite: 35, 41]
        rg.generate_report() 
        
        # Generate video with burned-in captions [cite: 15, 40]
        rg.burn_captions(video_path) 
        
        print("\n--- ALL DELIVERABLES GENERATED SUCCESSFULLY ---")

    except Exception as e:
        # Error handling and logging system for troubleshooting [cite: 80]
        print(f"--- ERROR IN PIPELINE: {e} --- [cite: 62]")

if __name__ == "__main__":
    # --- CONFIGURATION FOR PRIVATE VIDEOS ---
    # Set these if the web platform requires user credentials [cite: 8, 24]
    USER_CRED = None # e.g., "my_username"
    PASS_CRED = None # e.g., "my_password"

    # --- INPUT SELECTION ---
    # 1. Local (MP4, MOV, AVI) [cite: 20]
    # 2. YouTube Public URL [cite: 25] e.g: 'https://youtu.be/dh0pJdgY6Lc?si=Rrb3bezBlg6gnFch'
    # 3. Cloud Storage (Google Drive/Dropbox) [cite: 22]
    # 4. Private Internal Meetings [cite: 23]
    
    meeting_input = 'https://youtu.be/dh0pJdgY6Lc?si=Rrb3bezBlg6gnFch' 
    

    run_automated_pipeline(meeting_input, username=USER_CRED, password=PASS_CRED)
