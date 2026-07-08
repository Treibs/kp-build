Write a Sui Move module `config::config` (edition 2024) for publish-then-freeze configuration.
An `AdminCap` owner creates a `Config` object (fields: `fee_bps: u64`, `treasury: address`) as a
mutable draft they own, may update it with setter functions, and finally calls `publish(config)`
which makes the object permanently immutable so anyone can read it. Include a read function taking
`&Config` returning the fee.
