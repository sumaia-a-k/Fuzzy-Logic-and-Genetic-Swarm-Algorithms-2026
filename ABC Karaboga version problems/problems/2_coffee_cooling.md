# Problem 2: How Fast Does the Coffee Cool?

Rami makes a cup of coffee. Every 5 minutes he measures its temperature with a thermometer.

| Minute | 0 | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 |
|---|---|---|---|---|---|---|---|---|---|
| Temperature (°C) | 88.3 | 68.2 | 55.1 | 44.8 | 38.5 | 33.2 | 30.3 | 27.5 | 26.2 |

Hot coffee cools fast at the start, then slower and slower, until it reaches
the temperature of the room. Scientists use this model:

**T(t) = R + (S − R) · e<sup>−k·t</sup>**

- **R** = the room temperature
- **S** = the start temperature of the coffee
- **k** = the cooling speed (a big k means the coffee cools fast)

Rami forgot to write down R, S and k. Our job: find the three numbers that make
the model **fit his measurements best**.

## How we use ABC

- A **solution** is a list [R, S, k]. This time we have **3 variables**, and each one has its **own range**:

| Variable | From | To |
|---|---|---|
| R (room) | 0 | 40 |
| S (start) | 50 | 100 |
| k (speed) | 0.01 | 0.5 |

- **Cost** = the sum of squared errors. For every measurement:
  error = measured temperature − model temperature. We square each error and add them all.
  A small cost means the model is close to the measurements.

## Your task

Open `code/incomplete/2_coffee_cooling.py` and complete every function marked with **TODO**:

- `random_solution()`: Step 0
- `make_candidate()`: the formula v = x + φ · (x − neighbor)
- `try_to_improve()`: greedy selection and the failure counter
- `probabilities()`: the chance of each solution for the onlookers
- `scout_phase()`: Step 4
- `run_abc()`: the main loop with all the steps

Use the small tests at the bottom of the file to check each function.
When your code works, the program prints R, S, k and a table of measured and model temperatures.
You can compare your work with the full solution in `code/2_coffee_cooling.py`.

## Think about it

1. Why does each variable need its own range? What would happen if we used the range 50 to 100 for all three variables?
2. Look at the output: sometimes the best error stays the same for 50 cycles or more. Why is ABC slow at the end?
3. Change `MAX_CYCLES` to 100. Is the answer still good?
4. Use the numbers that the bees found: after how many minutes is the coffee at 40 °C?
