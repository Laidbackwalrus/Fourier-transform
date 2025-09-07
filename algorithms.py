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
    def __init__(self, num_samples, sample_rate, freq_range):
        self.num_samples = num_samples
        self.sample_rate = sample_rate
        self.freq_range = freq_range # (lb, ub)

        self.min_bin_size = sample_rate / num_samples 

    def compute_transform(self, data, t):
        upperHz = self.freq_range[1]
        lowerHz = self.freq_range[0]
        winding_frequencies = np.arange(lowerHz, upperHz, self.min_bin_size)

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
            return data * np.exp(-2j * np.pi * frequency)
        
        # split into even and odd indices
        even = data[0::2]
        odd = data[1::2]

        # first half of even = second half of even
        even_first_half = even[:N//4]
        calculation1 = self.recursive(even_first_half, frequency)
        evens = np.concatenate((calculation1, calculation1))

        odd_first_half = odd[:N//4]
        calculation2 = self.recursive(odd_first_half, frequency)
        odds = np.concatenate((calculation2, -calculation2))

        out = np.empty(N, dtype=complex)
        out[0::2] = evens
        out[1::2] = odds
        return out