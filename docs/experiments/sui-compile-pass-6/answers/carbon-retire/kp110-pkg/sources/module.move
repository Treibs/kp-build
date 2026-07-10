module 0x0::carbon_registry {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;
    use sui::event;

    public struct CarbonCredit has key, store {
        id: UID,
        tonnage: u64,
    }

    public struct IssuerCap has key, store {
        id: UID,
    }

    public struct CreditRegistry has key {
        id: UID,
        total_retired: u64,
    }

    public struct RetirementReceipt has key, store {
        id: UID,
        tonnage: u64,
        credit_id: address,
    }

    public struct CreditRetired has copy, drop {
        credit_id: address,
        tonnage: u64,
    }

    fun init(ctx: &mut TxContext) {
        let registry = CreditRegistry {
            id: object::new(ctx),
            total_retired: 0,
        };
        transfer::share_object(registry);

        let issuer_cap = IssuerCap {
            id: object::new(ctx),
        };
        transfer::transfer(issuer_cap, tx_context::sender(ctx));
    }

    public fun mint(
        _cap: &IssuerCap,
        tonnage: u64,
        ctx: &mut TxContext,
    ): CarbonCredit {
        CarbonCredit {
            id: object::new(ctx),
            tonnage,
        }
    }

    public fun retire(
        credit: CarbonCredit,
        registry: &mut CreditRegistry,
        ctx: &mut TxContext,
    ): RetirementReceipt {
        let credit_addr = object::id_to_address(object::id(&credit));
        let CarbonCredit { id, tonnage } = credit;
        
        registry.total_retired = registry.total_retired + tonnage;
        object::delete(id);

        event::emit(CreditRetired {
            credit_id: credit_addr,
            tonnage,
        });

        RetirementReceipt {
            id: object::new(ctx),
            tonnage,
            credit_id: credit_addr,
        }
    }

    public fun get_total_retired(registry: &CreditRegistry): u64 {
        registry.total_retired
    }
}
