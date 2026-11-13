"""
Problem 7: The Hiking Backpack (exercise: complete the code)

Rami goes on a one-day hike in the mountains. He has 12 items at home,
but his backpack can carry only 10 kg. Each item has a weight and a value
(how useful it is on the hike). Choose the items with the biggest total value
that are not heavier than 10 kg.

Selection:  roulette wheel selection
Survival:   keep the best (given)

Run:  python 7_hiking_backpack.py

What you have to do:
  Write every function marked with TODO. The comments tell you what each
  function must do. You decide how to do it.
  - You choose the representation (what a chromosome looks like).
  - You write the fitness function.
  - You choose a crossover and a mutation that fit your representation.
  You can add your own small helper functions.
  survival_selection() is already complete: you only call it.
  A TODO function stops the program with a message until you write it.
  Use the small tests at the bottom of the file to check each function.
  When everything works, the program prints the final solution.
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

names = list(items.keys())

N = len(items)

# The backpack can carry at most 10 kg
MAX_WEIGHT = 10

# The settings of the genetic algorithm
POP_SIZE = 30          # how many chromosomes live in each generation
NUM_PARENTS = 30       # how many parents we choose in each generation
CROSSOVER_RATE = 0.8   # pc: the chance that a pair of parents does crossover
MUTATION_RATE = 0.3    # pm: the chance of a mutation
MAX_GENERATIONS = 200  # stop after this many generations

PENALTY = 50

# ---------- Representation ----------
def random_chromosome():
    # TODO: return one random chromosome (one random backpack).
    # - First decide: what does a chromosome look like? What does one gene mean?
    # - Write your answer in a comment here.
    # backpack = []
    # total_weight = 0
    # available_items = names.copy()
    # random.shuffle(available_items)

    # for item in available_items:
    #     item_weight = items[item][0]
    #     if total_weight + item_weight <= MAX_WEIGHT:
    #         backpack.append(item)
    #         total_weight += item_weight
    #     else:
    #         continue

    # return backpack
    return [random.randint(0, 1) for _ in range(N)]


def get_total_weight(chromosome):
    total = 0
    for i in range(len(chromosome)):
        name = names[i]
        total += items[name][0]
    return total


def get_total_value(chromosome):
    total = 0
    for i in range(len(chromosome)):
        name = names[i]
        total += items[name][1]
    return total


def decode(chromosome):
    # TODO: print the backpack in a way people can read.
    # - Show the items in the backpack, the total weight and the total value.
    print("All items inside the backpack:\n")
    for n, i in enumerate(range(len(chromosome)), 1):
        name = names[i]
        print(f"item {n}  -->  {name},  weighs  {items[name][0]},  value  {items[name][1]}")

    print(f"Total weight:  {get_total_weight(chromosome)}")
    print(f"Total value:  {get_total_value(chromosome)}")


# ---------- Population ----------
def generate_population(size):
    # TODO: return a list with "size" random chromosomes.
    return [random_chromosome() for _ in range(size)]

# ---------- Fitness ----------
def fitness(chromosome):
    # TODO: return a number that tells how good this backpack is.
    # - A higher number must mean a better backpack,
    #   because survival_selection() keeps the highest fitness.
    # - Roulette wheel selection needs a fitness that is 0 or more.
    # - Think: what do you do with a backpack that is heavier than 10 kg?
    # if get_total_weight(chromosome) > MAX_WEIGHT:
    #     return 0

    # return get_total_value(chromosome)

    if get_total_weight(chromosome) > MAX_WEIGHT:
        return 0
    return get_total_value(chromosome)



# ---------- Selection: roulette wheel ----------
def selection(population, num_parents):
    # TODO: choose num_parents parents with roulette wheel selection.
    # - Return a list of num_parents chromosomes.
    # - Think: what happens if the fitness of every chromosome is 0?
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("selection() is not written yet")


# ---------- Crossover ----------
def crossover(parent1, parent2):
    # TODO: mix two parents and return two children: child1, child2
    # - Choose a crossover that fits your representation.
    # - Each child must be a correct chromosome, like the ones
    #   random_chromosome() makes.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("crossover() is not written yet")


def make_children(mating_pool):
    # TODO: make the children of the whole mating pool.
    # - Take the parents two by two: (1st, 2nd), (3rd, 4th), ...
    # - For each pair: with probability CROSSOVER_RATE, do crossover.
    #   Else the two children are copies of the two parents.
    # - Return the list of all children.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("make_children() is not written yet")


# ---------- Mutation ----------
def mutation(chromosome):
    # TODO: return a mutated copy of the chromosome.
    # - With probability MUTATION_RATE, make a small random change.
    # - Else return a copy with no change.
    # - Choose a mutation that fits your representation.
    # - The new chromosome must still be correct.
    # - Do not change the chromosome you got: change a copy.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("mutation() is not written yet")


def mutate_children(children):
    # TODO: call mutation() for every child.
    # - Return the list of the new children.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("mutate_children() is not written yet")


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
        # Stop when we have POP_SIZE chromosomes
        if len(next_population) == POP_SIZE:
            break

    # Not enough different chromosomes? Fill the free places with new random ones.
    while len(next_population) < POP_SIZE:
        next_population.append(random_chromosome())
    return next_population


# ---------- The genetic algorithm ----------
def run_ga():
    # TODO: the main loop of the genetic algorithm
    # 1. Make the first population with POP_SIZE chromosomes.
    # 2. Repeat for generation = 1, 2, ..., MAX_GENERATIONS:
    #    a. choose NUM_PARENTS parents
    #    b. make the children (crossover)
    #    c. mutate the children
    #    d. population = survival_selection(population, children)
    #    e. After survival selection, the best chromosome is population[0].
    #       Print the generation number and the best fitness.
    #    f. We do not know the best value, so do NOT stop early.
    #       Run all MAX_GENERATIONS generations.
    # 3. Return the best chromosome.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("run_ga() is not written yet")


# ---------- Test your functions one by one ----------
# Remove the # at the start of a line to run the test.

# print(names)

# c = random_chromosome()
# decode(c)

l = generate_population(10)

for c in l:
    decode(c)

# print(c)

# decode(c)

# decode(random_chromosome())
# print(fitness(random_chromosome()))
# print(generate_population(3))
# print(selection(generate_population(6), 4))
# print(crossover(random_chromosome(), random_chromosome()))
# print(mutation(random_chromosome()))


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
# random.seed(1)

# best = run_ga()

# print("\nFinal solution:")
# print(f"  Chromosome: {best}")
# print(f"  Fitness:    {fitness(best)}")
# decode(best)
