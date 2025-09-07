import sys
import time
import threading
import numpy as np

from audio_input import LiveAudioInput
from pitch_analyser import LivePitchAnalyser
# import LivePitchAnalyser lazily inside the test to avoid top-level import issues

try:
    import sounddevice as sd
except Exception:
    sd = None

upper_limit = 370  # Hz
lower_limit = 73     # Hz
sample_rate = 44100  # Hz


def interactive_live_test():
    print("Creating LiveAudioInput and starting buffering. Press Enter to stop.")
    l = LiveAudioInput(sample_rate=44100, buffer_size=44100 * 10, blocksize=1024)
    try:
        l.start_buffering()
    except Exception as e:
        print("Failed to start LiveAudioInput:", e)
        return

    try:
        input("Recording... press Enter to stop recording\n")
    except KeyboardInterrupt:
        print("Interrupted, stopping recording.")

    l.stop_buffering()

    buf = l.get_buffer()
    print(f"Buffer contains {len(buf)} samples")

    if len(buf) == 0:
        print("No audio captured.")
        return

    # play the entire buffer
    segment = np.array(buf, dtype='float32')

    if sd is None:
        print("sounddevice not available; install it to play back the recording")
        return

    try:
        input("Press Enter to play the recorded buffer (or Ctrl+C to skip)...")
    except KeyboardInterrupt:
        print("Skipping playback.")
        return

    print(f"Playing entire buffer ({len(segment)} samples)...")
    sd.play(segment, l.sample_rate)
    sd.wait()
    print("Done.")


def test_live_pitch_analyser():
    print("Creating LivePitchAnalyser and starting live analysis. Press Ctrl+C to stop.")
    lp = LivePitchAnalyser(frequency_range=(lower_limit, upper_limit), number_of_samples=2^15)
    try:
        lp.run(poll_interval=0.2, run_once=False)
    except KeyboardInterrupt:
        print("Interrupted, stopping live analysis.")
    except Exception as e:
        print("Failed to run LivePitchAnalyser:", e)

if __name__ == '__main__':
    test_live_pitch_analyser()