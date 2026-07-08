Write a Sui Move module `depot::inventory` (edition 2024). A shared `Depot` object tracks stock
counts for named goods in a `sui::table::Table<std::string::String, u64>`. An operator capability
(issued to the creator) gates `restock(name, qty)` which adds to a good's count (creating the
entry if absent). Anyone can call `consume(name)` which decrements the count by 1 and aborts if
the good is absent or at zero. Provide a public read function `stock(name): u64` returning 0 for
unknown goods.
