module hero::xp {
    use std::string::String;

    public struct Character has key {
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
        character.experience = character.experience + amount;
        loop {
            let required = character.level * 100;
            if (character.experience >= required) {
                character.experience = character.experience - required;
                character.level = character.level + 1;
            } else {
                break
            }
        }
    }

    public fun power(character: &Character): u64 {
        character.level * 10 + character.experience
    }
}
