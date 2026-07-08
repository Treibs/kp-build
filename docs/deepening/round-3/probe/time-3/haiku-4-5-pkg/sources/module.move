module harvest::farm {
    public struct Seedling has key {
        id: UID,
        planted_at_epoch: u64,
    }

    public struct Crop has key {
        id: UID,
        growth_epochs: u64,
    }

    public fun plant(ctx: &mut TxContext): Seedling {
        let epoch = sui::tx_context::epoch(ctx);
        Seedling {
            id: object::new(ctx),
            planted_at_epoch: epoch,
        }
    }

    public fun harvest(seedling: Seedling, ctx: &mut TxContext): Crop {
        let Seedling { id, planted_at_epoch } = seedling;
        let current_epoch = sui::tx_context::epoch(ctx);
        let growth_epochs = current_epoch - planted_at_epoch;
        
        assert!(growth_epochs >= 3);
        
        object::delete(id);
        Crop {
            id: object::new(ctx),
            growth_epochs,
        }
    }
}
