import time
import math

file = open("input.txt", "r")
start = time.time()

robots = []

# example
# space_width = 11
# space_height = 7
# inout
space_width = 101
space_height = 103

class Robot:
    def __init__(self, position_x, positon_y, velocity_x, velocity_y):
        self.p_x = position_x
        self.p_y = positon_y
        self.v_x = velocity_x
        self.v_y = velocity_y

    def move(self, seconds):
        final_x = self.p_x + (self.v_x * seconds)
        final_y = self.p_y + (self.v_y * seconds)

        if final_x < 0:
            mod = (final_x % -space_width)
            self.p_x = space_width + mod if mod != 0 else 0
        else:
            self.p_x = final_x % space_width

        if final_y < 0:
            mod = (final_y % -space_height)
            self.p_y = space_height + mod if mod != 0 else 0
        else:
            self.p_y = final_y % space_height

for line in file.readlines():
    p_x, p_y, v_x, v_y = [int(a) for a in line.replace("p=", "").replace("\n", "").replace(" v=", ",").split(",")]
    robots.append(Robot(p_x, p_y, v_x, v_y))

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
# quadrants = [0, 0, 0, 0]
#
# for robot in robots:
#     robot.move(100)
#     # print(robot.__dict__)
#     is_left = robot.p_x < (space_width - 1 ) / 2
#     is_right = robot.p_x > (space_width - 1 ) / 2
#     is_top = robot.p_y < (space_height - 1 ) / 2
#     is_bottom = robot.p_y > (space_height - 1 ) / 2
#
#     if (is_left and is_top):
#         quadrants[0] += 1
#     if (is_right and is_top):
#         quadrants[1] += 1
#     if (is_left and is_bottom):
#         quadrants[2] += 1
#     if (is_right and is_bottom):
#         quadrants[3] += 1
#
# print(f"Safety factor: {quadrants[0]*quadrants[1]*quadrants[2]*quadrants[3]}")

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

sleeps = 1
while True:
    matrix = []
    for y in range(space_height):
        line = []
        for x in range(space_width):
            line.append(".")
        matrix.append(line)

    for robot in robots:
        robot.move(1)

        matrix_value = matrix[robot.p_y][robot.p_x]
        if matrix_value == ".":
            matrix[robot.p_y][robot.p_x] = "1"
        else:
            matrix[robot.p_y][robot.p_x] = str(int(matrix_value) + 1)
    print(f"")
    print(f"")
    print(f"--------------- SLEEPS: {sleeps} ----------------")
    for line in matrix:
        print("".join(line))
    time.sleep(0.01)
    sleeps+= 1

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 5))
