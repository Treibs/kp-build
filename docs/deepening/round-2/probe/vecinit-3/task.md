Write a Sui Move module `tags::tags` (edition 2024). A `TagSet` object holds a collection of
distinct tags (`std::string::String`). `add_tag(set, tag)` aborts if the tag is already present.
`has_tag(set, tag): bool` reports membership. `clear(set)` removes all tags at once. Include a
function that creates an empty `TagSet` for the sender.
