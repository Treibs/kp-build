module notary::notary {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::clock::Clock;
    use sui::table::{Self, Table};
    use sui::balance::{Self, Balance};

    const RECORDING_FEE: u64 = 1000;

    public struct DigestRecord has store {
        recorder: address,
        timestamp: u64,
    }

    public struct Notary has key {
        id: UID,
        digests: Table<vector<u8>, DigestRecord>,
        total_digests: u64,
        fees: Balance<SUI>,
        operator: address,
    }

    fun init(ctx: &mut TxContext) {
        let notary = Notary {
            id: object::new(ctx),
            digests: table::new(ctx),
            total_digests: 0,
            fees: balance::zero(),
            operator: tx_context::sender(ctx),
        };
        transfer::share_object(notary);
    }

    public entry fun record_digest(
        notary: &mut Notary,
        digest: vector<u8>,
        fee: Coin<SUI>,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        assert!(coin::value(&fee) >= RECORDING_FEE, 0);
        assert!(!table::contains(&notary.digests, digest), 1);

        let recorder = tx_context::sender(ctx);
        let timestamp = clock::timestamp_ms(clock);

        let record = DigestRecord {
            recorder,
            timestamp,
        };

        table::add(&mut notary.digests, digest, record);
        notary.total_digests += 1;

        let fee_balance = coin::into_balance(fee);
        balance::join(&mut notary.fees, fee_balance);
    }

    public fun get_digest_record(
        notary: &Notary,
        digest: vector<u8>,
    ): (address, u64) {
        assert!(table::contains(&notary.digests, digest), 2);
        let record = table::borrow(&notary.digests, digest);
        (record.recorder, record.timestamp)
    }

    public fun get_total_digests(notary: &Notary): u64 {
        notary.total_digests
    }

    public entry fun sweep_fees(
        notary: &mut Notary,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(sender == notary.operator, 3);

        let fee_coin = coin::from_balance(
            balance::withdraw_all(&mut notary.fees),
            ctx,
        );
        transfer::public_transfer(fee_coin, sender);
    }
}
