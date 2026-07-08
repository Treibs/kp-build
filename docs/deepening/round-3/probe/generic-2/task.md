Write a Sui Move module `lostfound::office` (edition 2024). A shared `LostAndFound` office
accepts found items of any storable object type: `hand_in<T>(office, item, label, ctx)` stores
the item under a numbered claim ticket (the module issues the finder a `Receipt` object with the
ticket number). `claim<T>(office, ticket_no, ctx)` releases the item to the claimant if they
present the matching `Receipt` (which is consumed). Items of different types must be storable in
the same office concurrently.
