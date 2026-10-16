"""
Problem 1: Graph Coloring

Color the cities on a map with as few colors as possible,
so that two connected cities never have the same color.

Representation: integer, one gene per city (gene = color number 0 to 6)
Fitness:        MINIMIZE  bad_edges * 10 + colors_used

Run:  python 1_graph_coloring.py
"""

import random

# The map: each node is a city, and each edge connects two cities
nodes = [1, 2, 3, 4, 5, 6, 7]
edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 7), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
         (3, 5), (3, 6), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7)]

# At most one color per city
colors = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Pink"]

# One gene per city, so the chromosome has 7 genes
N = len(nodes)

# The gene number of each city, for example city 1 -> gene 0
gene_of = {node: i for i, node in enumerate(nodes)}

# One bad edge costs more than all 7 colors together
PENALTY = 10


# ---------- The map ----------
def neighbors(node):
    print("node is ",node)
    # Find all cities that have an edge to this city
    result = []
    for a, b in edges:
        if a == node:
            result.append(b)
        elif b == node:
            result.append(a)
    return sorted(result)


def print_map():
    # Show how the cities are connected
    print("The map (how the cities are connected):")
    for node in nodes:
        print(f"  City {node} -> {neighbors(node)}")


def print_colors():
    # Show the colors and the gene value of each one
    print("The colors we can use (gene value = color):")
    for value, name in enumerate(colors):
        print(f"  {value} = {name}")


# ---------- Representation ----------
def random_chromosome():
    # Give every city a random color number from 0 to 6
    return [random.randint(0, len(colors) - 1) for _ in range(N)]


def decode(chromosome):
    # Print the color name of each city
    for node in nodes:
        print(f"  City {node}: {colors[chromosome[gene_of[node]]]}")


# ---------- Fitness (lower is better) ----------
def count_bad_edges(chromosome):
    # Count the edges that join two cities of the same color
    bad_edges = 0
    for a, b in edges:
        if chromosome[gene_of[a]] == chromosome[gene_of[b]]:
            bad_edges += 1
    return bad_edges


def count_colors(chromosome):
    # A set keeps each color only once
    return len(set(chromosome))


def fitness(chromosome):
    # No bad edges is a must, few colors is a wish
    return count_bad_edges(chromosome) * PENALTY + count_colors(chromosome)


# ---------- Try it ----------
print_map()
print()
print_colors()

# Use the same random numbers on every run
random.seed(1)

# Make a small population of 6 random chromosomes
population = [random_chromosome() for _ in range(6)]

print("\nPopulation:")
for c in population:
    print(f"  {c}  bad edges = {count_bad_edges(c)}  colors = {count_colors(c)}"
          f"  fitness = {fitness(c)}")

# Lower is better, so the best chromosome has the smallest fitness
best = min(population, key=fitness)
print(f"\nThe best coloring in this population (fitness = {fitness(best)}):")
decode(best)
