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

print("~~~~~~~~~~RESULT 2~~~~~~~~~~")

def is_part_of_clique(clique, node):
    for c in clique:
        if c not in graph[node]:
            return False
    return True

def expand_clique(clique_so_far, evaluated):
    all_neighbors = []
    for node in clique_so_far:
        all_neighbors += [n for n in graph[node] if n not in evaluated and n not in clique_so_far]
    if not all_neighbors:
        return clique_so_far

    start_size = len(clique_so_far)
    new_clique_so_far = clique_so_far
    for neighbor in all_neighbors:
        if is_part_of_clique(new_clique_so_far, neighbor):
            new_clique_so_far.append(neighbor)
        evaluated.add(neighbor)

    if len(new_clique_so_far) > start_size:
        return expand_clique(new_clique_so_far, evaluated)
    else:
        return clique_so_far


def find_largest_clique():
    queue = list(graph.keys())
    known_cliques = []
    largest_clique = []
    while queue:
        current_node = queue[0]
        evaluated_nodes = [n for c in known_cliques for n in c]

        new_clique = expand_clique([current_node], set(evaluated_nodes))
        known_cliques.append(new_clique)
        if len(new_clique) > len(largest_clique):
            largest_clique = new_clique
        # Assumes all nodes are only part of one clique
        for node in new_clique:
            queue.remove(node)

    return largest_clique

print(",".join(sorted(find_largest_clique())))

# Save timestamp
end_time = time.time()
print("~~~~~~~~~~ RUNTIME ~~~~~~~~~~~~~~")
print(round(end_time - start_time, 5))
