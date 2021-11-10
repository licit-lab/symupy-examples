""" Launch a monitoring app for your simulation
"""

import os

from symupy.runtime.monitor import (
    MonitorApp,
    SymuviaMonitorMFD,
    SymuviaMonitorAccumulation,
    SymuviaMonitorVEH,
    SymuviaMonitorTTT,
    SymuviaMonitorTTD,
    SymuviaMonitorFlux,
    launch_simuflow,
)

FILE = os.path.join(
    os.getcwd(),
    "network",
    "SingleLink",
    "SingleLink_withcapacityrestriction.xml",
)

manager = MonitorApp()
manager.add_monitor(SymuviaMonitorMFD(), 0, 0)
manager.add_monitor(SymuviaMonitorAccumulation(), 0, 1)
manager.add_monitor(SymuviaMonitorVEH([3, 58], "speed"), 1, 0)
manager.add_monitor(SymuviaMonitorTTT(["L_0"], aggregation_period=1), 1, 1)
manager.add_monitor(
    SymuviaMonitorTTD(["L_0"], aggregation_period=1), 0, 2, rowspan=2
)
manager.add_monitor(
    SymuviaMonitorFlux(["L_0"], aggregation_period=10), 2, 0, colspan=3
)
manager.set_feeder(launch_simuflow(FILE))

if __name__ == "__main__":
    manager.launch_app()
