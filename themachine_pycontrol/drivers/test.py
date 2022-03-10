from hotplate import Hotplate
from valve import ValveModule, Valve
from relay import RelayModule, Relay
from vial import Container
from pump import PumpModule, Pump

hotplate1 = Hotplate(1)
hotplate1.heat(True, 30)
hotplate1.stir(True, 120)


valve_mod1 = ValveModule(1)
valve_mod1.valves[1].move(5) #move valve 1 to waste port 5

relay_mod1 = RelayModule(1)
relay_mod1.relays[1].set_relay(True)
relay_mod1.relays[1].read_relay()


pump_mod1 = PumpModule()
pump_mod1.pumps[1].move(5, topspeed = , volume = , True)
pump_mod1.pumps[1].dispense(1, 5, topspeed = , volume = , True)
pump_mod1.pumps[1].rinse(1, topspeed = , volume = , True)

#vial_1 = Container(min_volume = 1, max_volume = 10, current_volume = 1)





