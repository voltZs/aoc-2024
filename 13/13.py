import time
import math
from enum import Enum

file = open("example.txt", "r")
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
def get_valid_ab_combinations(a, b, prize):
    gcd = math.gcd(a, b)

    combinations = []

    if prize % gcd != 0:
        return combinations

    for a_presses in range(101):
        a_total = a * a_presses
        if a_total > prize:
            continue
        b_target = prize - a_total

        if b_target % b == 0:
            b_presses = int(b_target/b)
            if b_presses > 100:
                continue
            combinations.append((a_presses, b_presses))
    return combinations

def get_valid_game_combinations(game):
    x_combinations = get_valid_ab_combinations(game["a_x"], game["b_x"], game["prize_x"])
    y_combinations = get_valid_ab_combinations(game["a_y"], game["b_y"], game["prize_y"])

    return list(set(x_combinations).intersection(set(y_combinations)))

def cheapest_or_zero(game):
    combinations = get_valid_game_combinations(game)
    if not combinations:
        return 0
    tokens = [(comb[0] * 3) + comb[1] for comb in combinations]
    return min(tokens)

total_1 = 0
for game in games:
    total_1 += cheapest_or_zero(game)
print(total_1)

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")


# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 5))
