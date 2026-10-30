"""
Problem 4: The Bakery Oven

A small bakery has one oven that bakes one order at a time.
The morning starts at 8:00 with 7 orders. Each order has a baking time
and a pickup time. If an order is not ready, the customer waits.
Find the baking order with the smallest total waiting time.

Representation: permutation, the baking order (each order number appears once)
Fitness:        MINIMIZE  the total waiting time of all customers (in minutes)
Selection:      tournament (pick 3 different chromosomes, the lowest fitness wins)
Crossover:      single-point for a permutation (keep the start of parent 1,
                then add the missing orders in the order of parent 2)
Mutation:       inversion (with probability pm, a random block of orders
                is baked in the opposite order)

Run:  python 4_bakery_oven.py
"""

import random

# name: (baking minutes, pickup minute after 8:00)
orders = {
    "Birthday cake": (60, 90),
    "Croissants":    (20, 30),
    "Bread loaves":  (45, 120),
    "Cheesecake":    (50, 100),
    "Cookies":       (15, 40),
    "Wedding cake":  (90, 240),
    "Pizza dough":   (25, 60),
}

# The orders in a fixed order: order number i is names[i]
names = list(orders.keys())

# One gene per order, so the chromosome has 7 genes
N = len(names)

# The number of players in one tournament
TOURNAMENT_SIZE = 3

# M: how many parents we want. It does not have to be the population size.
NUM_PARENTS = 4

# pc: the chance that a pair of parents does crossover
CROSSOVER_RATE = 0.8

# pm: the chance that a child mutates (one time, for the whole chromosome).
# pm must be small, so most children stay the same. There is no exact
# value to use: 0.2 is our choice here, and other small values also work.
MUTATION_RATE = 0.2


# ---------- The problem ----------
def print_orders():
    # Show the number, baking time and pickup time of each order
    print("The orders (number: name, baking time, pickup time):")
    # enumerate() gives the number i together with the name
    for i, name in enumerate(names):
        bake, pickup = orders[name]
        print(f"  {i}: {name:<14} bake {bake:>2} min   pickup at {clock(pickup):>5}")


def clock(minutes):
    # Turn "minutes after 8:00" into a time, for example 90 -> 9:30.
    # // is division without the rest, % is the rest.
    return f"{8 + minutes // 60}:{minutes % 60:02d}"


# ---------- Representation ----------
def random_chromosome():
    # A random baking order: the numbers 0 to 6, each one once.
    # random.sample() takes all N numbers in a random order.
    return random.sample(range(N), N)


def decode(chromosome):
    # Print the baking plan: when each order is ready and how long its customer waits
    time = 0
    for number in chromosome:
        name = names[number]
        bake, pickup = orders[name]
        time += bake
        wait = max(0, time - pickup)
        print(f"  {name:<14} ready at {clock(time):>5}   pickup at {clock(pickup):>5}"
              f"   wait = {wait} min")


# ---------- Fitness (lower is better) ----------
def fitness(chromosome):
    # Bake the orders one by one and add up the waiting time
    time = 0
    total_wait = 0
    for number in chromosome:
        bake, pickup = orders[names[number]]
        # The order is ready when its baking ends
        time += bake
        # If it is ready before the pickup time, the customer waits 0 minutes
        total_wait += max(0, time - pickup)
    return total_wait


# ---------- Selection: tournament ----------
# Why a tournament?
# - The fitness is MIN, and the tournament can use min() directly.
#   A roulette wheel needs MAX, so we would have to change the numbers first.
# - The waiting times are big numbers (hundreds of minutes).
#   A tournament only asks "who is better?", so the size of the numbers does not matter.
# - Selection only looks at the fitness, so it works for a permutation
#   in the same way as for any other chromosome.
def pick_players(population):
    # Pick TOURNAMENT_SIZE different chromosomes at random
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


# ---------- Crossover: single-point for a permutation ----------
# A simple swap of the tails can bake an order two times and forget another one.
# So the child keeps the start of one parent, and then reads the other parent
# from its first gene and adds every order that it does not have yet.
def pick_cut():
    # Pick a random cut point between the first and the last gene
    return random.randint(1, N - 1)


def fill_child(first, second, cut):
    # Keep the start of the first parent
    child = first[:cut]
    # Add the missing orders in the order of the second parent
    for number in second:
        if number not in child:
            child.append(number)
    return child


def single_point_perm(parent1, parent2, cut):
    child1 = fill_child(parent1, parent2, cut)
    child2 = fill_child(parent2, parent1, cut)
    return child1, child2


def crossover(parent1, parent2):
    # Single-point crossover for a permutation, at a random cut point
    return single_point_perm(parent1, parent2, pick_cut())


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


# ---------- Mutation: inversion ----------
# Inversion only moves orders, so every order is still baked exactly once.
def pick_segment():
    # The segment is chromosome[start:end], with at least 2 orders
    start = random.randint(0, N - 2)
    end = random.randint(start + 2, N)
    return start, end


def inversion(chromosome, start, end):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    # [::-1] reads the segment from the end to the start
    mutant[start:end] = chromosome[start:end][::-1]
    return mutant


def mutation(chromosome):
    # With probability MUTATION_RATE, turn a random segment around
    if random.random() < MUTATION_RATE:
        start, end = pick_segment()
        return inversion(chromosome, start, end)
    # No mutation: the child stays the same
    return chromosome.copy()


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


def show_cut(chromosome, cut):
    # Write the genes as text, with | at the cut point.
    # " ".join() glues the genes together with a space between them.
    head = " ".join(map(str, chromosome[:cut]))
    tail = " ".join(map(str, chromosome[cut:]))
    return f"{head} | {tail}"


# ---------- Try it ----------
print_orders()

# Use the same random numbers on every run.
# Remove this line to see a new population each time.
random.seed(1)

# Make a small population of 6 random chromosomes
population = [random_chromosome() for _ in range(6)]

print("\nPopulation (the baking order, as order numbers):")
for c in population:
    print(f"  {c}  total wait = {fitness(c)} min")

# Lower is better, so the best plan has the smallest total waiting time
best = min(population, key=fitness)
print(f"\nThe best plan in this population (total wait = {fitness(best)} min):")
decode(best)
# We tried all 5,040 orders on a computer: the best one has 235 minutes.
print("  (The best possible plan has 235 minutes of waiting.)")

# One tournament, step by step
players = pick_players(population)
print(f"\nOne tournament with {TOURNAMENT_SIZE} players:")
for c in players:
    print(f"  {c}  total wait = {fitness(c)} min")
winner = tournament_winner(players)
print(f"  The winner is {winner} (the smallest total wait, {fitness(winner)} min)")

# Choose the mating pool: one tournament for each parent
mating_pool = selection(population, NUM_PARENTS)
print(f"\nMating pool ({NUM_PARENTS} parents):")
for c in mating_pool:
    print(f"  {c}  total wait = {fitness(c)} min")

# One crossover, step by step.
# We take the first and the last parent of the pool, because they are different.
# mating_pool[-1] is the last item of the list.
parent1, parent2 = mating_pool[0], mating_pool[-1]
# Here we cut after gene 3, like in the lecture. crossover() picks a random cut.
cut = 3
child1, child2 = single_point_perm(parent1, parent2, cut)
print(f"\nSingle-point crossover for a permutation, cut after gene {cut}:")
print(f"  Parent 1: {show_cut(parent1, cut)}   total wait = {fitness(parent1)} min")
print(f"  Parent 2: {show_cut(parent2, cut)}   total wait = {fitness(parent2)} min")
print(f"  Child 1:  {show_cut(child1, cut)}   total wait = {fitness(child1)} min")
print(f"  Child 2:  {show_cut(child2, cut)}   total wait = {fitness(child2)} min")
print("  Child 1 keeps the start of parent 1, then takes the missing orders")
print("  in the order they have in parent 2. Every order is baked exactly once.")

# Make the children of the whole mating pool
children = make_children(mating_pool)
print(f"\nChildren of the mating pool (crossover rate = {CROSSOVER_RATE}):")
# Children i and i + 1 come from parents i and i + 1.
# A child can be the same as a parent when the pair does no crossover
# (chance 1 - CROSSOVER_RATE), or when both parents have the same genes
# in the part that is filled in.
for i in range(0, len(children), 2):
    print(f"  Pair {i // 2 + 1}")
    print(f"    Parents:  {mating_pool[i]}  {mating_pool[i + 1]}")
    print(f"    Children: {children[i]}  {children[i + 1]}"
          f"   total wait = {fitness(children[i])}, {fitness(children[i + 1])} min")

# One mutation, step by step, with the first child.
# Here the segment is genes 5 to 7. mutation() picks a random segment.
child = children[0]
mutant = inversion(child, 4, 7)
print("\nInversion of genes 5 to 7 (bake the last 3 orders in the opposite order):")
print(f"  Before: {child}  total wait = {fitness(child)} min")
print(f"  After:  {mutant}  total wait = {fitness(mutant)} min")

# Mutate all children: each child mutates with probability pm
mutants = mutate_children(children)
print(f"\nMutation of all children (pm = {MUTATION_RATE} per child):")
# mutated counts the children that changed.
# zip() goes over the two lists together.
mutated = 0
for before, after in zip(children, mutants):
    if before != after:
        mutated += 1
    print(f"  {before} -> {after}   changed genes: {changed_text(before, after):<7}"
          f"  total wait {fitness(before)} -> {fitness(after)} min")
print(f"  {mutated} of {len(children)} children mutated. With pm = {MUTATION_RATE}, about 1 child in 5 mutates.")
print("  Remove random.seed(1) and run again to see other results.")
