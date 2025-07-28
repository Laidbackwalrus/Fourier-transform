import numpy as np
import plotting


duration = 10
samples = 1000
winding_frequency = 2

t = np.linspace(0, duration, 1000)

wave1 = np.sin(2 * np.pi * t * 3)
wave2 = np.sin(2 * np.pi * t * 2)

wave3 = wave1 + wave2

winding_frequencies = np.arange(0, 10, 0.05)  # Example range
integrals = [
    np.trapz(wave3 * np.exp(-2j * np.pi * t * wf), t)
    for wf in winding_frequencies
]

# integrals now contains the result for each winding frequency

# plotting.plot_graph_2(t, wave1, wave2)

# plotting.plot_graph_amps(four.real, four.imag)

plotting.plot_freqencies(winding_frequencies, np.abs(integrals))






