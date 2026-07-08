Write a Sui Move module `handover::handover` (edition 2024) implementing TWO-STEP ownership
transfer of an `Estate` object (key + store, with a `value: u64` field). `offer(estate, to, ctx)`
wraps the estate in an `Offer` object recording the original owner and transfers the Offer to `to`;
the recipient calls `accept(offer, ctx)` to unwrap and receive the estate; alternatively
`decline(offer, ctx)` returns the estate to the original owner. In both cases the Offer wrapper is
destroyed properly.
