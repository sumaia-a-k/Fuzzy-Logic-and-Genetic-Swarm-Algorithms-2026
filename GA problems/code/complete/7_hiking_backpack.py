"""
Problem 7: The Hiking Backpack (the full genetic algorithm)

Rami goes on a one-day hike in the mountains. He has 12 items at home,
but his backpack can carry only 10 kg. Each item has a weight and a value
(how useful it is on the hike). Choose the items with the biggest total value
that are not heavier than 10 kg.

Representation: binary, one gene per item (1 = in the backpack, 0 = at home)
Fitness:        MAXIMIZE  the total value of the items in the backpack
                (a backpack heavier than 10 kg gets fitness 0)
Selection:      roulette wheel (the slice of each backpack is its fitness)
Crossover:      uniform (flip a coin for every item: it decides from which
                parent each child takes this gene)
Mutation:       bit flip (each gene flips with probability pm:
                the item goes in or out of the backpack)
Survival:       keep the best (put parents and children together,
                keep the best POP_SIZE backpacks, one copy of each)

Run:  python 7_hiking_backpack.py
"""

import random

# name: (weight in kg, value)
items = {
    "Water":       (3, 10),
    "Sandwiches":  (1, 7),
    "Hammock":     (4, 9),
    "Rain coat":   (2, 8),
    "Sweater":     (1, 6),
    "First aid":   (1, 9),
    "Torch":       (1, 5),
    "Camera":      (1, 4),
    "Small stove": (2, 5),
    "Rope":        (1, 3),
    "Book":        (1, 2),
    "Guitar":      (3, 4),
}

# The items in a fixed order: gene i is always about item i
names = list(items.keys())

# One gene per item
N = len(names)

# The backpack can carry at most 10 kg
MAX_WEIGHT = 10

# We checked all 4096 backpacks by computer: the best possible value is 49.
# The genetic algorithm does not know this number. We only use it to check the result.
BEST_POSSIBLE = 49

# The settings of the genetic algorithm
POP_SIZE = 20          # how many backpacks live in each generation
NUM_PARENTS = 20       # how many parents we choose in each generation
CROSSOVER_RATE = 0.8   # pc: the chance that a pair of parents does crossover
MUTATION_RATE = 0.1    # pm: the chance that ONE gene flips
MAX_GENERATIONS = 30   # stop after this many generations


# ---------- Representation ----------
def random_chromosome():
    # For each item: 0 or 1 at random
    chromosome = []
    for _ in range(N):
        chromosome.append(random.randint(0, 1))
    return chromosome


def total_weight(chromosome):
    weight = 0
    for i in range(N):
        if chromosome[i] == 1:
            weight += items[names[i]][0]
    return weight


def total_value(chromosome):
    value = 0
    for i in range(N):
        if chromosome[i] == 1:
            value += items[names[i]][1]
    return value


def decode(chromosome):
    # Print the items in the backpack
    for i in range(N):
        if chromosome[i] == 1:
            # The item is a pair (weight, value): we take both parts
            weight, value = items[names[i]]
            # {names[i]:<12} fills the name with spaces to 12 letters
            print(f"  {names[i]:<12} {weight} kg   value {value}")
    print(f"  Total: {total_weight(chromosome)} kg of {MAX_WEIGHT} kg,"
          f" value {total_value(chromosome)}")


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
    # A backpack that is too heavy is not allowed: fitness 0
    if total_weight(chromosome) > MAX_WEIGHT:
        return 0
    return total_value(chromosome)


# ---------- Selection: roulette wheel ----------
def selection(population, num_parents):
    # The slice of each backpack is its fitness
    slices = []
    for chromosome in population:
        slices.append(fitness(chromosome))
    total = sum(slices)

    parents = []
    for _ in range(num_parents):
        # If all backpacks are too heavy, every slice is 0: pick at random
        if total == 0:
            parents.append(random.choice(population))
            continue
        # Spin the wheel: the pointer stops at a random point
        point = random.random() * total
        # Walk over the slices until we pass the point.
        # zip() goes over the two lists together.
        position = 0
        for chromosome, size in zip(population, slices):
            position += size
            if point < position:
                parents.append(chromosome)
                break
    return parents


# ---------- Crossover: uniform ----------
def crossover(parent1, parent2):
    child1 = []
    child2 = []
    for i in range(N):
        # Flip a coin for this gene
        if random.random() < 0.5:
            # Heads: each child takes the gene from its own parent
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            # Tails: the children take the gene from the other parent
            child1.append(parent2[i])
            child2.append(parent1[i])
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


# ---------- Mutation: bit flip ----------
def mutation(chromosome):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    for i in range(N):
        # Each gene flips with probability MUTATION_RATE: 0 -> 1 or 1 -> 0
        if random.random() < MUTATION_RATE:
            mutant[i] = 1 - mutant[i]
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
        # Stop when we have POP_SIZE backpacks
        if len(next_population) == POP_SIZE:
            break

    # Not enough different backpacks? Fill the free places with new random ones.
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

        # After survival selection, the best backpack is the first one.
        # We do not know the best value, so we do not stop early.
        best = population[0]
        print(f"Generation {generation:3}: best fitness = {fitness(best)}")

    return population[0]


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_ga()

print("\nFinal solution:")
print(f"  Chromosome: {best}")
print(f"  Fitness:    {fitness(best)}   (the best possible is {BEST_POSSIBLE})")
decode(best)
