Write a Sui Move module `board::bounty` (edition 2024). A poster creates a shared `Bounty`
describing a task (a `std::string::String`) and escrowing a reward that may or may not be
present: the reward slot holds an optional `Coin<SUI>`. The poster can `defund` (take the reward
back out, leaving the bounty open but unfunded), `refund_and_close` (destroy the bounty and
recover any reward), or `award(bounty, hunter)` which pays the reward to the hunter address and
closes the bounty. Closing must clean up the bounty object on every path.
