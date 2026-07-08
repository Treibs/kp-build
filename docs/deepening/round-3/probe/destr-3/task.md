Write a Sui Move module `molt::snake` (edition 2024). A `Snake` object owns a `Skin` object held
as a field (`Skin` has `id: UID` and a `pattern: u8`; the module defines both). `molt(snake,
new_pattern, ctx)` grows a fresh skin in place and gives the OLD skin to the snake's owner as a
collectible. `retire(snake)` destroys the snake AND its current skin entirely. Both functions
must account for every value; nothing may be silently discarded.
