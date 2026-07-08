module queue::waitlist {
    use sui::coin::Coin;
    use sui::sui::SUI;
    use std::vector;
    use std::option::{Option, some, none, is_some, extract, fill};

    const DEPOSIT_AMOUNT: u64 = 1_000_000;

    public struct HostCap has key, store {
        id: UID,
    }

    public struct Reservation has store {
        reservee: address,
        deposit: Coin<SUI>,
    }

    public struct Waitlist has key {
        id: UID,
        current: Option<Reservation>,
        tips: vector<Coin<SUI>>,
    }

    public struct Reserved has copy, drop {
        reservee: address,
    }

    public struct Seated has copy, drop {
        reservee: address,
    }

    public struct NoShowCleared has copy, drop {
        reservee: address,
    }

    fun init(ctx: &mut TxContext) {
        let waitlist = Waitlist {
            id: object::new(ctx),
            current: none(),
            tips: vector[],
        };
        transfer::share_object(waitlist);

        let cap = HostCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun reserve(
        waitlist: &mut Waitlist,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(payment.value() == DEPOSIT_AMOUNT);
        assert!(!is_some(&waitlist.current));

        let reservee = ctx.sender();
        let reservation = Reservation { reservee, deposit: payment };
        fill(&mut waitlist.current, reservation);

        sui::event::emit(Reserved { reservee });
    }

    public fun seat(
        _cap: &HostCap,
        waitlist: &mut Waitlist,
    ) {
        assert!(is_some(&waitlist.current));
        let reservation = extract(&mut waitlist.current);
        let reservee = reservation.reservee;
        let deposit = reservation.deposit;

        transfer::public_transfer(deposit, reservee);

        sui::event::emit(Seated { reservee });
    }

    public fun clear_no_show(
        _cap: &HostCap,
        waitlist: &mut Waitlist,
    ) {
        assert!(is_some(&waitlist.current));
        let reservation = extract(&mut waitlist.current);
        let reservee = reservation.reservee;
        let deposit = reservation.deposit;

        vector::push_back(&mut waitlist.tips, deposit);

        sui::event::emit(NoShowCleared { reservee });
    }

    public fun sweep_tips(
        _cap: &HostCap,
        waitlist: &mut Waitlist,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let mut total = sui::coin::zero<SUI>(ctx);
        while (!vector::is_empty(&waitlist.tips)) {
            let tip = vector::pop_back(&mut waitlist.tips);
            sui::coin::join(&mut total, tip);
        }
        total
    }
}
