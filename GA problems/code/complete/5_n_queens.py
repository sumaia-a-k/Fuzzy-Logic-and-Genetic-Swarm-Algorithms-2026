"""
Problem 5: The 8 Queens (the full genetic algorithm)

Put 8 queens on a chess board (8 x 8) so that no queen can attack another one.
A queen attacks along its row, its column and its two diagonals.

Representation: permutation, one gene per row (gene = the column of the queen
                in this row, 0 to 7, each column once)
Fitness:        MAXIMIZE  the number of queen pairs that do not attack each other
                (28 = a perfect board, because 8 queens make 28 pairs)
Selection:      rank (the worst board gets rank 1, the best gets rank N)
Crossover:      Davis order crossover, OX1 (keep a segment of parent 1,
                fill the rest in the order of parent 2)
Mutation:       scramble (with probability pm, mix the columns of a random
                group of rows)
Survival:       keep the best (put parents and children together,
                keep the best POP_SIZE boards, one copy of each)

Run:  python 5_n_queens.py
"""

import random

# The board has 8 rows and 8 columns, and we place 8 queens
N = 8

# 8 queens make 8 * 7 / 2 = 28 pairs. // is division without the rest.
ALL_PAIRS = N * (N - 1) // 2

# The settings of the genetic algorithm
POP_SIZE = 30          # how many boards live in each generation
NUM_PARENTS = 30       # how many parents we choose in each generation
CROSSOVER_RATE = 0.8   # pc: the chance that a pair of parents does crossover
MUTATION_RATE = 0.3    # pm: the chance that a child mutates
MAX_GENERATIONS = 200  # stop after this many generations


# ---------- Representation ----------
def random_chromosome():
    # The columns 0 to 7 in a random order.
    # random.sample() takes all N numbers in a random order.
    return random.sample(range(N), N)


def decode(chromosome):
    # Print the board: Q is a queen, . is an empty square
    for row in range(N):
        # One text for each square: "Q" in the column of the queen, "." in the others.
        # This is a list comprehension: a short way to build a list with a loop.
        # " ".join() glues the texts together with a space between them.
        squares = ["Q" if chromosome[row] == column else "." for column in range(N)]
        print("  " + " ".join(squares))


# ---------- Population ----------
def generate_population(size):
    # Make "size" random chromosomes
    population = []
    # _ is a name for a number we do not need
    for _ in range(size):
        population.append(random_chromosome())
    return population


# ---------- Fitness (higher is better) ----------
def count_attacks(chromosome):
    # Check every pair of queens once: row1 < row2
    attacks = 0
    for row1 in range(N):
        for row2 in range(row1 + 1, N):
            # Same diagonal: as many rows apart as columns apart.
            # abs() removes the minus sign.
            if abs(chromosome[row1] - chromosome[row2]) == abs(row1 - row2):
                attacks += 1
    return attacks


def fitness(chromosome):
    # The pairs that do not attack each other (28 is perfect)
    return ALL_PAIRS - count_attacks(chromosome)


# ---------- Selection: rank ----------
def selection(population, num_parents):
    # Sort from the worst to the best (smallest fitness first).
    # key=fitness: sorted() compares the boards by their fitness.
    ranked = sorted(population, key=fitness)
    # The worst gets rank 1, the next rank 2, ..., the best rank N
    ranks = list(range(1, len(ranked) + 1))
    total = sum(ranks)

    parents = []
    for _ in range(num_parents):
        # Spin the wheel: the pointer stops at a random point
        point = random.random() * total
        # Walk over the slices until we pass the point.
        # zip() goes over the two lists together.
        position = 0
        for chromosome, rank in zip(ranked, ranks):
            position += rank
            if point < position:
                parents.append(chromosome)
                break
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


# ---------- Mutation: scramble ----------
def mutation(chromosome):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    if random.random() < MUTATION_RATE:
        # A random segment with at least 2 rows
        start = random.randint(0, N - 2)
        end = random.randint(start + 2, N)
        segment = mutant[start:end]
        # random.shuffle() mixes the list in a random order
        random.shuffle(segment)
        mutant[start:end] = segment
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
    # Sort from the best to the worst (reverse=True: biggest fitness first)
    everyone.sort(key=fitness, reverse=True)

    next_population = []
    for chromosome in everyone:
        # Keep only one copy of each chromosome.
        # Many copies make the population too similar, and the search gets stuck.
        if chromosome not in next_population:
            next_population.append(chromosome)
        # Stop when we have POP_SIZE boards
        if len(next_population) == POP_SIZE:
            break

    # Not enough different boards? Fill the free places with new random ones.
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

        # After survival selection, the best board is the first one
        best = population[0]
        print(f"Generation {generation:3}: best fitness = {fitness(best)} of {ALL_PAIRS}")

        # Stop early when we find a perfect board
        if fitness(best) == ALL_PAIRS:
            break

    return population[0]


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_ga()

print("\nFinal solution:")
print(f"  Chromosome: {best}")
print(f"  Attacks:    {count_attacks(best)}")
print(f"  Fitness:    {fitness(best)} of {ALL_PAIRS}")
decode(best)
