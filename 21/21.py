import time
from enum import Enum
import itertools
import heapq

file = open("input.txt", "r")
start_time = time.time()

inputs = [list(input) for input in file.read().split("\n")]

class Direction(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
def position_on_num_pad(key):
    match key:
        case "7" | "8" | "9":
            y = 0
        case "4" | "5" | "6":
            y = 1
        case "1" | "2" | "3":
            y = 2
        case       "0" | "A":
            y = 3
    match key:
        case "9" | "6" | "3" | "A":
            x = 2
        case "8" | "5" | "2" | "0":
            x = 1
        case "7" | "4" | "1":
            x = 0
    return (x, y)


#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
def position_on_dir_pad(key):
    match key:
        case       "^" | "A":
            y = 0
        case "<" | "v" | ">":
            y = 1
    match key:
        case "A" | ">":
            x = 2
        case "^" | "v":
            x = 1
        case       "<" :
            x = 0
    return (x, y)

def position_in_direction(direction, position, max_x, max_y):
    x = position[0]
    y = position[1]
    p = None
    match direction:
        case Direction.UP:
            p = (x, y-1)
        case Direction.LEFT:
            p = (x-1, y)
        case Direction.RIGHT:
            p = (x+1, y)
        case Direction.DOWN:
            p = (x, y+1)
    if p[0] < 0 or p[0] > max_x or p[1] < 0 or p[1] > max_y:
        return None
    return p

def get_valid_paths(current, end, path_so_far, invalid_pos, max_x, max_y):
    if current == end:
        return [path_so_far]

    if current in invalid_pos:
        return None

    x_distance = current[0] - end[0]
    horizontal = []
    if x_distance != 0:
        horizontal_direction = Direction.RIGHT if x_distance < 0 else Direction.LEFT
        horizontal_neighbor = position_in_direction(horizontal_direction, current, max_x, max_y)
        if horizontal_neighbor is not None:
            horizontal_results = get_valid_paths(horizontal_neighbor, end, path_so_far + [horizontal_direction], invalid_pos, max_x, max_y)
            if horizontal_results is not None:
                horizontal = horizontal_results

    y_distance = current[1] - end[1]
    vertical = []
    if y_distance != 0:
        vertical_direction = Direction.DOWN if y_distance < 0 else Direction.UP
        vertical_neighbor = position_in_direction(vertical_direction, current, max_x, max_y)
        if vertical_neighbor is not None:
            vertical_results = get_valid_paths(vertical_neighbor, end, path_so_far + [vertical_direction], invalid_pos, max_x, max_y)
            if vertical_results is not None:
                vertical = vertical_results

    return horizontal + vertical


def all_directions_number_pad(start, end):
    start_pos = position_on_num_pad(start)
    end_pos = position_on_num_pad(end)
    return [[d.value for d in p] for p in get_valid_paths(start_pos, end_pos, [], [(0, 3)], 2, 3)]

def all_directions_dir_pad(start, end):
    start_pos = position_on_dir_pad(start)
    end_pos = position_on_dir_pad(end)
    return [[d.value for d in p] for p in get_valid_paths(start_pos, end_pos, [], [(0, 0)], 2, 1)]

# ------------------------------
robot_chain_size = 3
lowest_cost_memos = {} # (start, end, index): lowest_cost

def get_lowest_cost_directions(steps, robot_index = 1): # eg >^^A
    path = []
    robot_position = "A"
    for step in steps:
        existing_memo = lowest_cost_memos.get((robot_index, robot_position, step))
        if existing_memo:
            lowest_cost = existing_memo
        else:
            lowest_cost = get_lowest_cost_pad_directions(robot_position, step, robot_index)
            lowest_cost_memos[(robot_index, robot_position, step)] = lowest_cost

        path.extend(lowest_cost)
        robot_position = step
    return path


possible_paths_memos = {}

def get_lowest_cost_pad_directions(start, end, robot_index):
    # [[Direction]]
    if robot_index == 1:
        possible_instructions = all_directions_number_pad(start, end)
    else:
        existing_memo = possible_paths_memos.get((start, end))
        if existing_memo:
            possible_instructions = existing_memo
        else:
            possible_instructions = all_directions_dir_pad(start, end)
            possible_paths_memos[(start, end)] = possible_instructions

    lowest_cost = None
    for instructions in possible_instructions:
        # [Direction]
        directions = instructions + ["A"] # Add A to tell the robot to press the end dir
        # List of directions is accumulative. Because directions always end with A,
        # we can evaluate each list separately and return the lowest

        directions_to_compare = directions if robot_index == robot_chain_size else get_lowest_cost_directions(directions, robot_index + 1)

        if lowest_cost is None or len(lowest_cost) > len(directions_to_compare):
            lowest_cost = directions_to_compare

    return lowest_cost


print("~~~~~~~~~~RESULT~~~~~~~~~~")

complexity = 0
robot_chain_size = 3 # Only managed to get up to 20 robots in reasonable time for now
for input in inputs:
    shortest_solution = get_lowest_cost_directions(input, 1)
    numeric_input = int("".join(input).replace("A", ""))
    complexity += len(shortest_solution) * numeric_input

print(complexity)

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
