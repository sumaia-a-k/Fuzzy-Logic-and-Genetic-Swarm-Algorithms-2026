"""
Problem 6: The Eid Dinner Table (the full genetic algorithm)

Grandma invites 8 family members to Eid dinner at one round table.
Some people love to sit together, and some people always argue.
Find a seating plan where as many neighbours as possible are friends,
and nobody sits next to someone they argue with.

Representation: permutation, one gene per seat (gene = the guest number
                in this seat, each guest once). The table is round,
                so the last seat sits next to the first seat.
Fitness:        MAXIMIZE  the happiness of the table:
                +1 for each pair of friends that sit together,
                -1 for each pair that argues and sits together
                (8 = a perfect table: all 8 neighbour pairs are friends)
Selection:      tournament (pick 3 different chromosomes, the highest fitness wins)
Crossover:      single-point for a permutation (keep the start of parent 1,
                then add the missing guests in the order of parent 2)
Mutation:       inversion (with probability pm, a random block of seats
                is put in the opposite order)
Survival:       keep the best (put parents and children together,
                keep the best POP_SIZE tables, one copy of each)

Run:  python 6_eid_dinner_table.py
"""

import random

# The 8 guests. Gene value i means guests[i].
guests = ["Grandma", "Grandpa", "Ahmad", "Lina", "Omar", "Sara", "Rami", "Huda"]

# Pairs of guests who are happy to sit together
friends = [("Grandma", "Sara"), ("Sara", "Omar"), ("Omar", "Rami"), ("Rami", "Huda"),
           ("Huda", "Ahmad"), ("Ahmad", "Lina"), ("Lina", "Grandpa"), ("Grandpa", "Grandma"),
           ("Grandma", "Lina"), ("Omar", "Huda")]

# Pairs of guests who always argue
argue = [("Omar", "Ahmad"), ("Rami", "Lina"), ("Sara", "Grandpa"), ("Huda", "Grandma"),
         ("Ahmad", "Grandpa")]

# One gene per seat
N = len(guests)

# 8 seats around a round table make 8 neighbour pairs
PERFECT = N

# The settings of the genetic algorithm
POP_SIZE = 30          # how many tables live in each generation
NUM_PARENTS = 30       # how many parents we choose in each generation
TOURNAMENT_SIZE = 3    # how many chromosomes play in each tournament
CROSSOVER_RATE = 0.8   # pc: the chance that a pair of parents does crossover
MUTATION_RATE = 0.3    # pm: the chance that a child mutates
MAX_GENERATIONS = 100  # stop after this many generations


# ---------- Representation ----------
def random_chromosome():
    # The guest numbers 0 to 7 in a random order
    return random.sample(range(N), N)


def neighbour_score(name1, name2):
    # +1 for friends, -1 for people who argue, 0 for the others.
    # We check both orders, because (A, B) and (B, A) are the same pair.
    if (name1, name2) in friends or (name2, name1) in friends:
        return 1
    if (name1, name2) in argue or (name2, name1) in argue:
        return -1
    return 0


def decode(chromosome):
    # Print each seat and how this guest feels about the next guest
    labels = {1: "friends", -1: "ARGUE", 0: "ok"}
    for seat in range(N):
        name = guests[chromosome[seat]]
        # % N: after the last seat we go back to seat 0 (the table is round)
        next_name = guests[chromosome[(seat + 1) % N]]
        score = neighbour_score(name, next_name)
        # {name:<8} fills the name with spaces to 8 letters, so the columns line up
        print(f"  Seat {seat + 1}: {name:<8} -> next to {next_name:<8} ({labels[score]})")


# ---------- Population ----------
def generate_population(size):
    # Make "size" random chromosomes
    population = []
    # _ is a name for a number we do not need
    for _ in range(size):
        population.append(random_chromosome())
    return population


# ---------- Fitness (higher is better) ----------
def fitness(chromosome):
    # Add the score of every neighbour pair around the table
    happiness = 0
    for seat in range(N):
        name = guests[chromosome[seat]]
        next_name = guests[chromosome[(seat + 1) % N]]
        happiness += neighbour_score(name, next_name)
    return happiness


# ---------- Selection: tournament ----------
def selection(population, num_parents):
    parents = []
    for _ in range(num_parents):
        # Pick TOURNAMENT_SIZE different chromosomes at random
        players = random.sample(population, TOURNAMENT_SIZE)
        # The player with the highest fitness wins.
        # key=fitness: max() compares the players by their fitness.
        winner = max(players, key=fitness)
        parents.append(winner)
    return parents


# ---------- Crossover: single-point for a permutation ----------
def fill_child(first, second, cut):
    # Keep the start of the first parent
    child = first[:cut]
    # Add the missing guests in the order of the second parent
    for gene in second:
        if gene not in child:
            child.append(gene)
    return child


def crossover(parent1, parent2):
    # Pick a cut point between the first and the last gene
    cut = random.randint(1, N - 1)
    child1 = fill_child(parent1, parent2, cut)
    child2 = fill_child(parent2, parent1, cut)
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


# ---------- Mutation: inversion ----------
def mutation(chromosome):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    if random.random() < MUTATION_RATE:
        # A random block with at least 2 seats
        start = random.randint(0, N - 2)
        end = random.randint(start + 2, N)
        # [::-1] reads the block from the end to the start
        mutant[start:end] = mutant[start:end][::-1]
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
        # Stop when we have POP_SIZE tables
        if len(next_population) == POP_SIZE:
            break

    # Not enough different tables? Fill the free places with new random ones.
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

        # After survival selection, the best table is the first one
        best = population[0]
        print(f"Generation {generation:3}: best fitness = {fitness(best)} of {PERFECT}")

        # Stop early when we find a perfect table
        if fitness(best) == PERFECT:
            break

    return population[0]


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_ga()

print("\nFinal solution:")
print(f"  Chromosome: {best}")
print(f"  Fitness:    {fitness(best)} of {PERFECT}")
decode(best)
