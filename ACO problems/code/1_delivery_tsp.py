"""
Problem 1: The Bakery Delivery Tour (Ant Colony Optimization)

Layla works in a bakery. Every morning she delivers bread to 8 places (bakery + 7 places)
and then comes back to the bakery. She visits each place exactly one time.
Which order gives the shortest tour? (This is the famous Traveling
Salesman Problem, TSP.)

Representation: a tour is a list of place numbers, for example [0, 3, 1, ...]
                (0 = the bakery). The ant comes back to the start at the end.
Cost:           MINIMIZE the length of the tour
Ants:           each ant builds one tour, one place at a time
Choice rule:    the chance of a road = its desire / the sum of all desires
                desire = pheromone^ALPHA * closeness^BETA
Pheromone:      evaporation on all roads, then each ant adds Q / tour length
                on the roads of its tour

Run:  python 1_delivery_tsp.py
"""

import math
import random

# name: (x, y) position on a made-up map, in km
places = {
    "Bakery":   (5, 5),
    "Cafe":     (8, 9),
    "Kiosk":    (2, 8),
    "Canteen":  (9, 3),
    "School":   (2, 2),
    "Hotel":    (6, 1),
    "Market":   (5, 8),
    "Pharmacy": (8, 6),
}

# The places in a fixed order: number i is always the same place
names = list(places.keys())

# How many places we have
N = len(names)

# BEST_POSSIBLE km. The ants do not know this number.
# We only use it to check the result.
BEST_POSSIBLE = 28.5

# The settings of the ant colony
ALPHA = 1.0           # how much ants follow the pheromone
BETA = 3.0            # how much ants like short roads
RHO = 0.5             # evaporation: the part of pheromone that disappears
Q = 1.0               # the strength of the pheromone that an ant adds Δτᵏᵢⱼ = Q / Lₖ usually 1
TAU_0 = 1.0           # the start pheromone on every road
NUM_ANTS = 8          # how many ants build a tour in each iteration
MAX_ITERATIONS = 10  # stop after this many iterations


# ---------- The map ----------
# distance = [
#  row 0: [d(0,0), d(0,1), d(0,2), ..., d(0,7)],   # distances from Bakery
#  row 1: [d(1,0), d(1,1), d(1,2), ..., d(1,7)],   # distances from Cafe
#   ...
#  row 7: [d(7,0), d(7,1), d(7,2), ..., d(7,7)],   # distances from Pharmacy
# ]
def make_distance_table():
    # distance[i][j] = straight-line distance between place i and place j
    
    distance = []
    for i in range(N):
        row = []
        for j in range(N):
            # math.dist(p, q) gives the distance between two points: Euclidean distance 
            row.append(math.dist(places[names[i]], places[names[j]]))
        distance.append(row)
    return distance


distance = make_distance_table()


def make_pheromone():
    # One pheromone number for every pair of places. At the start they are equal.
    # symmetry 
    pheromone = []
    for i in range(N):
        # pheromone = 
        #  [[1.0, 1.0, 1.0],    # row 0: roads from place 0 to places 0, 1, 2
        #   [1.0, 1.0, 1.0],    # row 1: roads from place 
        #   [1.0, 1.0, 1.0]]    # row 2: roads from place 2
        pheromone.append([TAU_0] * N)
    return pheromone


# ---------- The tour ----------
# tour is a candidate solution, and tour_length measures it
def tour_length(tour):
    # Add the road from each place to the next one
    length = 0.0
    for i in range(N):
        place = tour[i]
        # (i + 1) % N makes the last place go back to the first place
        next_place = tour[(i + 1) % N]
        length += distance[place][next_place]
    return length


def decode(tour):
    # Print the tour with the place names
    route = ""
    for place in tour:
        route += names[place] + " -> "
    # The tour ends where it started
    route += names[tour[0]]
    print(f"  {route}")
    print(f"  Length: {tour_length(tour):.1f} km")


# ---------- Step 1: build a tour ----------
# current (int 0..7): the place the ant is standing on right now — the last entry of the partial tour
# allowed list[int]: the places the ant has not visited yet — the candidate next steps
# pheromone list[list[float]] (N×N): 	the shared "memory" matrix; pheromone[a][b] = how much pheromone is on the road a→b
def choose_next_place(current, allowed, pheromone):
    # Desire of each allowed place = pheromone^ALPHA * closeness^BETA
    desires = []
    for place in allowed:
        # pheromone[current][place]	τᵢⱼ, the pheromone
        # closeness = 1.0 / distance[current][place]	ηᵢⱼ = 1 / dᵢⱼ
        # (pheromone ** ALPHA) * (closeness ** BETA)	Desire = τ^α · η^β 
        # desires	The numerator for each allowed place
        # sum(desires)	The denominator: the sum of all desires
        closeness = 1.0 / distance[current][place]
        desires.append((pheromone[current][place] ** ALPHA) * (closeness ** BETA))
        
    # Roulette wheel: a big desire gives a big slice of the wheel.
    # spin is a random point on the wheel: a number between 0 and the sum of all desires.
    # Example: desires = [2.0, 0.5, 0.5], so the sum is 3.0 and spin is between 0 and 3.0.
    #   spin from 0 to 2.0   -> the 1st place wins (big slice)
    #   spin from 2.0 to 2.5 -> the 2nd place wins
    #   spin from 2.5 to 3.0 -> the 3rd place wins
    # random.uniform(a, b) — a random number where every value is equally likely
    spin = random.uniform(0, sum(desires))
    total = 0.0
    # Add the desires one by one. The first place where the total
    # reaches spin is the winner. Example: spin = 2.2 -> totals 2.0, 2.5 -> the 2nd place wins.
    for i in range(len(allowed)):
        total += desires[i]
        if total >= spin:
            return allowed[i]
    # Safety: if rounding gives no winner, take the last place
    return allowed[-1]


def build_tour(pheromone):
    # The ant starts at the bakery (place 0)
    # Note:  this code assumes a complete graph: every place is connected to every other place
    tour = [0]
    allowed = list(range(1, N))
    while len(allowed) > 0:
        current = tour[-1]
        next_place = choose_next_place(current, allowed, pheromone)
        tour.append(next_place)
        allowed.remove(next_place)
    return tour


# ---------- Step 2: evaporation ----------
def evaporate(pheromone):
    # Every road loses a part of its pheromone: new = (1 - RHO) * old
    for i in range(N):
        for j in range(N):
            pheromone[i][j] = (1 - RHO) * pheromone[i][j]


# ---------- Step 3: deposit ----------
def deposit(pheromone, tours):
    # Every ant adds Q / (its tour length) on the roads it used.
    # A short tour adds more pheromone than a long tour.
    for tour in tours:
        amount = Q / tour_length(tour)
        for i in range(N):
            a = tour[i]
            b = tour[(i + 1) % N]
            # The road works in both directions
            pheromone[a][b] += amount
            pheromone[b][a] += amount


# ---------- The main loop ----------
def run_aco():
    pheromone = make_pheromone()
    best_tour = None
    best_length = float("inf")

    for iteration in range(1, MAX_ITERATIONS + 1):
        # 1. Every ant builds one tour
        tours = []
        for _ in range(NUM_ANTS):
            tours.append(build_tour(pheromone))

        # 2. Evaporation
        evaporate(pheromone)

        # 3. Deposit
        deposit(pheromone, tours)

        # Remember the best tour of all iterations
        for tour in tours:
            if tour_length(tour) < best_length:
                best_tour = tour
                best_length = tour_length(tour)

        # The average length of the tours of this iteration.
        # It goes down when the colony learns.
        average = sum(tour_length(tour) for tour in tours) / len(tours)

        print(f"Iteration {iteration:3}: best length = {best_length:.1f} km,"
              f"  average length = {average:5.1f} km")
        print("------------------------------------")
    return best_tour


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
# random.seed(1)

best = run_aco()

print("\nBest tour found:")
print(f"  Tour: {best}")
decode(best)
print(f"  The shortest possible tour is {BEST_POSSIBLE:.1f} km")
