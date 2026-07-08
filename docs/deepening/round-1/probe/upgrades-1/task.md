Write a Sui Move module `registry::registry` (edition 2024) implementing the version-gated
shared-object pattern used for package upgrades. A shared `Registry` object has a `version: u64`
field and a package constant `VERSION: u64 = 1`. Every entry function must assert the object's
version equals the package VERSION before doing anything (named constant abort code). Include an
`AdminCap`-gated `migrate` entry function that sets the object's version to the package VERSION,
aborting if the object version is already current or newer. Registry state: a `total: u64` counter
with an entry `increment`.
