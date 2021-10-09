""" Simple step by step of manhattan grid files.
"""
import os
from ctypes import c_int, c_double, c_char, c_char_p
from symupy.runtime.api import Simulator
import pandas as pd

# This should be based on compilation see: https://gist.github.com/aladinoster/c477b37bb25ddc18c8d24229871d259e
LIBRARY_PATH = "/Users/andresladino/Documents/01-Code/02-Python/research/control-routing/symuflow/build/src/libSymuFlow.dylib"

# Path
manhattanxml = os.path.join(
    os.getcwd(),
    "network",
    "ManhattanGrid",
    "manhattan_3X3_scenario_G.xml",
)

demandpath = os.path.join(
    os.getcwd(),
    "network",
    "ManhattanGrid",
    "demand_scenario_G.csv",
)

# Simulation file
simulator = Simulator(
    write_xml=False, step_launch_mode="lite", library_path=LIBRARY_PATH
)
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


vehids = []


with simulator as s:
    vehids = []

    while s.do_next:
        for veh_data in extract_veh_data(demand, s.simulationstep):
            vehid = s.create_vehicle_with_route(*veh_data)
            vehids.append(vehid)
        s.run_step()

        if s.simulationstep > 10 or s.simulationstep < 20:
            # catching data for veh id 0

            print(
                f"""
                \tAcceleration: {s.get_vehicle_acceleration(1)}
                \tSpeed: {s.get_vehicle_speed(1)}
                \tLink: {s.get_vehicle_link(1)}
                \tAbscissa: {s.get_vehicle_abscissa(1)}
                \tOrdinate: {s.get_vehicle_ordinate(1)}
                \tLane: {s.get_vehicle_lane(1)}
                \tDistance: {s.get_vehicle_distance(1)}
                \tTotal Distance: {s.get_vehicle_total_travel_distance(1)}
                \tTotal Time: {s.get_vehicle_total_travel_time(1)}
            """
            )

        if s.simulationstep > 20:
            s.stop_step()
