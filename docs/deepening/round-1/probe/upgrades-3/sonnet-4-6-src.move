module nftpkg::registry {
    use std::ascii::String;
    use std::type_name;

    public struct Registry has key {
        id: UID,
        names: vector<String>,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(Registry {
            id: object::new(ctx),
            names: vector[],
        });
    }

    public fun register<W: drop>(_witness: W, reg: &mut Registry) {
        let name = type_name::get<W>();
        reg.names.push_back(type_name::into_string(name));
    }
}

module nftpkg::minter {
    use nftpkg::registry::{Self, Registry};

    public struct MinterWitness has drop {}

    entry fun do_register(reg: &mut Registry) {
        registry::register(MinterWitness {}, reg);
    }
}
