import time
from enum import Enum
import heapq

file = open("input.txt", "r")
start_time = time.time()

input_1, input_2 = file.read().split("\n\n")
towels = input_1.split(", ")
designs = input_2.split("\n")

known_impossible = set()

def towels_from_string(towels):
    return towels.split("_")

known_solutions = {}

def consume_next_stripes(towels, design):
    existing = known_solutions.get(design)
    if existing:
        return existing

    if len(design) == 0:
        return 1

    possible_next = [t for t in towels if design.startswith(t)]

    sum = 0
    for towel in possible_next:
        sum += consume_next_stripes(towels, design[len(towel):])

    known_solutions[design] = sum
    return sum

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
possible = 0
sum = 0

for index, design in enumerate(designs):
    length = consume_next_stripes(towels, design)
    possible += length != 0
    sum += length

print(possible)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
print(sum)

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
