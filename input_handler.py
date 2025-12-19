# input_handler.py

import os
import re
import requests
import yt_dlp

def get_video_source(input_value, username=None, password=None):
    """
    Handles all three input types defined in the Functional Requirements:
    1. Local Files (MP4, MOV, AVI) 
    2. Web Platform Videos (Cloud & Private with Credentials) [cite: 21-24]
    3. YouTube Videos (Public URLs) [cite: 25]
    """
    input_value = input_value.strip()
    target_filename = "meeting_video.mp4"

    # 1. REQUIREMENT: Local Video Files (MP4, MOV, AVI)
    # The doc specifically demands support for these three extensions.
    valid_extensions = ('.mp4', '.mov', '.avi')
    if any(input_value.lower().endswith(ext) for ext in valid_extensions):
        if os.path.exists(input_value):
            return input_value
        else:
            print(f"ERROR: Local file not found: {input_value} [cite: 63]")
            return None

    # 2. REQUIREMENT: YouTube Videos
    elif "youtube.com" in input_value or "youtu.be" in input_value:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': target_filename,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([input_value])
        return target_filename

    # 3. REQUIREMENT: Web Platform / Private Videos with Credentials
    # The doc requires handling private company videos and cloud links [cite: 22-24].
    elif input_value.startswith("http"):
        # Special logic for Google Drive direct downloading [cite: 22]
        if "drive.google.com" in input_value:
            try:
                file_id = re.search(r'd/([^/]+)', input_value).group(1)
                url = f"https://docs.google.com/uc?export=download&id={file_id}"
            except AttributeError:
                print("ERROR: Invalid Google Drive URL [cite: 64]")
                return None
        else:
            url = input_value

        # Support for Private Company Videos requiring credentials [cite: 23-24]
        auth = (username, password) if username and password else None
        
        try:
            # Scalability: Using 'stream=True' for videos up to 2 hours 
            response = requests.get(url, auth=auth, stream=True, timeout=60)
            response.raise_for_status() 
            
            with open(target_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            return target_filename
            
        except requests.exceptions.RequestException as e:
            # Meets the Error Handling requirement for missing/private URLs [cite: 64]
            print(f"ERROR: Web access failed. Credential or link error: {e}")
            return None

    else:
        print("ERROR: Unsupported file format or unrecognized URL [cite: 63]")
        return None