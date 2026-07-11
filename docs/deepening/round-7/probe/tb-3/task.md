A tram depot: each tram object logs shift records — the route number driven and the driver's
address — appended at shift end by the dispatcher (capability). At day close the depot wants
the tram's final shift (route and driver together) reported in a `DayClosed` event, or a
zeroed event if the tram never ran. View: total shifts logged on a tram.
