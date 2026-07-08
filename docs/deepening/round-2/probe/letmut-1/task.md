Write a Sui Move module `mint::batch` (edition 2024). A `Ticket` object carries `id: UID` and
`serial: u64`. Provide an entry function `mint_batch(count: u64, recipient: address,
ctx: &mut TxContext)` that mints `count` tickets with serials `0` through `count - 1` and
transfers each to the recipient.
