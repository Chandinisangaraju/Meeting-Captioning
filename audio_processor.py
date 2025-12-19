# audio_processor.py

import whisper

class AudioProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.model = whisper.load_model("base")

    def process_audio(self, visual_moments):
        print("Transcribing audio and generating summaries...")
        result = self.model.transcribe(self.video_path)
        
        full_transcript = result['text'] # The complete text of the meeting
        speech_segments = result['segments']
        
        # Associate summaries with each visual screen change [cite: 32, 33]
        for m in visual_moments:
            m_time = m['timestamp']
            # Get text from 5 seconds before to 10 seconds after the transition
            context = " ".join([s['text'] for s in speech_segments if abs(s['start'] - m_time) < 10])
            m['summary'] = context.strip() if context.strip() else "Screen transition/Interaction detected."

        return visual_moments, speech_segments, full_transcript