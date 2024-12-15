import time
from enum import Enum

file = open("input.txt", "r")
start = time.time()

free_space = 0
wall = 1
box = 2

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

map_input, movement_input = file.read().split("\n\n")

def import_matrix(matrix_string):
    matrix = []
    start_position = (0,0)
    for line_index, line in enumerate(matrix_string.split("\n")):
        matrix.append([])
        for column_index, tile in enumerate(line):
            if tile == ".":
                matrix[line_index].append(free_space)
            elif tile == "#":
                matrix[line_index].append(wall)
            elif tile == "O":
                matrix[line_index].append(box)
            elif tile == "@":
                matrix[line_index].append(free_space)
                start_position = (line_index, column_index)
    return (start_position, matrix)

movements = []
for movement in movement_input.replace("\n", ""):
    if movement == "^":
        movements.append(Direction.UP)
    elif movement == ">":
        movements.append(Direction.RIGHT)
    elif movement == "<":
        movements.append(Direction.LEFT)
    elif movement == "v":
        movements.append(Direction.DOWN)

def copy_matrix(a_matrix):
    new_matrix = []
    for line_index, line in enumerate(a_matrix):
        new_matrix.append([])
        for column in line:
            new_matrix[line_index].append(column)
    return new_matrix

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def get_new_tiles_ahead_or_none(tiles_ahead):
    new_tiles_ahead = []

    if tiles_ahead[0] == wall:
        return None

    elif tiles_ahead[0] == free_space:
        new_tiles_ahead = tiles_ahead

    elif tiles_ahead[0] == box:
        boxes_to_move = 0
        for tile in tiles_ahead:
            if tile == box:
                boxes_to_move += 1
            if tile == free_space:
                break
            if tile == wall:
                boxes_to_move = 0
                break
        if boxes_to_move == 0:
             # No free tile to move the box(es) to
            return None

        new_tiles_ahead = []
        for step, tile in enumerate(tiles_ahead):
            if step == 0:
                new_tiles_ahead.append(free_space)
            elif step <= boxes_to_move:
                new_tiles_ahead.append(box)
            else:
                new_tiles_ahead.append(tile)
    return new_tiles_ahead

def execute_move(old_position, direction, old_matrix):
    tiles_ahead = []
    line_index = old_position[0]
    column_index = old_position[1]

    match direction:
        case Direction.LEFT:
            line = old_matrix[line_index]
            tiles_up_to = list(reversed(line[column_index:]))
            tiles_ahead = list(reversed(line[:column_index]))

            new_tiles_ahead = get_new_tiles_ahead_or_none(tiles_ahead)
            if new_tiles_ahead is None:
                return (old_position, old_matrix)

            new_position = (old_position[0], old_position[1]-1)
            new_matrix = copy_matrix(old_matrix)
            new_matrix[line_index] = list(reversed(tiles_up_to + new_tiles_ahead))
            return (new_position, new_matrix) # TODO: new position

        case Direction.RIGHT:
            line = old_matrix[line_index]
            tiles_up_to = line[:column_index+1]
            tiles_ahead = line[old_position[1]+1:]

            new_tiles_ahead = get_new_tiles_ahead_or_none(tiles_ahead)
            if new_tiles_ahead is None:
                return (old_position, old_matrix)

            new_position = (old_position[0], old_position[1]+1)
            new_matrix = copy_matrix(old_matrix)
            new_matrix[line_index] = tiles_up_to + new_tiles_ahead
            return (new_position, new_matrix)

        case Direction.UP:
            column = [line[column_index] for line in old_matrix]
            tiles_up_to = list(reversed(column[line_index:]))
            tiles_ahead = list(reversed(column[:line_index]))

            new_tiles_ahead = get_new_tiles_ahead_or_none(tiles_ahead)
            if new_tiles_ahead is None:
                return (old_position, old_matrix)

            new_position = (old_position[0]-1, old_position[1])
            new_matrix = copy_matrix(old_matrix)
            new_column = list(reversed(tiles_up_to + new_tiles_ahead))
            for index, tile in enumerate(new_column):
                new_matrix[index][column_index] = tile
            return (new_position, new_matrix)

        case Direction.DOWN:
            column = [line[column_index] for line in old_matrix]
            tiles_up_to = column[:line_index+1]
            tiles_ahead = column[line_index+1:]

            new_tiles_ahead = get_new_tiles_ahead_or_none(tiles_ahead)
            if new_tiles_ahead is None:
                return (old_position, old_matrix)

            new_position = (old_position[0]+1, old_position[1])
            new_matrix = copy_matrix(old_matrix)
            new_column = tiles_up_to + new_tiles_ahead
            for index, tile in enumerate(new_column):
                new_matrix[index][column_index] = tile
            return (new_position, new_matrix)

start_import = import_matrix(map_input)
current_matrix = start_import[1]
current_position = start_import[0]
for direction in movements:
    result = execute_move(current_position, direction, current_matrix)
    current_position = result[0]
    current_matrix = result[1]

# printable_matrix = copy_matrix(current_matrix)
# printable_matrix[current_position[0]][current_position[1]] = "@"
# for line in printable_matrix:
#     print("".join([str(x) for x in line]).replace("0", ".").replace("1", "#").replace("2", "O"))

gps_sum = 0
for line_index, line in enumerate(current_matrix):
    for column_index, tile in enumerate(line):
        if tile == box:
            gps_sum += (100 * line_index) + column_index
print(f"GPS: {gps_sum}")

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 5))
