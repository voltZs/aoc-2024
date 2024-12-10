import itertools
import time

file = open("input.txt", "r")
start = time.time()

matrix = []
antennas = {}
antinondes_set = set()

for row_index, row in enumerate(file.readlines()):
    matrix.append([])
    for column_index, column in enumerate(row.replace("\n", "")):
        matrix[row_index].append(column)

        if column != ".":
            if column not in antennas.keys():
                antennas[column] = []
            antennas[column].append((row_index, column_index))

matrix_height = len(matrix)
matrix_width = len(matrix[0])

def attempt_adding_antinode(antinode):
    is_in_width = antinode[1] < matrix_height and antinode[1] >= 0
    is_in_height = antinode[0] < matrix_height and antinode[0] >= 0
    if is_in_width and is_in_height:
        antinondes_set.add(antinode)
        return True
    else:
        return False

# PART 1
# for antenna_type in antennas.keys():
#     antenna_combinations = list(itertools.combinations(antennas[antenna_type], 2))
#     for combination in antenna_combinations:
#         left_y = combination[0][0]
#         left_x = combination[0][1]
#         right_y = combination[1][0]
#         right_x = combination[1][1]
#         distance_y = right_y-left_y
#         distance_x = right_x-left_x
#
#         left_antinode = (left_y - distance_y, left_x - distance_x)
#         right_antinode = (right_y + distance_y, right_x + distance_x)
#
#         attempt_adding_antinode(left_antinode)
#         attempt_adding_antinode(right_antinode)

# PART 2

def add_antinodes(combination, direction):
    left_y = combination[0][0]
    left_x = combination[0][1]
    right_y = combination[1][0]
    right_x = combination[1][1]
    distance_y = right_y-left_y
    distance_x = right_x-left_x

    increment = 1
    do_continue = True
    while do_continue:
        left_antinode = (left_y + (distance_y*increment*direction), left_x + (distance_x*increment*direction))
        do_continue = attempt_adding_antinode(left_antinode)
        increment += 1

for antenna_type in antennas.keys():
    antenna_combinations = list(itertools.combinations(antennas[antenna_type], 2))
    for combination in antenna_combinations:
        add_antinodes(combination, -1)
        add_antinodes(combination, +1)

for key in antennas.keys():
    for antenna in antennas[key]:
        attempt_adding_antinode(antenna)

# for row_index, row in enumerate(matrix):
#     row_items = []
#     for column_index, column in enumerate(row):
#         if (row_index, column_index) in antinondes_set and column == ".":
#             row_items.append("#")
#         else:
#             row_items.append(column)
#     print("".join(row_items))

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
print(len(antinondes_set))

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(end - start)
