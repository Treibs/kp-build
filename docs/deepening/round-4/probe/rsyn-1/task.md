Write a Sui Move module `score::board` (edition 2024). Provide a public function `new` that
creates and returns a fresh `Scoreboard` together with a `RefereeCap`, so the caller decides
what to do with them (there is no `init`). The scoreboard tracks points per player address.
`add_point`, gated by the referee capability, increases a player's score by a given amount
(starting from zero the first time a player scores). `score(player)` is a public view returning
the player's current total, 0 for a player who never scored.
