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

def direction_to_target(current, target):
    if target.x > current.x:
        target_direction = Direction.RIGHT
    elif target.x < current.x:
        target_direction = Direction.LEFT
    elif target.y < current.y:
        target_direction = Direction.UP
    elif target.y > current.y:
        target_direction = Direction.DOWN
    return target_direction

def number_of_turns_to_position(current_direction, current_position, target_position):
    target_direction = direction_to_target(current_position, target_position)
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

def print_map(override_marks = set()):
    for line_index, line in enumerate(map):
        string = []
        for column_index, tile in enumerate(line):
            if tile == wall:
                string.append("#")
            elif Position(column_index, line_index) in override_marks:
                string.append("O")
            elif Position(column_index, line_index) == start:
                string.append("S")
            elif Position(column_index, line_index) == goal:
                string.append("E")
            else:
                string.append(".")
        print("".join(string))

def create_node_id(position, direction):
    return f"{position.x}-{position.y}-{direction}"

def create_weighted_graph():
    graph = {}
    for line_index, line in enumerate(map):
        for column_index, tile in enumerate(line):
            if tile == wall:
                continue
            position = Position(column_index, line_index)
            neighbors = get_neighbors(position)
            arrival_directions = [direction_to_target(n, position) for n in neighbors]

            if Position(column_index, line_index) == start:
                arrival_directions.append(Direction.RIGHT)

            for arrival_direction in arrival_directions:
                def neighbor_tuple(neighbor_position):
                    weight, direction = distance_and_direction(position, arrival_direction, neighbor_position)
                    neighbor_id = create_node_id(neighbor_position, direction)
                    return (neighbor_id, weight)

                node_id = create_node_id(position, arrival_direction)
                graph[node_id] = [neighbor_tuple(n) for n in neighbors]
    return graph

def dijkstra():
    graph = create_weighted_graph()

    source = create_node_id(start, start_direction)

    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    came_from = {node: [] for node in graph}
    queue = [(0, source)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # Skip if we've already found a better path
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # Update if a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                came_from[neighbor] = [current_node]
                heapq.heappush(queue, (distance, neighbor))

            elif distance == distances[neighbor]:
                came_from[neighbor].append(current_node)

    return distances, came_from

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
dijkstra = dijkstra()
goal_id = create_node_id(goal, Direction.UP).replace(f"{Direction.UP}", "")
goal_distances_key_value = [(k, dijkstra[0][k]) for k in dijkstra[0].keys() if goal_id in k]
solution_key_value = min(goal_distances_key_value, key = lambda kv: kv[1])
print(solution_key_value)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
def id_to_position(id):
    id_arr = id.split("-")
    return Position(int(id_arr[0]), int(id_arr[1]))

def dijkstra_came_from_tree(came_from, target):
    children = came_from[target]
    if len(children) == 0:
        return None
    prev = [x for x in [dijkstra_came_from_tree(came_from, child) for child in children] if x is not None]
    return {"pos": id_to_position(target), "prev": prev}

def add_tree_positions(tree, set):
    set.add(tree["pos"])
    for branch in tree.get("prev", []):
        add_tree_positions(branch, set)

tree = dijkstra_came_from_tree(dijkstra[1], solution_key_value[0])
all_positions = set()
add_tree_positions(dijkstra_came_from_tree(dijkstra[1], solution_key_value[0]), all_positions)
# print_map(all_positions)
print(len(all_positions)+1)

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
