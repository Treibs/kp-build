module warranty {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::event;
    use std::string::String;
    use std::option::{Self, Option};

    struct WarrantyRegistry has key {
        id: UID,
        reserve: Coin<SUI>,
    }

    struct MerchantCapability has key {
        id: UID,
        registry_id: ID,
    }

    struct Warranty has key {
        id: UID,
        registry_id: ID,
        product_name: String,
        valid_until_epoch: u64,
        claim_filed: bool,
        claim_resolved: bool,
        claim_filer: Option<address>,
    }

    struct WarrantyIssued has copy, drop {
        warranty_id: ID,
        valid_until_epoch: u64,
    }

    struct ClaimFiled has copy, drop {
        warranty_id: ID,
    }

    struct ClaimApproved has copy, drop {
        warranty_id: ID,
        reimbursement_amount: u64,
    }

    struct ClaimRejected has copy, drop {
        warranty_id: ID,
    }

    struct ReserveToppedUp has copy, drop {
        amount: u64,
    }

    public fun create_registry(
        initial_fund: Coin<SUI>,
        ctx: &mut TxContext,
    ): (WarrantyRegistry, MerchantCapability) {
        let registry_uid = object::new(ctx);
        let registry_id = object::uid_to_inner(&registry_uid);

        let registry = WarrantyRegistry {
            id: registry_uid,
            reserve: initial_fund,
        };

        let capability = MerchantCapability {
            id: object::new(ctx),
            registry_id,
        };

        (registry, capability)
    }

    public fun issue_warranty(
        cap: &MerchantCapability,
        registry: &WarrantyRegistry,
        product_name: String,
        valid_until_epoch: u64,
        ctx: &mut TxContext,
    ): Warranty {
        assert!(cap.registry_id == object::uid_to_inner(&registry.id), 0);

        let warranty = Warranty {
            id: object::new(ctx),
            registry_id: object::uid_to_inner(&registry.id),
            product_name,
            valid_until_epoch,
            claim_filed: false,
            claim_resolved: false,
            claim_filer: option::none(),
        };

        event::emit(WarrantyIssued {
            warranty_id: object::uid_to_inner(&warranty.id),
            valid_until_epoch,
        });

        warranty
    }

    public fun file_claim(
        warranty: &mut Warranty,
        current_epoch: u64,
        ctx: &TxContext,
    ) {
        assert!(!warranty.claim_filed, 0);
        assert!(!warranty.claim_resolved, 0);
        assert!(current_epoch < warranty.valid_until_epoch, 0);

        warranty.claim_filed = true;
        warranty.claim_filer = option::some(tx_context::sender(ctx));

        event::emit(ClaimFiled {
            warranty_id: object::uid_to_inner(&warranty.id),
        });
    }

    public fun approve_claim(
        cap: &MerchantCapability,
        warranty: &mut Warranty,
        registry: &mut WarrantyRegistry,
        reimbursement_amount: u64,
        ctx: &mut TxContext,
    ) {
        assert!(cap.registry_id == object::uid_to_inner(&registry.id), 0);
        assert!(warranty.claim_filed, 0);
        assert!(!warranty.claim_resolved, 0);

        warranty.claim_resolved = true;

        let filer = option::extract(&mut warranty.claim_filer);
        let payment = coin::split(&mut registry.reserve, reimbursement_amount, ctx);
        transfer::public_transfer(payment, filer);

        event::emit(ClaimApproved {
            warranty_id: object::uid_to_inner(&warranty.id),
            reimbursement_amount,
        });
    }

    public fun reject_claim(
        cap: &MerchantCapability,
        warranty: &mut Warranty,
        registry: &WarrantyRegistry,
    ) {
        assert!(cap.registry_id == object::uid_to_inner(&registry.id), 0);
        assert!(warranty.claim_filed, 0);
        assert!(!warranty.claim_resolved, 0);

        warranty.claim_resolved = true;

        event::emit(ClaimRejected {
            warranty_id: object::uid_to_inner(&warranty.id),
        });
    }

    public fun topup_reserve(
        cap: &MerchantCapability,
        registry: &mut WarrantyRegistry,
        additional_funds: Coin<SUI>,
    ) {
        assert!(cap.registry_id == object::uid_to_inner(&registry.id), 0);

        let amount = coin::value(&additional_funds);
        coin::join(&mut registry.reserve, additional_funds);

        event::emit(ReserveToppedUp {
            amount,
        });
    }

    public fun is_warranty_valid(
        warranty: &Warranty,
        current_epoch: u64,
    ): bool {
        !warranty.claim_filed && current_epoch < warranty.valid_until_epoch
    }
}
