file = open("input.txt", "r")
locationsLeft = []
locationsRight = []
for line in file.readlines():
    pair = line.split("   ")
    locationsLeft.append(int(pair[0]))
    locationsRight.append(int(pair[1]))

#  PART 1:
sortedLeft = sorted(locationsLeft)
sortedRight = sorted(locationsRight)

distance = 0

def absolute_distance(left, right):
    if left < right:
        return abs(right - left)
    else:
        return abs(left - right)

for index, left in enumerate(sortedLeft):
    distance += absolute_distance(left, sortedRight[index])

print("distance:")
print(distance)

# PART 2
similarity = 0
for left in locationsLeft:
    appearances = 0
    for right in locationsRight:
        if left == right:
            appearances += 1
    similarity += left * appearances

print("similarity:")
print(similarity)
