import time
file = open("input.txt", "r")
start = time.time()

equations = []

for line in file.readlines():
    split = line.split(": ")
    numbers = [int(x) for x in split[1].split(" ")]
    equations.append((int(split[0]), numbers))

# PART 1
print(equations)

def consume_next_number(current_result, target_result, numbers):
    if len(numbers) == 0:
        # reached end of array
        return current_result == target_result

    if current_result > target_result:
        return False

    current_num = numbers[0]
    remaining_numbers = numbers[1:]

    addition_sum = current_result + current_num
    addition_path_result = consume_next_number(addition_sum, target_result, remaining_numbers)

    multiply_sum = current_result * current_num
    multiply_path_result = consume_next_number(multiply_sum, target_result, remaining_numbers)

    return addition_path_result or multiply_path_result

def check_equation(result, numbers):
    return consume_next_number(numbers[0], result, numbers[1:])

doable_total = 0
for equation in equations:
    is_doable = check_equation(equation[0], equation[1])
    if is_doable:
        doable_total += equation[0]

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
print(doable_total)

# PART 2
def consume_next_number2(current_result, target_result, numbers):
    if len(numbers) == 0:
        # reached end of array
        return current_result == target_result

    if current_result > target_result:
        return False

    concat_result = int(str(current_result) + str(numbers[0]))
    concat_path_result = consume_next_number2(concat_result, target_result, numbers[1:])

    addition_sum = current_result + numbers[0]
    addition_path_result = consume_next_number2(addition_sum, target_result, numbers[1:])

    multiply_sum = current_result * numbers[0]
    multiply_path_result = consume_next_number2(multiply_sum, target_result, numbers[1:])

    return concat_path_result or addition_path_result or multiply_path_result

def check_equation2(result, numbers):
    return consume_next_number2(numbers[0], result, numbers[1:])

doable_2_total = 0
for equation in equations:
    print(equation[0], equation[1])
    is_doable = check_equation2(equation[0], equation[1])
    print(is_doable)
    if is_doable:
        doable_2_total += equation[0]

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
print(doable_2_total)


# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(end - start)
