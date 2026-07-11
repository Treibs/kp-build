module tram_depot::tram {
  use sui::event;

  public struct DispatcherCap has key {
    id: UID,
  }

  public struct Tram has key {
    id: UID,
    total_shifts: u64,
    last_route: u64,
    last_driver: address,
  }

  public struct ShiftRecord has copy, drop {
    route: u64,
    driver: address,
  }

  public struct DayClosed has copy, drop {
    route: u64,
    driver: address,
    total_shifts: u64,
  }

  public struct DayClosedZeroed has copy, drop {
    total_shifts: u64,
  }

  fun init(ctx: &mut TxContext) {
    let cap = DispatcherCap {
      id: object::new(ctx),
    };
    transfer::transfer(cap, ctx.sender());
  }

  public fun create_tram(ctx: &mut TxContext): Tram {
    Tram {
      id: object::new(ctx),
      total_shifts: 0,
      last_route: 0,
      last_driver: @0x0,
    }
  }

  public fun record_shift(_cap: &DispatcherCap, tram: &mut Tram, route: u64, driver: address) {
    tram.last_route = route;
    tram.last_driver = driver;
    tram.total_shifts = tram.total_shifts + 1;
    event::emit(ShiftRecord { route, driver });
  }

  public fun close_day(tram: &mut Tram) {
    if (tram.total_shifts > 0) {
      event::emit(DayClosed {
        route: tram.last_route,
        driver: tram.last_driver,
        total_shifts: tram.total_shifts,
      });
    } else {
      event::emit(DayClosedZeroed {
        total_shifts: 0,
      });
    };
  }

  public fun total_shifts(tram: &Tram): u64 {
    tram.total_shifts
  }
}
