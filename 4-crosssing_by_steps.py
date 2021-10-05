""" Simple step by step of bottleneck files.
"""
import os
from symupy.runtime.api import Simulator, Simulation
from ctypes import c_double, c_int, c_char_p

# https://gist.github.com/aladinoster/c477b37bb25ddc18c8d24229871d259e
LIBRARY_PATH = "/Users/andresladino/Documents/01-Code/02-Python/research/control-routing/symuflow/build/src/libSymuFlow.dylib"

scenario = os.path.join(
    os.getcwd(),
    "network",
    "Crossing",
    "crossing_singlevehicle.xml",
)

simulator = Simulator(step_launch_mode="full", library_path=LIBRARY_PATH)

simulator.register_simulation(scenario)

with simulator as s:
    simulator._Simulator__library.SymGetVehicleAcc.restype = c_double
    simulator._Simulator__library.SymGetVehicleSpeed.restype = c_double
    simulator._Simulator__library.SymGetVehicleLink.restype = c_char_p
    simulator._Simulator__library.SymGetVehicleX.restype = c_double
    simulator._Simulator__library.SymGetVehicleY.restype = c_double

    while s.do_next:
        s.run_step()

        # Retrieve original query
        # s.request.query

        # # Retreive vehicle data formated as dictionaries
        # s.request.get_vehicle_data()

        # # Retreive data as a vehicle list (printed as dataframe)
        print(s.vehicles)

        if s.simulationstep == 2:
            snewroute = "Link_A Link_C"
            print(
                s._Simulator__library.SymAlterRouteEx(
                    0, snewroute.encode("UTF8")
                )
            )

        print(f"\tLink: {s._Simulator__library.SymGetVehicleLink(c_int(0))}")
        print(f"\tX: {s._Simulator__library.SymGetVehicleX(c_int(0))}")
        print(f"\tY: {s._Simulator__library.SymGetVehicleY(c_int(0))}\n")
