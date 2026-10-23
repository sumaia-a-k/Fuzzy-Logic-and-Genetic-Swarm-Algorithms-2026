"""
Problem 3: The Exam Timetable

The faculty has 8 final exams and 3 exam slots.
Two courses that share students cannot have their exams in the same slot.

Representation: integer, one gene per course (gene = slot number 0, 1 or 2)
Fitness:        MINIMIZE  the number of clashes   (0 = a perfect timetable)
Selection:      roulette wheel on the score 1 / (1 + clashes) (bigger is better)

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
