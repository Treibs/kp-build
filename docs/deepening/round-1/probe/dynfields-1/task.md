Write a Sui Move module `attach::gadgets` (edition 2024). A `Device` object can have a named
`Accessory` child object attached to it and detached from it using dynamic object fields (the
accessory must remain a real object, independently transferable, so it needs `key` and `store`).
Provide: `new_device`, `new_accessory`, `attach(device: &mut Device, name: vector<u8>, acc: Accessory)`,
and `detach(device: &mut Device, name: vector<u8>): Accessory` which removes and returns the child.
