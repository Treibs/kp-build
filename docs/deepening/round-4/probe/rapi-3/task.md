Write a Sui Move module `robo::battery` (edition 2024). A `Robot` is an owned object that always
has exactly one `Battery` installed; a battery has a serial number and a charge level.
`build_robot` creates and returns a robot with a factory battery (serial 0, full charge 100).
`swap_battery(robot, fresh)` installs the fresh battery into the robot and returns the depleted
battery it replaced, so the caller can send it off for recycling. `recharge(battery, amount)`
tops up a battery that is out of the robot, capping the charge at 100. `charge_level(robot)` is
a public view returning the installed battery's charge.
