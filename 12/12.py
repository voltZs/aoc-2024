import time
from enum import Enum
from itertools import groupby
from operator import itemgetter

file = open("input.txt", "r")
start = time.time()

matrix = []
for line_index, line in enumerate(file.readlines()):
    matrix.append([])
    for column in line.replace("\n", ""):
        matrix[line_index].append(column)

matrix_width = len(matrix[0])
matrix_height = len(matrix)

def get_valid_neighbors(position, dict_check):
    plant = matrix[position[0]][position[1]]
    x = position[1]
    y = position[0]

    left = None if x == 0 else (y, x-1)
    right = None if x == matrix_width-1 else (y, x+1)
    up = None if y == 0 else (y-1, x)
    down = None if y == matrix_height-1 else (y+1, x)

    return [x for x in [left, right, up, down] if (x is not None and matrix[x[0]][x[1]] == plant and dict_check.get(x) is None)]

def draw_plot(plot):
    for line_index, line in enumerate(matrix):
        str_array = []
        for column_index, column in enumerate(line):
            if (line_index, column_index) in plot:
                str_array.append(matrix[line_index][column_index])
            else:
                str_array.append(" ")
        print("".join(str_array))

def mark_plot(position, id, plots, plots_inverse):
    plots_inverse[position] = id
    if plots.get(id) is None:
        plots[id] = set()
    plots[id].add(position)

def expand_plot(position, id, plots, plots_inverse):
    neighbors = get_valid_neighbors(position, plots_inverse)
    if not neighbors:
        return [position]
    else:
        result = []
        for plot in neighbors:
            mark_plot(plot, id, plots, plots_inverse)
            result += expand_plot(plot, id, plots, plots_inverse)
        return result

current_id = 1
plot_dict = {}
plot_dict_inverse = {}
for line_index, line in enumerate(matrix):
    for column_index, column in enumerate(line):
        position = (line_index, column_index)
        id = current_id
        if plot_dict_inverse.get(position) is None:
            mark_plot(position, id, plot_dict, plot_dict_inverse)
        expanded = expand_plot(position, id, plot_dict, plot_dict_inverse)
        if expanded:
            current_id += 1

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def get_region_price(region_id, plots, plots_inverse):
    region = plots[region_id]
    area = len(region)
    perimeter = 0
    for plot in region:
        x = plot[1]
        y = plot[0]

        left_p = (y, x-1)
        left = 1 if x == 0 else (plots_inverse[left_p] != region_id)
        right_p = (y, x+1)
        right = 1 if x == matrix_width-1 else (plots_inverse[right_p] != region_id)
        up_p = (y-1, x)
        up = 1 if y == 0 else (plots_inverse[up_p] != region_id)
        down_p = (y+1, x)
        down = 1 if y == matrix_height-1 else (plots_inverse[down_p] != region_id)

        perimeter += left + right + up + down

    example = list(region)[0]
    return area * perimeter

total_price = 0
for key in plot_dict.keys():
    # draw_plot(plot_dict[key])
    total_price += get_region_price(key, plot_dict, plot_dict_inverse)
print(f'total price: {total_price}')

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
class Edge(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

def get_sides(edges, target_edge):
    matching_edges = [x[1] for x in edges if x[0] == target_edge]
    is_axis_x = 1 if target_edge == Edge.RIGHT or target_edge == Edge.LEFT else 0

    # create groups with matching X/Y offsets
    sorted_x_edges = sorted(matching_edges, key = lambda edge: edge[is_axis_x])
    matching_x_offset_groups = []
    for y, matches in groupby(sorted_x_edges, lambda edge: edge[is_axis_x]):
        group = []
        for match in matches:
            group.append(match)
        matching_x_offset_groups.append(group)

    # append groups with consecutive Y/X offsets as "sides"
    sides = []
    for matching_x_offset_group in matching_x_offset_groups:
        sorted_y_edges = sorted(matching_x_offset_group, key = lambda edge: edge[not is_axis_x])
        for k, g in groupby(enumerate(sorted_y_edges), lambda e: e[0] - e[1][not is_axis_x]):
            consecutive_y_group = (map(itemgetter(1),g))
            consecutive_y_group = list(consecutive_y_group)
            sides.append(consecutive_y_group)
    return sides

def get_region_price2(region_id, plots, plots_inverse):
    region = plots[region_id]
    area = len(region)
    sides = 1

    edges = []
    for plot in region:
        x = plot[1]
        y = plot[0]

        left_p = (y, x-1)
        left = (Edge.LEFT, plot) if x == 0 else ((Edge.LEFT, plot) if plots_inverse[left_p] != region_id else None)
        right_p = (y, x+1)
        right = (Edge.RIGHT, plot) if x == matrix_width-1 else ((Edge.RIGHT, plot) if plots_inverse[right_p] != region_id else None)
        up_p = (y-1, x)
        up = (Edge.TOP, plot) if y == 0 else ((Edge.TOP, plot) if plots_inverse[up_p] != region_id else None)
        down_p = (y+1, x)
        down = (Edge.BOTTOM, plot) if y == matrix_height-1 else ((Edge.BOTTOM, plot) if plots_inverse[down_p] != region_id else None)

        edges += [x for x in [left, right, up, down] if x is not None]

    sides = get_sides(edges, Edge.TOP) + get_sides(edges, Edge.BOTTOM) + get_sides(edges, Edge.LEFT) + get_sides(edges, Edge.RIGHT)
    example = list(region)[0]
    return area * len(sides)

total_price2 = 0
for key in plot_dict.keys():
    # draw_plot(plot_dict[key])
    total_price2 += get_region_price2(key, plot_dict, plot_dict_inverse)
print(f'total price: {total_price2}')

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 3))
