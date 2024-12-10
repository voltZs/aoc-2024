import itertools
import time

file = open("input.txt", "r")
start = time.time()
input = file.read()

def checksum(representation):
    sum = 0
    for index, number in enumerate(representation):
        if number != ".":
            sum += index * int(number)
    return sum


print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def create_representation():
    # representation = ""
    representation = []
    current_id = 0
    for index, block in enumerate(input):
        if index == 0 or index % 2 == 0:
            # representation += "".join([str(current_id) for x in range(int(block))])
            representation.extend([str(current_id) for x in range(int(block))])
            current_id += 1
        else:
            representation.extend(["." for x in range(int(block))])
    return representation

def move_blocks(representation):
    empty_spaces = []
    id_spaces_reversed = []
    updated = []
    for index, block in enumerate(representation):
        if block == ".":
            empty_spaces.append(index)
        else:
            id_spaces_reversed.insert(0, index)

    for index, block in enumerate(representation):
        is_index_valid = id_spaces_reversed[0] >= index
        if block == "." and id_spaces_reversed and is_index_valid:
            updated.append(representation[id_spaces_reversed[0]])
            id_spaces_reversed = id_spaces_reversed[1:]
        elif not is_index_valid:
            updated.append(".")
        else:
            updated.append(block)

    return updated

def solution_1():
    representation = create_representation()
    # print("".join(representation))
    moved = move_blocks(representation)
    # print("".join(moved))
    print(checksum(moved))

# solution_1()

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
def create_representation_2():
    # representation = ""
    representation = []
    current_id = 0
    for index, block in enumerate(input):
        if index == 0 or index % 2 == 0:
            representation.append((int(block), current_id))
            current_id += 1
        else:
            representation.append((int(block), None))
    return representation

def representation_to_text_2(representation):
    string = ""
    for block in representation:
        if block[1] == None:
            string += "".join([ "." for _ in range(block[0])])
        else:
            string += "".join([ str(block[1]) for x in range(block[0])])
    return string

def reversables_to_text(representation, indices):
    string = ""
    for index in indices:
        string += f'i:{index} - {representation[index]}, '
    return string

def move_blocks_2(representation):
    id_files_reversed = []
    updated = []
    for index, file in enumerate(representation):
        updated.append(file)
        if file[1] != None:
            id_files_reversed.insert(0, index)

    id_file_index = id_files_reversed[0]

    while id_file_index:
        id_file = updated[id_file_index]
        id_file_size = id_file[0]

        for index, curr_file in enumerate(updated):
            if index >= id_file_index:
                # not to the left of the location
                break

            if curr_file[1] != None:
                # print("file taken")
                continue

            space = curr_file[0]

            if space < id_file_size:
                continue
            elif space == id_file_size:
                # print(f'Exact space at {index}')
                updated[index] = id_file
                updated[id_file_index] = (id_file_size, None)
                break
            else:
                remaining_space = space - id_file_size
                # print(f'Extra space {remaining_space} at {index}')
                updated[index] = id_file
                updated[id_file_index] = (id_file_size, None)
                updated.insert(index+1, (remaining_space, None))
                #this also pushes the index of everything in id_files_reversed
                for i, num in enumerate(id_files_reversed):
                    if num > index:
                        id_files_reversed[i] = num + 1
                break

        id_files_reversed = id_files_reversed[1:]
        if id_files_reversed:
            id_file_index = id_files_reversed[0]
        else:
            id_file_index = None

    return updated

def checksum_2(representation):
    flattened_representation = []
    for file in representation:
        size = file[0]
        id = file[1]
        if id == None:
            flattened_representation.extend(["." for x in range(size)])
        else:
            flattened_representation.extend([str(id) for x in range(size)])
    return checksum(flattened_representation)

def solution_2():
    representation = create_representation_2()
    # print(representation_to_text_2(representation))
    updated = move_blocks_2(representation)
    # print(moved)
    print(checksum_2(updated))

solution_2()

# Save timestamp
end = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end - start, 3))
