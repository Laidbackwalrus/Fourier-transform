import soundfile as sf
import sounddevice as sd
import numpy as np

class AudioInput:
    def __init__(self):
        pass

    def load_file(self, file_path):
        # Load audio data from any supported file (WAV, OGG, FLAC, etc.)
        data, sample_rate = sf.read(file_path)
        return data, sample_rate

    def live_audio(self, duration=5, sample_rate=44100, channels=1):
        # Capture live audio input
        print("Recording...")
        data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='float64')
        sd.wait()
        print("Recording complete.")
        return data