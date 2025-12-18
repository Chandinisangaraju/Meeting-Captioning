# input_handler.py

import os
import requests
from pytube import YouTube

# Define a temporary folder to store downloaded videos
TEMP_DIR = 'temp_videos'
os.makedirs(TEMP_DIR, exist_ok=True)

def get_video_source(input_value, source_type='local'):
    """
    Fetches video from the specified source and returns the local file path.
    :param input_value: File path or URL.
    :param source_type: 'local', 'youtube', or 'web_platform'.
    :return: The local path to the video file.
    """
    if source_type == 'local':
        if not os.path.exists(input_value):
            raise FileNotFoundError(f"Local video file not found at: {input_value}")
        return input_value
        
    elif source_type == 'youtube':
        return _download_youtube_video(input_value)
        
    elif source_type == 'web_platform':
        # For simplicity for a beginner, we treat all web platforms like a direct download link.
        # Handling credentials for private videos is more complex and can be added later.
        return _download_web_video(input_value)
        
    else:
        raise ValueError("Unsupported video source type.")

def _download_youtube_video(url):
    """Downloads the highest resolution MP4 stream of a public YouTube video."""
    print(f"-> Attempting to download YouTube video from: {url}")
    try:
        yt = YouTube(url)
        # Select the best quality progressive stream (contains both video and audio)
        stream = yt.streams.get_highest_resolution() 
        
        # Download the file to our temp directory
        video_path = stream.download(output_path=TEMP_DIR, filename=f"youtube_{yt.video_id}.mp4")
        print(f"-> YouTube video downloaded successfully.")
        return video_path
    except Exception as e:
        raise Exception(f"Failed to download YouTube video. Check URL or network: {e}")

def _download_web_video(url):
    """Downloads a video file from a direct web link."""
    print(f"-> Attempting to download web video from: {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Check for bad status codes (4xx or 5xx)

        file_name = url.split('/')[-1] if url.split('/')[-1].endswith(('.mp4', '.mov', '.avi')) else 'web_video.mp4'
        video_path = os.path.join(TEMP_DIR, file_name)
        
        # Save the content chunk by chunk (good for large files)
        with open(video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"-> Web video downloaded successfully.")
        return video_path
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download web video: {e}")