import time
import math
from enum import Enum

file = open("input.txt", "r")
start = time.time()

line_type = 0
current_game = {}
games = []
for line in file.readlines():
    match line_type:
        case 0:
            a_moves = [int(x) for x in line.replace("Button A: X+", "").replace(" Y+", "").split(",")]
            current_game["a_x"] = a_moves[0]
            current_game["a_y"] = a_moves[1]
        case 1:
            b_moves = [int(x) for x in line.replace("Button B: X+", "").replace(" Y+", "").split(",")]
            current_game["b_x"] = b_moves[0]
            current_game["b_y"] = b_moves[1]
        case 2:
            prize_coords = [int(x) for x in line.replace("Prize: X=", "").replace(" Y=", "").split(",")]
            current_game["prize_x"] = prize_coords[0]
            current_game["prize_y"] = prize_coords[1]
        case 3:
            games.append(current_game.copy())
            line_type = 0
            current_game = {}
            continue
    line_type += 1

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def combination_if_valid(b_presses, a, b, prize, gcd):
    if prize % gcd != 0:
        return None

    b_total = b * b_presses
    if b_total > prize:
        return None

    a_target = prize - b_total
    if a_target % a == 0:
        a_presses = int(a_target/a)
        return (a_presses, b_presses)
    else:
        return None

def get_cheapest_ab_combination(game):
    a_x = game["a_x"]
    b_x = game["b_x"]
    prize_x = game["prize_x"]
    gcd_x = math.gcd(a_x, b_x)

    a_y = game["a_y"]
    b_y = game["b_y"]
    prize_y = game["prize_y"]
    gcd_y = math.gcd(a_y, b_y)

    # X or Y don't have a GCD - there will be no solution
    if prize_x % gcd_x != 0 or prize_y % gcd_y != 0:
        return None

    # Going from highest possible B presses cause A cost more
    max_x_b_presses = math.ceil(prize_x/b_x)
    max_y_b_presses = math.ceil(prize_y/b_y)
    max_b_presses = min([max_x_b_presses, max_y_b_presses])

    b_presses = max_b_presses
    while b_presses >= 0 :
        x_combination = combination_if_valid(b_presses, a_x, b_x, prize_x, gcd_x)
        y_combination = combination_if_valid(b_presses, a_y, b_y, prize_y, gcd_y)

        if x_combination == None or y_combination == None or x_combination != y_combination:
            b_presses -= 1
            continue
        else:
            return x_combination # can return either, they are the same
    return None

def cheapest_or_zero(game):
    combination = get_cheapest_ab_combination(game)
    if not combination:
        return 0
    return (combination[0] * 3) + combination[1]

total_1 = 0
for game in games:
    total_1 += cheapest_or_zero(game)
print(total_1)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 5))
