# Problem 5: The 8 Queens

You have a chess board with 8 rows and 8 columns, and 8 queens.
Put the 8 queens on the board so that **no queen can attack another queen**.

A queen can attack any queen in the same row, the same column or the same diagonal.

## Your task

Solve this problem with a genetic algorithm. You decide:

- **Representation:** what does a chromosome look like? What does one gene mean?
- **Fitness:** how do you measure how good a solution is? Higher must be better.
- **Crossover and mutation:** choose the ones that fit your representation.

Selection: **rank selection**. Survival selection is given.

Open `incomplete/5_n_queens.py` and complete every function marked with **TODO**.
When your code works, the program prints the final solution.

## Think about it

Can your chromosome put two queens in the same row? In the same column?
If yes, how does your fitness deal with it?
