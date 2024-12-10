import re
input = open("input.txt", "r").read()
valid_inputs = re.findall(r'mul\(\d{1,3},\d{1,3}\)', input)

def multiply(mul_string):
    numbers = re.findall(r'\d{1,3},\d{1,3}', mul_string)[0].split(",")
    return int(numbers[0]) * int(numbers[1])

# PART 1
sum1 = 0
for valid_input in valid_inputs:
    sum1 += multiply(valid_input)


print(sum1)

# PART 2
mul_pattern = r'(mul\(\d{1,3},\d{1,3}\))'
do_pattern = r'(do\(\))'
dont_pattern = r'(don\'t\(\))'
matches = re.findall(do_pattern + '|' + dont_pattern + '|' + mul_pattern, input)

def is_do(match_tuple):
    return not not match_tuple[0]

def is_dont(match_tuple):
    return not not match_tuple[1]

def mul_value(match_tuple):
    return multiply(match_tuple[2])

sum2 = 0
is_addition_enabled = True
for match in matches:
    if is_do(match):
        is_addition_enabled = True
    elif is_dont(match):
        is_addition_enabled = False
    elif is_addition_enabled:
        sum2 += mul_value(match)

print(sum2)
