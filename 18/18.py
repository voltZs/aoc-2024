import time
from enum import Enum
import heapq

file = open("input.txt", "r")
start_time = time.time()

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"{self.x}-{self.y}")

input_size_string, input_bytes_string = file.read().split("\n\n")

matrix_width, matrix_height = [int(s) for s in input_size_string.split("x")]
byte_array = [Position(int(p[0]), int(p[1])) for p in [str.split(",") for str in input_bytes_string.split("\n")]]

healthy = 0
corrupted = 1

def simulate_matrix(corrupted_positions):
    matrix = []
    for line_index, line in enumerate(range(matrix_height)):
        matrix.append([])
        for column_index, space in enumerate(range(matrix_width)):
            if Position(column_index, line_index) in corrupted_positions:
                matrix[line_index].append(corrupted)
            else:
                matrix[line_index].append(healthy)
    return (matrix)

def print_matrix(matrix, path):
    for line_index, line in enumerate(matrix):
        line_arr = []
        for column_index, column in enumerate(line):
            if Position(column_index, line_index) in path:
                line_arr.append("O")
            elif matrix[line_index][column_index] == corrupted:
                line_arr.append("#")
            else:
                line_arr.append(".")
        print("".join(line_arr))

def get_neighbors(current_position, matrix):
    neighbors = [
        Position(current_position.x-1, current_position.y),
        Position(current_position.x, current_position.y-1),
        Position(current_position.x, current_position.y+1),
        Position(current_position.x+1, current_position.y)
    ]
    valid = [n for n in neighbors if n.x >= 0 and n.x < len(matrix[0]) and n.y >= 0 and n.y < len(matrix)]
    return [n for n in valid if matrix[n.y][n.x] == healthy]

def build_path(node, total_path = []):
    if node.parent:
        return [node] + build_path(node.parent, total_path)
    else:
        return [node]

class TraversalNode:
    def __init__(self, position, cost_so_far, total_estimate, parent):
        self.position = position
        self.cost_so_far = cost_so_far
        self.total_estimate = total_estimate
        self.parent = parent

    def __repr__(self):
        return f"position: {self.position}, cost_so_far: {self.cost_so_far}, parent: {self.parent is not None}"

    def __lt__(self, other):
        return self.total_estimate < other.total_estimate

def heuristic(position, goal):
    return abs(goal.x-position.x) + abs(goal.y-position.y)

def a_star(matrix):
    open_list = []
    open_list_weights = {}
    goal = Position(matrix_width-1, matrix_height-1)

    start = Position(0, 0)
    heapq.heappush(open_list, TraversalNode(start, 0, heuristic(start, goal), None))
    open_list_weights[start] = 0

    while open_list:
        current = heapq.heappop(open_list)
        # if open_list_weights.get(current.position):
        #     open_list_weights.pop(current.position)

        if current.position == goal:
            return build_path(current)

        neighbors = get_neighbors(current.position, matrix)
        for neighbor_position in neighbors:
            distance_to_neighbor = 1
            cost_so_far = current.cost_so_far + distance_to_neighbor
            total_estimate = cost_so_far + heuristic(neighbor_position, goal)

            existing = open_list_weights.get(neighbor_position)
            if existing and existing <= total_estimate:
                continue

            successor = TraversalNode(neighbor_position, cost_so_far, total_estimate, current)
            heapq.heappush(open_list, successor)
            open_list_weights[neighbor_position] = total_estimate
    return None

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
initial_bytes = 1024

def solution():
    corrupted_positions = byte_array[:initial_bytes]
    matrix = simulate_matrix(corrupted_positions)

    best_path_length = a_star(matrix)[0].cost_so_far
    print(best_path_length)
    # print_matrix(matrix, path_positions)
    
solution()

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

def solution_2():
    for bytes_fallen in range(initial_bytes, len(byte_array)):
        print(f"Bytes fallen: {bytes_fallen}")
        corrupted_positions = byte_array[:bytes_fallen]
        matrix = simulate_matrix(corrupted_positions)

        if a_star(matrix) is None:
            print(corrupted_positions[-1])
            break

solution_2()

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
