A gym locker room: members are assigned `Locker` objects (number and combination) by the
front desk (capability). A member who loses their key gets a replacement: the old locker
object is destroyed and a new one (same number, fresh combination) is issued to them, with a
`Rekeyed` event recording which locker object was retired and which replaced it. Replacement
costs a small SUI fee into the gym's pool.
