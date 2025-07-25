import matplotlib.pyplot as plt


def plot_graph_2(t, wave1, wave2):
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(t, wave1)
    plt.plot(t, wave2)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
    plt.ylim(-3,3)


    plt.subplot(2, 1, 2)
    plt.plot(t, wave1 + wave2)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
    plt.ylim(-3,3)

    plt.tight_layout()
    plt.show()

def plot_graph_amps(t, amps):

    plt.plot(t, amps)
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)

    plt.axhline(y=0, color='black', linestyle='-', linewidth=1)  
    plt.axvline(x=0, color='black', linestyle='-', linewidth=1)  

    plt.show()


def plot_freqencies(frequencies, amplitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, amplitudes)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Frequency Spectrum")
    plt.grid()
    plt.show()