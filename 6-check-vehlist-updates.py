import os
from symupy.runtime.api import Simulator, Simulation

bottleneck01 = os.path.join(
    os.getcwd(), "network", "SingleLink", "SingleLink_hybridfiniteflow.xml",
)

simulator = Simulator(step_launch_mode="full")

simulator.register_simulation(bottleneck01)


if __name__ == "__main__":

    with simulator as s:
        while s.do_next:
            s.run_step()˝

            print("Nb vehicles:", len(s.vehicles))
