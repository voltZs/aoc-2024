import time
from enum import Enum
import heapq

file = open("input.txt", "r")
start_time = time.time()

input_1, input_2 = file.read().split("\n\n")

towels = [list(stripes) for stripes in input_1.split(", ")]
towels_dict = {}
for towel in towels:
    stripes_count = len(towel)
    existing = towels_dict.get(stripes_count)
    if existing:
        existing.append(towel)
    else:
        towels_dict[stripes_count] = [towel]

designs =  [list(stripes) for stripes in input_2.split("\n")]

known_solutions = {

}


def consume_next_stripes(towels, remaining_design):
    if len(remaining_design) == 0:
        return True

    possible_next = [p for p in towels if remaining_design[:len(p)] == p]
    if not possible_next:
        return False

    for pattern in possible_next:
        remaining_pattern = remaining_design[len(pattern):]
        known_solution = known_solutions.get(str(remaining_pattern))
        if known_solution:
            return known_solution

        if consume_next_stripes(towels, remaining_pattern):
            known_solutions[str(remaining_pattern)] = True
            return True

    known_solutions[str(remaining_design)] = False
    return False

def check_design(design, towels):
    return consume_next_stripes(towels, design)


print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
# possible = 0
# for index, design in enumerate(designs):
#     print(f"{index}/{len(design)}: {design}")
#     is_doable = check_design(design, towels)
#     possible += is_doable

print(sum([check_design(design, towels) for design in designs]))


print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
