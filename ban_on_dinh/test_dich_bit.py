import numpy as np
a = [9,6,3,-10,9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
b = []
for i in range(0, len(a)):
    if a[i] != -1:
        b.append(a[i])
    else:
        i = i+1
print(b[:])

def count_occurrences(arr):
    count_dict = {}
    for element in arr:
        if element in count_dict:
            count_dict[element] += 1
        else:
            count_dict[element] = 1
    return count_dict
count_dict = count_occurrences(b)
for element in count_dict:
    print(f"{element} appears {count_dict[element]} times in the array")