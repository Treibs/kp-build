A racing ghost system: each track (shared object) holds at most one `GhostRun` object — the
best run so far (driver + time). Submitting a faster run replaces the stored ghost: the new
run takes its place and the old ghost object is returned to the previous record holder as a
keepsake. A slower submission is returned to the sender untouched. View: the current record
time for a track, if any run exists.
