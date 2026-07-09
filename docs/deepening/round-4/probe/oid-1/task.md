Write a Sui Move module `member::card` (edition 2024). A `MemberCard` is an owned object with a
tier number. The club (holding a `ClubCap`) issues cards at tier 1 with `issue(recipient)`.
A member upgrades by calling `renew(old_card)`: the old card is retired (destroyed), the member
receives a successor card one tier higher, and a `CardRenewed` event is emitted recording which
card was retired, which card replaced it, and the new tier — so an indexer can follow the chain
of succession.
