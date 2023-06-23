# import matplotlib.pyplot as plt

# x_data = [1, 2, 3, 4, 5]
# y_data = [2, 4, 6, 8, 10]

# plt.scatter(x_data, y_data)
# plt.show()

import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
padded_arr = np.pad(arr, ((1, 1), (1, 1)), 'constant', constant_values=0)

print("Original array:\n", arr)
print("Padded array:\n", padded_arr)