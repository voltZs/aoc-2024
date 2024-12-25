import time
from enum import Enum
import heapq

file = open("input.txt", "r")
start_time = time.time()

keys = []
locks = []

for block in file.read().split("\n\n"):
    schem = block.split("\n")
    is_lock = schem[0][0] == "#"
    trimmed = schem[1:-1]
    flipped = []
    for i in range(len(trimmed)):
        flipped.append([])
        for j in range(len(trimmed)):
            flipped[i].append(trimmed[j][i])
    nums = [len("".join(row).replace(".", "")) for row in flipped]
    if is_lock:
        locks.append(nums)
    else:
        keys.append(nums)

# print("Locks")
# for lock in locks:
#     print(lock)
# print("")
# print("Keys")
# for key in keys:
#     print(key)

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")

def get_fittting_combinations():
    combos = 0
    for key in keys:
        for lock in locks:
            fits = True
            for pin in range(5):
                if key[pin] + lock[pin] > 5:
                    fits = False
                    break
            if fits:
                combos += 1
    return combos

print(get_fittting_combinations())

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
