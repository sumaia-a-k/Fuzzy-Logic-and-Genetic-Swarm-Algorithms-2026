# Problem 7: The Hiking Backpack

Rami goes on a one-day hike in the mountains. He has 12 items at home,
but his backpack can carry **only 10 kg**.

Each item has a weight and a value (how useful it is on the hike).
Choose the items with the **biggest total value** that are **not heavier than 10 kg**.

| Item | Weight (kg) | Value |
|---|---|---|
| Water | 3 | 10 |
| Sandwiches | 1 | 7 |
| Hammock | 4 | 9 |
| Rain coat | 2 | 8 |
| Sweater | 1 | 6 |
| First aid | 1 | 9 |
| Torch | 1 | 5 |
| Camera | 1 | 4 |
| Small stove | 2 | 5 |
| Rope | 1 | 3 |
| Book | 1 | 2 |
| Guitar | 3 | 4 |

## Your task

Solve this problem with a genetic algorithm. You decide:

- **Representation:** what does a chromosome look like? What does one gene mean?
- **Fitness:** how do you measure how good a solution is? Higher must be better.
- **Crossover and mutation:** choose the ones that fit your representation.

Selection: **roulette wheel selection**. Survival selection is given.

Open `incomplete/7_hiking_backpack.py` and complete every function marked with **TODO**.
When your code works, the program prints the final solution.

## Think about it

We do not know the best value, so the program does not stop early.
How can we know if the genetic algorithm found the best backpack?
