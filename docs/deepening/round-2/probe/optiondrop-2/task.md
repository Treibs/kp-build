Write a Sui Move module `market::listing` (edition 2024). A seller creates a shared `Listing<T>`
holding a single item of generic type `T` (with the abilities storage requires) and a note field
`note: std::string::String`. The seller may `cancel(listing, ctx)` — which removes the item from
the listing and returns it to the seller, leaving the listing open but empty — and later
`relist(listing, item, ctx)` — which puts an item back into the empty listing (abort if it is not
empty, and only the original seller may relist).
