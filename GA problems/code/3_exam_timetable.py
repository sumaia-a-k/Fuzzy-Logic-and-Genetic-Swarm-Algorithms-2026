"""
Problem 3: The Exam Timetable

The faculty has 8 final exams and 3 exam slots.
Two courses that share students cannot have their exams in the same slot.

Representation: integer, one gene per course (gene = slot number 0, 1 or 2)
Fitness:        MINIMIZE  the number of clashes   (0 = a perfect timetable)
Selection:      roulette wheel on the score 1 / (1 + clashes) (bigger is better)
Crossover:      single-point (cut both parents at one random point
                and swap the tails)
Mutation:       swap (with probability pm, two courses change their slots)

Run:  python 3_exam_timetable.py
"""

import random

# The 8 courses that have a final exam
courses = ["Math", "Physics", "Programming", "Databases",
           "Networks", "English", "Statistics", "AI"]

# Pairs of courses that share at least one student
conflicts = [("Math", "Physics"), ("Math", "Statistics"), ("Physics", "Programming"),
             ("Programming", "Databases"), ("Programming", "AI"), ("Databases", "Networks"),
             ("Statistics", "AI"), ("Networks", "English"), ("AI", "Databases"),
             ("English", "Math")]

NUM_SLOTS = 3

# One gene per course, so the chromosome has 8 genes
N = len(courses)

# The gene number of each course, for example "Math" -> gene 0
gene_of = {course: i for i, course in enumerate(courses)}

# M: how many parents we want. It does not have to be the population size.
NUM_PARENTS = 4

# pc: the chance that a pair of parents does crossover
CROSSOVER_RATE = 0.8

# pm: the chance that a child mutates (one time, for the whole chromosome).
# pm must be small, so most children stay the same. There is no exact
# value to use: 0.2 is our choice here, and other small values also work.
MUTATION_RATE = 0.2


# ---------- The problem ----------
def print_conflicts():
    # Show which courses share students
    print("Courses that share students (their exams must be in different slots):")
    for a, b in conflicts:
        print(f"  {a} - {b}")


# ---------- Representation ----------
def random_chromosome():
    # Put every course in a random slot: 0, 1 or 2
    return [random.randint(0, NUM_SLOTS - 1) for _ in range(N)]


def decode(chromosome):
    # Print the courses of each slot
    for slot in range(NUM_SLOTS):
        names = [c for c, g in zip(courses, chromosome) if g == slot]
        print(f"  Slot {slot + 1}: {names}")


# ---------- Fitness (lower is better) ----------
def fitness(chromosome):
    # Count the pairs of conflicting courses that are in the same slot
    clashes = 0
    for a, b in conflicts:
        if chromosome[gene_of[a]] == chromosome[gene_of[b]]:
            clashes += 1
    return clashes


# ---------- Turn MIN into MAX for the wheel ----------
def score(chromosome):
    # 0 clashes -> 1.0, 1 clash -> 0.5, 3 clashes -> 0.25 (bigger is better)
    return 1 / (1 + fitness(chromosome))


# ---------- Selection: roulette wheel ----------
def spin_wheel(chromosomes, slices):
    # The pointer stops at a random point between 0 and the size of the wheel
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
    # The slice of each chromosome is its score
    slices = [score(c) for c in population]
    # Spin once for each parent.
    # "for _ in range(num_parents)" repeats num_parents times.
    return [spin_wheel(population, slices) for _ in range(num_parents)]


# ---------- Crossover: single-point ----------
def pick_cut():
    # Pick a random cut point between the first and the last gene
    return random.randint(1, N - 1)


def single_point(parent1, parent2, cut):
    # Child 1 takes the head of parent 1 and the tail of parent 2
    child1 = parent1[:cut] + parent2[cut:]
    # Child 2 takes the head of parent 2 and the tail of parent 1
    child2 = parent2[:cut] + parent1[cut:]
    return child1, child2


def crossover(parent1, parent2):
    # Single-point crossover at a random cut point
    return single_point(parent1, parent2, pick_cut())


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


# ---------- Mutation: swap ----------
# Swap works for integer genes too: gene i is always the same course,
# so when two genes change places, two courses change their slots.
def pick_two_genes():
    # Two different gene positions. random.sample() never takes the same one twice.
    return random.sample(range(N), 2)


def swap(chromosome, i, j):
    # .copy() makes a new list, so the child before mutation does not change
    mutant = chromosome.copy()
    # Gene i and gene j change places (Python can swap two values in one line)
    mutant[i], mutant[j] = mutant[j], mutant[i]
    return mutant


def mutation(chromosome):
    # With probability MUTATION_RATE, swap two random genes
    if random.random() < MUTATION_RATE:
        i, j = pick_two_genes()
        return swap(chromosome, i, j)
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
print_conflicts()

# Use the same random numbers on every run.
# Remove this line to see a new population each time.
random.seed(1)

# Make a small population of 6 random chromosomes
population = [random_chromosome() for _ in range(6)]

# The size of the whole wheel
total = sum(score(c) for c in population)

print("\nPopulation:")
for c in population:
    print(f"  {c}  clashes = {fitness(c)}  score = {score(c):.2f}"
          f"  chance = {score(c) / total * 100:.1f}%")

# Lower is better, so the best timetable has the fewest clashes
best = min(population, key=fitness)
print(f"\nThe best timetable in this population (clashes = {fitness(best)}):")
decode(best)

# Choose the mating pool: one spin of the wheel for each parent
mating_pool = selection(population, NUM_PARENTS)
print(f"\nMating pool ({NUM_PARENTS} parents):")
for c in mating_pool:
    print(f"  {c}  clashes = {fitness(c)}")

# One crossover, step by step.
# We take the first and the last parent of the pool, because they are very different.
# mating_pool[-1] is the last item of the list.
parent1, parent2 = mating_pool[0], mating_pool[-1]
cut = pick_cut()
child1, child2 = single_point(parent1, parent2, cut)
print(f"\nSingle-point crossover, cut after gene {cut}:")
print(f"  Parent 1: {show_cut(parent1, cut)}   clashes = {fitness(parent1)}")
print(f"  Parent 2: {show_cut(parent2, cut)}   clashes = {fitness(parent2)}")
print(f"  Child 1:  {show_cut(child1, cut)}   clashes = {fitness(child1)}")
print(f"  Child 2:  {show_cut(child2, cut)}   clashes = {fitness(child2)}")

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
    print(f"    Children: {children[i]}  {children[i + 1]}"
          f"   clashes = {fitness(children[i])}, {fitness(children[i + 1])}")

# One mutation, step by step, with the first child.
# Here we swap Physics (gene 2) and Programming (gene 3). mutation() picks two genes at random.
child = children[0]
mutant = swap(child, 1, 2)
print("\nSwap of gene 2 (Physics) and gene 3 (Programming): they change their slots")
print(f"  Before: {child}  clashes = {fitness(child)}")
print(f"  After:  {mutant}  clashes = {fitness(mutant)}")

# Mutate all children: each child mutates with probability pm
mutants = mutate_children(children)
print(f"\nMutation of all children (pm = {MUTATION_RATE} per child):")
# mutated counts the children that changed.
# zip() goes over the two lists together.
mutated = 0
for before, after in zip(children, mutants):
    if before != after:
        mutated += 1
    print(f"  {before} -> {after}   changed genes: {changed_text(before, after):<6}"
          f"  clashes {fitness(before)} -> {fitness(after)}")
print(f"  {mutated} of {len(children)} children mutated. With pm = {MUTATION_RATE}, about 1 child in 5 mutates.")
print("  Remove random.seed(1) and run again to see other results.")
# Think: swap keeps the number of exams in each slot. Can it fix every timetable?
