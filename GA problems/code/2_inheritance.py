"""
Problem 2: The Inheritance

A grandfather leaves 12 items to his grandchildren.
Split the items so the totals are as close as possible.

Representation: binary, one gene per item (0 = Lina, 1 = Omar)
                for 3 grandchildren: integer (0 = Lina, 1 = Omar, 2 = Sara)
Fitness:        MINIMIZE  | total of Lina - total of Omar |   (0 = perfectly fair)

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

print("\nThree grandchildren (0 = Lina, 1 = Omar, 2 = Sara):")
for _ in range(2):
    c = random_chromosome_3()
    print(f"  {''.join(map(str, c))}  gap = {fitness_3(c)}")
