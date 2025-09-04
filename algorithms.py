import numpy as np

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


