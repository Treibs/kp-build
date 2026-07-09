Write a Sui Move module `hero::xp` (edition 2024). Provide a public function `create_character`
that creates and returns an owned `Character` with a name, level 1, and 0 experience. Each level
`L` requires `L * 100` experience to advance. `gain_xp(amount)` adds experience and then levels
the character up as many times as the accumulated experience allows, spending the required
experience at each level-up and carrying the remainder forward. `power` is a public view
returning `level * 10` plus the current unspent experience.
