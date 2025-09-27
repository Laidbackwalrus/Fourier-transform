import soundfile as sf
import sounddevice as sd
import numpy as np
from collections import deque
import threading
import queue


class AudioInput:
    pass


class StaticAudioInput(AudioInput):
    def load_file(self, file_path):
        data, sample_rate = sf.read(file_path)
        return data, sample_rate


class LiveAudioInput(AudioInput):
    def __init__(self, sample_rate=44100, buffer_size=32768, blocksize=1024, queue_maxsize=8):
        self.sample_rate = sample_rate
        self.channels = 1
        self.dtype = 'float32'
        self.buffer_size = buffer_size
        self.blocksize = blocksize
        self.queue_maxsize = queue_maxsize

        # rolling buffer for samples (mono) and a lock for safe reads
        self._buffer = deque(maxlen=self.buffer_size)
        self._lock = threading.Lock()

        # runtime primitives
        self._q = None
        self._stream = None
        self._consumer_thread = None
        self._stop_event = None

    def _callback(self, indata, frames, time_info, status):
        # tiny, real-time safe callback: copy and enqueue
        if status:
            print("InputStream status:", status)
        if self._q is None:
            return
        try:
            self._q.put_nowait(indata.copy())
        except queue.Full:
            # drop block if queue is full
            pass

    def _consumer(self):
        # drain queued blocks until stop_event is set and queue empty
        while not (self._stop_event and self._stop_event.is_set() and (self._q is not None and self._q.empty())):
            try:
                if self._q is None:
                    continue
                block = self._q.get(timeout=0.1)
            except Exception:
                continue

            # input is assumed mono; flatten to 1-D
            mono = block.reshape(-1)

            with self._lock:
                self._buffer.extend(mono.tolist())

            try:
                if self._q is not None:
                    self._q.task_done()
            except Exception:
                pass

    def start_buffering(self):
        if self._stream is not None:
            return

        self._q = queue.Queue(maxsize=self.queue_maxsize)
        self._stop_event = threading.Event()

        self._consumer_thread = threading.Thread(target=self._consumer, daemon=True)
        self._consumer_thread.start()

        # open and start input stream
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            callback=self._callback,
            blocksize=self.blocksize,
        )
        self._stream.start()

    def stop_buffering(self, join_timeout=1.0):
        if self._stream is None:
            return

        # signal consumer to finish
        if self._stop_event:
            self._stop_event.set()

        try:
            self._stream.stop()
            self._stream.close()
        except Exception:
            pass

        if self._consumer_thread is not None:
            self._consumer_thread.join(timeout=join_timeout)

        # clear stream-related handles but keep the buffer
        self._stream = None
        self._consumer_thread = None
        self._q = None
        self._stop_event = None

    def get_buffer(self):
        with self._lock:
            return np.array(self._buffer, dtype=self.dtype)

    def clear_buffer(self):
        with self._lock:
            self._buffer.clear()

    def is_buffering(self):
        return self._stream is not None

    def get_sample_rate(self):
        return self.sample_rate

