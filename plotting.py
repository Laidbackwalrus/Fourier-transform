import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

_PLOTTER = None

class FrequencyPlotter:
    def __init__(self, title: str = "Frequency Spectrum"):
        # create or reuse the QApplication
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.win = pg.GraphicsLayoutWidget(title=title)
        self.win.resize(900, 500)
        self.plot = self.win.addPlot(title=title)
        self.plot.setLabel('bottom', 'Frequency', units='Hz')
        self.plot.setLabel('left', 'Amplitude')
        self.plot.showGrid(x=True, y=True)
        self.curve = self.plot.plot([], [], pen=pg.mkPen(color='y', width=1))
        self.win.show()

    def update(self, frequencies, amplitudes):
        freqs = np.asarray(frequencies)
        amps = np.asarray(amplitudes)
        self.curve.setData(freqs, amps)
        # process events so the plot updates immediately
        QtWidgets.QApplication.processEvents()

    def close(self):
        self.win.close()
# def plot_freqencies(frequencies, amplitudes):
#     plt.figure(figsize=(10, 6))
#     plt.plot(frequencies, amplitudes)
#     plt.xlabel("Frequency (Hz)")
#     plt.ylabel("Amplitude")
#     plt.title("Frequency Spectrum")
#     plt.grid()
#     plt.show()