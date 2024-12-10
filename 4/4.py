file = open("input.txt", "r")
matrix = []

for line in file.readlines():
    matrix.append(line.replace("\n", ""))

num_columns = len(matrix[0])
num_rows = len(matrix)

# PART 1
horizontal = []
vertical = []
diagonal_left = []
diagonal_left2 = []
diagonal_right = []
diagonal_right2 = []

# Horizontal
for row_index in range(num_rows):
    horizontal.append([])
    for column_index in range(num_columns):
        horizontal[row_index].append(matrix[row_index][column_index])
        # horizontal.append(matrix[row_index][column_index])

# Vertical
for column_index in range(num_columns):
    vertical.append([])
    for row_index in range(num_rows):
        vertical[column_index].append(matrix[row_index][column_index])
        # vertical.append(matrix[row_index][column_index])

# Diagonal left
for column_index in range(num_columns):
    diagonal_left.append([])
    for row_index in range(column_index+1):
        diagonal_left[column_index].append(matrix[row_index][column_index-row_index])

for row_index in range(num_rows):
    if row_index == 0:
        continue
    diagonal_left2.append([])
    for column_index in reversed(range(row_index, num_columns)):
        diagonal_left2[row_index-1].append(matrix[row_index+(num_columns-column_index-1)][column_index])

#  Diagonal right

for column_index in reversed(range(num_columns)):
    diagonal_right.append([])
    for row_index in range((num_columns - column_index)):
        diagonal_right[num_columns-column_index-1].append(matrix[row_index][column_index+row_index])

for row_index in range(num_rows):
    if row_index == 0:
        continue
    diagonal_right2.append([])
    for column_index in range(num_columns - row_index):
        # print(f'[{row_index+column_index}][{column_index}]')
        diagonal_right2[row_index-1].append(matrix[row_index+column_index][column_index])

def count_xmas(matrix):
    count = 0
    for line in matrix:
        line_string = "".join(line)
        count += line_string.count("XMAS") + line_string.count("SAMX")
    return count

xmax_count = 0
xmax_count += count_xmas(horizontal)
xmax_count += count_xmas(vertical)
xmax_count += count_xmas(diagonal_left)
xmax_count += count_xmas(diagonal_left2)
xmax_count += count_xmas(diagonal_right)
xmax_count += count_xmas(diagonal_right2)
print(xmax_count)

# PART 2
def get_block(row: int, column: int):
    blank = [["", "", ""], ["", "", ""], ["", "", ""]]
    columns = len(matrix[0])
    rows = len(matrix)
    if (column+3 > columns) or (row+3 > rows):
        return blank
    block = [[],[],[]]
    for row_index in range(3):
        for column_index in range(3):
            char = matrix[row+row_index][column+column_index]
            block[row_index].append(char)
    return block

def is_block_xmax(block):
    diagonal1 = block[0][0] + block[1][1] + block[2][2]
    diagonal1_string = "".join(diagonal1)
    diagonal2 = block[2][0] + block[1][1] + block[0][2]
    diagonal2_string = "".join(diagonal2)
    return (diagonal1_string == "MAS" or diagonal1_string == "SAM" ) and (diagonal2_string == "MAS" or diagonal2_string == "SAM" )

mas_count = 0
for row_index in range(num_rows):
    for column_index in range(num_columns):
        if is_block_xmax(get_block(row_index, column_index)):
            mas_count += 1
print(mas_count)
