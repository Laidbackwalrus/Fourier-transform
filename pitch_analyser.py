from audio_input import *
from algorithms import *
import numpy as np
import plotting
import time
import threading

class PitchAnalyser:
    pass

class StaticPitchAnalyser(PitchAnalyser):
    """Static pitch analyser that operates on audio files.

    This class preserves the existing `static_analysis` implementation from
    `PitchAnalyser` but provides a clearer type for callers.
    """
    def __init__(self, frequency_range, number_of_samples):
        self.audio_input = StaticAudioInput()
        self.frequency_range = frequency_range  # Frequency range in Hz
        self.number_of_samples = number_of_samples

    def static_analysis(self, file_path):
        """Perform static pitch analysis on the data"""
        start_time = time.time()

        file_data, sample_rate = self.audio_input.load_file(file_path)

        file_data = file_data[:len(file_data)]
        num_samples = len(file_data)
        duration = num_samples / sample_rate
        t = np.linspace(0, duration, num_samples, endpoint=False)
        data_collection_time = time.time()

        ft = BasicFourierTransform(duration, self.frequency_range)
        integrals, winding_frequencies = ft.compute_transform(file_data, t)
        computation_time = time.time()

        plotting.plot_freqencies(winding_frequencies, np.abs(integrals))

        end_time = time.time()
        print(f"Data collection time: {data_collection_time - start_time:.4f} seconds")
        print(f"Computation time: {computation_time - data_collection_time:.4f} seconds")
        print(f"Total time: {end_time - start_time:.4f} seconds")

class LivePitchAnalyser(PitchAnalyser):
    """Live pitch analyser that will operate on live audio input.

    Currently `PitchAnalyser.live_analysis` is a stub; this subclass exists
    so callers can explicitly choose a live analyser type.
    """
    def __init__(self, frequency_range, number_of_samples):
        self.audio_input = LiveAudioInput()
        self.frequency_range = frequency_range
        self.number_of_samples = number_of_samples

    def run(self, poll_interval: float = 0.1, run_once: bool = False):
        audio = self.audio_input

        try:
            audio.start_buffering()
        except Exception as e:
            print("Failed to start live audio:", e)
            return
        stop_event = threading.Event()

        thread = threading.Thread(
            target=self._live_analysis,
            args=(audio, stop_event, poll_interval, run_once),
            daemon=True,
        )
        thread.start()

        # worker thread will stop by itself when run_once=True or when you signal stop_event
        thread.join(timeout=10.0)
        audio.stop_buffering()

    def _live_analysis(self, audio, stop_event, poll_interval, run_once: bool = False):
        iterations = 0
        while not stop_event.is_set():
            try:
                buf = audio.get_buffer()
            except Exception as e:
                print("Error reading buffer:", e)
                buf = np.array([])

            if buf.size >= self.number_of_samples:
                segment = buf[-self.number_of_samples:]
                duration = self.number_of_samples / audio.sample_rate
                t = np.linspace(0, duration, self.number_of_samples, endpoint=False)
                ft = FastFourierTransform(self.number_of_samples, 44100, freq_range=self.frequency_range)
                try:
                    integrals, winding_frequencies = ft.compute_transform(segment, t)
                    plotting.plot_freqencies(winding_frequencies, integrals)
                except Exception as e:
                    print("Live analysis error:", e)

            stop_event.wait(poll_interval)
            iterations += 1
            if run_once and iterations >= 1:
                break