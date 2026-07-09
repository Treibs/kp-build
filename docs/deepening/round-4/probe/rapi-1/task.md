Write a Sui Move module `duel::record` (edition 2024). A shared `DuelLedger` tracks head-to-head
results between pairs of fencers, identified by address. `record_win(winner, loser)`, gated by a
`ScorekeeperCap` issued at creation, adds one to the count of times `winner` has beaten `loser`
(each ordered pair keeps its own count, so A-beats-B and B-beats-A are tracked separately).
`wins(winner, loser)` is a public view returning how many times `winner` has beaten `loser`,
0 for a pairing never recorded.
