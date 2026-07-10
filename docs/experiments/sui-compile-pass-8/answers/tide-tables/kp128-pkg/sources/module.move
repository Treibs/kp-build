module 0x0::harbor {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;
    use std::option::{Self, Option};

    const ERROR_ALREADY_POSTED: u64 = 1;

    public struct HarborMasterCap has key, store {
        id: UID,
    }

    public struct TideBoard has key {
        id: UID,
        last_posted_epoch: u64,
        last_posted_level: u64,
        ever_posted: bool,
    }

    public struct Mooring has key {
        id: UID,
        draft: u64,
    }

    fun init(ctx: &mut TxContext) {
        let board = TideBoard {
            id: object::new(ctx),
            last_posted_epoch: 0,
            last_posted_level: 0,
            ever_posted: false,
        };
        transfer::share_object(board);
        
        let cap = HarborMasterCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun post_level(
        _cap: &HarborMasterCap,
        board: &mut TideBoard,
        level: u64,
        ctx: &TxContext,
    ) {
        let current_epoch = ctx.epoch();
        assert!(board.last_posted_epoch != current_epoch, ERROR_ALREADY_POSTED);
        board.last_posted_epoch = current_epoch;
        board.last_posted_level = level;
        board.ever_posted = true;
    }

    public fun can_sail(
        board: &TideBoard,
        mooring: &Mooring,
        ctx: &TxContext,
    ): bool {
        if (board.last_posted_epoch != ctx.epoch()) {
            false
        } else {
            mooring.draft <= board.last_posted_level
        }
    }

    public fun get_last_level(board: &TideBoard): Option<u64> {
        if (board.ever_posted) {
            option::some(board.last_posted_level)
        } else {
            option::none()
        }
    }

    public fun create_mooring(draft: u64, ctx: &mut TxContext): Mooring {
        Mooring {
            id: object::new(ctx),
            draft,
        }
    }
}
