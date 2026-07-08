module nftpkg::registry {
    use std::type_name::{Self, TypeName};
    use std::vector;

    public struct Registry has key {
        id: UID,
        names: vector<TypeName>,
    }

    public fun register<W: drop>(_witness: W, reg: &mut Registry) {
        vector::push_back(&mut reg.names, type_name::with_defining_ids<W>());
    }

    fun init(ctx: &mut TxContext) {
        let registry = Registry {
            id: object::new(ctx),
            names: vector::empty(),
        };
        transfer::share_object(registry);
    }
}

module nftpkg::minter {
    use nftpkg::registry;

    public struct MinterWitness has drop {}

    public fun register(reg: &mut registry::Registry) {
        let witness = MinterWitness {};
        registry::register(witness, reg);
    }
}
