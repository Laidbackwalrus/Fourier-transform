import numpy as np
import matplotlib.pyplot as plt


repetions = 10
t = np.linspace(0, 2 * repetions * np.pi, 1000)

wave1 = np.sin(t)

plt.plot(t, wave1)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
# plt.xlim(2 * repetions * np.pi)
plt.ylim(-2,2)
plt.show()