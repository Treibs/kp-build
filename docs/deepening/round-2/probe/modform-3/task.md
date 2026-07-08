Write a Sui Move module (edition 2024) implementing a fee-splitting payment. A shared
`FeeConfig` object holds `fee_bps: u64` (basis points) and `treasury: address`. An entry function
`pay(config: &FeeConfig, payment: Coin<SUI>, recipient: address, ctx: &mut TxContext)` splits the
fee share off the payment, sends the fee to the treasury address, and sends the remainder to the
recipient. Include a function that creates and shares the `FeeConfig`.
