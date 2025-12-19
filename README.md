Meeting Video Captioning & Documentation Program

This automated Python-based solution generates detailed documented reports and burned-in captions for meeting videos. It is designed as a single-click process requiring minimal user input.


🚀 Features

Multi-Source Video Input: Supports local files (MP4, MOV, AVI), YouTube URLs, and Cloud links (Google Drive/Dropbox).
Private Meeting Support: Handles videos requiring user credentials (e.g., internal company meetings).
Visual Interaction Detection: Automatically detects and documents screen transitions, clicks, and slide changes.
AI Transcription & Summary: Utilizes OpenAI Whisper for speech-to-text and generates contextual summaries for every key moment.
Burned-in Captions: Generates a synchronized video with visible captions.
Professional Reporting: Produces a detailed report in HTML and PDF formats with timestamps and summaries.


🛠️ Installation

1. Prerequisites
Python 3.8+
FFmpeg: Required for burning captions into the video.
Windows: choco install ffmpeg or download from official site.
Mac: brew install ffmpeg

2. Setup Environment

# Clone the repository
git clone <your-repo-link>
cd Meeting_Captioning_Program

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


💻 Usage (Single-Click Process)
To process a video and generate all deliverables:

Open main_app.py.
Update the meeting_input variable with your URL or local file path.
Run the script:

python main_app.py

📁 Expected Deliverables
Upon completion, the program generates:

meeting_video_captions.mp4: Video with burned-in captions.
Detailed_Meeting_Report.pdf: Documented report with transcript and summaries.
visual_moments.json: Raw diagnostic data for troubleshooting.


🛡️ Security & Reliability

Data Privacy: Ensures safe handling of sensitive internal meeting data.
Error Handling: Includes a logging system for unsupported formats or private URL errors.
Scalability: Optimized to process videos up to 2 hours long without performance degradation.
