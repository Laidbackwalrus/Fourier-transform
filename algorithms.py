import numpy as np
from numpy.typing import NDArray

class BasicFourierTransform:
    def __init__(self, duration, freq_range, freq_resolution=0.05):
        self.duration = duration
        self.freq_range = freq_range # (lb, ub)
        self.freq_resolution = freq_resolution

    def compute_transform(self, data, t):
        
        winding_frequencies = np.arange(self.freq_range[0], self.freq_range[1], 0.5)  # Example range
        integrals = [
            np.trapz(data * np.exp(-2j * np.pi * t * wf), t)
            for wf in winding_frequencies
        ]

        return integrals, winding_frequencies


class FastFourierTransform:
    def __init__(self, num_samples, sample_rate):
        self.num_samples = num_samples
        self.sample_rate = sample_rate

        self.min_bin_size = sample_rate / num_samples 

    def compute_transform(self, data, t):
        winding_frequencies = np.arange(0, self.num_samples - 1)

        full_result = np.zeros((len(winding_frequencies),), dtype=np.complex_)

        # recursively compute FFT on even and odd parts
        for wf in winding_frequencies:
            fft_result = self.recursive(data, wf)
            full_result += fft_result
        
        return np.abs(full_result), winding_frequencies

    def recursive(self, data: NDArray[np.complex_], frequency) -> NDArray[np.complex_]:
        # normalize input to a numpy complex array so operations and type checking are consistent
        N = data.size
        if N <= 1:
            return data
        
        # split into even and odd indices
        even = data[0::2]
        odd = data[1::2]

        # first half of even = second half of even
        even_k = self.recursive(even, frequency)
        odd_k = self.recursive(odd, frequency)

        twiddle_factors = np.exp(-2j * np.pi * np.arange(N) * frequency / N)

        out = np.empty(N, dtype=complex)
        out[0:(N/2)] = even_k + twiddle_factors
        out[(N/2+1):] = even_k - twiddle_factors
        return out
    

class NumpyFFT:
    def __init__(self, num_samples, sample_rate):
        self.num_samples = num_samples
        self.sample_rate = sample_rate


    def compute_transform(self, data, t):
        fft_vals = np.fft.rfft(data)
        integrals = np.abs(fft_vals)
        print(self.num_samples, len(integrals))
        winding_frequencies = np.fft.rfftfreq(len(data), d=1.0 / self.sample_rate)
        return integrals, winding_frequencies