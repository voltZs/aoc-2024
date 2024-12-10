import math
import functools

file = open("input.txt", "r").read()
rules = []
for line in file.split("\n\n")[0].split("\n"):
    nums = line.split("|")
    rules.append((int(nums[0]), int(nums[1])))

updates = []
for line in file.split("\n\n")[1].split("\n"):
    updates.append([int(x) for x in line.split(",")])

# PART 1
def middle_number_or_none(update):
    middle_num_index = math.ceil(len(update)/2)-1
    middle_num = None

    applicable_rules = []
    for index, page in enumerate(update):
        if index == middle_num_index:
            middle_num = page
        for rule in rules:
            if rule[0] == page and rule[1] in update:
                applicable_rules.append(rule)

    is_correct = True
    for rule in applicable_rules:
        target_index = update.index(rule[0])
        later_index = update.index(rule[1])
        if later_index < target_index:
            is_correct = False
            break

    if is_correct:
        return middle_num
    else:
        return None

middles_sum = 0
for update in updates:
    middle = middle_number_or_none(update)
    if middle is not None:
        middles_sum += middle

# print(middles_sum)

# PART 2
def update_cmp(page1, page2):
    for rule in rules:
        if rule[0] == page1 and rule[1] == page2:
            return -1
        elif rule[0] == page2 and rule[1] == page1:
            return 1
        else:
            continue
    return 0

def incorrect_middles(update):
    applicable_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            applicable_rules.append(rule)

    is_correct = True
    for rule in applicable_rules:
        target_index = update.index(rule[0])
        later_index = update.index(rule[1])
        if later_index < target_index:
            is_correct = False
            break
    if is_correct:
        return None

    middle_num_index = math.ceil(len(update)/2)-1
    corrected = sorted(update, key=functools.cmp_to_key(update_cmp))
    return corrected[middle_num_index]

corrected_middles_sum = 0

for update in updates:
    middle = incorrect_middles(update)
    if middle is not None:
        corrected_middles_sum += middle

print(corrected_middles_sum)
