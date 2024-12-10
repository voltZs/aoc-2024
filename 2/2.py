file = open("input.txt", "r")
reports = []
for line in file.readlines():
    reports.append([int(x) for x in line.split(" ")])

# PART 1
safe_count = 0
for report in reports:
    is_safe_increase = True
    is_safe_decrease = True

    for index, level in enumerate(report):
        if index == 0:
            continue
        if is_safe_increase:
            min = report[index-1]+1
            max = report[index-1]+3
            if level >= min and level <= max:
                is_safe_increase = True
                is_safe_decrease = False
            else:
                is_safe_increase = False
        if is_safe_decrease:
            min = report[index-1]-1
            max = report[index-1]-3
            if level <= min and level >= max:
                is_safe_decrease = True
                is_safe_increase = False
            else:
                is_safe_decrease = False
        # print(f'{report[index-1]} -> {level} increase {is_safe_increase} decrease {is_safe_decrease}')

    if is_safe_increase or is_safe_decrease:
        safe_count += 1

print(safe_count)

# PART 2

def evaluate_report(report, isDampened):
    is_safe_increase = True
    is_safe_decrease = True

    for index, level in enumerate(report):
        if index == 0:
            continue
        if is_safe_increase:
            min = report[index-1]+1
            max = report[index-1]+3
            if level >= min and level <= max:
                is_safe_increase = True
                is_safe_decrease = False
            else:
                is_safe_increase = False
        if is_safe_decrease:
            min = report[index-1]-1
            max = report[index-1]-3
            if level <= min and level >= max:
                is_safe_decrease = True
                is_safe_increase = False
            else:
                is_safe_decrease = False

    if is_safe_increase or is_safe_decrease:
        return True
    elif not isDampened:
        any_removal_safe = False
        for index, level in enumerate(report):
            removed_at_index = report[:index] + report[index+1:]
            if not any_removal_safe:
                any_removal_safe = evaluate_report(removed_at_index, True)
        return any_removal_safe
    else:
        return False

safe_count_p2 = 0
for report in reports:
    if evaluate_report(report, False):
        safe_count_p2 += 1

print(safe_count_p2)
