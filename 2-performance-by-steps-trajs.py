""" Simple step by step of manhattan grid files.
"""
import os
from symupy.runtime.api import Simulator
import pandas as pd

# Path
manhattanxml = os.path.join(
    os.getcwd(), "network", "ManhattanGrid", "manhattan_3X3_scenario_G.xml",
)

demandpath = os.path.join(
    os.getcwd(), "network", "ManhattanGrid", "demand_scenario_G.csv",
)

# Simulation file
simulator = Simulator(step_launch_mode="full")
simulator.register_simulation(manhattanxml)

# Demand file
read_demand = lambda demand_path: pd.read_csv(demand_path, sep=";")
demand = read_demand(demandpath)

# Auxiliary functions
def extract_veh_data(demand: pd.DataFrame, time: int) -> tuple:
    creation_query = f"{time} < creation<={time+1}"
    current_demand = demand.query(creation_query)
    # Generator
    for _, veh in current_demand.iterrows():
        yield (
            veh["typeofvehicle"],
            veh["origin"],
            veh["destination"],
            1,
            veh["creation"],
            veh["path"],
        )


if __name__ == "__main__":

    vehids = []

    with simulator as s:
        vehids = []
        while s.do_next:
            for veh_data in extract_veh_data(demand, s.simulationstep):
                vehid = s.create_vehicle_with_route(*veh_data)
                vehids.append(vehid)

            s.run_step()

            # Retrieve original query
            # s.request.query

            # # Retreive vehicle data formated as dictionaries
            # s.request.get_vehicle_data()

            # # Retreive data as a vehicle list (printed as dataframe)
            # s.vehicles
