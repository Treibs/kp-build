Write a Sui Move module `party::pinata` (edition 2024). A `Pinata` object is created filled with
a SUI balance (the candy fund) and a `Toy` object (a struct with `id: UID` the module also
defines and mints at fill time). `smash(pinata, ctx)` destroys the pinata: the entire candy fund
is paid to the smasher as a `Coin<SUI>` and the toy is transferred to the smasher. The pinata
must be fully cleaned up; nothing it contained may be lost or left behind.
