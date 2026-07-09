module robo::battery {
    public struct Battery has key, store {
        id: UID,
        serial: u64,
        charge: u64,
    }

    public struct Robot has key {
        id: UID,
        battery: Battery,
    }

    public fun build_robot(ctx: &mut TxContext): Robot {
        Robot {
            id: object::new(ctx),
            battery: Battery {
                id: object::new(ctx),
                serial: 0,
                charge: 100,
            },
        }
    }

    public fun swap_battery(robot: &mut Robot, fresh: Battery): Battery {
        let mut depleted = fresh;
        std::mem::swap(&mut robot.battery, &mut depleted);
        depleted
    }

    public fun recharge(battery: &mut Battery, amount: u64) {
        let new_charge = battery.charge + amount;
        if (new_charge > 100) {
            battery.charge = 100;
        } else {
            battery.charge = new_charge;
        };
    }

    public fun charge_level(robot: &Robot): u64 {
        robot.battery.charge
    }
}
