Write a Sui Move module `dispatch::carebox` (edition 2024), generic over the packed item type.
`pack(item, note)` wraps a single item of any suitable type into a `CareBox` together with a
short text note, and returns the box to the caller. `send_batch(boxes, recipients)` takes a
vector of care boxes and a matching vector of recipient addresses (abort if the lengths differ)
and delivers each box to the recipient at the same position. `unpack(box)` lets a recipient take
the item back out of a box they received, returning the item and discarding the wrapping.
