"""
Problem 2: The Inheritance

A grandfather leaves 12 items to his grandchildren.
Split the items so the totals are as close as possible.

Representation: binary, one gene per item (0 = Lina, 1 = Omar)
                for 3 grandchildren: integer (0 = Lina, 1 = Omar, 2 = Sara)
Fitness:        MINIMIZE  | total of Lina - total of Omar |   (0 = perfectly fair)
Selection:      rank (the worst split gets rank 1, the best gets rank N,
                and the slice of the wheel is the rank)
Crossover:      uniform (flip a coin for every item: it decides from which
                parent each child takes this gene)
Mutation:       bit flip (each gene flips with probability pm:
                the item goes to the other grandchild)

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

# pc: the chance that a pair of parents does crossover
CROSSOVER_RATE = 0.8

# pm: the chance that one gene mutates. pm must be small.
# 1 / N is a common choice (a convention, not a rule): about one gene
# changes in each child. Other small values, like 0.05, also work.
MUTATION_RATE = 1 / N


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


# ---------- Crossover: uniform ----------
def random_mask():
    # One coin for each gene: 1 or 0
    return [random.randint(0, 1) for _ in range(N)]


def uniform(parent1, parent2, mask):
    child1, child2 = [], []
    # zip() goes over the three lists together, gene by gene
    for gene1, gene2, coin in zip(parent1, parent2, mask):
        if coin == 1:
            # Coin 1: child 1 takes the gene of parent 1
            child1.append(gene1)
            child2.append(gene2)
        else:
            # Coin 0: child 1 takes the gene of parent 2
            child1.append(gene2)
            child2.append(gene1)
    return child1, child2


def crossover(parent1, parent2):
    # Uniform crossover with new random coins
    return uniform(parent1, parent2, random_mask())


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


def as_text(chromosome):
    # Write the genes as one short text, like 010110000110.
    # map(str, ...) turns each gene into text, "".join() glues them together.
    return "".join(map(str, chromosome))


# ---------- Mutation: bit flip ----------
def pick_genes():
    # One random number r for each gene. The gene mutates if r < MUTATION_RATE.
    positions = []
    for i in range(N):
        if random.random() < MUTATION_RATE:
            positions.append(i)
    return positions


def bit_flip(chromosome, positions):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    # 0 becomes 1 and 1 becomes 0: the item goes to the other grandchild
    for i in positions:
        mutant[i] = 1 - mutant[i]
    return mutant


def mutation(chromosome):
    # Bit flip on the genes that pick_genes() chooses
    return bit_flip(chromosome, pick_genes())


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

# One crossover, step by step, with the first two parents
parent1, parent2 = mating_pool[0], mating_pool[1]
mask = random_mask()
child1, child2 = uniform(parent1, parent2, mask)
print("\nUniform crossover (coin 1: child 1 takes the gene of parent 1):")
print(f"  Parent 1: {as_text(parent1)}  gap = {fitness(parent1):>5}")
print(f"  Parent 2: {as_text(parent2)}  gap = {fitness(parent2):>5}")
print(f"  Coins:    {as_text(mask)}")
print(f"  Child 1:  {as_text(child1)}  gap = {fitness(child1):>5}")
print(f"  Child 2:  {as_text(child2)}  gap = {fitness(child2):>5}")

# Make the children of the whole mating pool
children = make_children(mating_pool)
print(f"\nChildren of the mating pool (crossover rate = {CROSSOVER_RATE}):")
# Children i and i + 1 come from parents i and i + 1.
# A child can be the same as a parent when the pair does no crossover
# (chance 1 - CROSSOVER_RATE), or when both parents have the same genes
# in the part that is swapped.
for i in range(0, len(children), 2):
    print(f"  Pair {i // 2 + 1}")
    print(f"    Parents:  {as_text(mating_pool[i])}  {as_text(mating_pool[i + 1])}")
    print(f"    Children: {as_text(children[i])}  {as_text(children[i + 1])}"
          f"   gaps = {fitness(children[i])}, {fitness(children[i + 1])}")

print("\nThree grandchildren (0 = Lina, 1 = Omar, 2 = Sara):")
for _ in range(2):
    c = random_chromosome_3()
    print(f"  {''.join(map(str, c))}  gap = {fitness_3(c)}")

# One mutation, step by step, with the first child.
# Here we flip gene 2 (the piano), like in the lecture. mutation() picks the genes at random.
child = children[0]
mutant = bit_flip(child, [1])
print("\nBit flip on gene 2 (the piano goes to the other grandchild):")
print(f"  Before: {as_text(child)}  gap = {fitness(child):>5}")
print(f"  After:  {as_text(mutant)}  gap = {fitness(mutant):>5}")

# Mutate all children: each gene flips with probability pm
mutants = mutate_children(children)
print(f"\nMutation of all children (pm = 1/{N} = {MUTATION_RATE:.2f} per gene):")
# zip() goes over the two lists together
for before, after in zip(children, mutants):
    print(f"  {as_text(before)} -> {as_text(after)}   changed genes: {changed_text(before, after):<6}"
          f"  gap {fitness(before)} -> {fitness(after)}")
