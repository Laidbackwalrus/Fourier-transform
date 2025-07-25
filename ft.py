import numpy as np
import plotting


duration = 5
samples = 1000
winding_frequency = 2

t = np.linspace(0, duration, 1000)

wave1 = np.sin(2 * np.pi * t * 3)
wave2 = np.sin(2 * np.pi * t * 2)

wave3 = wave1 + wave2

four = wave3 * np.exp(-2j * np.pi * t * winding_frequency)

# plotting.plot_graph_2(t, wave1, wave2)

plotting.plot_graph_amps(four.real, four.imag)

