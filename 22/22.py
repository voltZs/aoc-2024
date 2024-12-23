import time
from enum import Enum
import itertools
from collections import deque

file = open("input.txt", "r")
start_time = time.time()

initial_secret_nums = [int(n) for n in file.read().split("\n")]

def mix_and_prune(secret_number, new_number):
    return (new_number ^ secret_number) % 16777216

def get_next_secret_number(secret_number):
    new_secret = mix_and_prune(secret_number * 64, secret_number)
    new_secret = mix_and_prune(new_secret // 32, new_secret)
    return mix_and_prune(new_secret * 2048, new_secret)

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def generate_secret(seed, iterations):
    current_secret = seed
    for i in range(iterations):
        current_secret = get_next_secret_number(current_secret)
    return current_secret

sum = 0
for num in initial_secret_nums:
    sum += generate_secret(num, 2000)
print(sum)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

def attempt_add_sequence_to_dict(dict, sequence, price):
    sequence_string = ",".join([str(n) for n in sequence])
    existing_price = dict.get(sequence_string)
    if not existing_price:
        dict[sequence_string] = price

def generate_sequence_dict(seed, iterations):
    dict = {}
    current_secret = seed
    differences = deque([])
    for i in range(iterations):
        last_secret = current_secret
        last_price = last_secret % 10
        new_secret = get_next_secret_number(current_secret)
        new_price = new_secret % 10

        differences.appendleft(new_price - last_price)
        if i > 3:
            differences.pop()

        if len(differences) == 4:
            attempt_add_sequence_to_dict(dict, differences, new_price)
        current_secret = new_secret

    return dict

def find_best_sequence():
    dict_list = []
    unique_sequences = set()
    for seller in initial_secret_nums:
        seller_dict = generate_sequence_dict(seller, 2000)
        dict_list.append(seller_dict)
        unique_sequences = unique_sequences.union(set(seller_dict.keys()))

    highest_bananas = 0
    for sequence in unique_sequences:
        sequence_bananas = 0
        for dict in dict_list:
            dict_bananas = dict.get(sequence)
            sequence_bananas += 0 if dict_bananas is None else dict_bananas

        if sequence_bananas > highest_bananas:
            highest_bananas = sequence_bananas

    return highest_bananas

print(find_best_sequence())

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
