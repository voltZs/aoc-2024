import time
from enum import Enum
import itertools

file = open("input.txt", "r")
start_time = time.time()

class CompGroup():
    def __init__(self, comps):
        self.comps = comps

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        return sorted(self.comps) == sorted(other.comps)

    def __hash__(self):
        return hash(f"{'_'.join(sorted(self.comps))}")


pairs = [ps.split("-") for ps in file.read().split("\n")]
connections = [(pa[0], pa[1]) for pa in pairs]
graph = {}

for connection in connections:
    comp1 = connection[0]
    comp2 = connection[1]

    def add_to_graph(a, b):
        existing = graph.get(a)
        if existing:
            existing.append(b)
        else:
            graph[a] = [b]

    add_to_graph(comp1, comp2)
    add_to_graph(comp2, comp1)

print(len(graph))

def groups_for_comp(comp):
    groups = set()
    neighbors = set(graph[comp])

    for neighbor in neighbors:
        neighbor_neighbors = set(graph[neighbor])
        intersecting_neighbors = neighbor_neighbors.intersection(neighbors)
        for mutual_neighbor in intersecting_neighbors:
            groups.add(CompGroup([comp, neighbor, mutual_neighbor]))
    return groups

print("~~~~~~~~~~RESULT 1~~~~~~~~~~")
def find_groups():
    computers_with_t = [comp for comp in graph.keys() if comp[:1] == "t"]

    groups = set()
    for comp in computers_with_t:
        groups = groups.union(groups_for_comp(comp))
    return groups

print(len(find_groups()))


# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
