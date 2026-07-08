Write a Sui Move module `wrap::gifting` (edition 2024). A generic gift-wrapping service:
`wrap<T>(item: T, recipient: address, note: std::string::String, ctx)` seals ANY storable item
inside a `WrappedGift<T>` object and delivers the wrapped gift to the recipient.
`unwrap<T>(gift, ctx)` opens a wrapped gift the caller owns: the inner item ends up owned by the
caller and the wrapping is destroyed. Choose the generic bounds so the module actually compiles
and the items remain usable objects after unwrapping.
