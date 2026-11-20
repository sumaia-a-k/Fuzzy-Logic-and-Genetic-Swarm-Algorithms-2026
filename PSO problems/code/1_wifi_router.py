"""
Problem 1: Where Should We Put the Wi-Fi Router? (Particle Swarm Optimization)

A family has one Wi-Fi router for the whole flat. The signal gets weak
fast when a room is far from the router. Some rooms use the internet
many hours a day, so they need a strong signal more than other rooms.
Where should we put the router?

Representation: a particle is a point [x, y] on the plan of the flat,
                in meters. x and y are between 0 and 10.
Cost:           MINIMIZE the bad signal of all rooms:
                sum of (hours * distance^2)
PSO:            each particle has a position, a velocity, and a memory
                of its best position. The swarm remembers the best
                position of all particles (g).

Run:  python 1_wifi_router.py
"""

import random

# name: ((x, y) position in meters, hours of internet per day)
rooms = {
    "Living room": ((2, 3), 6),
    "Kitchen":     ((8, 2), 2),
    "Bedroom":     ((2, 8), 3),
    "Kids room":   ((8, 8), 4),
    "Office":      ((5, 9), 5),
}

# The flat: every variable is between LOWER and UPPER
LOWER = 0.0
UPPER = 10.0
D = 2                          # number of variables: x and y

# The settings of the swarm
NUM_PARTICLES = 10             # N: number of particles
MAX_ROUNDS = 30                # stop after this many rounds
W = 0.7                        # inertia weight
C1 = 1.5                       # weight of the particle's own best place
C2 = 1.5                       # weight of the swarm's best place

# The best possible cost (found with a formula, see the problem sheet).
# The swarm does not know this number. We only use it to check.
BEST_POSSIBLE = 289.5


# ---------- The problem ----------
def cost(position):
    # The bad signal of all rooms: hours * distance^2
    total = 0.0
    # Each value in rooms is a pair: (room position, hours).
    # The for loop puts the two parts into two names.
    for room_position, hours in rooms.values():
        dx = position[0] - room_position[0]
        dy = position[1] - room_position[1]
        total += hours * (dx ** 2 + dy ** 2)
    return total


def decode(position):
    # Print the solution in human terms
    print(f"  Put the router at x = {position[0]:.2f} m, y = {position[1]:.2f} m")
    # items() gives (name, (room position, hours)) for each room
    for name, (room_position, hours) in rooms.items():
        dx = position[0] - room_position[0]
        dy = position[1] - room_position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        print(f"    {name:12}: {distance:.2f} m away, {hours} hours a day")
    print(f"  Bad signal (cost): {cost(position):.1f}")


# ---------- The PSO formulas ----------
def random_position():
    # Step 0: a random point inside the flat, for every variable
    position = []
    for j in range(D):
        position.append(LOWER + random.random() * (UPPER - LOWER))
    return position


def random_velocity():
    # Step 0: a small random velocity, between -1 and +1 meter per round
    velocity = []
    for j in range(D):
        velocity.append(random.uniform(-1, 1))
    return velocity


def new_velocity(position, velocity, own_best, swarm_best):
    # Step 3: v = W*v + C1*rand1*(p - x) + C2*rand2*(g - x), for every variable
    result = []
    for j in range(D):
        # New random numbers for every variable
        rand1 = random.random()
        rand2 = random.random()
        inertia = W * velocity[j]
        own_pull = C1 * rand1 * (own_best[j] - position[j])
        swarm_pull = C2 * rand2 * (swarm_best[j] - position[j])
        result.append(inertia + own_pull + swarm_pull)
    return result


def new_position(position, velocity):
    # Step 3: x = x + v, for every variable
    result = []
    for j in range(D):
        value = position[j] + velocity[j]
        # If the particle leaves the flat, put it back on the border
        value = min(max(value, LOWER), UPPER)
        result.append(value)
    return result


def best_of(positions):
    # The position with the smallest cost in a list
    best = positions[0]
    for position in positions:
        if cost(position) < cost(best):
            best = position
    return best.copy()


# ---------- The main loop ----------
def run_pso():
    # Step 0: random positions and velocities
    positions = []
    velocities = []
    for _ in range(NUM_PARTICLES):
        positions.append(random_position())
        velocities.append(random_velocity())

    # Each particle remembers its best place. At the start it is where it stands.
    # copy() makes a new list, so the memory does not change when the particle moves.
    own_bests = []
    for position in positions:
        own_bests.append(position.copy())

    for round_number in range(1, MAX_ROUNDS + 1):
        # Step 1: if a particle is in a better place, update its memory
        for i in range(NUM_PARTICLES):
            if cost(positions[i]) < cost(own_bests[i]):
                own_bests[i] = positions[i].copy()

        # Step 2: the best memory of all particles becomes g
        swarm_best = best_of(own_bests)

        # Step 3: new velocity, then new position, for every particle
        for i in range(NUM_PARTICLES):
            velocities[i] = new_velocity(positions[i], velocities[i],
                                         own_bests[i], swarm_best)
            positions[i] = new_position(positions[i], velocities[i])

        # Print every 5 rounds
        if round_number % 5 == 0:
            print(f"Round {round_number:3}: best cost = {cost(swarm_best):.2f}  "
                  f"at ({swarm_best[0]:.2f}, {swarm_best[1]:.2f})")

    # Step 4: we stop after MAX_ROUNDS. The answer is g.
    return swarm_best


# ---------- Try it ----------
# Use the same random numbers on every run.
# Remove this line to see a new run each time.
random.seed(1)

best = run_pso()

print("\nBest place found:")
decode(best)
print(f"  The best possible cost is {BEST_POSSIBLE:.1f}")
