"""
Problem 2: The Inheritance

A grandfather leaves 12 items to his grandchildren.
Split the items so the totals are as close as possible.

Representation: binary, one gene per item (0 = Lina, 1 = Omar)
                for 3 grandchildren: integer (0 = Lina, 1 = Omar, 2 = Sara)
Fitness:        MINIMIZE  | total of Lina - total of Omar |   (0 = perfectly fair)
Selection:      rank (the worst split gets rank 1, the best gets rank N,
                and the slice of the wheel is the rank)

Run:  python 2_inheritance.py
"""

import random

# The 12 items and their values
items = {
    "Car": 12000, "Piano": 7000, "Watch": 1500, "Painting": 4300,
    "Carpet": 2100, "Gold ring": 3200, "Books": 900, "Sewing machine": 450,
    "Dining table": 1800, "Bicycle": 350, "Camera": 1250, "Coin collection": 5600,
}

# The items in a fixed order: gene i is always about item i
names = list(items.keys())

# One gene per item, so the chromosome has 12 genes
N = len(names)

# M: how many parents we want. It does not have to be the population size.
NUM_PARENTS = 4


# ---------- Representation ----------
def random_chromosome():
    # Give every item to Lina (0) or Omar (1) at random
    return [random.randint(0, 1) for _ in range(N)]


def decode(chromosome):
    # Print the items of each grandchild
    print("  Lina:", [n for n, g in zip(names, chromosome) if g == 0])
    print("  Omar:", [n for n, g in zip(names, chromosome) if g == 1])


# ---------- Fitness (lower is better) ----------
def totals(chromosome):
    # Add up the value of the items that each grandchild gets
    lina = sum(items[n] for n, g in zip(names, chromosome) if g == 0)
    omar = sum(items[n] for n, g in zip(names, chromosome) if g == 1)
    return lina, omar


def fitness(chromosome):
    # The gap between the two totals; abs() removes the minus sign
    lina, omar = totals(chromosome)
    return abs(lina - omar)


# ---------- Selection: rank ----------
def sort_worst_to_best(population):
    # Lower is better, so the biggest gap comes first.
    # key=fitness means "sort by the fitness", reverse=True means "from big to small".
    return sorted(population, key=fitness, reverse=True)


def rank_slices(ranked):
    """
    The slice of each chromosome on the wheel is its rank.
    The worst gets rank 1, the next one rank 2, ..., the best rank N.

    The slices stay as rank numbers. We do not change them to chances
    between 0 and 1, because spin_wheel() makes the wheel as big as
    the sum of the slices.

    Example with 6 chromosomes:
        slices = [1, 2, 3, 4, 5, 6]     the wheel has size 1 + 2 + ... + 6 = 21
        the best one has the slice from 15 to 21, so its chance is 6 / 21 = 28.6%
        the worst one has the slice from 0 to 1, so its chance is 1 / 21 = 4.8%
    If the pointer stops at 16.4, it is in the slice from 15 to 21,
    so the best chromosome becomes a parent.
    """
    # range(1, N + 1) gives 1, 2, ..., N
    return list(range(1, len(ranked) + 1))


def spin_wheel(chromosomes, slices):
    # The size of the wheel is the sum of the slices (21 for 6 ranks).
    # The pointer stops at a random point between 0 and this size.
    point = random.random() * sum(slices)
    # Walk over the slices until we pass the point
    position = 0
    for chromosome, size in zip(chromosomes, slices):
        position += size
        if point < position:
            return chromosome
    # Rounding can leave the point just after the last slice
    return chromosomes[-1]


def selection(population, num_parents):
    # Sort the population and give the ranks
    ranked = sort_worst_to_best(population)
    slices = rank_slices(ranked)
    # Spin once for each parent.
    # "for _ in range(num_parents)" repeats num_parents times.
    return [spin_wheel(ranked, slices) for _ in range(num_parents)]


# ---------- Three grandchildren: Lina, Omar and Sara ----------
def random_chromosome_3():
    # Give every item to Lina (0), Omar (1) or Sara (2) at random
    return [random.randint(0, 2) for _ in range(N)]


def fitness_3(chromosome):
    # Add up the value of the items that each grandchild gets
    money = [0, 0, 0]
    for n, g in zip(names, chromosome):
        money[g] += items[n]
    # The gap between the richest and the poorest grandchild
    return max(money) - min(money)


# ---------- Try it ----------
# random.seed(4) is only for this lesson.
# It makes Python pick the same "random" numbers on every run,
# so every student gets the same output as the lecture.
# The number 4 has no special meaning; another number gives other results.
# In a real GA we remove this line, so each run starts from a new population.
random.seed(4)

# Make a small population of 6 random chromosomes
population = [random_chromosome() for _ in range(6)]

print("Population:")
for c in population:
    lina, omar = totals(c)
    print(f"  {''.join(map(str, c))}  Lina = {lina:>5}  Omar = {omar:>5}"
          f"  gap = {fitness(c):>5}")

# Lower is better, so the best split has the smallest gap
best = min(population, key=fitness)
print(f"\nThe best split in this population (gap = {fitness(best)}):")
decode(best)

# Rank selection: only the order counts, not the size of the gap
ranked = sort_worst_to_best(population)
slices = rank_slices(ranked)
total = sum(slices)
print(f"\nRank selection (the total of the ranks is {total}):")
# zip() goes over the two lists together
for c, rank in zip(ranked, slices):
    print(f"  {''.join(map(str, c))}  gap = {fitness(c):>5}  rank = {rank}"
          f"  chance = {rank / total * 100:.1f}%")

# Choose the mating pool: one spin of the wheel for each parent
mating_pool = selection(population, NUM_PARENTS)
print(f"\nMating pool ({NUM_PARENTS} parents):")
for c in mating_pool:
    print(f"  {''.join(map(str, c))}  gap = {fitness(c):>5}")

print("\nThree grandchildren (0 = Lina, 1 = Omar, 2 = Sara):")
for _ in range(2):
    c = random_chromosome_3()
    print(f"  {''.join(map(str, c))}  gap = {fitness_3(c)}")
