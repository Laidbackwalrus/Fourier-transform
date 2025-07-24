import numpy as np
import matplotlib.pyplot as plt


repetions = 10
t = np.linspace(0, 2 * repetions * np.pi, 1000)

wave1 = np.sin(t)
wave2 = np.sin(t + np.pi/2)

plt.plot(t, wave1)
plt.plot(t, wave2)
plt.plot(t, wave1 + wave2)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
# plt.xlim(2 * repetions * np.pi)
plt.ylim(-3,3)
plt.show()