Write a Sui Move module `queue::waitlist` (edition 2024). A shared `Waitlist` for a popup
restaurant holds an optional next-up reservation: when empty, anyone may `reserve` by paying a
deposit of exactly 1_000_000 MIST in SUI (their address becomes next-up and the deposit is held);
when occupied, `reserve` aborts. The host can `seat` the next-up party: the reservation clears
and the deposit is returned to the seated address. The host can also `clear_no_show`: the
reservation clears and the deposit is forfeited into the waitlist's tip pool, sweepable by the
host.
