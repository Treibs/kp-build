Write a Sui Move module `reg::whitelist` (edition 2024). A shared `TypeRegistry` records which
TYPES have been registered. Registering requires presenting a witness value of the type itself:
`public fun register<T: drop>(_witness: T, reg: &mut TypeRegistry)` stores the type's name in a
`sui::vec_set::VecSet` of type names (abort with a named constant if already registered), and
`public fun is_registered<T>(reg: &TypeRegistry): bool` checks membership without a witness.
