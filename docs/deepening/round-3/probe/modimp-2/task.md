Write a Sui Move module `beacon::status` (edition 2024). Each user can create their own owned
`Beacon` object carrying a status code (`u8`) and a note (`std::string::String`). Updating either
field must emit a `StatusChanged` event carrying the beacon's ID, the new status code, and the
epoch of the change. Creating a beacon must emit a `BeaconCreated` event with the beacon's ID and
the owner address. Provide `create`, `set_status`, and `set_note` entry functions.
