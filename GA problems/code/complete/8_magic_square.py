"""
Problem 8: The Magic Square (the full genetic algorithm)

Put the numbers 1 to 9 in a 3 x 3 square, each number once,
so that every row, every column and both diagonals add up to 15.

    2 7 6
    9 5 1     <- an example: 2+7+6 = 15, 2+9+4 = 15, 2+5+8 = 15, ...
    4 3 8

Representation: permutation, one gene per cell (cells 0 to 8, row by row),
                gene = the number in this cell (1 to 9, each number once)
Fitness:        MINIMIZE  the error: for each of the 8 lines,
                how far its sum is from 15   (0 = a perfect magic square)
Selection:      tournament (pick 3 different chromosomes, the lowest fitness wins)
Crossover:      Davis order crossover, OX1 (keep a segment of parent 1,
                fill the rest in the order of parent 2)
Mutation:       swap (with probability pm, two cells change their numbers)
Survival:       keep the best (put parents and children together,
                keep the best POP_SIZE squares, one copy of each)

Run:  python 8_magic_square.py
"""

import random

# 9 cells, numbered row by row:
#   0 1 2
#   3 4 5
#   6 7 8
N = 9

# Each line must add up to 15
TARGET = 15

# The 8 lines of the square: 3 rows, 3 columns and 2 diagonals
lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
         (0, 3, 6), (1, 4, 7), (2, 5, 8),
         (0, 4, 8), (2, 4, 6)]

# The settings of the genetic algorithm
POP_SIZE = 30          # how many squares live in each generation
NUM_PARENTS = 30       # how many parents we choose in each generation
TOURNAMENT_SIZE = 3    # how many chromosomes play in each tournament
CROSSOVER_RATE = 0.8   # pc: the chance that a pair of parents does crossover
MUTATION_RATE = 0.3    # pm: the chance that a child mutates
MAX_GENERATIONS = 200  # stop after this many generations


# ---------- Representation ----------
def random_chromosome():
    # The numbers 1 to 9 in a random order.
    # range(1, N + 1) gives 1, 2, ..., 9.
    return random.sample(range(1, N + 1), N)


def decode(chromosome):
    # Print the square, 3 numbers in each row, with the sum of the row
    for row in range(3):
        # The 3 cells of this row: for row 1 this is chromosome[3:6]
        cells = chromosome[row * 3: row * 3 + 3]
        print(f"  {cells[0]} {cells[1]} {cells[2]}   (sum {sum(cells)})")


# ---------- Population ----------
def generate_population(size):
    # Make "size" random chromosomes
    population = []
    # _ is a name for a number we do not need
    for _ in range(size):
        population.append(random_chromosome())
    return population


# ---------- Fitness (lower is better) ----------
def fitness(chromosome):
    error = 0
    for line in lines:
        # The sum of the 3 numbers on this line
        line_sum = 0
        for cell in line:
            line_sum += chromosome[cell]
        # How far is it from 15? abs() removes the minus sign.
        error += abs(line_sum - TARGET)
    return error


# ---------- Selection: tournament ----------
def selection(population, num_parents):
    parents = []
    for _ in range(num_parents):
        # Pick TOURNAMENT_SIZE different chromosomes at random
        players = random.sample(population, TOURNAMENT_SIZE)
        # Lower is better, so the player with the smallest fitness wins.
        # key=fitness: min() compares the players by their fitness.
        winner = min(players, key=fitness)
        parents.append(winner)
    return parents


# ---------- Crossover: Davis order crossover (OX1) ----------
def order_child(first, second, cut1, cut2):
    # None means "this place is still empty".
    # [None] * N makes a list with N times None.
    child = [None] * N
    # 1. Copy the segment between the cuts from the first parent
    child[cut1:cut2] = first[cut1:cut2]
    # 2. Read the second parent, starting after the second cut.
    #    % N goes back to the start when we reach the end of the list.
    place = cut2 % N
    for k in range(N):
        gene = second[(cut2 + k) % N]
        # 3. Skip the genes the child already has, write the others in the free places
        if gene not in child:
            child[place] = gene
            place = (place + 1) % N
    return child


def crossover(parent1, parent2):
    # Pick 2 different cut points, in order
    cut1, cut2 = sorted(random.sample(range(1, N), 2))
    child1 = order_child(parent1, parent2, cut1, cut2)
    child2 = order_child(parent2, parent1, cut1, cut2)
    return child1, child2


def make_children(mating_pool):
    children = []
    # Take the parents two by two: (1st, 2nd), (3rd, 4th), ...
    for i in range(0, len(mating_pool) - 1, 2):
        parent1 = mating_pool[i]
        parent2 = mating_pool[i + 1]
        if random.random() < CROSSOVER_RATE:
            child1, child2 = crossover(parent1, parent2)
        else:
            # No crossover: the children are copies of the parents.
            # .copy() makes a new list with the same genes.
            child1, child2 = parent1.copy(), parent2.copy()
        children += [child1, child2]
    return children


# ---------- Mutation: swap ----------
def mutation(chromosome):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    if random.random() < MUTATION_RATE:
        # Pick 2 different cells
        i, j = random.sample(range(N), 2)
        # Swap their numbers in one line: the left gets the values on the right
        mutant[i], mutant[j] = mutant[j], mutant[i]
    return mutant


def mutate_children(children):
    mutants = []
    for child in children:
        mutants.append(mutation(child))
    return mutants


# ---------- Survival selection: keep the best (this part is given) ----------
def survival_selection(population, children):
    # Parents and children compete together for a place
    everyone = population + children
    # Sort from the best to the worst (lower is better, so smallest first)
    everyone.sort(key=fitness)

    next_population = []
    for chromosome in everyone:
        # Keep only one copy of each chromosome.
        # Many copies make the population too similar, and the search gets stuck.
        if chromosome not in next_population:
            next_population.append(chromosome)
        # Stop when we have POP_SIZE squares
        if len(next_population) == POP_SIZE:
            break

    # Not enough different squares? Fill the free places with new random ones.
    while len(next_population) < POP_SIZE:
        next_population.append(random_chromosome())
    return next_population


# ---------- The genetic algorithm ----------
def run_ga():
    population = generate_population(POP_SIZE)

    for generation in range(1, MAX_GENERATIONS + 1):
        # One generation: selection -> crossover -> mutation -> survival
        mating_pool = selection(population, NUM_PARENTS)
        children = make_children(mating_pool)
        children = mutate_children(children)
        population = survival_selection(population, children)

        # After survival selection, the best square is the first one
        best = population[0]
        print(f"Generation {generation:3}: best error = {fitness(best)}")

        # Stop early when we find a perfect magic square
        if fitness(best) == 0:
            break

    return population[0]


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_ga()

print("\nFinal solution:")
print(f"  Chromosome: {best}")
print(f"  Error:      {fitness(best)}   (0 = perfect)")
decode(best)
