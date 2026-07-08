module molt::snake {
    public struct Skin has key, store {
        id: UID,
        pattern: u8,
    }

    public struct Snake has key, store {
        id: UID,
        skin: Skin,
    }

    public fun molt(snake: Snake, new_pattern: u8, ctx: &mut TxContext) {
        let Snake { id: snake_id, skin: old_skin } = snake;
        
        let new_skin = Skin {
            id: object::new(ctx),
            pattern: new_pattern,
        };
        
        let new_snake = Snake {
            id: snake_id,
            skin: new_skin,
        };
        
        let owner = ctx.sender();
        transfer::public_transfer(new_snake, owner);
        transfer::public_transfer(old_skin, owner);
    }

    public fun retire(snake: Snake) {
        let Snake { id: snake_id, skin } = snake;
        let Skin { id: skin_id, pattern: _ } = skin;
        object::delete(snake_id);
        object::delete(skin_id);
    }
}
