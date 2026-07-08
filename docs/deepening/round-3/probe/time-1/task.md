Write a Sui Move module `faucet::drip` (edition 2024). A shared `Faucet` is funded with SUI and
pays out a fixed drip amount per request. Each address may draw at most once every 5 epochs: a
successful `draw` records when the caller drew, and a repeat attempt inside the cooldown window
aborts. Track per-address draw history inside the faucet. Provide a funder-only `top_up` and a
read function reporting whether an address may currently draw.
