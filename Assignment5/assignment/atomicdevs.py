from copy import deepcopy
### EDIT THIS FILE ###

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses
import collections

@dataclasses.dataclass
class QueueState:
    queues: dict
    remaining_time: float
    outgoing_ship: Ship|None
    def __init__(self, ship_sizes):
        self.queues = {}
        for size in ship_sizes:
            self.queues[size] = []
        self.remaining_time = float("inf")
        self.outgoing_ship = None

class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        self.state = QueueState(ship_sizes)
        self.in_ship = self.addInPort("in_ship")
        self.in_get_ship = self.addInPort("in_get_ship")
        self.out_ship = self.addOutPort("out_ship")
        self.in_return_ship = self.addInPort("in_return_ship")
        self.out_available_ships = self.addOutPort("out_available_ships")

    def extTransition(self, inputs):
        if self.in_return_ship in inputs:
            self.state.queues[inputs[self.in_return_ship].size].append(inputs[self.in_return_ship])
            self.state.outgoing_ship = None
            self.state.remaining_time = 0
            return self.state

        if self.in_ship in inputs:
            self.state.queues[inputs[self.in_ship].size].insert(0, inputs[self.in_ship])
            self.state.outgoing_ship = None
            self.state.remaining_time = 0

        if self.in_get_ship in inputs:
            assert self.state.outgoing_ship is None, f"WTF {inputs}"
            self.state.outgoing_ship = self.state.queues[inputs[self.in_get_ship]].pop()
            self.state.remaining_time = 0

        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        output = {self.out_available_ships: {key: len(value) for key, value in self.state.queues.items()}}
        if self.state.outgoing_ship is not None:
            output[self.out_ship] = self.state.outgoing_ship
        return output
    
    def intTransition(self):
        #only called on out event
        self.state.remaining_time = float("inf")
        self.state.outgoing_ship = None
        return self.state

@dataclasses.dataclass
class LoadBalancerState:
    remaining_time: float
    lock_capacities: list
    lock_available_space: list
    next_ship: Ship|None
    priority: int
    lock_open_list: list
    current_serving_lock: int
    available_ship_count_in_queue: dict
    locked: bool
    get_ship_size: int
    wait_for_ship: bool
    def __init__(self, lock_capacities, priority):
        self.lock_capacities = lock_capacities
        self.lock_available_space = deepcopy(lock_capacities)
        self.remaining_time = float("inf")
        self.next_ship = None
        self.priority = priority
        self.lock_open_list = [True] * len(lock_capacities)
        self.current_serving_lock = 0
        self.available_ship_count_in_queue = {}
        self.locked = False
        self.get_ship_size = -1
        self.wait_for_ship = False
        #0: ship is ready to be moved
        #1: there are ships availble in queue
        #2: ship is ack
        #3: the lock state changed

PRIORITIZE_BIGGER_SHIPS = 0
PRIORITIZE_SMALLER_SHIPS = 1

class RoundRobinLoadBalancer(AtomicDEVS):
    def __init__(self,
                 lock_capacities=[3, 2],  # two locks of capacities 3 and 2.
                 priority=PRIORITIZE_BIGGER_SHIPS,
                 ):
        super().__init__("RoundRobinLoadBalancer")
        self.state = LoadBalancerState(lock_capacities, priority)
        self.in_ship = self.addInPort("in_ship")
        self.out_return_ship = self.addOutPort("out_return_ship")
        self.out_get_ship = self.addOutPort("out_get_ship")
        self.in_available_ships = self.addInPort("in_available_ships")

        self.out_ship_list = []
        self.in_lock_opened_list = []
        for i in range(len(lock_capacities)):
            self.out_ship_list.append(self.addOutPort(f"out_ship_{i}"))
            self.in_lock_opened_list.append(self.addInPort(f"in_lock_open_{i}"))

        self.state.remaining_time = 0

    def extTransition(self, inputs):
        if self.in_available_ships in inputs:
            self.state.available_ship_count_in_queue = inputs[self.in_available_ships]
            if self.state.locked:
                self.state.remaining_time = 0

        if self.in_ship in inputs:  # pass boat trough
            self.state.next_ship = inputs[self.in_ship]
            self.state.remaining_time = 0
            return self.state

        for i in range(len(self.state.lock_capacities)):  # When lock open/locked changes
            if self.in_lock_opened_list[i] in inputs:
                if inputs[self.in_lock_opened_list[i]] and self.state.lock_open_list[i] == False:
                    self.state.lock_available_space[i] = self.state.lock_capacities[i]
                    self.state.remaining_time = 0
                self.state.lock_open_list[i] = inputs[self.in_lock_opened_list[i]]

        return self.state

    def timeAdvance(self):
        return self.state.remaining_time

    def outputFnc(self):
        if self.state.next_ship is not None and self.state.lock_open_list[self.state.current_serving_lock]:
            return {self.out_ship_list[self.state.current_serving_lock]: self.state.next_ship}
        elif self.state.next_ship is not None and not self.state.lock_open_list[self.state.current_serving_lock]:
            return {self.out_return_ship: self.state.next_ship}
        elif self.state.get_ship_size != -1:
            return {self.out_get_ship: self.state.get_ship_size}
        return {}

    def check_if_boats_and_lock_are_available(self):
        """
        checks for valid combination
        """
        for i in range(len(self.state.lock_capacities)):
            if self.get_needed_ship_size(i) != -1:
                return True
        return False

    def get_needed_ship_size(self, lock=None):
        """
        Based on self.state.current_serving_lock
        """
        if lock is None:
            lock = self.state.current_serving_lock
        ordered_queues = sorted(self.state.available_ship_count_in_queue.items(), reverse=(self.state.priority == PRIORITIZE_BIGGER_SHIPS))#order depending on priority
        for boat_size, boats in ordered_queues:
            if self.state.available_ship_count_in_queue[boat_size] > 0 and self.state.lock_available_space[lock] >= boat_size and self.state.lock_open_list[lock]:
                return boat_size
        return -1

    def intTransition(self):
        if self.state.next_ship is not None:
            self.state.lock_available_space[self.state.current_serving_lock] -= self.state.next_ship.size
            self.state.current_serving_lock = (self.state.current_serving_lock + 1) % len(self.state.lock_capacities)  # take other lock when a ship was moved
            self.state.wait_for_ship = False
        self.state.next_ship = None
        self.state.locked = False

        if self.state.wait_for_ship:
            self.state.get_ship_size = -1
            self.state.remaining_time = float("inf")
        elif not self.check_if_boats_and_lock_are_available():
            self.state.locked = True
            self.state.remaining_time = float("inf")  # There can nothing be done wait for a new external event
        else:
            self.state.wait_for_ship = True
            self.state.remaining_time = 0
            self.state.get_ship_size = self.get_needed_ship_size()  # try the next lock (roundrobin)
            while self.state.get_ship_size == -1:  # When the default roundrobin lock is not valid loop until a valid lock is found, cannot be an inf loop because of the check_if_boats_and_lock_are_available
                self.state.current_serving_lock = (self.state.current_serving_lock + 1) % len(self.state.lock_capacities)
                self.state.get_ship_size = self.get_needed_ship_size()

        return self.state


class FillErUpLoadBalancer(AtomicDEVS):
    def __init__(self,
                 lock_capacities=[3, 2],  # two locks of capacities 3 and 2.
                 priority=PRIORITIZE_BIGGER_SHIPS,
                 ):
        super().__init__("FillErUpLoadBalancer")
        self.state = LoadBalancerState(lock_capacities, priority)
        self.in_ship = self.addInPort("in_ship")
        self.out_return_ship = self.addOutPort("out_return_ship")
        self.out_get_ship = self.addOutPort("out_get_ship")
        self.in_available_ships = self.addInPort("in_available_ships")

        self.out_ship_list = []
        self.in_lock_opened_list = []
        for i in range(len(lock_capacities)):
            self.out_ship_list.append(self.addOutPort(f"out_ship_{i}"))
            self.in_lock_opened_list.append(self.addInPort(f"in_lock_open_{i}"))

        self.state.remaining_time = 0

    def extTransition(self, inputs):
        if self.in_available_ships in inputs:
            self.state.available_ship_count_in_queue = inputs[self.in_available_ships]
            if self.state.locked:
                self.state.remaining_time = 0

        if self.in_ship in inputs:  # pass boat trough
            self.state.next_ship = inputs[self.in_ship]
            self.state.remaining_time = 0
            return self.state

        for i in range(len(self.state.lock_capacities)):  # When lock open/locked changes
            if self.in_lock_opened_list[i] in inputs:
                if inputs[self.in_lock_opened_list[i]] and self.state.lock_open_list[i] == False:
                    self.state.lock_available_space[i] = self.state.lock_capacities[i]
                    self.state.remaining_time = 0
                self.state.lock_open_list[i] = inputs[self.in_lock_opened_list[i]]

        return self.state

    def timeAdvance(self):
        return self.state.remaining_time

    def outputFnc(self):
        if self.state.next_ship is not None and self.state.lock_open_list[self.state.current_serving_lock]:
            return {self.out_ship_list[self.state.current_serving_lock]: self.state.next_ship}
        elif self.state.next_ship is not None and not self.state.lock_open_list[self.state.current_serving_lock]:
            return {self.out_return_ship: self.state.next_ship}
        elif self.state.get_ship_size != -1:
            return {self.out_get_ship: self.state.get_ship_size}
        return {}

    def get_needed_optimal_ship_and_lock(self):
        """
        Based on self.state.current_serving_lock
        """
        maximal_fill = (-1, -1, +float("inf"))
        for lock in range(len(self.state.lock_capacities) - 1, -1, -1):
            if not self.state.lock_open_list[lock]:
                continue
            for boat_size, boats in self.state.available_ship_count_in_queue.items():
                if self.state.available_ship_count_in_queue[boat_size] > 0 and self.state.lock_available_space[
                    lock] >= boat_size:
                    if self.state.lock_available_space[lock] - boat_size < maximal_fill[2]:
                        maximal_fill = (lock, boat_size, self.state.lock_available_space[lock] - boat_size)
                    elif self.state.lock_available_space[lock] - boat_size == maximal_fill[2] and (
                            PRIORITIZE_BIGGER_SHIPS == self.state.priority and maximal_fill[1] <= boat_size) or (
                            PRIORITIZE_SMALLER_SHIPS == self.state.priority and maximal_fill[1] >= boat_size):
                        maximal_fill = (lock, boat_size, self.state.lock_available_space[lock] - boat_size)
        return maximal_fill

    def intTransition(self):
        if self.state.next_ship is not None:
            self.state.lock_available_space[self.state.current_serving_lock] -= self.state.next_ship.size
            self.state.wait_for_ship = False
        self.state.next_ship = None
        self.state.locked = False

        optimal_solution = self.get_needed_optimal_ship_and_lock()
        if self.state.wait_for_ship:
            self.state.get_ship_size = -1
            self.state.remaining_time = float("inf")
        elif optimal_solution[0] == -1:
            self.state.locked = True
            self.state.remaining_time = float("inf")  # There can nothing be done wait for a new external event
        else:
            self.state.wait_for_ship = True
            self.state.remaining_time = 0 #get boat
            self.state.current_serving_lock = optimal_solution[0]
            self.state.get_ship_size = optimal_solution[1]

        return self.state

@dataclasses.dataclass
class LockState:
    remaining_time: float
    max_wait_duration: float
    passthrough_duration: float
    ships: list
    available_capacity: int
    open: bool
    closed_open_event: bool
    current_time: int
    max_amount_in_lock_at_once:int
    def __init__(self, capacity, max_wait_duration, passthrough_duration):
        self.max_wait_duration = max_wait_duration
        self.remaining_time = float('inf')
        self.passthrough_duration = passthrough_duration
        self.ships = []
        self.available_capacity = capacity
        self.open = True
        self.ack_ship = False
        self.current_time = 0
        self.closed_open_event = False
        self.boat_leave_event = False
        self.max_amount_in_lock_at_once = 0

class Lock(AtomicDEVS):
    def __init__(self,
        capacity=2, # lock capacity (2 means: 2 ships of size 1 will fit, or 1 ship of size 2)
        max_wait_duration=60.0, 
        passthrough_duration=60.0*15.0, # how long does it take for the lock to let a ship pass through it
    ):
        super().__init__("Lock")
        self.state = LockState(capacity, max_wait_duration, passthrough_duration)
        self.state.remaining_time = float('inf')
        self.in_ship = self.addInPort("in_ship")

        self.out_ships = self.addOutPort("out_ships")
        self.out_lock_opened = self.addOutPort("out_lock_opened")
        self.state.time_until_max_wait_duration = self.state.max_wait_duration


    def extTransition(self, inputs):
        self.state.current_time += self.elapsed
        if self.state.closed_open_event:
            assert self.in_ship not in inputs,  f"Cannot have an input event while processing the closed_open_event" #cannot ever happen because the LoadBalancerState never gives a boat when the lock is closed
            return self.state

        if self.in_ship in inputs:
            if len(self.state.ships) == 0:
                self.state.remaining_time = self.state.max_wait_duration
            self.state.ships.append(inputs[self.in_ship])

        if sum(ship.size for ship in self.state.ships) >= self.state.available_capacity:
            self.state.open = False
            self.state.closed_open_event = True
            self.state.remaining_time = 0

        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        output = {}
        if self.state.closed_open_event:
            output[self.out_lock_opened] = self.state.open
        if self.state.boat_leave_event:
            output[self.out_ships] = self.state.ships
        return output
    
    def intTransition(self):
        self.state.current_time += self.state.remaining_time
        if self.state.closed_open_event and self.state.open == False:#close lock
            self.state.remaining_time = self.state.passthrough_duration
            self.state.open = True #state will be set to True after passthrough_duration
            self.state.boat_leave_event = True #let boats exit after passthrough_duration
            self.state.closed_open_event = True
        elif self.state.closed_open_event and self.state.open == True:
            self.state.closed_open_event = False
            self.state.boat_leave_event = False
            self.state.remaining_time = float('inf')
            #self.state.time_until_max_wait_duration = self.state.current_time + self.state.max_wait_duration
            if self.state.max_amount_in_lock_at_once < len(self.state.ships):
                self.state.max_amount_in_lock_at_once = len(self.state.ships)
            self.state.ships = []
        elif self.state.remaining_time == self.state.max_wait_duration and len(self.state.ships) > 0:#max duration time is over let ships through
            self.state.open = False #close lock
            self.state.closed_open_event = True #send closing event to load balancer
            self.state.remaining_time = 0 #do this immediately
            #this will start the pass through event on line 269
        else:
            assert "wtf is this"
            self.state.remaining_time = float('inf')

        return self.state

### EDIT THIS FILE ###
