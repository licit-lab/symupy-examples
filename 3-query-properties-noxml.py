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
simulator = Simulator(step_launch_mode="lite", library_path=LIBRARY_PATH)
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
    simulator._Simulator__library.SymGetVehicleAcc.restype = c_double
    simulator._Simulator__library.SymGetVehicleSpeed.restype = c_double
    simulator._Simulator__library.SymGetVehicleLink.restype = c_char_p
    simulator._Simulator__library.SymGetVehicleX.restype = c_double
    simulator._Simulator__library.SymGetVehicleY.restype = c_double

    while s.do_next:
        for veh_data in extract_veh_data(demand, s.simulationstep):
            vehid = s.create_vehicle_with_route(*veh_data)
            vehids.append(vehid)
        s.run_step()

        if s.simulationstep > 10 or s.simulationstep < 20:
            # catching data for veh id 0

            print(
                f"\n\tAcceleration: {s._Simulator__library.SymGetVehicleAcc(c_int(1))}"
            )
            print(
                f"\tSpeed: {s._Simulator__library.SymGetVehicleSpeed(c_int(1))}"
            )
            print(
                f"\tLink: {s._Simulator__library.SymGetVehicleLink(c_int(1))}"
            )
            print(f"\tX: {s._Simulator__library.SymGetVehicleX(c_int(1))}")
            print(f"\tY: {s._Simulator__library.SymGetVehicleY(c_int(1))}\n")

        if s.simulationstep > 20:
            s.stop_step()
