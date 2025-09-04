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


def interactive_live_pitch_test():
    """Run the LivePitchAnalyser interactively.

    This will start the analyser's live loop which itself waits for Enter to stop.
    Press Enter in the console to stop live analysis and return.
    """
    print("Creating LivePitchAnalyser and starting live analysis. Press Enter to stop.")
    analyser = LivePitchAnalyser(frequency_range=(100.0, 2000.0), number_of_samples=4096)

    try:
        analyser.live_analysis(poll_interval=0.2)
    except Exception as e:
        print("Live pitch analyser failed:", e)


if __name__ == '__main__':
    # CLI options: run interactive test (default) or automated tests
    if len(sys.argv) > 1 and sys.argv[1] == 'test_live_pitch':
        def test_live_pitch_analyser(runtime_seconds: float = 5.0):
            """Start the LivePitchAnalyser for a short time and ensure it runs without error.

            This test is non-interactive and does not perform audio playback. It will assert
            that the live audio buffer has collected samples after the run.
            """
            sr = 44100
            buffer_size = sr * 5  # keep a 5-second rolling buffer

            # Import locally to keep the module import cheap at top-level
            from pitch_analyser import LivePitchAnalyser

            analyser = LivePitchAnalyser(frequency_range=(100.0, 2000.0), number_of_samples=4096)

            # Start analyser in a thread to avoid blocking on input()
            t = threading.Thread(target=lambda: analyser.live_analysis(poll_interval=0.2), daemon=True)
            t.start()

            # Let it run for runtime_seconds
            time.sleep(runtime_seconds)

            # Signal stop by sending an Enter to stdin is not possible here; instead, stop underlying audio
            try:
                analyser.audio_input.stop_buffering()
            except Exception:
                pass

            # Give analyser a moment to finish
            time.sleep(0.5)

            # Check buffer
            buf = analyser.audio_input.get_buffer()
            print(f"Live buffer length after run: {len(buf)} samples")

            if len(buf) == 0:
                raise AssertionError("No audio captured during live test")

            print("test_live_pitch_analyser: PASS")

        try:
            test_live_pitch_analyser()
        except AssertionError as e:
            print(e)
            sys.exit(2)
        except Exception as e:
            print("Unexpected error:", e)
            sys.exit(3)
        else:
            sys.exit(0)
    else:
        interactive_live_test()