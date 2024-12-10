from enum import Enum
import time
file = open("input.txt", "r")
# Save timestamp
start = time.time()

matrix = []
# 3D array - each tile has a list of directions that represent the history of walking there
path = []

free_space = 0
obstacle = 1

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def next_direction(direction):
    match direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP

start_position = (0,0)
start_direction = Direction.UP

for line_index, line in enumerate(file.readlines()):
    matrix.append([])
    path.append([])
    for column_index, tile in enumerate(line.replace("\n", "")):
        path[line_index].append([])
        if tile == ".":
            matrix[line_index].append(free_space)
        elif tile == "#":
            matrix[line_index].append(obstacle)
        elif tile == "^":
            matrix[line_index].append(free_space)
            start_position = (line_index, column_index)
            path[line_index][column_index].append(start_direction)


height = len(matrix)
width = len(matrix[0])

# PART 1
def is_within_bounds(position):
    is_in_width = position[1] <= width-1 and position[1] >= 0
    is_in_height = position[0] <= height-1 and position[0] >= 0
    return is_in_width and is_in_height

def get_next_position(position, direction):
    match direction:
        case Direction.UP:
            return (position[0]-1, position[1])
        case Direction.RIGHT:
            return (position[0], position[1]+1)
        case Direction.DOWN:
            return (position[0]+1, position[1])
        case Direction.LEFT:
            return (position[0], position[1]-1)

def copy_starting_path():
    new_path = []
    for line_index, line in enumerate(path):
        new_path.append([])
        for column_index, column in enumerate(line):
            new_path[line_index].append([])
    new_path[start_position[0]][start_position[1]].append(start_direction)
    return new_path

def copy_matrix():
    new_matrix = []
    for line_index, line in enumerate(matrix):
        new_matrix.append([])
        for column in line:
            new_matrix[line_index].append(column)
    return new_matrix

def get_og_traversal():
    traversal = copy_starting_path()

    current_position = (start_position[0],start_position[1])
    current_direction = Direction.UP
    is_in_map = True

    while(is_in_map):
        next_position = get_next_position(current_position, current_direction)
        # Check if in bounds
        if not is_within_bounds(next_position):
            break
        # Check if we encountered a loop:
        if current_direction in traversal[next_position[0]][next_position[1]]:
            break

        is_next_obstacle = matrix[next_position[0]][next_position[1]] == obstacle
        if is_next_obstacle:
            current_direction = next_direction(current_direction)
            traversal[current_position[0]][current_position[1]].append(current_direction)
        else:
            current_position = next_position
            traversal[current_position[0]][current_position[1]].append(current_direction)

    return traversal

og_path = get_og_traversal()
# for line_index, line in enumerate(og_path):
#     string = []
#     for column_index, item in enumerate(line):
#         if item:
#             string.append("X")
#         elif matrix[line_index][column_index] == obstacle:
#             string.append("#")
#         else:
#             string.append(".")
#     print("".join(string))

visited_count = 0
for line in og_path:
    for item in line:
        if item: #array of directions not empty
            visited_count += 1

# print(visited_count)

# PART 2

def is_loopy(new_obstacle):
    new_matrix = copy_matrix()
    new_matrix[new_obstacle[0]][new_obstacle[1]] = obstacle

    traversal = copy_starting_path()

    current_position = (start_position[0], start_position[1])
    current_direction = Direction.UP
    is_in_map = True

    while(is_in_map):
        next_position = get_next_position(current_position, current_direction)
        # Check if in bounds
        if not is_within_bounds(next_position):
            break
        # Check if we encountered a loop:
        if current_direction in traversal[next_position[0]][next_position[1]]:
            return True

        is_next_obstacle = new_matrix[next_position[0]][next_position[1]] == obstacle
        if is_next_obstacle:
            current_direction = next_direction(current_direction)
            traversal[current_position[0]][current_position[1]].append(current_direction)
        else:
            current_position = next_position
            traversal[current_position[0]][current_position[1]].append(current_direction)

    return False

loopy_count = 0

og_traversal_list = []

for line_index, line in enumerate(og_path):
    for column_index, item in enumerate(line):
        if item:
            og_traversal_list.append((line_index, column_index))
print(len(og_traversal_list))

for path_tile in og_traversal_list:
    # Ignore start position of guard
    if start_position[0] == path_tile[0] and start_position[1] == path_tile[1]:
        continue
    if is_loopy((path_tile[0], path_tile[1])):
        loopy_count += 1

# for line_index, line in enumerate(matrix):
#     for column_index, colument in enumerate(line):
#         # Ignore start position of guard
#         if start_position[0] == line_index and start_position[1] == column_index:
#             continue
#         # Ignore existing obstacles
#         if matrix[line_index][column_index] == obstacle:
#             continue
#         if is_loopy((line_index, column_index)):
#             loopy_count += 1
print(loopy_count)

# Save timestamp
end = time.time()

print(end - start)
