Write a Sui Move module `exchange::gifts` (edition 2024), generic over the gift type. A shared
`GiftPool` collects wrapped gifts for a holiday exchange: `deposit_gift(pool, item, giver)` wraps
an item of any suitable type and adds it to the pool, recording who gave it. The organizer
(holding an `OrganizerCap` issued when the pool is created) calls `hand_out(pool, index,
recipient)`, which removes the wrapped gift at that position from the pool and delivers it to
the recipient's address (abort if the index is out of range). `gifts_remaining` is a public
view returning how many gifts are still in the pool.
