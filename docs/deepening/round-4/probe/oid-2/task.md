Write a Sui Move module `pets::registry` (edition 2024). A shelter (holding a `ShelterCap`)
mints `Pet` objects with a name. A shared `AdoptionRegistry` records, for every adopted pet,
which address adopted it, keyed by the pet's on-chain identity. `adopt(registry, pet, adopter)`,
gated by the shelter capability, records the adoption in the registry and delivers the pet to
the adopter. `adopter_of` is a public view that, given a pet's identity, returns the adopter's
address, aborting for a pet that was never adopted. `adoption_count` returns how many adoptions
the registry has recorded.
