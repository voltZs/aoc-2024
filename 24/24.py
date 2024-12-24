import time
from enum import Enum
import math
import itertools

file = open("input.txt", "r")
start_time = time.time()


wires_input, conn_input = [i.split("\n") for i in file.read().split("\n\n")]

def create_wire_values():
    wire_values = {}
    for wire_str in wires_input:
        name, value = wire_str.split(": ")
        wire_values[name] = int(value)
    return wire_values

z_wires = 0
for conn_str in conn_input:
    output_wire = conn_str.split(" -> ")[1]
    if output_wire.startswith("z"):
        significance = int(output_wire[1:])
        z_wires = max(z_wires, significance)

def create_graph():
    x_wires = 0
    y_wires = 0
    z_wires = 0
    graph = {}
    for conn_str in conn_input:
        inputs, output_wire = conn_str.split(" -> ")
        wire1, gate, wire2 = inputs.split(" ")
        graph[output_wire] = (wire1, wire2, gate)
    return graph

def resolve_gate(gate, w_1, w_2):
    match gate:
        case "AND":
            return int(w_1 and w_2)
        case "XOR":
            return int(w_1 != w_2)
        case "OR":
            return int(w_1 or w_2)

def backtrack_wire(wire_name, graph, wire_values):
    inputs = graph[wire_name]
    input_1 = inputs[0]
    input_2 = inputs[1]
    input_gate = inputs[2]
    input_1_value = wire_values.get(input_1)
    input_2_value = wire_values.get(input_2)

    if input_1_value is None:
        input_1_value = backtrack_wire(input_1, graph, wire_values)

    if input_2_value is None:
        input_2_value = backtrack_wire(input_2, graph, wire_values)

    output_value = resolve_gate(input_gate, input_1_value, input_2_value)
    wire_values[wire_name] = output_value
    return output_value

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def solution_1():
    result = 0
    graph = create_graph()
    wire_values = create_wire_values()
    for z_index in range(z_wires+1):
        z_name = f"z{str(z_index).zfill(2)}"
        z_value = backtrack_wire(z_name, graph, wire_values)
        result += int(z_value * math.pow(2, z_index))
    return result

print(solution_1())

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")


# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
