import time
from enum import Enum
import heapq

file = open("input.txt", "r")
start_time = time.time()

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"{self.x}_{self.y}")

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class TrackNode:
    def __init__(self, position, order):
        self.position = position
        self.order = order

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        return self.position == other.position and self.order == other.order

    def __hash__(self):
        return hash(f"{self.position}_{self.order}")

class Cheat:
    def __init__(self, s, e):
        self.s = s
        self.e = e

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        return self.s == other.s and self.e == other.e

    def __hash__(self):
        return hash(f"{self.s}_{self.e}")

space = 0
wall = 1

def import_matrix(matrix_string):
    matrix = []
    start_position = None
    goal_position = None
    for line_index, line in enumerate(matrix_string.split("\n")):
        matrix.append([])
        # print(line)
        for column_index, tile in enumerate(line):
            if tile == ".":
                matrix[line_index].append(space)
            elif tile == "#":
                matrix[line_index].append(wall)
            elif tile == "S":
                matrix[line_index].append(space)
                start_position = Position(column_index, line_index)
            elif tile == "E":
                matrix[line_index].append(space)
                goal_position = Position(column_index, line_index)
    return (matrix, start_position, goal_position)

map, start, goal = import_matrix(file.read())

def print_map(path = set()):
    for line_index, line in enumerate(map):
        string = []
        for column_index, tile in enumerate(line):
            if Position(column_index, line_index) == start:
                string.append("S")
            elif Position(column_index, line_index) == goal:
                string.append("E")
            elif Position(column_index, line_index) in path:
                string.append("O")
            elif tile == wall:
                string.append("#")
            else:
                string.append(".")
        print("".join(string))

def get_valid_in_direction(current_position, direction):
    match direction:
        case Direction.UP:
            p = Position(current_position.x, current_position.y-1)
        case Direction.LEFT:
            p = Position(current_position.x-1, current_position.y)
        case Direction.RIGHT:
            p = Position(current_position.x+1, current_position.y)
        case Direction.DOWN:
            p = Position(current_position.x, current_position.y+1)

    if p.x < 0 or p.x >= len(map[0]) or p.y < 0 or p.y >= len(map):
        return None

    return (p, direction)

def get_neighbors_and_cheats(current_position):
    directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
    neighbors_in_map = [get_valid_in_direction(current_position, d) for d in directions]
    neighbors = []
    walls_with_direction = []
    for n in neighbors_in_map:
        if n is None:
            continue
        if map[n[0].y][n[0].x] == space:
            neighbors.append(n[0])
        else:
            walls_with_direction.append(n)

    cheats = []
    for wd in walls_with_direction:
        possible_cheat = get_valid_in_direction(wd[0], wd[1])
        if possible_cheat is None:
            continue
        if map[possible_cheat[0].y][possible_cheat[0].x] == space:
            cheats.append(Cheat(wd[0], possible_cheat[0]))

    return (neighbors, cheats)

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def create_track_1():
    graph = {}
    cheats_dict = {}
    for line_index, line in enumerate(map):
        for column_index, tile in enumerate(line):
            if tile == wall:
                continue
            position = Position(column_index, line_index)
            (neighbors, cheats) = get_neighbors_and_cheats(position)
            graph[position] = neighbors
            cheats_dict[position] = cheats

    # track = {} # step: position
    track = {} # position: step
    cheats = {} # step: [Cheat]
    ignore = set() # tracks what steps to ignore in track building; should contain whole path
    current_position = start
    current_step = 0
    while True:
        ignore.add(current_position)
        # track[current_step] = current_position
        track[current_position] = current_step

        if current_position == goal:
            break

        # ignore already traversed track (backward cheat is not a cheat)
        valid_cheats = [c for c in cheats_dict[current_position] if c.e not in ignore]
        cheats[current_step] = valid_cheats

        neighbors = graph[current_position]
        # assuming only one valid path forward (or none if end)
        for neighbor in neighbors:
            if neighbor not in ignore: # ignore already traversed track
                current_position = neighbor
                continue

        current_step += 1

    return (track, cheats, current_step)

(track, cheats, total_steps) = create_track_1()

solution = 0
for step in cheats.keys():
    for cheat in cheats[step]:
        length_up_to_cheat = step
        step_at_cheat_end = track[cheat.e]
        resulting_length = length_up_to_cheat + 2 + (total_steps - step_at_cheat_end)
        steps_saved = total_steps - resulting_length
        if steps_saved >= 100:
            solution += 1
print(solution)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

# for key in cheats.keys():
#     print(f"{key}: {cheats[key]}")

# for key in sorted(result_dict.keys()):
#     print(f"{key}: {len(result_dict[key])}") # {result_dict[key]}")

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
