Write a Sui Move module `wreck::permit` (edition 2024). A `Building` is an owned object with a
street name and a floor count. `construct(street, floors)` creates and returns a building. The
city (holding a `CityCap`) demolishes a building with `demolish(building)`: the building is
destroyed, a `Demolished` event is emitted recording which building was demolished along with
its street name, and the caller receives a `SalvageReceipt` object that references the
demolished building and records how many floors of material were salvaged.
