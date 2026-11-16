"""
Problem 2: How Fast Does the Coffee Cool? (exercise: complete the code)

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

What you have to do:
  Write every function marked with TODO. The comments tell you what each
  function must do. You decide how to do it.
  model(), cost(), decode(), fitness() and choose_solution() are complete.
  A TODO function stops the program with a message until you write it.
  Use the small tests at the bottom of the file to check each function.
  When everything works, the program prints the best model.
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
    # TODO: make one random solution [R, S, k] (Step 0 of the lecture).
    # - For every variable j = 0, 1, 2 use the formula:
    #     x = LOWER[j] + rand(0, 1) * (UPPER[j] - LOWER[j])
    # - random.random() gives a random number from 0 to 1.
    # - Return the list of 3 numbers.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("random_solution() is not written yet")


def make_candidate(solutions, i):
    # TODO: make a new candidate solution near solution i.
    # - Choose a random neighbor k between 0 and len(solutions) - 1.
    #   k must not be i. Choose again while k == i.
    # - Choose one random variable j between 0 and D - 1.
    # - Choose a random phi between -1 and +1 (random.uniform(-1, 1)).
    # - Copy solution i with .copy(). Change ONLY variable j of the copy:
    #     v = x + phi * (x - neighbor)
    # - If the new value is outside LOWER[j] .. UPPER[j],
    #   put it back on the border.
    # - Return the candidate.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("make_candidate() is not written yet")


def try_to_improve(solutions, trials, i):
    # TODO: greedy selection for solution i.
    # - Make a candidate with make_candidate(solutions, i).
    # - If its cost is smaller than the cost of solutions[i]:
    #     put the candidate in solutions[i] and set trials[i] to 0.
    # - Else: add 1 to trials[i].
    # - This function changes the lists. It returns nothing.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("try_to_improve() is not written yet")


def probabilities(solutions):
    # TODO: the chance of each solution for the onlooker bees.
    # - Find the fitness of every solution: fitness(cost(solution)).
    # - p = fitness of the solution / the sum of all fitness
    # - Return the list of probabilities (one for each solution).
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("probabilities() is not written yet")


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
    # TODO: the scout bee (Step 4 of the lecture).
    # - Find the solution i with the biggest number in trials.
    #   Tip: trials.index(max(trials)) gives its position.
    # - If trials[i] > LIMIT: replace solutions[i] with a new
    #   random_solution(), set trials[i] to 0 and return True.
    # - Else return False.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("scout_phase() is not written yet")


# ---------- The main loop ----------
def run_abc():
    # TODO: the main loop of the bee colony.
    # Step 0: make NUM_SOLUTIONS random solutions and a list of zeros
    #         for the trials. Remember the best one (use .copy()).
    # Repeat for cycle = 1, 2, ..., MAX_CYCLES:
    #   Step 1: employed bees. For every i, call try_to_improve().
    #   Step 2: onlooker bees. Find the probabilities ONE time.
    #           Then NUM_SOLUTIONS times: choose i with choose_solution(),
    #           and call try_to_improve().
    #   Step 3: memorize the best solution (save a copy if one is better).
    #   Step 4: call scout_phase(). Count the scouts.
    #   Every 50 cycles print the cycle, the best error and the scouts.
    # Return the best solution.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("run_abc() is not written yet")


# ---------- Test your functions one by one ----------
# Remove the # at the start of a line to run the test.
# print(random_solution())                 # 3 numbers, each inside its range
# test_solutions = [[20.0, 90.0, 0.1], [30.0, 70.0, 0.2], [10.0, 60.0, 0.05]]
# print(make_candidate(test_solutions, 0)) # like [20.0, 90.0, 0.1], but ONE number changed
# print(probabilities(test_solutions))     # the first number is the biggest
# print(sum(probabilities(test_solutions))) # should be 1.0 (or very close)
# test_trials = [0, 0, 0]
# try_to_improve(test_solutions, test_trials, 2)
# print(test_trials)                       # [0, 0, 0] or [0, 0, 1]
# test_trials = [0, LIMIT + 1, 3]
# print(scout_phase(test_solutions, test_trials), test_trials)  # True [0, 0, 3]


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_abc()

print("\nBest model found:")
decode(best)
print(f"  The smallest possible error is about {BEST_POSSIBLE:.2f}")
