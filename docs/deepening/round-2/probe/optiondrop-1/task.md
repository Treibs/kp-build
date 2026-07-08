Write a Sui Move module `shop::consign` (edition 2024). A `Shop` object (owned by the shopkeeper)
has ONE display slot that may hold a consigned item of a generic type `T` (with the abilities
storage requires) plus an asking price `price: u64`. `stock(shop, item, price)` places an item in
the slot; if the slot is already occupied, the previously displayed item must be sent back to the
shopkeeper (the shop owner address, stored in the shop), never destroyed. `buy(shop, payment, ctx)`
takes a `Coin<SUI>` of exactly the asking price, sends the payment to the shopkeeper, and gives
the displayed item to the buyer; it aborts if the slot is empty.
