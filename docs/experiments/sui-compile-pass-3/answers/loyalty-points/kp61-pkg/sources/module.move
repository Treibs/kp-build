module loyalty::program {
    public struct Points has key {
        id: UID,
        amount: u64,
    }

    public struct Reward has key, store {
        id: UID,
    }

    public struct OperatorCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let cap = OperatorCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun issue(
        _cap: &OperatorCap,
        amount: u64,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let points = Points {
            id: object::new(ctx),
            amount,
        };
        transfer::transfer(points, recipient);
    }

    public fun redeem(points: Points, ctx: &mut TxContext): Reward {
        assert!(points.amount >= 100);
        let Points { id, amount: _ } = points;
        object::delete(id);
        Reward {
            id: object::new(ctx),
        }
    }

    public fun merge(p1: Points, p2: Points, ctx: &mut TxContext): Points {
        let Points { id: id1, amount: amount1 } = p1;
        let Points { id: id2, amount: amount2 } = p2;
        object::delete(id1);
        object::delete(id2);
        Points {
            id: object::new(ctx),
            amount: amount1 + amount2,
        }
    }

    public fun balance(points: &Points): u64 {
        points.amount
    }
}
