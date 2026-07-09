Write a Sui Move module `steps::pedometer` (edition 2024). Provide a public function
`new_pedometer` that creates and returns an owned `Pedometer` for the caller to keep. The
pedometer tracks `today` (steps logged since the last rollover) and `lifetime` (steps from all
completed days). `log_steps(n)` adds `n` to today's count. `rollover` closes the day: it adds
today's count into the lifetime total, resets today to zero, and returns the count the day
closed with. `lifetime_total` is a public view that reports lifetime plus today.
