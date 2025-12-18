# audio_processor.py

import whisper
import os

class AudioProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        # Requirement: Transcribe audio into text (speech-to-text) 
        print("Initializing OpenAI Whisper model...")
        self.model = whisper.load_model("base")

    def process_audio(self, key_moments):
        print("-> Extracting audio and transcribing...")
        # Whisper can transcribe directly from the video file
        result = self.model.transcribe(self.video_path)
        full_text = result['text']
        segments = result['segments']

        # Save full transcript for records 
        with open('full_transcript.txt', 'w', encoding='utf-8') as f:
            f.write(full_text)

        print("-> Summarizing key points for segments...")
        # Requirement: Summarize key points for each segment 
        # We match transcript segments to our detected key moments
        for moment in key_moments:
            # Simple logic to find text spoken around the moment's timestamp
            m_time = self._timestamp_to_seconds(moment['timestamp'])
            relevant_text = " ".join([
                s['text'] for s in segments 
                if abs(s['start'] - m_time) < 10  # 10-second window
            ])
            
            # Requirement: Context-aware captions and descriptions [cite: 37, 76]
            moment['description'] = f"Context: {relevant_text[:100]}..." if relevant_text else "No speech detected."
            moment['summary'] = self._generate_summary(relevant_text)

        return key_moments

    def _timestamp_to_seconds(self, ts):
        m, s = map(int, ts.split(':'))
        return m * 60 + s

    def _generate_summary(self, text):
        # Requirement: Summaries of key points [cite: 38]
        if not text: return "N/A"
        return f"Summary: {text[:50]}..." # In a real scenario, use an LLM here