import time

file = open("input.txt", "r")
start = time.time()

matrix = []
trailheads = []

for line_index, line in enumerate(file.readlines()):
    matrix.append([])
    for column_index, column in enumerate(line.replace("\n", "")):
        elevation = int(column)
        matrix[line_index].append(elevation)
        if elevation == 0:
            trailheads.append((line_index, column_index))

matrix_width = len(matrix[0])
matrix_height = len(matrix)

# for line in matrix:
#     print(line)

def get_valid_neighbors(position):
    y = position[0][0]
    x = position[0][1]
    position_elevation = position[1]

    left_p = (y, x-1)
    left = None if x == 0 else (left_p, matrix[left_p[0]][left_p[1]])
    # left = (None, (left_p, matrix[left_p[0]][left_p[1]]))[x > 0]

    right_p = (y, x+1)
    right = None if x == matrix_width-1 else (right_p, matrix[right_p[0]][right_p[1]])
    # right = (None, (right_p, matrix[right_p[0]][right_p[1]]))[x < matrix_width-1]

    up_p = (y-1, x)
    up = None if y == 0 else (up_p, matrix[up_p[0]][up_p[1]])
    # up = (None, (up_p, matrix[up_p[0]][up_p[1]]))[y > 0]

    down_p = (y+1, x)
    down = None if y == matrix_height-1 else (down_p, matrix[down_p[0]][down_p[1]])
    # down = (None, (down_p, matrix[down_p[0]][down_p[1]]))[y < matrix_height-1]
    return [x for x in [left, right, up, down] if (x is not None and x[1] == position_elevation + 1)]


print("~~~~~~~~~~RESULT 1~~~~~~~~~~")

def traverse(position):
    if position[1] == 9:
        return [position]

    neighbors = get_valid_neighbors(position)
    if not neighbors:
        return []
    else:
        result = []
        for traverse_result in [traverse(x) for x in neighbors]:
            result += traverse_result
        return result

# total_score = 0
# for trailhead in trailheads:
#     peaks = set()
#     for trail_end in traverse(((trailhead), 0)):
#         peaks.add(trail_end[0])
#     total_score += len(peaks)
#
# print(total_score)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

def copy_2d_list(two_d_list):
    new = []
    for index_x, x in enumerate(two_d_list):
        new.append([])
        for y in x:
            new[index_x].append(y)
    return new

def copy_list(list):
    new = []
    for x in list:
        new.append(x)
    return new

def traverse2(complete, incomplete):
    updated_complete = copy_2d_list(complete)
    updated_incomplete = []

    for trail in incomplete:
        last_step = trail[len(trail)-1]
        if last_step[1] == 9:
            updated_complete.append(copy_list(trail))
        else:
            neighbors = get_valid_neighbors(last_step)
            if not neighbors:
                # no onward paths for this trail, removed from incomplete
                continue
            for neighbor in get_valid_neighbors(last_step):
                updated_incomplete.append(copy_list(trail) + [neighbor])

    if not updated_incomplete:
        return updated_complete

    return traverse2(updated_complete, updated_incomplete)



total_score2 = 0
for trailhead in trailheads:
    rating = len(traverse2([], [[((trailhead), 0)]]))
    total_score2 += rating

print(total_score2)

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 3))
