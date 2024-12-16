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

gps_sum = 0
for line_index, line in enumerate(current_matrix):
    for column_index, tile in enumerate(line):
        if tile == box:
            gps_sum += (100 * line_index) + column_index
print(f"GPS: {gps_sum}")

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__dict__}"


class Box:
    def __init__(self, position, width, height, id):
        self.p = position
        self.width = width
        self.height = height
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"{self.__dict__}"


def import_boxes(matrix_string):
    boxes = []
    for line_index, line in enumerate(matrix_string.split("\n")):
        column_index = 0
        while column_index < len(line):
            if line[column_index] == "[":
                boxes.append(Box(Position(column_index, line_index), 2, 1, len(boxes)))
                column_index += 2
                continue
            column_index += 1
    return boxes

def print_matrix(matrix, position, boxes):
    box_positions = [(b.p.x, b.p.y) for b in boxes]

    for line_index, line in enumerate(matrix):
        string = []
        for column_index, tile in enumerate(line):
            if position.y == line_index and position.x == column_index:
                string.append("@")
            elif tile == wall:
                string.append("#")
            elif (column_index, line_index) in box_positions:
                string.append("[")
            elif (column_index-1, line_index) in box_positions:
                string.append("]")
            else:
                string.append(".")
        print("".join(string))

def get_position_ahead(current_position, direction):
    match direction:
        case Direction.UP:
            return Position(current_position.x, current_position.y-1)
        case Direction.DOWN:
            return Position(current_position.x, current_position.y+1)
        case Direction.LEFT:
            return Position(current_position.x-1, current_position.y)
        case Direction.RIGHT:
            return Position(current_position.x+1, current_position.y)

def get_boxes_to_move(current_position, direction, matrix, boxes):
    position_ahead = get_position_ahead(current_position, direction)

    if matrix[position_ahead.y][position_ahead.x] == wall:
        # None returned when chain cannot be moved
        return None
    else:
        boxes_ahead = set()
        for box in boxes:
            is_within_width = position_ahead.x >= box.p.x and position_ahead.x < box.p.x+box.width
            is_within_height = position_ahead.y >= box.p.y and position_ahead.y < box.p.y+box.height
            if is_within_width and is_within_height:
                boxes_ahead.add(box)

        # print(f"boxes ahead: {boxes}")

        if not boxes_ahead:
            return []

        further_positions = [] #represents the edges of the boxes ahead based on direction
        for box in boxes_ahead:
            match direction:
                case Direction.UP:
                    for x in range(box.p.x, box.p.x + box.width):
                        further_positions.append(Position(x, box.p.y))
                case Direction.DOWN:
                    for x in range(box.p.x, box.p.x + box.width):
                        further_positions.append(Position(x, box.p.y+box.height-1))
                case Direction.LEFT:
                    for y in range(box.p.y, box.p.y + box.height):
                        further_positions.append(Position(box.p.x, y))
                case Direction.RIGHT:
                    for y in range(box.p.y, box.p.y + box.height):
                        further_positions.append(Position(box.p.x+box.width-1, y))

        further_boxes_ahead = [get_boxes_to_move(position, direction, matrix, boxes) for position in further_positions]

        if None in further_boxes_ahead:
            return None
        else:
            all_further_boxes = []
            for boxes in further_boxes_ahead:
                all_further_boxes += boxes
            result = list(boxes_ahead) + all_further_boxes
            return list(set(result))

def make_move(current_position, direction, matrix, boxes):
    boxes_to_move = get_boxes_to_move(current_position, direction, matrix, boxes)
    if boxes_to_move is None:
        # Ran into wall
        return current_position
    print(f"moving boxes: {sorted([box.id for box in boxes_to_move])}")
    for box in boxes_to_move:
        box.p = get_position_ahead(box.p, direction)

    return get_position_ahead(current_position, direction)


matrix_input = map_input.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
start_import = import_matrix(matrix_input.replace("[]", ".."))
current_position = Position(start_import[0][1], start_import[0][0])
room_layout = start_import[1]
boxes = import_boxes(matrix_input)

for direction in movements:
    current_position = make_move(current_position, direction, room_layout, boxes)

gps_sum = 0
for box in boxes:
    gps_sum += (100 * box.p.y) + box.p.x
print(f"GPS: {gps_sum}")

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 5))
