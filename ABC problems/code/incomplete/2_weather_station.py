"""
Problem 2: The Highest Hill for a Weather Station (exercise: complete the code)

A town wants to build a weather station on the highest point of a hilly
area. The area is 10 km x 10 km. It has three hills: a wide hill (60 m),
a small hill (40 m) and a narrow, high hill (80 m).
The bees cannot see the map. They can only stand on a point and measure
its height. The wide hill is easy to find, but it is not the highest one.
Can the bees find the top of the high hill?

Representation: a site is a point [x, y] on the map, in km.
                x and y are between 0 and 10.
Fitness:        MAXIMIZE the height of the point (in meters)
Bees:           n scout bees, the best m sites are selected, the elite sites
                (better than the average) get n2 bees each, the other selected
                sites get n1 bees each, and n - m bees search at random.

Run:  python 2_weather_station.py

What you have to do:
  Write every function marked with TODO. The comments tell you what each
  function must do. You decide how to do it.
  current_height(), decode() and sort_by_fitness() are complete.
  A TODO function stops the program with a message until you write it.
  Use the small tests at the bottom of the file to check each function.
  When everything works, the program prints the highest point it found.
"""

import math
import random

# Each hill: (center (x, y) in km, height in meters, width in km)
hills = [
    ((2.0, 3.0), 60, 3.0),    # wide hill
    ((7.5, 7.0), 80, 0.7),    # narrow, high hill
    ((8.0, 2.0), 40, 1.5),    # small hill
]

# The search range of x and y
LOWER = 0.0
UPPER = 10.0
D = 2             # number of variables: x and y

# The settings of the bees
N = 10            # n: number of scout bees
M = 4             # m: number of selected sites
N2 = 5            # n2: bees for each elite site
N1 = 2            # n1: bees for each other selected site (n1 < n2)
A = 0.5           # a: size of the neighborhood, we search in [x - a, x + a]
MAX_ROUNDS = 20   # stop after this many rounds

# The highest point is the top of the high hill: 80 m at (7.5, 7).
# The bees do not know this. We only use it to check.
BEST_POSSIBLE = 80.0


# ---------- The problem ----------
def current_height(site, center, top, width):
    # The height of the ground at this point, from ONE hill.
    # top is the height of the hill's top. At the top (distance 0) the
    # result is top. Far from the top the result goes down to 0.
    # math.dist gives the distance from the point to the hill center.
    distance = math.dist(site, center)
    return top * math.exp(-distance ** 2 / (2 * width ** 2))


def fitness(site):
    # TODO: return the height of the map at this site.
    # - current_height(site, center, top, width) gives the height at the
    #   site from ONE hill.
    # - The map has 3 hills (the list hills at the top of the file).
    # - Think: which hill is the bee standing on? What is the height there?
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("fitness() is not written yet")


def decode(site):
    # Print the site in human terms
    print(f"  Build the station at x = {site[0]:.2f} km, y = {site[1]:.2f} km")
    print(f"  Height: {fitness(site):.1f} m")


# ---------- The steps of the algorithm ----------
def random_site():
    # TODO: make one random site [x, y] (Step 0 of the lecture).
    # - For every variable j = 0, 1 use the formula:
    #     value = LOWER + rand(0, 1) * (UPPER - LOWER)
    # - random.random() gives a random number from 0 to 1.
    # - Return the list of 2 numbers.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("random_site() is not written yet")


def sort_by_fitness(sites):
    # Step 1: sort the sites from best to worst.
    # key=fitness: compare the sites by their fitness.
    # reverse=True: the biggest fitness comes first (we want the maximum).
    sites.sort(key=fitness, reverse=True)


def choose_elite(selected):
    # TODO: Step 2. Find e = the number of elite sites.
    # - selected is the list of the m best sites, already sorted (best first).
    # - Find the average fitness of the selected sites.
    # - Count the sites with fitness bigger than the average. This is e.
    # - If e is 0 (all sites are equal), set e = 1: the best site is elite.
    # - Return e.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("choose_elite() is not written yet")


def recruit_point(site):
    # TODO: one recruited bee lands near the site.
    # - For every variable j, choose a random value between
    #   site[j] - A and site[j] + A. Use random.uniform(low, high).
    # - If the value is below LOWER or above UPPER, put it on the border.
    # - Return the new point [x, y].
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("recruit_point() is not written yet")


def search_near(site, num_bees):
    # TODO: Step 3. Send num_bees bees near the site. Keep the fittest point.
    # - Start with best = site.
    # - num_bees times: make a point with recruit_point(site).
    #   If its fitness is bigger than the fitness of best, it is the new best.
    # - Return best. (If no bee was better, the site itself stays.)
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("search_near() is not written yet")


# ---------- The main loop ----------
def run_bees():
    # TODO: the main loop of the algorithm.
    # Step 0: make a list of N random sites.
    # Repeat for round_number = 1, 2, ..., MAX_ROUNDS:
    #   Step 1: sort the sites with sort_by_fitness().
    #   Step 2: selected = the first M sites (sites[:M]).
    #           e = choose_elite(selected).
    #   Step 3: for each selected site i = 0 ... M - 1:
    #           N2 bees if i < e (elite), else N1 bees.
    #           Keep the result of search_near() in a new list.
    #   Step 4: make N - M random sites with random_site().
    #   Step 5: the new population = the M sites of Step 3 + the random sites.
    #           Sort it and print the round number, the best point and its height.
    # Return the best site.
    # Delete the next line when you write your code.
    # It stops the program with a message.
    raise NotImplementedError("run_bees() is not written yet")


# ---------- Test your functions one by one ----------
# Remove the # at the start of a line to run the test.
# print(fitness([7.5, 7.0]))               # should be 80.0 (top of the high hill)
# print(fitness([2.0, 3.0]))               # should be 60.0 (top of the wide hill)
# print(fitness([5.0, 5.0]))               # should be about 29.1
# print(random_site())                     # 2 numbers between 0 and 10
# test_selected = [[2.0, 3.0], [1.0, 3.0], [5.0, 5.0], [9.0, 9.0]]
# print(choose_elite(test_selected))       # should be 2
# print(choose_elite([[2.0, 3.0]]))        # should be 1 (only one site)
# print(recruit_point([5.0, 5.0]))         # 2 numbers between 4.5 and 5.5
# print(recruit_point([0.1, 9.9]))         # stays inside 0 ... 10
# better = search_near([7.0, 7.0], 5)
# print(fitness(better) >= fitness([7.0, 7.0]))   # should be True


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(3)

best = run_bees()

print("\nHighest point found:")
decode(best)
print(f"  The highest point of the map is {BEST_POSSIBLE:.1f} m")
