Write a Sui Move module `toll::booth` (edition 2024). A shared `TollBooth` charges a fixed toll
in MIST. `pay_toll` takes a payment in SUI of exactly the toll (abort otherwise), adds it to the
booth's accumulated balance, and emits a `TollPaid` event carrying the payer's address and the
amount. The operator (holding an `OperatorCap` issued at creation) calls `sweep(max_amount)`,
which withdraws up to `max_amount` (or everything, if less is available) from the booth's
balance and returns it to the operator as spendable coin.
