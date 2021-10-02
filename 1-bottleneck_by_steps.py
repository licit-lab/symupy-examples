""" Simple step by step of bottleneck files.
"""
import os
from symupy.runtime.api import Simulator, Simulation

bottleneck01 = os.path.join(
    os.getcwd(),
    "network",
    "SingleLink",
    "SingleLink_withcapacityrestriction.xml",
)

simulator = Simulator(step_launch_mode="full")

simulator.register_simulation(bottleneck01)

with simulator as s:
    while s.do_next:
        s.run_step()

        # Retrieve original query
        # s.request.query

        # # Retreive vehicle data formated as dictionaries
        # s.request.get_vehicle_data()

        # # Retreive data as a vehicle list (printed as dataframe)
        s.vehicles
