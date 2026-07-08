module loyalty::points {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;

    /// Capability to issue points - held only by the program operator
    public struct OperatorCap has key {
        id: UID,
    }

    /// Points object - non-transferable between users
    /// Does not have `store` ability to prevent transfers
    public struct Points has key {
        id: UID,
        owner: address,
        balance: u64,
    }

    /// Reward object that users receive when redeeming points
    public struct Reward has key, store {
        id: UID,
    }

    const POINTS_PER_REWARD: u64 = 100;
    const INSUFFICIENT_BALANCE: u64 = 1;
    const OWNER_MISMATCH: u64 = 2;

    /// Issue points to a user - only callable by operator
    public fun issue(
        _cap: &OperatorCap,
        recipient: address,
        amount: u64,
        ctx: &mut TxContext,
    ) {
        let points = Points {
            id: object::new(ctx),
            owner: recipient,
            balance: amount,
        };
        transfer::transfer(points, recipient);
    }

    /// Redeem points for rewards - burns the points
    public fun redeem(
        points: Points,
        ctx: &mut TxContext,
    ): Reward {
        assert!(points.balance >= POINTS_PER_REWARD, INSUFFICIENT_BALANCE);
        
        let Points { id, owner: _, balance: _ } = points;
        object::delete(id);

        Reward {
            id: object::new(ctx),
        }
    }

    /// Merge two Points objects owned by the same user
    public fun merge_balance(
        points1: Points,
        points2: Points,
        _ctx: &mut TxContext,
    ): Points {
        assert!(points1.owner == points2.owner, OWNER_MISMATCH);
        
        let balance = points1.balance + points2.balance;
        let owner = points1.owner;
        
        let Points { id: id1, owner: _, balance: _ } = points1;
        let Points { id: id2, owner: _, balance: _ } = points2;
        
        object::delete(id2);

        Points {
            id: id1,
            owner,
            balance,
        }
    }

    /// Get the balance of a Points object
    public fun balance(points: &Points): u64 {
        points.balance
    }

    /// Get the owner of a Points object
    public fun owner(points: &Points): address {
        points.owner
    }

    /// Create operator capability
    public fun create_operator_cap(ctx: &mut TxContext) {
        let cap = OperatorCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, sui::tx_context::sender(ctx));
    }
}
