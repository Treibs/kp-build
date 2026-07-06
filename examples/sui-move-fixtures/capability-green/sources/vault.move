module capability_green::vault {
    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Vault has key {
        id: UID,
        value: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(AdminCap { id: object::new(ctx) }, ctx.sender());
        transfer::share_object(Vault { id: object::new(ctx), value: 0 });
    }

    /// Possession of the capability IS the authorization.
    public fun set_value(_cap: &AdminCap, vault: &mut Vault, value: u64) {
        vault.value = value;
    }
}
