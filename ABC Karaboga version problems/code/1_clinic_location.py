"""
Problem 1: Where Should We Build the Clinic? (Artificial Bee Colony)

Five villages want to build one small clinic together. People walk from
their village to the clinic. A village with more families walks more.
Where should we build the clinic, so the total walking of ALL families
is as small as possible?

Representation: a solution is a point [x, y] on the map, in km.
                x and y are between 0 and 10.
Cost:           MINIMIZE total walking = sum of (families * distance)
Bees:           one employed bee for each solution, the same number of
                onlooker bees, and a scout when a solution is stuck.

Run:  python 1_clinic_location.py
"""

import math
import random

# name: ((x, y) position in km, number of families)
villages = {
    "Ain":   ((1, 2), 40),
    "Baida": ((8, 1), 25),
    "Qasr":  ((9, 7), 30),
    "Deir":  ((3, 9), 20),
    "Tal":   ((2, 6), 15),
}

# The search area: every variable is between LOWER and UPPER
LOWER = 0.0
UPPER = 10.0
D = 2                          # number of variables: x and y

# The settings of the bee colony
NUM_SOLUTIONS = 6              # SN: solutions = employed bees = onlooker bees
LIMIT = NUM_SOLUTIONS * D      # failures allowed before a scout replaces a solution
MAX_CYCLES = 40                # MCN: stop after this many cycles

# The best possible total walking (found with a slow search over the
# whole map). The bees do not know this number. We only use it to check.
BEST_POSSIBLE = 586.4


# ---------- The problem ----------
def cost(solution):
    # Total walking of all families to the clinic at this point
    total = 0.0
    # Each value in villages is a pair: (position, families).
    # The for loop puts the two parts into two names.
    for position, families in villages.values():
        # math.dist(p, q) gives the straight-line distance between two points
        total += families * math.dist(solution, position)
    return total


def decode(solution):
    # Print the solution in human terms
    print(f"  Build the clinic at x = {solution[0]:.2f} km, y = {solution[1]:.2f} km")
    # items() gives (name, (position, families)) for each village
    for name, (position, families) in villages.items():
        print(f"    {name:6}: {math.dist(solution, position):.2f} km away, {families} families")
    print(f"  Total walking: {cost(solution):.1f} family-km")


# ---------- The ABC formulas ----------
def fitness(solution_cost):
    # Small cost -> big fitness
    if solution_cost >= 0:
        return 1 / (1 + solution_cost)
    return 1 + abs(solution_cost)


def random_solution():
    # Step 0 formula: x = min + rand(0, 1) * (max - min), for every variable
    solution = []
    for j in range(D):
        solution.append(LOWER + random.random() * (UPPER - LOWER))
    return solution


def make_candidate(solutions, i):
    # A random neighbor solution k (not i itself)
    k = random.randrange(len(solutions))
    while k == i:
        k = random.randrange(len(solutions))

    # One random variable j and a random number phi between -1 and +1
    j = random.randrange(D)
    phi = random.uniform(-1, 1)

    # Copy solution i, then change only variable j.
    # copy() makes a new list, so solution i itself does not change.
    # v = x + phi * (x - neighbor)
    candidate = solutions[i].copy()
    candidate[j] = solutions[i][j] + phi * (solutions[i][j] - solutions[k][j])

    # If the new value is outside the map, put it back on the border
    candidate[j] = min(max(candidate[j], LOWER), UPPER)
    return candidate


def try_to_improve(solutions, trials, i):
    # Greedy selection: keep the better one and count the failures
    candidate = make_candidate(solutions, i)
    if cost(candidate) < cost(solutions[i]):
        solutions[i] = candidate
        trials[i] = 0
    else:
        trials[i] += 1


def probabilities(solutions):
    # p = fitness of the solution / the sum of all fitness
    fitness_list = []
    for solution in solutions:
        fitness_list.append(fitness(cost(solution)))
    total = sum(fitness_list)

    probs = []
    for fit in fitness_list:
        probs.append(fit / total)
    return probs


def choose_solution(probs):
    # Roulette wheel: a big probability is a big slice of the wheel
    spin = random.random()
    total = 0.0
    for i in range(len(probs)):
        total += probs[i]
        if total >= spin:
            return i
    # Safety: if rounding gives no winner, take the last one
    return len(probs) - 1


def scout_phase(solutions, trials):
    # Take the solution with the biggest number of failures
    i = trials.index(max(trials))
    # If it failed too many times, replace it with a random solution
    if trials[i] > LIMIT:
        solutions[i] = random_solution()
        trials[i] = 0
        return True
    return False


# ---------- The main loop ----------
def run_abc():
    # Step 0: random solutions, no failures yet
    solutions = []
    for _ in range(NUM_SOLUTIONS):
        solutions.append(random_solution())
    # [0] * NUM_SOLUTIONS makes a list with NUM_SOLUTIONS zeros
    trials = [0] * NUM_SOLUTIONS

    best = solutions[0].copy()
    for solution in solutions:
        if cost(solution) < cost(best):
            best = solution.copy()

    for cycle in range(1, MAX_CYCLES + 1):
        # Step 1: employed bees, one try for every solution
        for i in range(NUM_SOLUTIONS):
            try_to_improve(solutions, trials, i)

        # Step 2: onlooker bees, good solutions get more tries
        probs = probabilities(solutions)
        for _ in range(NUM_SOLUTIONS):
            i = choose_solution(probs)
            try_to_improve(solutions, trials, i)

        # Step 3: memorize the best solution (before the scout)
        for solution in solutions:
            if cost(solution) < cost(best):
                best = solution.copy()

        # Step 4: scout bee
        scout = scout_phase(solutions, trials)

        # Print every 5 cycles, and always when a scout works
        if cycle % 5 == 0 or scout:
            # "A" if test else "B" gives A when the test is true, else B
            note = "  (a scout found a new random place)" if scout else ""
            print(f"Cycle {cycle:3}: best total walking = {cost(best):.1f}{note}")
    return best


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_abc()

print("\nBest place found:")
decode(best)
print(f"  The best possible total walking is {BEST_POSSIBLE:.1f} family-km")
