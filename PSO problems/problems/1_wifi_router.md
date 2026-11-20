# Problem 1: Where Should We Put the Wi-Fi Router?

A family has **one** Wi-Fi router for the whole flat.
The signal gets weak fast when a room is far from the router.
Some rooms use the internet many hours a day, so they need a strong signal more than other rooms.

| Room | Position (x, y) in meters | Internet hours per day |
|---|---|---|
| Living room | (2, 3) | 6 |
| Kitchen | (8, 2) | 2 |
| Bedroom | (2, 8) | 3 |
| Kids room | (8, 8) | 4 |
| Office | (5, 9) | 5 |

The router can be anywhere in the flat: x and y are between 0 and 10 m.

**Bad signal (cost)** = for every room: hours × distance², then add them all.
We use distance² (distance × distance) because the signal gets weak fast when the room is far.

Example: if we put the router in the living room (2, 3), the living room has a perfect signal,
but the office is 6.7 m away. The total cost is 618.
Can we find a better place?

## How we use PSO

- A **particle** is a point [x, y]. This is a possible place for the router.
- Each particle also has a **velocity** [vx, vy]: how far it moves in one round.
- **Cost** = bad signal. We want it small.
- Each particle remembers its best place (p). The swarm remembers the best place of all particles (g).
- Settings: 10 particles, 30 rounds, w = 0.7, c1 = c2 = 1.5.

Open `code/1_wifi_router.py`, read it from top to bottom and run it.
Find each step of the lecture (Step 0 to Step 4) in the function `run_pso()`.

## Think about it

1. The best place is closer to the living room and the office than to the kitchen. Why?
2. For this cost there is a short formula for the best place: the average point,
   where each room counts by its hours: x = (6·2 + 2·8 + 3·2 + 4·8 + 5·5) / 20.
   Find x and y by hand. Did the swarm find the same place?
3. Change `W` to 0 and run again. Then change it to 0.95. What changes in the output? Why?
4. Change `C2` to 0 (the particles do not share g). Does the swarm still find the best place?
