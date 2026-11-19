"""
Problem 2: How Fast Does the Coffee Cool? (Artificial Bee Colony)

Rami makes a cup of coffee. Every 5 minutes he measures its temperature.
Hot coffee cools fast at the start, then slower and slower, until it
reaches the temperature of the room. Scientists use this model:

    T(t) = R + (S - R) * e^(-k * t)

    R = room temperature, S = start temperature, k = cooling speed

Rami forgot to write down R, S and k. We look for the three numbers that
make the model fit his measurements best.

Representation: a solution is a list [R, S, k]. Each number has its own
                range: R from 0 to 40, S from 50 to 100, k from 0.01 to 0.5.
Cost:           MINIMIZE the sum of squared errors
                (measured temperature - model temperature) ^ 2

Run:  python 2_coffee_cooling.py
"""

import math
import random

# Rami's measurements: (minute, temperature in °C)
measurements = [
    (0, 88.3), (5, 68.2), (10, 55.1), (15, 44.8), (20, 38.5),
    (25, 33.2), (30, 30.3), (35, 27.5), (40, 26.2),
]

# The range of each variable: [R, S, k]
LOWER = [0.0, 50.0, 0.01]
UPPER = [40.0, 100.0, 0.5]
D = 3                          # number of variables: R, S and k

# The settings of the bee colony
NUM_SOLUTIONS = 20             # SN: solutions = employed bees = onlooker bees
LIMIT = NUM_SOLUTIONS * D      # failures allowed before a scout replaces a solution
MAX_CYCLES = 500               # MCN: stop after this many cycles

# The smallest possible error (found with a slow search).
# The bees do not know this number. We only use it to check.
BEST_POSSIBLE = 0.56


# ---------- The problem ----------
def model(solution, minute):
    # The temperature that the model gives at this minute
    # Put the 3 values of the list into 3 names
    room, start, speed = solution
    return room + (start - room) * math.exp(-speed * minute)


def cost(solution):
    # Sum of squared errors: a small cost means a good fit
    total = 0.0
    # Each measurement is a pair: (minute, temperature)
    for minute, measured in measurements:
        error = measured - model(solution, minute)
        total += error ** 2
    return total


def decode(solution):
    # Print the solution in human terms
    room, start, speed = solution
    print(f"  Room temperature R  = {room:.1f} °C")
    print(f"  Start temperature S = {start:.1f} °C")
    print(f"  Cooling speed k     = {speed:.3f}")
    print("  Minute   measured   model")
    for minute, measured in measurements:
        print(f"  {minute:6}   {measured:8.1f}   {model(solution, minute):5.1f}")
    print(f"  Sum of squared errors: {cost(solution):.2f}")


# ---------- The ABC formulas ----------
def fitness(solution_cost):
    # Small cost -> big fitness
    if solution_cost >= 0:
        return 1 / (1 + solution_cost)
    return 1 + abs(solution_cost)


def random_solution():
    # Step 0 formula: x = min + rand(0, 1) * (max - min).
    # Each variable uses its own range.
    solution = []
    for j in range(D):
        solution.append(LOWER[j] + random.random() * (UPPER[j] - LOWER[j]))
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
    candidate = solutions[i].copy()
    candidate[j] = solutions[i][j] + phi * (solutions[i][j] - solutions[k][j])

    # If the new value is outside its range, put it back on the border
    candidate[j] = min(max(candidate[j], LOWER[j]), UPPER[j])
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

    scouts = 0
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
        if scout_phase(solutions, trials):
            scouts += 1

        if cycle % 50 == 0:
            print(f"Cycle {cycle:3}: best error = {cost(best):8.3f},  scouts so far = {scouts}")
    return best


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_abc()

print("\nBest model found:")
decode(best)
print(f"  The smallest possible error is about {BEST_POSSIBLE:.2f}")
