Write a Sui Move module `raffle::pot` (edition 2024). A shared `Raffle` has a fixed ticket price
in MIST and a prize pot. `enter` takes a payment in SUI of exactly the ticket price (abort
otherwise), adds it to the pot, and records the entrant's address. The organizer (holding an
`OrganizerCap`) calls `draw(winner_index)`: it aborts if the index is out of range, otherwise
pays the entire pot to the entrant at that index as spendable coin and empties the entrant list
so the raffle can run again.
