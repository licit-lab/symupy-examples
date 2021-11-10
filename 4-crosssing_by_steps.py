""" Simple step by step route change of a vehicle in a crossing
"""
import os
from symupy.runtime.api import Simulator, Simulation
from ctypes import c_double, c_int, c_char_p

# https://gist.github.com/aladinoster/c477b37bb25ddc18c8d24229871d259e
LIBRARY_PATH = "/Users/andresladino/Documents/01-Code/11-Licit/symuvia/symuflow/build/src/libSymuFlow.dylib"

scenario = os.path.join(
    os.getcwd(), "network", "Crossing", "crossing_singlevehicle.xml",
)

simulator = Simulator(step_launch_mode="full", library_path=LIBRARY_PATH)

simulator.register_simulation(scenario)

if __name__ == "__main__":

    REROUTE = True

    with simulator as s:

        while s.do_next:

            if s.simulationstep == 2 and REROUTE:
                SNEWROUTE = "Link_A Link_C"
                output = s.drive_vehicle_new_route(0, SNEWROUTE)
                print(output)

            # print(s.vehicles)

            print(f"\tLink: {s.get_vehicle_link(0)}")

            s.run_step()
