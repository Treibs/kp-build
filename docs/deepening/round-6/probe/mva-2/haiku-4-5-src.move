module courier::manifest {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use std::vector;

    public struct Manifest has key {
        id: UID,
        total_insured: u64,
        parcels: vector<Parcel>,
    }

    public struct Parcel has store {
        destination: address,
        declared_value: u64,
    }

    public fun create_manifest(ctx: &mut TxContext): Manifest {
        Manifest {
            id: object::new(ctx),
            total_insured: 0,
            parcels: vector[],
        }
    }

    public fun deliver_parcel(manifest: &mut Manifest, destination: address, value: u64) {
        let parcel = Parcel {
            destination,
            declared_value: value,
        };
        vector::push_back(&mut manifest.parcels, parcel);
        manifest.total_insured = manifest.total_insured + value;
    }

    public fun total_insured(manifest: &Manifest): u64 {
        manifest.total_insured
    }

    public fun parcels_delivered(manifest: &Manifest): u64 {
        vector::length(&manifest.parcels)
    }

    public fun parcel_at(manifest: &Manifest, index: u64): (address, u64) {
        let parcel = vector::borrow(&manifest.parcels, index);
        (parcel.destination, parcel.declared_value)
    }
}
