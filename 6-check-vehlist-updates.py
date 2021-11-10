"""
Finite demand
=============
This script is for testing the number of vehicles registered within the network. Plus the object creation.
"""

import os
from symupy.runtime.api import Simulator

import objgraph # Uncomment for memory tracing

# https://gist.github.com/aladinoster/c477b37bb25ddc18c8d24229871d259e
LIBRARY_PATH = "/Users/andresladino/Documents/01-Code/11-Licit/symuvia/symuflow/build/src/libSymuFlow.dylib"

bottleneck01 = os.path.join(
    os.getcwd(), "network", "SingleLink", "SingleLink_hybridfiniteflow.xml",
)

simulator = Simulator(step_launch_mode="full",library_path=LIBRARY_PATH)

simulator.register_simulation(bottleneck01)


if __name__ == "__main__":

    objgraph.show_most_common_types()

    with simulator as s:
        objgraph.show_growth()
        while s.do_next:
            s.run_step()

            print("Nb vehicles:", len(s.vehicles))

    objgraph.show_growth()