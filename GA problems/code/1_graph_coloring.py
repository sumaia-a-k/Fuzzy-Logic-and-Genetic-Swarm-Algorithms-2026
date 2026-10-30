"""
Problem 1: Graph Coloring

Color the cities on a map with as few colors as possible,
so that two connected cities never have the same color.

Representation: integer, one gene per city (gene = color number 0 to 6)
Fitness:        MINIMIZE  bad_edges * 10 + colors_used
Selection:      tournament (pick 3 different chromosomes, the lowest fitness wins)
Crossover:      two-point (cut both parents at two random points
                and swap the middle part)
Mutation:       random resetting (each gene mutates with probability pm
                and gets a new random color)

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

# The number of players in one tournament
TOURNAMENT_SIZE = 3

# M: how many parents we want. It does not have to be the population size.
NUM_PARENTS = 4

# pc: the chance that a pair of parents does crossover
CROSSOVER_RATE = 0.8

# pm: the chance that one gene mutates. pm must be small.
# 1 / N is a common choice (a convention, not a rule): about one gene
# changes in each child. Other small values, like 0.05, also work.
MUTATION_RATE = 1 / N


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


# ---------- Selection: tournament ----------
def pick_players(population):
    # Pick TOURNAMENT_SIZE different chromosomes at random.
    # random.sample() never takes the same chromosome twice.
    return random.sample(population, TOURNAMENT_SIZE)


def tournament_winner(players):
    # Lower is better, so the player with the smallest fitness wins.
    # key=fitness means "compare the players by their fitness".
    return min(players, key=fitness)


def selection(population, num_parents):
    # Play one tournament for each parent we want
    mating_pool = []
    for _ in range(num_parents):
        players = pick_players(population)
        mating_pool.append(tournament_winner(players))
    return mating_pool


# ---------- Crossover: two-point ----------
def pick_two_cuts():
    # Pick 2 different cut points between gene 1 and gene N.
    # random.sample() takes 2 different numbers, sorted() puts them in order.
    return sorted(random.sample(range(1, N), 2))


def two_point(parent1, parent2, cut1, cut2):
    # Child 1: start and end of parent 1, middle part of parent 2
    child1 = parent1[:cut1] + parent2[cut1:cut2] + parent1[cut2:]
    # Child 2: the opposite
    child2 = parent2[:cut1] + parent1[cut1:cut2] + parent2[cut2:]
    return child1, child2


def crossover(parent1, parent2):
    # Two-point crossover at two random cut points
    cut1, cut2 = pick_two_cuts()
    return two_point(parent1, parent2, cut1, cut2)


def make_children(mating_pool):
    children = []
    # Take the parents two by two: (1st, 2nd), (3rd, 4th), ...
    # range(0, M - 1, 2) gives 0, 2, 4, ... (with an odd M, the last parent has no partner)
    for i in range(0, len(mating_pool) - 1, 2):
        parent1 = mating_pool[i]
        parent2 = mating_pool[i + 1]
        # Do crossover with probability CROSSOVER_RATE
        if random.random() < CROSSOVER_RATE:
            child1, child2 = crossover(parent1, parent2)
        else:
            # No crossover: the children are copies of the parents.
            # .copy() makes a new list with the same genes.
            child1, child2 = parent1.copy(), parent2.copy()
        children += [child1, child2]
    return children


# ---------- Mutation: random resetting ----------
def pick_genes():
    # One random number r for each gene. The gene mutates if r < MUTATION_RATE.
    positions = []
    for i in range(N):
        if random.random() < MUTATION_RATE:
            positions.append(i)
    return positions


def random_resetting(chromosome, positions):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    # Each chosen gene gets a new random color (it can be the same color again)
    for i in positions:
        mutant[i] = random.randint(0, len(colors) - 1)
    return mutant


def mutation(chromosome):
    # Random resetting on the genes that pick_genes() chooses
    return random_resetting(chromosome, pick_genes())


def changed_genes(before, after):
    # The gene numbers (1, 2, ...) where before and after are different
    changed = []
    for i in range(len(before)):
        if before[i] != after[i]:
            changed.append(i + 1)
    return changed


def changed_text(before, after):
    # The changed genes as text, for example "3, 6", or "none"
    changed = changed_genes(before, after)
    if not changed:
        return "none"
    # map(str, ...) turns each number into text, ", ".join() glues them together
    return ", ".join(map(str, changed))


def mutate_children(children):
    # Mutate every child. Most genes stay the same, because pm is small.
    mutants = []
    for child in children:
        mutants.append(mutation(child))
    return mutants


def show_cuts(chromosome, cuts):
    # Write the genes as text, with | at each cut point
    text = ""
    # enumerate() gives the position i together with the gene
    for i, gene in enumerate(chromosome):
        if i in cuts:
            text += "| "
        text += f"{gene} "
    return text


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

# One tournament, step by step
players = pick_players(population)
print(f"\nOne tournament with {TOURNAMENT_SIZE} players:")
for c in players:
    print(f"  {c}  fitness = {fitness(c)}")
winner = tournament_winner(players)
print(f"  The winner is {winner} (the smallest fitness, {fitness(winner)})")

# Choose the mating pool: one tournament for each parent
mating_pool = selection(population, NUM_PARENTS)
print(f"\nMating pool ({NUM_PARENTS} parents):")
for c in mating_pool:
    print(f"  {c}  fitness = {fitness(c)}")

# One crossover, step by step, with the first two parents
parent1, parent2 = mating_pool[0], mating_pool[1]
cut1, cut2 = pick_two_cuts()
child1, child2 = two_point(parent1, parent2, cut1, cut2)
print(f"\nTwo-point crossover, cuts after gene {cut1} and gene {cut2}:")
print(f"  Parent 1: {show_cuts(parent1, [cut1, cut2])}  fitness = {fitness(parent1)}")
print(f"  Parent 2: {show_cuts(parent2, [cut1, cut2])}  fitness = {fitness(parent2)}")
print(f"  Child 1:  {show_cuts(child1, [cut1, cut2])}  fitness = {fitness(child1)}")
print(f"  Child 2:  {show_cuts(child2, [cut1, cut2])}  fitness = {fitness(child2)}")

# Make the children of the whole mating pool
children = make_children(mating_pool)
print(f"\nChildren of the mating pool (crossover rate = {CROSSOVER_RATE}):")
# Children i and i + 1 come from parents i and i + 1.
# A child can be the same as a parent when the pair does no crossover
# (chance 1 - CROSSOVER_RATE), or when both parents have the same genes
# in the part that is swapped.
for i in range(0, len(children), 2):
    print(f"  Pair {i // 2 + 1}")
    print(f"    Parents:  {mating_pool[i]}  {mating_pool[i + 1]}")
    print(f"    Children: {children[i]}  {children[i + 1]}")

# One mutation, step by step, with the first child.
# Here we choose gene 3 and gene 6, like in the lecture. mutation() picks the genes at random.
child = children[0]
mutant = random_resetting(child, [2, 5])
print("\nRandom resetting on gene 3 and gene 6:")
print(f"  Before: {child}  fitness = {fitness(child)}")
print(f"  After:  {mutant}  fitness = {fitness(mutant)}   changed genes: {changed_text(child, mutant)}")

# Mutate all children: each gene mutates with probability pm
mutants = mutate_children(children)
print(f"\nMutation of all children (pm = 1/{N} = {MUTATION_RATE:.2f} per gene):")
# zip() goes over the two lists together
for before, after in zip(children, mutants):
    print(f"  {before} -> {after}   changed genes: {changed_text(before, after):<6}"
          f"  fitness {fitness(before)} -> {fitness(after)}")
