A firework show: a pyrotechnician loads `Firework` objects (name and burst size) into a rack,
then `run_show` fires them all in loading order — each firework is consumed with a `Burst`
event carrying its name and size — leaving the rack spent and the show marked complete. A
view reports how many fireworks are loaded before the show.
