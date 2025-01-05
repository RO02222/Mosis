### EDIT THIS FILE ###
from copy import copy
from itertools import islice
from typing import overload

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses
from icecream import ic
from collections import deque



class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        self.state = QueueState(ship_sizes)
        self.in_ship = self.addInPort("in_ship")
        self.in_update_ship = self.addInPort("in_update_ship")
        self.out_ship_content = self.addOutPort("out_ship_content")


    def extTransition(self, inputs):
        print(inputs)
        if self.in_ship in inputs:
            ship = inputs[self.in_ship]
            self.state.ship_queue[ship.size].append(ship)
        elif self.in_update_ship in inputs:
            ship = inputs[self.in_update_ship]
            self.state.ship_queue[ship.size].popleft()
        self.state.remaining_time = 0
        return self.state


    def timeAdvance(self):
        return self.state.remaining_time


    def outputFnc(self):
        return {self.out_ship_content: {size: (queue[0] if queue else None) for size, queue in self.state.ship_queue.items()}}


    def intTransition(self):
        self.state.remaining_time = float("inf")
        return self.state


class QueueState:
    def __init__(self, ship_sizes):
        self.ship_queue = {size: deque() for size in ship_sizes}
        self.remaining_time = float("inf")

    def __repr__(self):
        return f"{ self.ship_queue}"


class LoadBalancer(AtomicDEVS):
    def __init__(self, lock_capacities=[3,2], *, ship_sizes): # two locks of capacities 3 and 2.
        super().__init__("LoadBalancer") #RoundRobin
        self.state = LoadBalancerState(lock_capacities, ship_sizes)
        self.in_update_queue = self.addInPort("in_update_queue")
        self.in_update_lock = self.addInPort("in_update_lock")
        self.out_update_ship = self.addOutPort("out_update_ship")
        self.out_update_lock = [self.addOutPort("out_update_lock") for _ in range(len(lock_capacities))]

    def extTransition(self, inputs):
        print(inputs)
        if self.in_update_queue in inputs:
            for size, ship in inputs[self.in_update_queue].items():
                self.state.queueContent[size] = ship
            self.state.state = 0
        elif self.in_update_lock in inputs:
            index, self.state.data, capacity = inputs[self.in_update_lock]
            self.state.locks_status[index] = capacity
            self.state.state = 1

        else:
            return self.state

        self.state.remaining_time = 0
        return self.state


    def timeAdvance(self):
        return self.state.remaining_time

    def outputFnc(self):
        i = self.state.state

        if i == 1:
            if self.state.data != 0:
                return {self.out_update_ship: self.state.data}


        ship = self.fill_lock()
        if ship[0] != -1:
            return {self.out_update_lock[ship[0]]: self.state.queueContent[ship[1]]}
        return {}



    def intTransition(self):
        self.state.remaining_time = float("inf")
        return self.state


    def available_locks(self):
        return (i for i, value in enumerate(self.state.locks_status) if value != 0)

    def fill_lock(self):
        best = [-1,-1,float("inf")]
        for shipSize in self.state.ship_sizes:
            if self.state.queueContent[shipSize] is None:
                continue

            locks = self.available_locks()
            while (i:= next(locks, -1)) != -1:
                remaining = self.state.locks_status[i] - shipSize

                if remaining == 0:
                    return [i, shipSize,0]

                if remaining > 0 and remaining < best[2]:
                    best[0] = i
                    best[1] = shipSize
                    best[2] = remaining
        return best


class LoadBalancerState:
    def __init__(self, lock_capacities, ship_sizes: set[int]):
        self.remaining_time = float("inf")
        self.locks_cap = copy(lock_capacities)
        self.locks_status = copy(lock_capacities)
        self.queueContent = {size: 0 for size in ship_sizes}
        self.ship_sizes = [size for size in ship_sizes]
        self.ship_sizes.sort(reverse=False)

        self.data = None
        self.state = 0

    def __repr__(self):
        return f"{self.remaining_time}\n"\
               f"{self.locks_status} / {self.locks_cap}\n"\
                f"{self.queueContent}"



class Lock(AtomicDEVS):
    def __init__(self,*,
                 index=0,
                 capacity=2, # lock capacity (2 means: 2 ships of size 1 will fit, or 1 ship of size 2)
                 max_wait_duration=60.0,
                 passthrough_duration=60.0*15.0, # how long does it take for the lock to let a ship pass through it
                 ):
        super().__init__("Lock")
        self.in_lock = self.addInPort("in_lock")
        self.out_update_capacity = self.addOutPort("out_update_capacity")
        self.out_sink = self.addOutPort("out_sink")
        self.state = LockState(index, capacity, max_wait_duration, passthrough_duration)


    def extTransition(self, inputs):
        print(inputs)
        self.state.remaining_time_event -= self.elapsed
        if self.in_lock in inputs:
            if self.state.state == 0:
                self.state.remaining_time_event = self.state.max_wait_duration
            self.state.state = 1
            self.state.latest_ship = inputs[self.in_lock]
            self.state.ships.append(self.state.latest_ship)
            self.state.remaining_capacity -= self.state.latest_ship.size
            self.state.remaining_time = 0
        return self.state


    def timeAdvance(self):
        return self.state.remaining_time


    def outputFnc(self):

        if self.state.state == 5:
            return {self.out_sink : [ship for ship in self.state.ships]}

        if self.state.out:
            return {self.out_update_capacity: (self.state.index, self.state.latest_ship, self.state.remaining_capacity)}
        return {}

    def intTransition(self):
        self.state.out = False
        i = self.state.state

        # 0: idle

        # 1: ship arrived

        # 2: max waitduration

        # 3: passthrough completed

        if i == 1:
            if (self.state.remaining_capacity == 0 or self.state.remaining_time_event <= 0):
                self.activate()
                self.state.out = True
                self.state.state = 4
                return self.state
            else:
                self.state.out = True
                self.state.state = 2
                return self.state

        elif i == 2:
            self.state.state = 3

        elif i == 3:
            self.state.out = True
            self.activate()
            self.state.latest_ship = 0
            self.state.state = 4
            return self.state


        elif i == 4:
            self.state.state = 5

        elif i == 5:
            self.state.remaining_capacity = self.state.capacity
            self.state.ships.clear()
            self.state.remaining_time_event = float("inf")
            self.state.remaining_time = 0
            self.state.state = 0
            self.state.latest_ship = 0
            self.state.out = True
            return self.state

        self.state.remaining_time = self.state.remaining_time_event
        return self.state

    def activate(self):
        self.state.remaining_time_event = self.state.passthrough_duration
        self.state.remaining_capacity = 0
        self.state.remaining_time = 0
        self.state.out = True

class LockState:
    def __init__(self, index, capacity, max_wait_duration, passthrough_duration):
        self.index = index
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.remaining_time = float("inf")
        self.remaining_time_event = float("inf")
        self.max_wait_duration = max_wait_duration
        self.passthrough_duration = passthrough_duration

        self.state = 0
        self.latest_ship = 0
        self.out = False
        self.ships = []

    def __repr__(self):
        return f"lock"



PRIORITIZE_BIGGER_SHIPS = 0
PRIORITIZE_SMALLER_SHIPS = 1