"""
Problem 2: The Shortest Delivery Route (exercise: complete the code)

Samer drives a van from the Warehouse to a Shop in a small city.
The city has 10 places (junctions) and 15 roads. Each road takes some
minutes. Samer does NOT need to visit every place. He only needs the
fastest route from the Warehouse to the Shop.

Representation: a route is a list of place names, for example
                ["Warehouse", "Market", "Square", "Shop"]
Cost:           MINIMIZE the total minutes of the route

Run:  python 2_shortest_route.py

What you have to do:
  Write every function marked with TODO. The comments tell you what each
  function must do. You decide how to do it.
  The map, route_time(), decode() and make_pheromone() are already complete.
  A TODO function stops the program with a message until you write it.
  Use the small tests at the bottom of the file to check each function.
  When everything works, the program prints the best route.
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

# The settings of the ant colony
ALPHA = 1.0           # how much ants follow the pheromone
BETA = 2.0            # how much ants like short roads
RHO = 0.5             # evaporation: the part of pheromone that disappears
Q = 10.0              # the strength of the pheromone that an ant adds
TAU_0 = 1.0           # the start pheromone on every road
NUM_ANTS = 20         # how many ants walk in each iteration
MAX_ITERATIONS = 30   # stop after this many iterations


# ---------- The map (complete) ----------
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


# ---------- The route (complete) ----------
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
    # TODO: return the list of allowed places for the ant.
    # - Allowed = a neighbour of the current place that the ant
    #   has not visited yet (it is not in the route).
    # - Use neighbours[current] to get the neighbours.
    # - The list can be empty. That is a dead end.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("allowed_places() is not written yet")


def choose_next_place(current, allowed, pheromone):
    # TODO: choose the next place with the roulette wheel.
    # - For each allowed place, calculate its desire:
    #     desire = pheromone^ALPHA * closeness^BETA
    #   The pheromone of the road is pheromone[(current, place)].
    #   The closeness of the road is 1 / minutes[(current, place)].
    # - The chance of a place = its desire / the sum of all desires.
    # - Spin the wheel: pick a random number between 0 and the sum
    #   of the desires, then add the desires one by one until you pass it.
    # - Return the chosen place.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("choose_next_place() is not written yet")


def build_route(pheromone):
    # TODO: one ant walks from START to GOAL. Return its route.
    # - Start with the route [START].
    # - Repeat until the last place of the route is GOAL:
    #     a. find the allowed places
    #     b. if there is none, the ant is lost: return None
    #     c. choose the next place and add it to the route
    # - Return the route.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("build_route() is not written yet")


# ---------- Step 2: evaporation ----------
def evaporate(pheromone):
    # TODO: every road loses a part of its pheromone.
    # - New pheromone = (1 - RHO) * old pheromone
    # - Change the values inside the dictionary. Do this for ALL roads.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("evaporate() is not written yet")


# ---------- Step 3: deposit ----------
def deposit(pheromone, routes):
    # TODO: every ant adds pheromone on the roads of its route.
    # - The amount is Q / (route time). A faster route adds more.
    # - Add the amount to every road of the route.
    # - A road works in both directions: update (a, b) and (b, a).
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("deposit() is not written yet")


# ---------- The main loop ----------
def run_aco():
    # TODO: the main loop of the ant colony.
    # 1. Make the start pheromone with make_pheromone().
    # 2. Repeat for iteration = 1, 2, ..., MAX_ITERATIONS:
    #    a. Let NUM_ANTS ants build a route with build_route().
    #       Throw away the lost ants (None). Count them.
    #    b. Evaporation: call evaporate().
    #    c. Deposit: call deposit() with the routes of the ants that arrived.
    #    d. Remember the best route (the smallest time) of all iterations.
    #    e. Print the iteration number, the best time and the number of lost ants.
    # 3. Return the best route.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("run_aco() is not written yet")


# ---------- Test your functions one by one ----------
# Remove the # at the start of a line to run the test.
# print(allowed_places("Warehouse", ["Warehouse"]))
# print(allowed_places("Market", ["Warehouse", "Market"]))
# print(choose_next_place("Warehouse", ["Bridge", "Market"], make_pheromone()))
# print(build_route(make_pheromone()))
# test_pheromone = make_pheromone()
# evaporate(test_pheromone)
# print(test_pheromone[("Warehouse", "Bridge")])    # should be 0.5
# deposit(test_pheromone, [["Warehouse", "Market", "Square", "Park", "Shop"]])
# print(test_pheromone[("Market", "Warehouse")])    # should be 0.5 + 10 / 11


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_aco()

print("\nBest route found:")
print(f"  Route: {best}")
decode(best)
