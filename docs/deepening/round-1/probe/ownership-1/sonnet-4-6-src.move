module escrow::locker {
    public struct Locker<T: store> has key {
        id: UID,
        item: T,
    }

    public fun lock<T: key + store>(item: T, ctx: &mut TxContext) {
        let locker = Locker { id: object::new(ctx), item };
        transfer::transfer(locker, ctx.sender());
    }

    public fun unlock<T: key + store>(locker: Locker<T>, ctx: &mut TxContext) {
        let Locker { id, item } = locker;
        object::delete(id);
        transfer::public_transfer(item, ctx.sender());
    }
}
