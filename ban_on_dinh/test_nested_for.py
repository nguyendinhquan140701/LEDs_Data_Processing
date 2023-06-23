import numpy as np
import time
# array1 = np.zeros(500, dtype=int)
# array2 = np.zeros(100, dtype=int)
# i = j = k =0
# a = b =0

# start_time = time.time()
# # for i in range(0, len(array2)):
# #     if array2[i] % 2 == 0:
# #         for j in range(0, 10):
# #             a = a + array2[i]

# end_time = time.time()
# elapsed_time = end_time - start_time
# print("elapsed time:", elapsed_time)
a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
b = a[::3]
print(b)