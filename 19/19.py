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

def consume_next_stripes(towels, design, depth):
    if len(design) == 0:
        return []

    if design in known_impossible:
        return None

    if design in known_solutions:
        return known_solutions[design]

    possible_next = [t for t in towels if design.startswith(t)]
    if not possible_next:
        known_impossible.add(design)
        return None

    all_solutions_for_branch = []

    for towel in possible_next:
        print(f"Checking towel {towel} for {design}")
        remaining_pattern = design[len(towel):]

        towel_branch_solutions = consume_next_stripes(towels, remaining_pattern, depth+1)

        if towel_branch_solutions is not None:
            if len(towel_branch_solutions) == 0:
                all_solutions_for_branch.append([towel])
            else:
                for towel_branch_solution in towel_branch_solutions:
                    all_solutions_for_branch.append([towel] + towel_branch_solution)

    # At this point we know all possible solutions for design
    if not all_solutions_for_branch:
        known_impossible.add(design)
        return None
    else:
        known_solutions[design] = all_solutions_for_branch
        return all_solutions_for_branch


def check_design(design, towels):
    return consume_next_stripes(towels, design, 0)


print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
possible = 0
sum = 0

for index, design in enumerate(designs):
    result = check_design(design, towels)
    print(f"{design}: {result}")
    length = 0 if result is None else len(result)
    possible += length != 0
    sum += length

print(possible)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
print(sum)

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
