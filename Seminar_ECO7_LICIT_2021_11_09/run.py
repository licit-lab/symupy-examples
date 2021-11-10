import argparse
import sys
from symupy.runtime.api import Simulator
from symupy.runtime.monitor import MonitorApp
from symupy.runtime.monitor.manager import LineMonitorView

from symupy.plugins.reader.symuflow import SymuFlowNetworkReader


def simulation_without_control(manhattanxml):
    simulator = Simulator()
    simulator.trace_flow = True
    simulator.step_launch_mode = "full"
    simulator.register_simulation(manhattanxml)

    with simulator as s:
        while s.do_next:
            s.run_step()
            yield s.simulationstep, s


def simulation_with_control(manhattanxml, controlsensor, maxveh=5):
    simulator = Simulator()
    simulator.trace_flow = True
    simulator.step_launch_mode = "full"
    simulator.register_simulation(manhattanxml)
    control = 0

    with simulator as s:
        while s.do_next:
            tron = s.request.datatraj.tron
            nbveh = 0
            for tr in tron.values():
                if tr in controlsensor:
                    nbveh += 1

            if s.simulationstep == 0:
                s.add_control_probability_zone_mfd({'Cpt_Inner': control}, {'Cpt_Inner': 0})

            if s.simulationstep > 0:
                if nbveh >= maxveh:
                    control = 1
                else:
                    control = 0
                s.modify_control_probability_zone_mfd({'Cpt_Inner': control})

            s.run_step()
            yield s.simulationstep, s


class MonitorVEHNumber(LineMonitorView):
    def __init__(self, title, sensor):
        super(MonitorVEHNumber, self).__init__(title, 'Step', 'VEH Number')
        self.sensor = set(sensor)

    def update(self, step, simulator, ind):
        tron = simulator.request.datatraj.tron
        nbveh = sum([1 if tr in self.sensor else 0 for tr in tron.values()])
        return step, nbveh


def parse_args():
    parser = argparse.ArgumentParser(description='Run SymuFlow simulation')
    parser.add_argument('--type', default='default',
                        help='Type of simulation, either free or control')

    args = parser.parse_args()

    return args.type


def main():
    SCENARIO = "network/ManhattanGrid/manhattan_2_sensors.xml"
    simu_type = parse_args()

    reader = SymuFlowNetworkReader(SCENARIO)
    sensor_inner = list(reader.iter_sensor('Cpt_Inner'))
    sensor_outer = list(reader.iter_sensor('Cpt_Outer'))

    if simu_type == 'free':
        itersim = simulation_without_control(SCENARIO)
    elif simu_type == 'control':
        itersim = simulation_with_control(SCENARIO, sensor_inner, maxveh=0)
    else:
        sys.exit("Error: type is either 'free' or 'control'")

    next(itersim)

    manager = MonitorApp()
    manager.add_monitor(MonitorVEHNumber("Inner", sensor_inner), 0, 0, colspan=2)
    manager.add_monitor(MonitorVEHNumber("Outer", sensor_outer), 1, 0, colspan=2)
    manager.set_feeder(itersim)
    manager.launch_app()


if __name__ == "__main__":
    main()
