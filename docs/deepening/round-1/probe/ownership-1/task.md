Write a Sui Move module `escrow::locker` (edition 2024) implementing object wrapping. A generic
`Locker<T>` object WRAPS an item of type `T` (with the abilities object wrapping requires) as a
plain field, so the wrapped item disappears from global storage while locked.
`lock<T>(item: T, ctx: &mut TxContext)` wraps the item and transfers the locker to the sender;
`unlock<T>(locker: Locker<T>, ctx: &mut TxContext)` consumes the locker, deletes its id, and
transfers the inner item back to the sender.
