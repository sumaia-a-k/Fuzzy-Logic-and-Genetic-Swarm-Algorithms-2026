# Problem 2: How Does the Taxi App Count the Price?

Lina uses a taxi app every week. The app does not show how it counts the price.
She kept 8 old receipts:

| Ride | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Distance (km) | 2.0 | 3.5 | 5.0 | 1.5 | 8.0 | 6.5 | 4.0 | 10.0 |
| Time (minutes) | 6 | 10 | 12 | 8 | 20 | 25 | 9 | 22 |
| Price ($) | 2.75 | 3.85 | 4.95 | 2.60 | 7.20 | 6.90 | 3.95 | 8.40 |

She thinks the app uses this rule:

**price = START + PER_KM · km + PER_MINUTE · minutes**

- **START** = the price when the ride starts
- **PER_KM** = the price of one km
- **PER_MINUTE** = the price of one minute in the car

Our job: find the three numbers that make the rule **fit her receipts best**.

## How we use PSO

- A **particle** is a list [START, PER_KM, PER_MINUTE]. This time we have **3 variables**, and each one has its **own range**:

| Variable | From | To |
|---|---|---|
| START | 0 | 5 |
| PER_KM | 0 | 2 |
| PER_MINUTE | 0 | 1 |

- Each particle also has a **velocity** with 3 numbers. At the start it is small: at most 10 % of the range of each variable.
- **Cost** = the sum of squared errors. For every receipt:
  error = real price − rule price. We square each error and add them all.
  A small cost means the rule is close to the receipts.
- Settings: 20 particles, 100 rounds, w = 0.7, c1 = c2 = 1.5.

## Your task

Open `code/incomplete/2_taxi_fare.py` and complete every function marked with **TODO**:

- `random_position()`: Step 0, a random position
- `random_velocity()`: Step 0, a small random velocity
- `new_velocity()`: the velocity formula v = w·v + c1·rand1·(p − x) + c2·rand2·(g − x)
- `new_position()`: the position formula x = x + v, and the border rule
- `run_pso()`: the main loop with all the steps

Use the small tests at the bottom of the file to check each function.
When your code works, the program prints the three prices and a table of real and rule prices.
You can compare your work with the full solution in `code/2_taxi_fare.py`.

## Think about it

1. Why does each variable need its own range? What would happen if PER_MINUTE could go up to 5?
2. Look at the output: after round 50 the best error does not change any more. Is it good to stop here? Which stop rule from the lecture would stop the program earlier?
3. Use the prices that the swarm found: how much does a ride of 7 km and 15 minutes cost?
4. Change `NUM_PARTICLES` to 3. Is the answer still good? Run it with 3 different seeds.
