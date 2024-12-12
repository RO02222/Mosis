import functools
import dataclasses
from lib.test import run_scenarios, AbstractEnvironmentState

from srcgen.lock_controller import LockController
# from srcgen.solution import Solution as LockController # Teacher's solution

# For each test scenario, sends a sequence of timed input events to the statechart, and checks if the expected sequence of timed output events occurs.

# Each timed event is a tuple (timestamp, event_name, parameter_value)
# For events that don't have a parameter, the parameter value is always 'None'.
# Timestamps are in nanoseconds since simulation start!

SCENARIOS = [
{
    "name": "normal operation, serve two requests",
    "input_events": [
        (0, "water_lvl", 508),
        (2393556604, "request_lvl_change", None),
        (4493556604, "water_lvl", 675),
        (4593556604, "water_lvl", 811),
        (4693556604, "water_lvl", 926),
        (4793556604, "water_lvl", 1025),
        (4893556604, "water_lvl", 1105),
        (4993556604, "water_lvl", 1176),
        (5093556604, "water_lvl", 1228),
        (5193556604, "water_lvl", 1276),
        (5293556604, "water_lvl", 1316),
        (5393556604, "water_lvl", 1352),
        (5493556604, "water_lvl", 1375),
        (5593556604, "water_lvl", 1395),
        (5693556604, "water_lvl", 1419),
        (5793556604, "water_lvl", 1433),
        (5893556604, "water_lvl", 1443),
        (5993556604, "water_lvl", 1460),
        (6093556604, "water_lvl", 1470),
        (6193556604, "water_lvl", 1476),
        (6293556604, "water_lvl", 1483),
        (6393556604, "water_lvl", 1482),
        (6493556604, "water_lvl", 1491),
        (6593556604, "water_lvl", 1496),
        (6693556604, "water_lvl", 1497),
        (6793556604, "water_lvl", 1498),
        (6893556604, "water_lvl", 1496),
        (6993556604, "water_lvl", 1501),
        (7093556604, "water_lvl", 1504),
        (7193556604, "water_lvl", 1509),
        (9193747734, "request_lvl_change", None),
        (11293747734, "water_lvl", 1341),
        (11393747734, "water_lvl", 1197),
        (11493747734, "water_lvl", 1084),
        (11593747734, "water_lvl", 981),
        (11693747734, "water_lvl", 906),
        (11793747734, "water_lvl", 836),
        (11893747734, "water_lvl", 774),
        (11993747734, "water_lvl", 735),
        (12093747734, "water_lvl", 692),
        (12193747734, "water_lvl", 664),
        (12293747734, "water_lvl", 636),
        (12393747734, "water_lvl", 606),
        (12493747734, "water_lvl", 592),
        (12593747734, "water_lvl", 581),
        (12693747734, "water_lvl", 561),
        (12793747734, "water_lvl", 551),
        (12893747734, "water_lvl", 548),
        (12993747734, "water_lvl", 533),
        (13093747734, "water_lvl", 531),
        (13193747734, "water_lvl", 522),
        (13293747734, "water_lvl", 525),
        (13393747734, "water_lvl", 520),
        (13493747734, "water_lvl", 513),
        (13593747734, "water_lvl", 507),
        (13693747734, "water_lvl", 507),
        (13793747734, "water_lvl", 507),
        (13893747734, "water_lvl", 510),
        (13993747734, "water_lvl", 501),
        (14093747734, "water_lvl", 504),
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (2393556604, "red_light", 0),
        (4393556604, "close_doors", 0),
        (2393556604, "set_request_pending", True),
        (4393556604, "open_flow", 1),
        (7193556604, "close_flow", 1),
        (7193556604, "set_request_pending", False),
        (7193556604, "open_doors", 1),
        (7193556604, "green_light", 1),
        (9193747734, "red_light", 1),
        (11193747734, "close_doors", 1),
        (9193747734, "set_request_pending", True),
        (11193747734, "open_flow", 0),
        (14193747734, "close_flow", 0),
        (14193747734, "set_request_pending", False),
        (14193747734, "open_doors", 0),
        (14193747734, "green_light", 0),
    ],
},
{
    "name": "break sensor, fix sensor, then change water lvl",
    "input_events": [
        (0, "water_lvl", 508),
        (2084169493, "water_lvl", 99007),
        (4084274216, "water_lvl", 504),
        (5420871976, "resume", None),
        (7100735485, "request_lvl_change", None),
        (9200735485, "water_lvl", 670),
        (9300735485, "water_lvl", 812),
        (9400735485, "water_lvl", 927),
        (9500735485, "water_lvl", 1028),
        (9600735485, "water_lvl", 1104),
        (9700735485, "water_lvl", 1173),
        (9800735485, "water_lvl", 1231),
        (9900735485, "water_lvl", 1281),
        (10000735485, "water_lvl", 1316),
        (10100735485, "water_lvl", 1346),
        (10200735485, "water_lvl", 1378),
        (10300735485, "water_lvl", 1399),
        (10400735485, "water_lvl", 1414),
        (10500735485, "water_lvl", 1436),
        (10600735485, "water_lvl", 1450),
        (10700735485, "water_lvl", 1459),
        (10800735485, "water_lvl", 1469),
        (10900735485, "water_lvl", 1471),
        (11000735485, "water_lvl", 1481),
        (11100735485, "water_lvl", 1488),
        (11200735485, "water_lvl", 1490),
        (11300735485, "water_lvl", 1492),
        (11400735485, "water_lvl", 1491),
        (11500735485, "water_lvl", 1497),
        (11600735485, "water_lvl", 1501),
        (11700735485, "water_lvl", 1506),
        (11800735485, "water_lvl", 1508),
        (11900735485, "water_lvl", 1504),
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (2084169493, "red_light", 0),
        (2084169493, "close_doors", 0),
        (2084169493, "set_sensor_broken", None),
        (5420871976, "open_doors", 0),
        (5420871976, "green_light", 0),
        (7100735485, "red_light", 0),
        (7100735485, "set_request_pending", True),
        (9100735485, "close_doors", 0),
        (9100735485, "open_flow", 1),
        (11900735485, "close_flow", 1),
        (11900735485, "set_request_pending", False),
        (11900735485, "open_doors", 1),
        (11900735485, "green_light", 1),
    ],
},
{
    "name": "break sensor DURING water lvl change, then fix and resume",
    "input_events": [
        (0, "water_lvl", 508),
        (2661508910, "request_lvl_change", None),
        (4761508910, "water_lvl", 675),
        (4861508910, "water_lvl", 811),
        (4961508910, "water_lvl", 926),
        (5061508910, "water_lvl", 1025),
        (5093300938, "water_lvl", 99004),
        (7821829184, "water_lvl", 1028),
        (9213791769, "resume", None),
        (9313791769, "water_lvl", 1104),
        (9413791769, "water_lvl", 1173),
        (9513791769, "water_lvl", 1231),
        (9613791769, "water_lvl", 1281),
        (9713791769, "water_lvl", 1316),
        (9813791769, "water_lvl", 1346),
        (9913791769, "water_lvl", 1378),
        (10013791769, "water_lvl", 1399),
        (10113791769, "water_lvl", 1414),
        (10213791769, "water_lvl", 1436),
        (10313791769, "water_lvl", 1450),
        (10413791769, "water_lvl", 1459),
        (10513791769, "water_lvl", 1469),
        (10613791769, "water_lvl", 1471),
        (10713791769, "water_lvl", 1481),
        (10813791769, "water_lvl", 1488),
        (10913791769, "water_lvl", 1490),
        (11013791769, "water_lvl", 1492),
        (11113791769, "water_lvl", 1491),
        (11213791769, "water_lvl", 1497),
        (11313791769, "water_lvl", 1501),
        (11413791769, "water_lvl", 1506),
        (11513791769, "water_lvl", 1508),
        (11613791769, "water_lvl", 1504),
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (2661508910, "red_light", 0),
        (2661508910, "set_request_pending", True),
        (4661508910, "close_doors", 0),
        (4661508910, "open_flow", 1),
        (5093300938, "close_flow", 1),
        (5093300938, "set_sensor_broken", None),
        (9213791769, "open_flow", 1),
        (11613791769, "close_flow", 1),
        (11613791769, "set_request_pending", False),
        (11613791769, "open_doors", 1),
        (11613791769, "green_light", 1),
    ],
},
{
    "name": "2 pendings with both broken sensor DURING water lvl change",
    "input_events":
    [(0, 'water_lvl', 508), (1708282000.0, 'request_lvl_change', None), (3808282000.0, 'water_lvl', 675), (3908282000.0, 'water_lvl', 811), (4008282000.0, 'water_lvl', 926), (4108282000.0, 'water_lvl', 1025), (4134066800.0, 'water_lvl', 99004), (6610830900.0, 'water_lvl', 1028), (7781407300.0, 'resume', None), (7881407300.0, 'water_lvl', 1104), (7981407300.0, 'water_lvl', 1173), (8081407300.0, 'water_lvl', 1231), (8181407300.0, 'water_lvl', 1281), (8281407300.0, 'water_lvl', 1316), (8381407300.0, 'water_lvl', 1346), (8481407300.0, 'water_lvl', 1378), (8581407300.0, 'water_lvl', 1399), (8681407300.0, 'water_lvl', 1414), (8781407300.0, 'water_lvl', 1436), (8881407300.0, 'water_lvl', 1450), (8981407300.0, 'water_lvl', 1459), (9081407300.0, 'water_lvl', 1469), (9181407300.0, 'water_lvl', 1471), (9281407300.0, 'water_lvl', 1481), (9381407300.0, 'water_lvl', 1488), (9481407300.0, 'water_lvl', 1490), (9581407300.0, 'water_lvl', 1492), (9681407300.0, 'water_lvl', 1491), (9781407300.0, 'water_lvl', 1497), (9881407300.0, 'water_lvl', 1501), (9981407300.0, 'water_lvl', 1506), (10081407300.0, 'water_lvl', 1508), (10181407300.0, 'water_lvl', 1504), (12864339000.0, 'request_lvl_change', None), (14964339000.0, 'water_lvl', 1340), (15064339000.0, 'water_lvl', 1195), (15164339000.0, 'water_lvl', 1084), (15264339000.0, 'water_lvl', 984), (15364339000.0, 'water_lvl', 898), (15434342400.0, 'water_lvl', 99007), (16703926500.0, 'water_lvl', 902), (17472391800.0, 'resume', None), (17572391800.0, 'water_lvl', 839), (17672391800.0, 'water_lvl', 781), (17772391800.0, 'water_lvl', 727), (17872391800.0, 'water_lvl', 693), (17972391800.0, 'water_lvl', 665), (18072391800.0, 'water_lvl', 631), (18172391800.0, 'water_lvl', 610), (18272391800.0, 'water_lvl', 596), (18372391800.0, 'water_lvl', 574), (18472391800.0, 'water_lvl', 564), (18572391800.0, 'water_lvl', 550), (18672391800.0, 'water_lvl', 549), (18772391800.0, 'water_lvl', 539), (18872391800.0, 'water_lvl', 529), (18972391800.0, 'water_lvl', 521), (19072391800.0, 'water_lvl', 519), (19172391800.0, 'water_lvl', 517), (19272391800.0, 'water_lvl', 518), (19372391800.0, 'water_lvl', 507), (19472391800.0, 'water_lvl', 510), (19572391800.0, 'water_lvl', 509), (19672391800.0, 'water_lvl', 506), (19772391800.0, 'water_lvl', 508), (19872391800.0, 'water_lvl', 504)],
    "output_events":
    [(0, 'open_doors', 0), (0, 'green_light', 0), (1708282000.0, 'set_request_pending', True), (1708282000.0, 'red_light', 0), (3708282000.0, 'close_doors', 0), (3708282000.0, 'open_flow', 1), (4134066800.0, 'red_light', 0), (4134066800.0, 'red_light', 1), (4134066800.0, 'close_doors', 0), (4134066800.0, 'close_doors', 1), (4134066800.0, 'close_flow', 0), (4134066800.0, 'close_flow', 1), (4134066800.0, 'set_sensor_broken', None), (7781407300.0, 'open_flow', 1), (10181407300.0, 'close_flow', 1), (10181407300.0, 'set_request_pending', False), (10181407300.0, 'open_doors', 1), (10181407300.0, 'green_light', 1), (12864339000.0, 'set_request_pending', True), (12864339000.0, 'red_light', 1), (14864339000.0, 'close_doors', 1), (14864339000.0, 'open_flow', 0), (15434342400.0, 'red_light', 0), (15434342400.0, 'red_light', 1), (15434342400.0, 'close_doors', 0), (15434342400.0, 'close_doors', 1), (15434342400.0, 'close_flow', 0), (15434342400.0, 'close_flow', 1), (15434342400.0, 'set_sensor_broken', None), (17472391800.0, 'open_flow', 0), (19872391800.0, 'close_flow', 0), (19872391800.0, 'set_request_pending', False), (19872391800.0, 'open_doors', 0), (19872391800.0, 'green_light', 0)]
}
]

LOW = 0
HIGH = 1

# Simulated state of the 'plant'.
# This is used for checking whether an event has any effect wrt. idempotency
@dataclasses.dataclass
class PlantState(AbstractEnvironmentState):
    # initial state of the plant
    door_low_open: bool = False
    door_high_open: bool = False
    flow_low_open: bool = False
    flow_high_open: bool = False
    light_low: str = "RED"
    light_high: str = "RED"
    request_is_pending: bool = False
    sensor_is_broken: bool = False

    def handle_event(self, event_name, param):
        if event_name == "open_doors":
            if param == LOW:
                return dataclasses.replace(self, door_low_open=True)
            elif param == HIGH:
                return dataclasses.replace(self, door_high_open=True)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "close_doors":
            if param == LOW:
                return dataclasses.replace(self, door_low_open=False)
            elif param == HIGH:
                return dataclasses.replace(self, door_high_open=False)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "open_flow":
            if param == LOW:
                return dataclasses.replace(self, flow_low_open=True)
            elif param == HIGH:
                return dataclasses.replace(self, flow_high_open=True)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "close_flow":
            if param == LOW:
                return dataclasses.replace(self, flow_low_open=False)
            elif param == HIGH:
                return dataclasses.replace(self, flow_high_open=False)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "green_light":
            if param == LOW:
                return dataclasses.replace(self, light_low="GREEN")
            elif param == HIGH:
                return dataclasses.replace(self, light_high="GREEN")
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "red_light":
            if param == LOW:
                return dataclasses.replace(self, light_low="RED")
            elif param == HIGH:
                return dataclasses.replace(self, light_high="RED")
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "set_request_pending":
            return dataclasses.replace(self, request_is_pending=param)
        elif event_name == "set_sensor_broken":
            return dataclasses.replace(self, sensor_is_broken=param)
        else:
            raise Exception("don't know how to handle event:", event_name)

if __name__ == "__main__":
    run_scenarios(SCENARIOS, LockController, PlantState, verbose=False)
