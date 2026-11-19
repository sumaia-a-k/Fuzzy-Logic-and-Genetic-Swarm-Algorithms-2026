# Problem 1: The Best Sandwich Price

Nour sells sandwiches. One sandwich costs her **2 dollars** to make.
If the price is high, she earns more for each sandwich, but fewer people buy.
Nour noticed this rule: at a price of **x** dollars, about **100 − 8x** people buy each day.

| Price x | Customers (100 − 8x) | Profit (x − 2) × customers |
|---|---|---|
| 4 | 68 | 136 |
| 6 | 52 | 208 |
| 8 | 36 | 216 |
| 10 | 20 | 160 |

The profit goes up, then down. Which price gives the **biggest** profit?
The price can be anything from 2 to 12 dollars. Below 2 dollars Nour loses money on every sandwich,
so we do not search there.

## How we use the algorithm

This is the Bees Algorithm version of ABC, with the same steps and names as the lecture.

- A **site** is one price x. Fitness = the profit. We want the **maximum**.
- n = 6 scout bees, m = 3 selected sites, n2 = 4 bees for each elite site,
  n1 = 2 bees for each other selected site, a = 0.5, 10 rounds.

Open `code/1_sandwich_price.py`, read it from top to bottom and run it.
Find each step of the lecture (Step 0 to Step 5) in the function `run_bees()`.

## Think about it

1. Look at the column "elite sites" in the output. Why is it 1 in the first rounds and 2 later?
2. Change `A` to 0.01 and run again. Does the bees' answer get worse? Why?
3. Change `N1` to 4, so n1 = n2. Is there still a difference between elite sites and the other selected sites?
4. Here we can find the best price with math (x = 7.25). Why do we need an algorithm like this for other problems?
5. Nour now wants the **smallest** cost, not the biggest profit. What changes in Step 1 and in Step 2?
6. We search from 2 to 12, not from 0 to 12. Would the bees still find the best price with 0 to 12? Why is a good search range still useful?
