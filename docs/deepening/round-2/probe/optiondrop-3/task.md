Write a Sui Move module `capsule::capsule` (edition 2024). A `TimeCapsule` object holds an
optional `Gift` (a struct with an `id: UID` and a `message: std::string::String`) and an
`unlock_epoch: u64`. `bury(capsule, gift)` places a gift into an empty capsule (abort if it
already holds one). `unearth(capsule, ctx)` aborts before `unlock_epoch`, otherwise takes the
gift out and transfers it to the sender. `discard_empty(capsule)` destroys a capsule ONLY if it
holds no gift.
