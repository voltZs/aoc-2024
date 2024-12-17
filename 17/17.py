import time
from enum import Enum
import math
import itertools

file = open("input.txt", "r")
start_time = time.time()

def parse_input(input):
    registers_str, program_str = input.split("\n\n")
    registers = [int(line.split(" ")[2]) for line in registers_str.split("\n")]
    program = [int(x) for x in program_str.split(" ")[1].split(",")]
    return (registers, program)

input = parse_input(file.read())

class Instruction(Enum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bvd = 6
    cdv = 7

class Register:
    def __init__(self, value):
        self.value = value


def combo_operand(opcode, a, b, c):
    if opcode >= 0 and opcode <= 3:
        return opcode
    elif opcode == 4:
        return a
    elif opcode == 5:
        return b
    elif opcode == 6:
        return c
    else:
        # should never happen
        print("combo operand was 7!!!!!!!!!!!!!")
        return None

def bitwise_xor(a, b):
    a_binary = list(f"{a:b}")
    b_binary = list(f"{b:b}")
    binary_len = max(len(a_binary), len(b_binary))

    a_binary = list(itertools.repeat("0", binary_len-len(a_binary))) + a_binary
    b_binary = list(itertools.repeat("0", binary_len-len(b_binary))) + b_binary

    return int("".join(["1" if a_binary[i] != b_binary[i] else "0" for i in range(binary_len)]), 2)


def handle_instruction(instruction_opcode, operand_opcode, pointer, reg_a, reg_b, reg_c):
    instruction = Instruction(instruction_opcode)

    def combo_value():
        return combo_operand(operand_opcode, reg_a.value, reg_b.value, reg_c.value)

    new_pointer = pointer + 2
    output = None

    match instruction:
        case Instruction.adv:
            reg_a.value = int(reg_a.value / math.pow(2, combo_value()))
        case Instruction.bxl:
            reg_b.value = bitwise_xor(reg_b.value, operand_opcode)
        case Instruction.bst:
            reg_b.value = combo_value() % 8
        case Instruction.jnz:
            if reg_a.value != 0:
                new_pointer = operand_opcode
        case Instruction.bxc:
            reg_b.value = bitwise_xor(reg_b.value, reg_c.value)
        case Instruction.out:
             output = combo_value() % 8
        case Instruction.bvd:
            reg_b.value = int(reg_a.value / math.pow(2, combo_value()))
        case Instruction.cdv:
            reg_c.value = int(reg_a.value / math.pow(2, combo_value()))

    return (new_pointer, output)


print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def run_program(register_values, program):
    reg_a = Register(register_values[0])
    reg_b = Register(register_values[1])
    reg_c = Register(register_values[2])

    complete_output = []
    pointer_index = 0
    while pointer_index < len(program):
        outcome = handle_instruction(program[pointer_index], program[pointer_index+1], pointer_index, reg_a, reg_b, reg_c)
        pointer_index = outcome[0]

        if outcome[1] is not None:
            complete_output.append(outcome[1])
    return complete_output

print(",".join([str(x) for x in run_program(input[0], input[1])]))

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")
attempts = [(1, 0)]
valid_values = []
for i, a in attempts:
    for a in range(a, a+8):
        program = input[1]
        if run_program([a, 0, 0], program) == program[-i:]:
            attempts += [(i+1, a*8)]
            if i == len(program):
                valid_values.append(a)

print(valid_values[0])

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
