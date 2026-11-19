"""
Problem 2: The Shortest Delivery Route (Ant Colony Optimization)

Samer drives a van from the Warehouse to a Shop in a small city.
The city has 10 places (junctions) and 15 roads. Each road takes some
minutes. Samer does NOT need to visit every place. He only needs the
fastest route from the Warehouse to the Shop.

Representation: a route is a list of place names, for example
                ["Warehouse", "Market", "Square", "Shop"]
Cost:           MINIMIZE the total minutes of the route
Ants:           each ant starts at the Warehouse and walks road by road
                until it reaches the Shop
Allowed places: an ant can only go to a neighbour (a place that has a
                road from here) that it has not visited yet
Dead end:       if the ant has no allowed place, it is lost and
                its route is thrown away
Choice rule:    chance of a road = its desire / the sum of all desires
                desire = pheromone^ALPHA * closeness^BETA
Pheromone:      evaporation on all roads, then each ant that reached the Shop
                adds Q / (route minutes) on the roads of its route

Run:  python 2_shortest_route.py
"""

import random

# (place A, place B, minutes). A road works in both directions.
road_list = [
    ("Warehouse", "Bridge", 3),
    ("Warehouse", "Market", 4),
    ("Warehouse", "Station", 6),
    ("Bridge", "Market", 6),
    ("Bridge", "Hospital", 9),
    ("Market", "Square", 3),
    ("Market", "School", 6),
    ("Station", "Square", 5),
    ("Station", "Port", 6),
    ("Hospital", "Park", 3),
    ("Square", "Park", 2),
    ("Square", "Shop", 7),
    ("School", "Shop", 5),
    ("Port", "Shop", 4),
    ("Park", "Shop", 2),
]

START = "Warehouse"
GOAL = "Shop"

# We checked all possible routes by computer: the fastest route takes
# BEST_POSSIBLE minutes. The ants do not know this number.
# We only use it to check the result.
BEST_POSSIBLE = 11

# The settings of the ant colony
ALPHA = 1.0           # how much ants follow the pheromone
BETA = 2.0            # how much ants like short roads
RHO = 0.5             # evaporation: the part of pheromone that disappears
Q = 10.0              # the strength of the pheromone that an ant adds
TAU_0 = 1.0           # the start pheromone on every road
NUM_ANTS = 20         # how many ants walk in each iteration
MAX_ITERATIONS = 30   # stop after this many iterations


# ---------- The map ----------
def make_road_tables():
    # minutes[(a, b)] = minutes of the road from a to b
    # (a, b) is a tuple (two values together). We use it as a dictionary key.
    # neighbours[a] = the list of places that have a road from a
    minutes = {}
    neighbours = {}
    for place_a, place_b, time in road_list:
        # Save the road in both directions
        minutes[(place_a, place_b)] = time
        minutes[(place_b, place_a)] = time
        # setdefault makes an empty list the first time we see a place
        neighbours.setdefault(place_a, []).append(place_b)
        neighbours.setdefault(place_b, []).append(place_a)
    return minutes, neighbours


minutes, neighbours = make_road_tables()


def make_pheromone():
    # One pheromone number for every road (in both directions).
    # At the start they are all equal.
    pheromone = {}
    for road in minutes:
        pheromone[road] = TAU_0
    return pheromone


# ---------- The route ----------
def route_time(route):
    # Add the minutes of each road in the route
    total = 0
    for i in range(len(route) - 1):
        total += minutes[(route[i], route[i + 1])]
    return total


def decode(route):
    # Print the route with the place names
    print("  " + " -> ".join(route))
    print(f"  Time: {route_time(route)} minutes")


# ---------- Step 1: build a route ----------
def allowed_places(current, route):
    # Allowed = neighbours of the current place that the ant has not visited yet
    allowed = []
    for place in neighbours[current]:
        if place not in route:
            allowed.append(place)
    return allowed


def choose_next_place(current, allowed, pheromone):
    # Desire of each allowed place = pheromone^ALPHA * closeness^BETA
    desires = []
    for place in allowed:
        closeness = 1.0 / minutes[(current, place)]
        desires.append((pheromone[(current, place)] ** ALPHA) * (closeness ** BETA))

    # Roulette wheel: a big desire gives a big slice of the wheel
    spin = random.uniform(0, sum(desires))
    total = 0.0
    for i in range(len(allowed)):
        total += desires[i]
        if total >= spin:
            return allowed[i]
    # Safety: if rounding gives no winner, take the last place
    return allowed[-1]


def build_route(pheromone):
    # The ant starts at the warehouse and walks until it reaches the shop
    route = [START]
    while route[-1] != GOAL:
        allowed = allowed_places(route[-1], route)
        if len(allowed) == 0:
            # Dead end: the ant is lost
            return None
        route.append(choose_next_place(route[-1], allowed, pheromone))
    return route


# ---------- Step 2: evaporation ----------
def evaporate(pheromone):
    # Every road loses a part of its pheromone: new = (1 - RHO) * old
    for road in pheromone:
        pheromone[road] = (1 - RHO) * pheromone[road]


# ---------- Step 3: deposit ----------
def deposit(pheromone, routes):
    # Every ant adds Q / (its route minutes) on the roads it used.
    # A fast route adds more pheromone than a slow route.
    for route in routes:
        amount = Q / route_time(route)
        for i in range(len(route) - 1):
            # The road works in both directions
            pheromone[(route[i], route[i + 1])] += amount
            pheromone[(route[i + 1], route[i])] += amount


# ---------- The main loop ----------
def run_aco():
    pheromone = make_pheromone()
    best_route = None
    best_time = float("inf")

    for iteration in range(1, MAX_ITERATIONS + 1):
        # 1. Every ant walks. Lost ants (None) are thrown away.
        routes = []
        lost = 0
        for _ in range(NUM_ANTS):
            route = build_route(pheromone)
            if route is None:
                lost += 1
            else:
                routes.append(route)

        # 2. Evaporation
        evaporate(pheromone)

        # 3. Deposit
        deposit(pheromone, routes)

        # Remember the best route of all iterations
        for route in routes:
            if route_time(route) < best_time:
                best_route = route
                best_time = route_time(route)

        # The average time of the ants that reached the shop.
        # It goes down when the colony learns.
        average = sum(route_time(route) for route in routes) / len(routes)

        print(f"Iteration {iteration:3}: best time = {best_time} min,"
              f"  average time = {average:5.1f} min,  lost ants = {lost}")

    return best_route


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_aco()

print("\nBest route found:")
print(f"  Route: {best}")
decode(best)
print(f"  The fastest possible route takes {BEST_POSSIBLE} minutes")
