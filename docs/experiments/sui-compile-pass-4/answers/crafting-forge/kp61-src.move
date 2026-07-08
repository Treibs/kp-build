module crafting::forge {
    public struct Blade has key, store {
        id: UID,
    }

    public struct Hilt has key, store {
        id: UID,
    }

    public struct Sword has key, store {
        id: UID,
        blades_consumed: u64,
        hilts_consumed: u64,
    }

    public fun mint_blade(ctx: &mut TxContext): Blade {
        Blade {
            id: object::new(ctx),
        }
    }

    public fun mint_hilt(ctx: &mut TxContext): Hilt {
        Hilt {
            id: object::new(ctx),
        }
    }

    public fun forge(blade: Blade, hilt: Hilt, ctx: &mut TxContext): Sword {
        let Blade { id } = blade;
        object::delete(id);
        
        let Hilt { id } = hilt;
        object::delete(id);
        
        Sword {
            id: object::new(ctx),
            blades_consumed: 1,
            hilts_consumed: 1,
        }
    }

    public fun smelt(sword: Sword, ctx: &mut TxContext): (Blade, Hilt) {
        let Sword { id, blades_consumed: _, hilts_consumed: _ } = sword;
        object::delete(id);
        
        (
            Blade { id: object::new(ctx) },
            Hilt { id: object::new(ctx) }
        )
    }
}
