# main_app.py 
import os
import json
import shutil
import gc
import time
from input_handler import get_video_source
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
from report_generator import ReportGenerator

# Ensure MoviePy finds FFMPEG
from moviepy.config import change_settings
FFMPEG_BINARY_PATH = r"D:\FFMPEG\ffmpeg-master-latest-win64-gpl-shared\bin"
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"

change_settings({

    "IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY
})

if os.path.exists(FFMPEG_BINARY_PATH):
    change_settings({"FFMPEG_BINARY": FFMPEG_BINARY_PATH})
    print(f"[CONFIG] FFMPEG detected at: {FFMPEG_BINARY_PATH}")
else:
    print("[WARNING] FFMPEG path not found. MoviePy might fail.")

# --- Configuration ---
TEMP_DIR = 'temp_videos'
KEY_MOMENTS_JSON = 'key_moments.json'

def load_key_moments():
    try:
        if os.path.exists(KEY_MOMENTS_JSON):
            with open(KEY_MOMENTS_JSON, 'r') as f:
                return json.load(f)
    except Exception:
        return []
    return []

def run_project():
    print("\n=====================================================")
    print(" Meeting Video Captioning & Documentation Program")
    print(" (Final Verified Submission Version)")
    print("=====================================================")

    # --- STEP 0: CLEANUP ---
    print("-> Cleaning up previous run data...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    time.sleep(1)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # --- STEP 1: INPUT HANDLING ---
    input_value = 'sample_meeting.mp4'  
    source_type = 'local' 
    
    print(f"\n[STEP 1/4] Ingesting Video: {input_value}")
    video_path = get_video_source(input_value, source_type)

    try:
        # --- STEP 2: VIDEO PROCESSING ---
        print(f"\n[STEP 2/4] Detecting Content Changes & Interactions...")
        processor = VideoProcessor(video_path)
        processor.process_video()
        key_moments_list = load_key_moments()
        
        # Release Video Processor immediately
        del processor
        gc.collect()

        # --- STEP 3: AUDIO PROCESSING ---
        print(f"\n[STEP 3/4] Transcribing & Summarizing (Whisper AI)...")
        audio_processor = AudioProcessor(video_path)
        final_processed_moments = audio_processor.process_audio(key_moments_list)
        
        # CRITICAL: Release file handles before Step 4
        print("-> Finalizing audio data and releasing file locks...")
        del audio_processor
        gc.collect()
        time.sleep(3) 

        # --- STEP 4: REPORT & VIDEO GENERATION ---
        print(f"\n[STEP 4/4] Creating Deliverables...")
        
        # Create a copy for MoviePy to prevent Access Denied on original
        processing_video = "temp_processing_video.mp4"
        shutil.copy2(video_path, processing_video)

        report_gen = ReportGenerator(final_processed_moments)
        
        # 1. Generate PDF
        report_gen.generate_pdf_report() 
        
        # 2. Generate Captioned Video
        report_gen.burn_in_captions(processing_video) 
        
        print("\n=====================================================")
        print(" SUCCESS: ALL DELIVERABLES CREATED")
        print(" 1. Meeting_Documentation_Report.pdf")
        print(" 2. meeting_video_captions.mp4")
        print("=====================================================")

    except Exception as e:
        print(f"\n--- ERROR --- \nExecution failed: {e}")
    
    finally:
        # Final cleanup of temp copy
        if os.path.exists("temp_processing_video.mp4"):
            try: os.remove("temp_processing_video.mp4")
            except: pass

if __name__ == '__main__':
    run_project()