"""
Problem 1: The Best Sandwich Price (ABC, Bees Algorithm version)

Nour sells sandwiches. One sandwich costs her 2 dollars to make.
A high price gives more money for each sandwich, but fewer people buy.
Nour noticed: at a price of x dollars, about (100 - 8x) people buy each day.
Which price gives the biggest profit?

Representation: a site is one number x = the price in dollars, from 2 to 12.
                Below 2 dollars Nour loses money, so we do not search there.
Fitness:        MAXIMIZE profit = (x - 2) * (100 - 8x)
Bees:           n scout bees, the best m sites are selected, the elite sites
                (better than the average) get n2 bees each, the other selected
                sites get n1 bees each, and n - m bees search at random.

Run:  python 1_sandwich_price.py
"""

import random

# The search range of the price.
# Below 2 dollars (the cost of one sandwich) Nour loses money.
LOWER = 2.0
UPPER = 12.0

# The settings of the bees (the same as in the lecture example)
N = 6             # n: number of scout bees
M = 3             # m: number of selected sites
N2 = 4            # n2: bees for each elite site
N1 = 2            # n1: bees for each other selected site (n1 < n2)
A = 0.5           # a: size of the neighborhood, we search in [x - a, x + a]
MAX_ROUNDS = 10   # stop after this many rounds

# The best possible profit (from math, at x = 7.25).
# The bees do not know this number. We only use it to check.
BEST_POSSIBLE = 220.5


# ---------- The problem ----------
def fitness(x):
    # The profit of one day at price x
    customers = 100 - 8 * x
    return (x - 2) * customers


def decode(x):
    # Print the site in human terms
    print(f"  Price:     {x:.2f} dollars")
    print(f"  Customers: {100 - 8 * x:.0f} per day")
    print(f"  Profit:    {fitness(x):.2f} dollars per day")


# ---------- The steps of the algorithm ----------
def random_site():
    # Step 0 formula: x = min + rand(0, 1) * (max - min)
    return LOWER + random.random() * (UPPER - LOWER)


def sort_by_fitness(sites):
    # Step 1: sort the sites from best to worst.
    # key=fitness: compare the sites by their fitness.
    # reverse=True: the biggest fitness comes first (we want the maximum).
    sites.sort(key=fitness, reverse=True)


def choose_elite(selected):
    # Step 2: the elite sites are the selected sites above the average
    total = 0.0
    for x in selected:
        total += fitness(x)
    average = total / len(selected)

    # The list is sorted, so the elite sites are the first e sites
    e = 0
    for x in selected:
        if fitness(x) > average:
            e += 1

    # If no site is above the average (all are equal), the best site is elite
    if e == 0:
        e = 1
    return e


def recruit_point(x):
    # One recruited bee: a random point in the neighborhood [x - a, x + a]
    new_x = random.uniform(x - A, x + A)
    # If it is outside the range, put it back on the border
    new_x = min(max(new_x, LOWER), UPPER)
    return new_x


def search_near(x, num_bees):
    # Step 3: send num_bees bees near site x. Keep the fittest point.
    # The site itself stays if no bee finds a better point.
    best = x
    for _ in range(num_bees):
        new_x = recruit_point(x)
        if fitness(new_x) > fitness(best):
            best = new_x
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
        for _ in range(N - M):
            new_sites.append(random_site())

        # Step 5: the new population. We sort it to see the best site.
        sites = new_sites
        sort_by_fitness(sites)
        print(f"Round {round_number:2}: best price = {sites[0]:5.2f} dollars,"
              f"  profit = {fitness(sites[0]):6.2f}  (elite sites: {e})")

    return sites[0]


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
# random.seed(15)

best = run_bees()

print("\nBest price found:")
decode(best)
print(f"  The best possible profit is {BEST_POSSIBLE:.2f} dollars per day")
