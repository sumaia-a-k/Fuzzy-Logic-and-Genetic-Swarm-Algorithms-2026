# Problem 1: Where Should We Build the Clinic?

Five villages want to build **one** small clinic together.
People walk from their village to the clinic. A village with more families walks more.
We want the place where the **total walking of all families** is as small as possible.

| Village | Position (x, y) in km | Families |
|---|---|---|
| Ain | (1, 2) | 40 |
| Baida | (8, 1) | 25 |
| Qasr | (9, 7) | 30 |
| Deir | (3, 9) | 20 |
| Tal | (2, 6) | 15 |

The clinic can be anywhere on the map: x and y are between 0 and 10 km.

**Total walking** = for every village: families × distance to the clinic, then add them all.

Example: if we build the clinic in Tal (2, 6), the families of Tal walk 0 km,
but the 40 families of Ain walk 4.1 km each. The total walking is 635.6 family-km.
Can we find a better place?

## How we use ABC

- A **solution** is a point [x, y]. This is the place of a food source.
- **Cost** = total walking. We want it small.
- The bees try small changes near the solutions, keep the better ones,
  and a scout tries a new random place when a solution is stuck.

Open `code/1_clinic_location.py`, read it from top to bottom and run it.
Find each step of the lecture (Step 0 to Step 4) in the function `run_abc()`.

## Think about it

1. The best place is not in a village. Why is it not in Ain, the biggest village?
2. A friend says: "Just take the average point of the villages, where each village counts by its families."
   This point is (4.62, 4.50). Add `print(cost([4.62, 4.50]))` to the code. Is it better than the bees' answer?
3. Change the families of Ain from 40 to 80. Run again. Where does the clinic go now? Why?
4. Change `NUM_SOLUTIONS` to 2. Do the bees still find the best place? How many cycles do they need?
