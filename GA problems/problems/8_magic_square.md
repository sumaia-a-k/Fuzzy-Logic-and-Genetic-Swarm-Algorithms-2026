# Problem 8: The Magic Square

Put the numbers **1 to 9** in a 3 x 3 square. Use each number only once.
Every row, every column and both diagonals must add up to **15**.

```
? ? ?
? ? ?
? ? ?
```

There are 8 lines to check: 3 rows, 3 columns and 2 diagonals.

## Your task

Solve this problem with a genetic algorithm. You decide:

- **Representation:** what does a chromosome look like? What does one gene mean?
- **Fitness:** how do you measure how good a solution is? Lower must be better.
- **Crossover and mutation:** choose the ones that fit your representation.

Selection: **tournament selection**. Survival selection is given.

Open `incomplete/8_magic_square.py` and complete every function marked with **TODO**.
When your code works, the program prints the final solution.

## Think about it

How many different ways are there to put the numbers 1 to 9 in the square?
A computer can check all of them. What about a 5 x 5 square with the numbers 1 to 25?
