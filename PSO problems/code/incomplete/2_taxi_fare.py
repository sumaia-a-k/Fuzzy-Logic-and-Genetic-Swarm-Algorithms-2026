"""
Problem 2: How Does the Taxi App Count the Price? (exercise: complete the code)

Lina uses a taxi app every week. The app does not show how it counts the
price. She kept 8 old receipts: the distance, the time and the price.
She thinks the app uses this rule:

    price = START + PER_KM * km + PER_MINUTE * minutes

We look for the three numbers that fit her receipts best.

Representation: a particle is a list [START, PER_KM, PER_MINUTE].
                Each number has its own range:
                START from 0 to 5, PER_KM from 0 to 2, PER_MINUTE from 0 to 1.
Cost:           MINIMIZE the sum of squared errors
                (real price - rule price) ^ 2

Run:  python 2_taxi_fare.py

What you have to do:
  Write every function marked with TODO. The comments tell you what each
  function must do. You decide how to do it.
  rule_price(), cost(), decode() and best_of() are complete.
  A TODO function stops the program with a message until you write it.
  Use the small tests at the bottom of the file to check each function.
  When everything works, the program prints the best rule.
"""

import random

# Lina's receipts: (km, minutes, price in $)
receipts = [
    (2.0, 6, 2.75), (3.5, 10, 3.85), (5.0, 12, 4.95), (1.5, 8, 2.60),
    (8.0, 20, 7.20), (6.5, 25, 6.90), (4.0, 9, 3.95), (10.0, 22, 8.40),
]

# The range of each variable: [START, PER_KM, PER_MINUTE]
LOWER = [0.0, 0.0, 0.0]
UPPER = [5.0, 2.0, 1.0]
D = 3                          # number of variables

# The settings of the swarm
NUM_PARTICLES = 20             # N: number of particles
MAX_ROUNDS = 100               # stop after this many rounds
W = 0.7                        # inertia weight
C1 = 1.5                       # weight of the particle's own best place
C2 = 1.5                       # weight of the swarm's best place

# The smallest possible error (found with a formula from statistics).
# The swarm does not know this number. We only use it to check.
BEST_POSSIBLE = 0.0226


# ---------- The problem ----------
def rule_price(position, km, minutes):
    # The price that the rule gives for one ride
    # Put the 3 values of the list into 3 names
    start, per_km, per_minute = position
    return start + per_km * km + per_minute * minutes


def cost(position):
    # Sum of squared errors: a small cost means the rule fits the receipts
    total = 0.0
    # Each receipt has 3 parts: (km, minutes, price)
    for km, minutes, price in receipts:
        error = price - rule_price(position, km, minutes)
        total += error ** 2
    return total


def decode(position):
    # Print the solution in human terms
    start, per_km, per_minute = position
    print(f"  Start price       = ${start:.2f}")
    print(f"  Price per km      = ${per_km:.2f}")
    print(f"  Price per minute  = ${per_minute:.2f}")
    print("     km   minutes   real price   rule price")
    for km, minutes, price in receipts:
        print(f"  {km:5.1f}   {minutes:7}   {price:10.2f}   {rule_price(position, km, minutes):10.2f}")
    print(f"  Sum of squared errors: {cost(position):.4f}")


# ---------- The PSO formulas ----------
def random_position():
    # TODO: make one random position [START, PER_KM, PER_MINUTE] (Step 0).
    # - For every variable j = 0, 1, 2 use the formula:
    #     x = LOWER[j] + rand(0, 1) * (UPPER[j] - LOWER[j])
    # - random.random() gives a random number from 0 to 1.
    # - Return the list of 3 numbers.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("random_position() is not written yet")


def random_velocity():
    # TODO: make one small random velocity (Step 0).
    # - For every variable j: size = 0.1 * (UPPER[j] - LOWER[j])
    #   (10 % of the range of that variable).
    # - The velocity of variable j is a random number from -size to +size.
    #   random.uniform(a, b) gives a random number from a to b.
    # - Return the list of 3 numbers.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("random_velocity() is not written yet")


def new_velocity(position, velocity, own_best, swarm_best):
    # TODO: the velocity formula of the lecture (Step 3).
    # - For every variable j:
    #     take two NEW random numbers rand1 and rand2 (random.random()),
    #     v = W * velocity[j] + C1 * rand1 * (own_best[j] - position[j])
    #                         + C2 * rand2 * (swarm_best[j] - position[j])
    # - Return the list of the 3 new velocities.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("new_velocity() is not written yet")


def new_position(position, velocity):
    # TODO: the position formula of the lecture (Step 3).
    # - For every variable j: new value = position[j] + velocity[j]
    # - If the new value is outside LOWER[j] .. UPPER[j],
    #   put it back on the border. Tip: min(max(value, LOWER[j]), UPPER[j])
    # - Return the list of the 3 new values.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("new_position() is not written yet")


def best_of(positions):
    # The position with the smallest cost in a list
    best = positions[0]
    for position in positions:
        if cost(position) < cost(best):
            best = position
    return best.copy()


# ---------- The main loop ----------
def run_pso():
    # TODO: the main loop of PSO.
    # Step 0: make NUM_PARTICLES random positions and NUM_PARTICLES random
    #         velocities (two lists). Each particle's memory (own_bests)
    #         starts as a copy of its position. Use .copy().
    # Repeat for round_number = 1, 2, ..., MAX_ROUNDS:
    #   Step 1: for every particle i: if cost(positions[i]) is smaller than
    #           cost(own_bests[i]), save a copy of positions[i] in own_bests[i].
    #   Step 2: swarm_best = best_of(own_bests)
    #   Step 3: for every particle i: first the new velocity with
    #           new_velocity(), then the new position with new_position().
    #   Every 10 rounds print the round number and the best error.
    # Step 4: after MAX_ROUNDS, return swarm_best.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("run_pso() is not written yet")


# ---------- Test your functions one by one ----------
# Remove the # at the start of a line to run the test.
# print(random_position())        # 3 numbers, each inside its own range
# print(random_velocity())        # 3 small numbers, like [0.3, -0.1, 0.05]
# print(new_velocity([1.0, 0.5, 0.1], [1.0, 1.0, 1.0], [1.0, 0.5, 0.1], [1.0, 0.5, 0.1]))
#                                 # [0.7, 0.7, 0.7]: p = g = x, so only W * v is left
# print(new_position([4.9, 1.0, 0.5], [0.5, 0.2, -0.1]))
#                                 # [5.0, 1.2, 0.4]: START is put back on the border 5.0


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_pso()

print("\nBest rule found:")
decode(best)
print(f"  The smallest possible error is about {BEST_POSSIBLE:.4f}")
