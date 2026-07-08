Write a Sui Move package (edition 2024) as two modules IN ONE ANSWER: `nftpkg::registry` and
`nftpkg::minter`. `nftpkg::registry` defines a shared `Registry` object and a
`public fun register<W: drop>(_witness: W, reg: &mut Registry)` that records the fully-qualified
type name of `W` (use the standard type-name facility) in a vector of recorded names.
`nftpkg::minter` defines its own witness struct and an entry function that registers itself by
calling `registry::register` with a fresh witness value.
