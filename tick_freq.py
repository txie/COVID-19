import numpy as np
import matplotlib.pyplot as plt

y = np.array([4,4,4,5,5,6,5,5,4,4,4])
x = np.arange(y.shape[0])
my_xticks = np.array(['a','b','c','d','e','f','g','h','i','j','k'])
frequency = 3
plt.plot(x, y)
plt.xticks(x[::frequency], my_xticks[::frequency])

plt.show()