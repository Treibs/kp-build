Write a Sui Move module `airdrop::airdrop` (edition 2024). It mints a simple `Badge` object
(with `key` and `store`) carrying an `id` and a `serial: u64`. Provide an entry function
`claim(serial: u64, recipient: Option<address>, ctx: &mut TxContext)`: if a recipient address is
provided, transfer the badge there; otherwise transfer it to the transaction sender.
