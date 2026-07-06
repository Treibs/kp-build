module counter::shared_counter;

use sui::object::{Self, UID};
use sui::transfer;
use sui::tx_context::{Self, TxContext};

/// Shared counter object that anyone can increment but only creator can reset.
public struct Counter has key {
    id: UID,
    creator: address,
    value: u64,
}

/// Capability object given to the creator at init time.
public struct CreatorCap has key, store {
    id: UID,
    counter_id: ID,
}

/// Create a new shared counter and give the creator a capability.
public fun create(ctx: &mut TxContext) {
    let counter = Counter {
        id: object::new(ctx),
        creator: tx_context::sender(ctx),
        value: 0,
    };

    let cap = CreatorCap {
        id: object::new(ctx),
        counter_id: object::id(&counter),
    };

    transfer::share_object(counter);
    transfer::transfer(cap, tx_context::sender(ctx));
}

/// Anyone can increment the counter.
public fun increment(counter: &mut Counter) {
    counter.value = counter.value + 1;
}

/// Only the holder of the matching CreatorCap can reset the counter to zero.
public fun reset(counter: &mut Counter, cap: &CreatorCap) {
    assert!(cap.counter_id == object::id(counter), 0);
    counter.value = 0;
}

/// Read the current value.
public fun value(counter: &Counter): u64 {
    counter.value
}
