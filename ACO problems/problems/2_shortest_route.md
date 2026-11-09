# Problem 2: The Shortest Delivery Route

Samer drives a van from the **Warehouse** to a **Shop**.
The city has 10 places and 15 roads. Each road takes some minutes.
Samer does **not** have to visit every place. He wants the **fastest route**
from the Warehouse to the Shop.

| Road | Minutes |
|---|---|
| Warehouse - Bridge | 3 |
| Warehouse - Market | 4 |
| Warehouse - Station | 6 |
| Bridge - Market | 6 |
| Bridge - Hospital | 9 |
| Market - Square | 3 |
| Market - School | 6 |
| Station - Square | 5 |
| Station - Port | 6 |
| Hospital - Park | 3 |
| Square - Park | 2 |
| Square - Shop | 7 |
| School - Shop | 5 |
| Port - Shop | 4 |
| Park - Shop | 2 |

Every road works in both directions.

## Your task

Solve this problem with **ant colony optimization**. An ant starts at the
Warehouse and walks from place to place until it reaches the Shop.

- An ant never visits the same place twice.
- If an ant has no place to go (a dead end), it is lost. We throw its route away.
- Use the choice rule from the lecture: desire = pheromone^alpha * closeness^beta.

Open `incomplete/2_shortest_route.py` and complete every function marked with **TODO**.
When your code works, the program prints the best route.

## Think about it

1. In problem 1 (the bakery tour) the ant could go to any place it had not visited.
   Here the ant can only use the roads of the map. How does this change the list of **allowed places**?
2. The road Warehouse - Bridge is the shortest road from the Warehouse. Is it a good first step? Why or why not?
3. What happens if you set `RHO = 0.9`? And `RHO = 0.05`?
4. What happens if you set `BETA = 0`? Do the ants still find a good route?
