"""
Problem 2: The Highest Hill for a Weather Station (ABC, Bees Algorithm version)

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
    # The height of the map at this point.
    # We find the current height from each of the 3 hills. The bee stands
    # on the hill that is highest here, so we keep the biggest value.
    height = 0.0
    # print("Site is ")
    # print(site)
    # Each hill is a group of 3 values. The for loop puts them into 3 names.
    for center, top, width in hills:
        height = max(height, current_height(site, center, top, width))
    return height


def decode(site):
    # Print the site in human terms
    print(f"  Build the station at x = {site[0]:.2f} km, y = {site[1]:.2f} km")
    print(f"  Height: {fitness(site):.1f} m")


# ---------- The steps of the algorithm ----------
def random_site():
    # Step 0 formula: x = min + rand(0, 1) * (max - min), for every variable
    site = []
    for j in range(D):
        site.append(LOWER + random.random() * (UPPER - LOWER))
    return site


def sort_by_fitness(sites):
    # Step 1: sort the sites from best to worst.
    # key=fitness: compare the sites by their fitness.
    # reverse=True: the biggest fitness comes first (we want the maximum).
    sites.sort(key=fitness, reverse=True)


def choose_elite(selected):
    # Step 2: the elite sites are the selected sites above the average
    total = 0.0
    for site in selected:
        total += fitness(site)
    average = total / len(selected)

    # The list is sorted, so the elite sites are the first e sites
    e = 0
    for site in selected:
        if fitness(site) > average:
            e += 1

    # If no site is above the average (all are equal), the best site is elite
    if e == 0:
        e = 1
    return e


def recruit_point(site):
    # One recruited bee: a random point in the neighborhood of the site.
    # Every variable moves at random inside [value - a, value + a].
    new_site = []
    for j in range(D):
        value = random.uniform(site[j] - A, site[j] + A)
        # If it is outside the map, put it back on the border
        value = min(max(value, LOWER), UPPER)
        new_site.append(value)
    return new_site


def search_near(site, num_bees):
    # Step 3: send num_bees bees near the site. Keep the fittest point.
    # The site itself stays if no bee finds a better point.
    best = site
    for _ in range(num_bees):
        new_site = recruit_point(site)
        if fitness(new_site) > fitness(best):
            best = new_site
    return best


# ---------- The main loop ----------
def run_bees():
    # Step 0: n scout bees at random places
    sites = []
    for _ in range(N):
        sites.append(random_site())

    for round_number in range(1, MAX_ROUNDS + 1):
        # Step 1: evaluate and sort (best first)
        sort_by_fitness(sites)

        # Step 2: the first m sites are selected. How many are elite?
        # sites[:M] gives the first M items of the list.
        selected = sites[:M]
        e = choose_elite(selected)

        # Step 3: search near each selected site.
        # Elite sites get N2 bees, the other selected sites get N1 bees.
        new_sites = []
        for i in range(M):
            if i < e:
                num_bees = N2
            else:
                num_bees = N1
            new_sites.append(search_near(selected[i], num_bees))

        # Step 4: the other n - m bees fly to new random places
        random_sites = []
        for _ in range(N - M):
            random_sites.append(random_site())

        # Step 5: the new population = m sites + (n - m) random sites.
        # We sort it to see the best site. The + joins two lists into one.
        sites = new_sites + random_sites
        sort_by_fitness(sites)
        best = sites[0]

        # Was the best site found by a random bee of Step 4?
        # "in" checks if the best site is inside the list random_sites.
        note = ""
        if best in random_sites:
            note = "  <- found by a random bee!"
        print(f"Round {round_number:2}: best point = ({best[0]:.2f}, {best[1]:.2f}),"
              f"  height = {fitness(best):5.1f} m{note}")

    return sites[0]


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(3)

best = run_bees()

print("\nHighest point found:")
decode(best)
print(f"  The highest point of the map is {BEST_POSSIBLE:.1f} m")
