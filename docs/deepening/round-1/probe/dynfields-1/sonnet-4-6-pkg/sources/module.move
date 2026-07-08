module attach::gadgets;

use sui::dynamic_object_field;

public struct Device has key, store {
    id: UID,
}

public struct Accessory has key, store {
    id: UID,
}

public fun new_device(ctx: &mut TxContext): Device {
    Device { id: object::new(ctx) }
}

public fun new_accessory(ctx: &mut TxContext): Accessory {
    Accessory { id: object::new(ctx) }
}

public fun attach(device: &mut Device, name: vector<u8>, acc: Accessory) {
    dynamic_object_field::add(&mut device.id, name, acc);
}

public fun detach(device: &mut Device, name: vector<u8>): Accessory {
    dynamic_object_field::remove(&mut device.id, name)
}
