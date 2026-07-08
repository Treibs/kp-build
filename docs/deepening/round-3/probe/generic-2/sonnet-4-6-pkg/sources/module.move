module lostfound::office {
    use sui::dynamic_object_field;
    use std::string::String;

    public struct LostAndFound has key {
        id: UID,
        next_ticket: u64,
    }

    public struct Receipt has key, store {
        id: UID,
        ticket_no: u64,
        label: String,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(LostAndFound {
            id: object::new(ctx),
            next_ticket: 0,
        });
    }

    public fun hand_in<T: key + store>(
        office: &mut LostAndFound,
        item: T,
        label: String,
        ctx: &mut TxContext,
    ): Receipt {
        let ticket_no = office.next_ticket;
        office.next_ticket = ticket_no + 1;
        dynamic_object_field::add(&mut office.id, ticket_no, item);
        Receipt {
            id: object::new(ctx),
            ticket_no,
            label,
        }
    }

    public fun claim<T: key + store>(
        office: &mut LostAndFound,
        receipt: Receipt,
        _ctx: &mut TxContext,
    ): T {
        let Receipt { id, ticket_no, label: _ } = receipt;
        object::delete(id);
        dynamic_object_field::remove(&mut office.id, ticket_no)
    }
}
