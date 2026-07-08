Write a Sui Move module `merge::merger` (edition 2024) with an entry function that takes a
`vector<Coin<SUI>>` and a recipient `address`, joins all the coins into a single coin, and
transfers the merged coin to the recipient. If the vector is empty, abort with a named constant
error code. Clean up the empty vector properly.
