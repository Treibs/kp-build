module hero::xp {
    use std::string::String;

    public struct Character has key, store {
        id: UID,
        name: String,
        level: u64,
        experience: u64,
    }

    public fun create_character(name: String, ctx: &mut TxContext): Character {
        Character {
            id: object::new(ctx),
            name,
            level: 1,
            experience: 0,
        }
    }

    public fun gain_xp(character: &mut Character, amount: u64) {
        character.experience += amount;
        
        while character.experience >= character.level * 100 {
            character.experience -= character.level * 100;
            character.level += 1;
        }
    }

    public fun power(character: &Character): u64 {
        character.level * 10 + character.experience
    }
}
