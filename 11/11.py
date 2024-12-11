import time

file = open("input.txt", "r")
start = time.time()

initial_stones = []
for stone in (file.read().split(" ")):
    initial_stones.append(int(stone))

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
print(initial_stones)

def blink(stones):
    new_stones = []

    for stone_num in stones:
        stone_string = str(stone_num)

        if stone_num == 0:
            new_stones.append(1)

        elif len(stone_string) % 2 == 0:
            stone_string_list = list(stone_string)
            half_len = int(len(stone_string)/2)
            new_stones.append(int("".join(stone_string_list[:half_len])))
            new_stones.append(int("".join(stone_string_list[half_len:])))

        else:
            new_stones.append(stone_num * 2024)
    return new_stones

current_stones = initial_stones
for x in range(25):
    current_stones = blink(current_stones)
print(len(current_stones))

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

stone_index = {}

def blink_recursive(iteration, stone):
    if iteration == 75:
        return 1
    if stone_index.get(iteration) is not None:
        if stone_index[iteration].get(stone) is not None:
            return stone_index[iteration][stone]

    result = 0
    for blink_result in [blink_recursive(iteration+1, x) for x in blink([stone])]:
        result += blink_result
    stone_index_for_interation = {}
    if stone_index.get(iteration) is not None:
        stone_index_for_interation = stone_index[iteration]

    stone_index_for_interation[stone] = result
    stone_index[iteration] = stone_index_for_interation
    return result

result = 0
for blink_result in [blink_recursive(0, x) for x in initial_stones]:
    result += blink_result
print(result)
# print(stone_index)

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 3))
