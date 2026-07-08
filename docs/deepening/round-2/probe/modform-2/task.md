Write a Sui Move module (edition 2024) implementing an on-chain name registry. A shared
`Registry` maps names (`std::string::String`) to owner addresses. `register(registry, name, ctx)`
aborts if the name is taken, otherwise records the sender as owner. `release(registry, name, ctx)`
aborts unless the sender owns the name, otherwise removes it. Include a function to create and
share the `Registry`.
