import time
from enum import Enum
import itertools

file = open("input.txt", "r")
start_time = time.time()

initial_secret_nums = [int(n) for n in file.read().split("\n")]

def mix_and_prune(secret_number, new_number):
    return (new_number ^ secret_number) % 16777216

def get_next_secret_number(secret_number):
    new_secret = mix_and_prune(secret_number * 64, secret_number)
    new_secret = mix_and_prune(new_secret // 32, new_secret)
    return mix_and_prune(new_secret * 2048, new_secret)

def generate_secret(seed, iterations):
    current_secret = seed
    for i in range(iterations):
        current_secret = get_next_secret_number(current_secret)
    return current_secret

print("~~~~~~~~~~RESULT~~~~~~~~~~")
sum = 0
for num in initial_secret_nums:
    sum += generate_secret(num, 2000)
print(sum)

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
