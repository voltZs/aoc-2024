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
        return hash((1000000 * self.x) + self.y)

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

start_direction = Direction.RIGHT
map, start, goal = import_matrix(file.read())

def number_of_turns(current_direction, target_direction):
    direction = current_direction
    left_turns = 0
    while direction != target_direction:
        match direction:
            case Direction.LEFT:
                direction = Direction.DOWN
            case Direction.DOWN:
                direction = Direction.RIGHT
            case Direction.RIGHT:
                direction = Direction.UP
            case Direction.UP:
                direction = Direction.LEFT
        left_turns += 1

    return min(left_turns, 4 - left_turns)


def number_of_turns_to_position(current_direction, current_position, target_position):
    target_direction = None
    if target_position.x > current_position.x:
        target_direction = Direction.RIGHT
    elif target_position.x < current_position.x:
        target_direction = Direction.LEFT
    elif target_position.y < current_position.y:
        target_direction = Direction.UP
    elif target_position.y > current_position.y:
        target_direction = Direction.DOWN

    return (number_of_turns(current_direction, target_direction), target_direction)

def get_neighbors(current_position):
    neighbors = [
        Position(current_position.x-1, current_position.y),
        Position(current_position.x, current_position.y-1),
        Position(current_position.x, current_position.y+1),
        Position(current_position.x+1, current_position.y)
    ]
    valid = [n for n in neighbors if n.x >= 0 and n.x < len(map[0]) and n.y >= 0 and n.y < len(map)]
    return [n for n in valid if map[n.y][n.x] == space]

def build_path(node, total_path = []):
    if node.parent:
        return [node] + build_path(node.parent, total_path)
    else:
        return [node]

def distance_and_direction(current_position, current_direction, target_position):
    turns, new_direction = number_of_turns_to_position(current_direction, current_position, target_position)
    # print(turns, new_direction)
    return ((turns * 1000) + 1, new_direction)

def print_map():
    for line_index, line in enumerate(map):
        string = []
        for column_index, tile in enumerate(line):
            if tile == wall:
                string.append("#")
            elif Position(column_index, line_index) == start:
                string.append("S")
            elif Position(column_index, line_index) == goal:
                string.append("E")
            else:
                string.append(".")
        print("".join(string))


class TraversalNode:
    def __init__(self, position, direction, cost_so_far, parent):
        self.position = position
        self.direction = direction
        self.cost_so_far = cost_so_far
        self.parent = parent

    def __repr__(self):
        return f"position: {self.position}, direction: {self.direction}, cost_so_far: {self.cost_so_far}, parent: {self.parent is not None}"

    def __lt__(self, other):
        return self.cost_so_far < other.cost_so_far

def a_star():
    open_list = []
    open_list_weights = {}

    heapq.heappush(open_list, TraversalNode(start, start_direction, 0, None))
    open_list_weights[(start, start_direction)] = 0

    while open_list:
        # print("------")
        # print(f"OPEN: {open_list}")
        current = heapq.heappop(open_list)
        if open_list_weights.get((current.position, current.direction)):
            open_list_weights.pop((current.position, current.direction))

        if current.position == goal:
            return build_path(current)

        neighbors = get_neighbors(current.position)
        # print(f"neighbors {neighbors}")
        for neighbor_position in neighbors:
            # print(f"handling neighbor: {neighbor_position} | CURR position: {current.position} direction {current.direction}")
            distance_to_neighbor, new_direction = distance_and_direction(current.position, current.direction, neighbor_position)
            # print(f"new direction {new_direction}")
            cost_so_far = current.cost_so_far + distance_to_neighbor

            existing = open_list_weights.get((neighbor_position, new_direction))
            if existing and existing <= cost_so_far:
                continue

            successor = TraversalNode(neighbor_position, new_direction, cost_so_far, current)
            heapq.heappush(open_list, successor)
            open_list_weights[(neighbor_position, new_direction)] = cost_so_far
    return None

def find_all_paths_of_length(position, previous_position, direction, remaining_length):
    if previous_position is not None and position == previous_position:
        return None
    if remaining_length < 0:
        return None
    if remaining_length == 0 and position == goal:
        return [position]

    neighbors = get_neighbors(position)

    neighbor_paths = [] #arrays and None's
    for neighbor in neighbors:
        distance, new_direction = distance_and_direction(position, direction, neighbor)
        paths = find_all_paths_of_length(neighbor, position, new_direction, remaining_length - distance)
        neighbor_paths.append(paths)

    valid_neighbor_paths = [path for path in neighbor_paths if path is not None and len(path) > 0]
    result = []
    for path in valid_neighbor_paths:
        result.append(position)
        result.extend(path)
    return result

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
print_map()
print(f"start: {start}")
print(f"end: {goal}")
a_best_path_length = a_star()[0].cost_so_far
print(a_best_path_length)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
