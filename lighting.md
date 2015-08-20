Hm.

I was going to use (x2 - x1)^2 + (y2 - y1)^2 as my distance_squared value, then
divide that by 2/r^2. But I think that doesn't make sense. I thought about it,
and since (x2 - x1)^2 + (y2 - y1)^2 = r^2, dividing by 2/r^2 when I'm...

Wait. Okay, let's think about this. The formula was going to be 1/(distance^2), as
mentioned above. If I instead change it to 1/(2/(distance^2)  *  distance^2), that
gives... 1/2. It gives 1/2 no matter what distance is. So that can't be right.

What I want is, when distance = r, the light should be 0.5. When distance =

Say I have a radius of 7. So, the formula gives 1/49 light at the edge of the
radius. How do I transform that into 0.5 for all values of 1/d^2?

For 1/49 specifically, hmm... 1/49 * k = 1/2. k/49 = 1/2. Multiplying both sides
by 49, we get k = 49/2. So k = 49/2. But that's obviously not going to work for
all values.

Maybe if I multiply by two, then take the inverse? Let's try that for another
formula.

For r = 5, d^2 = 25. 1/25 * 2 = 2/25. 25/2 = 12.5. Multiply 1/25 by 12.5 and you
get 1/2, or close. But what about for other values of 5?

Fuck. I think I'll have to write several formulas and change them out and see
which one works the best.
