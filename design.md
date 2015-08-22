Imagine I have only a week to implement a functional "complete" roguelike. What
core features do I need to have a workable, playable concept?

* Pseudorandom level generation.
* Lighting system.
* Fog of fh'tagn.
* Line of sight.
* Eldritch abomination monsters.
* Clients that follow you around (unless told to wait?) and can observe the
  house.  I can probably cut the command portion of that, actually, and just
  have them follow you all the time.
* A functional UI.



Extra stuff I don't need in the very base:

* Traps, either for you or abominations or otherwise.
* Health or sanity. Tax collectors/enraged clients/traps aren't in. Abominations
  can just one-hit (or three-hit?) kill you when you get too close.
* Vaults. Pure pseudorandom generation should do decently for the first version.
  Not as well as I'd like, but well enough.
* Items.
* Inventory.
* Money.
* Any kind of shopping/trading system.
* Tax collectors.
* Complicated artificial intelligence.
* Any kind of complicated client AI (no weighting reversal/adjustment, no rage
  level, no terror or discomfort level, nothing).
* Clients stealing shit.
* Any kind of item-shop or cross-level tracking, except perhaps for score.
* Any kind of endgame content. This includes the mansion/castle idea, the
  difficulty ramp-up and the (currently, conceptually simplistic) magic-learning
  system.
* A sound system.
* A message log. (Though this should be one of the first 'extra' features I
  implement, I think.)
* Score-tracking, except whether you succeeded or failed in selling the house.
* Complicated abomination/tax collector spawning-logic.
* Complicated fade-in fog-of-fh'tagn logic involving abomination vicinity and
spawn times.
* Eldritch abominations with ears, because there's no sound system.
* Any variation in eldritch abominations. I may have two or three types in the
first version, but that's an upper bound, not a requirement. I only need one.
* 'Pointing-out' or other client-focused game logic.
* A pretty UI.
* Any variation in clients at all.
* Any variation in tax collectors, since they don't exist yet.
* A combat system for fighting the eldritch abominations. It's simply not needed
  at this stage of the game.





Idea: Seeing suspicious stuff raises momentary suspicion as well as the
"suspicion floor" -- a client's suspicion dissipates over time, but it will
never get below this floor value. It rises slowly, but if they see enough
suspicious shit, it's going to be very difficult or impossible to get them to
calm down. So don't let them.

What does suspicion do? I'm not sure yet, exactly. Might make them panic and try
to leave the property, or might cause some other behavior. Will have to figure
that out.
