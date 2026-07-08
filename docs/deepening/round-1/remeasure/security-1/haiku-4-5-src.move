module reg::whitelist {
    use sui::vec_set::{Self, VecSet};
    use std::type_name::{Self, TypeName};

    const ETypeAlreadyRegistered: u64 = 0;

    public struct TypeRegistry has key {
        id: UID,
        registered_types: VecSet<TypeName>,
    }

    fun init(ctx: &mut TxContext) {
        let registry = TypeRegistry {
            id: object::new(ctx),
            registered_types: vec_set::empty(),
        };
        transfer::share_object(registry);
    }

    public fun register<T: drop>(_witness: T, reg: &mut TypeRegistry) {
        let type_name = type_name::with_defining_ids<T>();
        assert!(!vec_set::contains(&reg.registered_types, &type_name), ETypeAlreadyRegistered);
        vec_set::insert(&mut reg.registered_types, type_name);
    }

    public fun is_registered<T>(reg: &TypeRegistry): bool {
        vec_set::contains(&reg.registered_types, &type_name::with_defining_ids<T>())
    }
}
