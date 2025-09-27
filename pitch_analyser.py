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
    def __init__(self, frequency_range, number_of_samples, algorithm=NumpyFFT):
        self.audio_input = LiveAudioInput(buffer_size=number_of_samples)
        self.sample_rate = self.audio_input.get_sample_rate()
        self.frequency_range = frequency_range
        self.number_of_samples = number_of_samples
        self.algorithm = algorithm  # for testing, skip custom FFT and use numpy FFT

    def run(self, poll_interval: float = 0.1, run_once: bool = False):
        # setup plotting
        self.graph = plotting.FrequencyPlotter()

        try:
            self.audio_input.start_buffering()
        except Exception as e:
            print("Failed to start live audio:", e)
            return

        # create instance-level stop event and worker thread so stop() can control them
        if getattr(self, "_thread", None) and getattr(self, "_thread").is_alive():
            print("Live analysis already running")
            return

        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            target=self._live_analysis,
            args=(self.audio_input, self._stop_event, poll_interval, run_once),
            daemon=True,
        )
        self._thread.start()

        # note: do not join or stop buffering here — caller should call stop() when they want to finish
    def _live_analysis(self, audio, stop_event, poll_interval, run_once: bool = False):
        iterations = 0
        while not stop_event.is_set():
            try:
                buf = audio.get_buffer()
            except Exception as e:
                print("Error reading buffer:", e)
                buf = np.array([])

            if buf.size == self.number_of_samples:
                duration = self.number_of_samples / self.sample_rate
                t = np.linspace(0, duration, self.number_of_samples, endpoint=False)
                
                if self.algorithm == NumpyFFT:
                    ft = NumpyFFT(self.number_of_samples, self.sample_rate)
                    integrals, winding_frequencies = ft.compute_transform(buf, t)
                else:
                    ft = FastFourierTransform(self.number_of_samples, self.sample_rate)
                    integrals, winding_frequencies = ft.compute_transform(buf, t)

                winding_frequencies, integrals = self.takesubset(winding_frequencies, integrals, self.frequency_range)

                self.graph.update(winding_frequencies, integrals)


            stop_event.wait(poll_interval)
            if run_once and iterations >= 1:
                break

    def takesubset(self, x, y, range):
        lb, ub = range
        mask = (x >= lb) & (x <= ub)
        return x[mask], y[mask]
    
    def stop(self, timeout: float = 5.0):
        """
        Stop the live analyser: signal the worker to exit, join the thread,
        stop audio buffering and close the plot window.
        """
        # signal worker to stop
        stop_event = getattr(self, "_stop_event", None)
        if stop_event is None:
            return

        stop_event.set()

        # join worker thread
        thread = getattr(self, "_thread", None)
        if thread is not None:
            try:
                thread.join(timeout=timeout)
            except Exception as e:
                print("Failed to join worker thread:", e)

        # stop audio buffering
        try:
            if getattr(self, "audio_input", None) is not None:
                self.audio_input.stop_buffering()
        except Exception as e:
            print("Failed to stop audio buffering:", e)

        # close plotting window if present
        try:
            if getattr(self, "graph", None) is not None:
                if hasattr(self.graph, "win"):
                    self.graph.close()
        except Exception as e:
            print("Failed to close plot window:", e)

        # clear internal handles
        self._thread = None
        self._stop_event = None
