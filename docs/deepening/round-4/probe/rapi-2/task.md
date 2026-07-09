Write a Sui Move module `rank::ladder` (edition 2024). A shared `Ladder` holds climbing-gym
rankings: an ordered list of entries, each an address with its score, kept sorted from highest
score to lowest. `submit_score(player, score)`, gated by a `GymCap`, inserts a new entry at its
correct sorted position (a player may appear more than once; ties go below existing equal
scores). `position(player)` is a public view returning the 1-based position of the player's
best entry, aborting if the player has no entry. `podium` is a public view returning the
addresses of the top three entries in order (or as many as exist, if fewer).
