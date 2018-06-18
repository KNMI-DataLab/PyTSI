import numpy as np
import matplotlib.pyplot as plt
import settings

data = np.genfromtxt(settings.output_data_copy, delimiter=settings.delimiter, names=True, dtype=None)

x = data['cloud_cover_GT']
y = data['cloud_cover_fixed']
diff = abs(x-y)

plt.

plt.hist(diff, bins=100)
plt.show()
plt.close()