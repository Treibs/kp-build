Write a Sui Move module `text::builder` (edition 2024). Provide a public function
`join(parts: vector<std::string::String>, sep: std::string::String): std::string::String` that
concatenates all parts in order, inserting the separator between consecutive parts (no leading or
trailing separator, empty input gives an empty string).
