import numpy as np
import matplotlib.pyplot as plt


duration = 5
samples = 1000

t = np.linspace(0, duration, 1000)

wave1 = np.sin(2 * np.pi * t * 3)
wave2 = np.sin(2 * np.pi * t * 2)

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