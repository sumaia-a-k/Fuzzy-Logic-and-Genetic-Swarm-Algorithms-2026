# Problem 6: The Eid Dinner Table

Grandma invites 8 family members to Eid dinner. They all sit at **one round table**.
Some people love to sit together, and some people always argue.

Find a seating plan where **every person sits next to friends**,
and nobody sits next to someone they argue with.

The guests: Grandma, Grandpa, Ahmad, Lina, Omar, Sara, Rami, Huda

| Friends (happy together) | Argue (keep them apart) |
|---|---|
| Grandma and Sara | Omar and Ahmad |
| Sara and Omar | Rami and Lina |
| Omar and Rami | Sara and Grandpa |
| Rami and Huda | Huda and Grandma |
| Huda and Ahmad | Ahmad and Grandpa |
| Ahmad and Lina | |
| Lina and Grandpa | |
| Grandpa and Grandma | |
| Grandma and Lina | |
| Omar and Huda | |

The table is round, so the person in seat 8 also sits next to the person in seat 1.

## Your task

Solve this problem with a genetic algorithm. You decide:

- **Representation:** what does a chromosome look like? What does one gene mean?
- **Fitness:** how do you measure how good a solution is? Higher must be better.
- **Crossover and mutation:** choose the ones that fit your representation.

Selection: **tournament selection**. Survival selection is given.

Open `incomplete/6_eid_dinner_table.py` and complete every function marked with **TODO**.
When your code works, the program prints the final solution.

## Think about it

If you turn the whole table one seat to the left, is it a new solution or the same one?
