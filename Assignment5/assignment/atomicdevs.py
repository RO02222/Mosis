### EDIT THIS FILE ###
from copy import copy
from itertools import islice
from typing import overload

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses
from icecream import ic




class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        self.state = QueueState(ship_sizes)
        self.in_ship = self.addInPort("in_ship")
        self.request_ship = self.addInPort("request_ship")
        self.out_ship = self.addOutPort("out_ship")


    def extTransition(self, inputs):
        if self.in_ship in inputs:
            self.state.ship_queue[inputs[self.in_ship].size] += 1
            self.state.remaining_time = 0
        elif inputs[self.request_ship] is not None:
            self.state.remaining_time = 0
        return self.state


    def timeAdvance(self):
        return self.state.remaining_time


    def outputFnc(self):
        return {self.out_ship: self.state.ship_queue}


    def intTransition(self):
        self.state.remaining_time = float("inf")
        return self.state


class QueueState:
    def __init__(self, ship_sizes):
        self.ship_queue = {size: 0 for size in ship_sizes}
        self.remaining_time = float("inf")

    def __repr__(self):
        return f"{ self.ship_queue}"


class LoadBalancer(AtomicDEVS):
    def __init__(self, lock_capacities=[3,2], *, ship_sizes): # two locks of capacities 3 and 2.
        super().__init__("LoadBalancer") #RoundRobin
        self.state = LoadBalancerState(lock_capacities, ship_sizes)
        self.ship_update = self.addInPort("ship_update")
        self.request_ship = self.addOutPort("request_ship")
        self.update_lock = [self.addOutPort("update_lock") for _ in range(len(lock_capacities))]

    def extTransition(self, inputs):
        if self.ship_update in inputs:
            for size, amount in inputs[self.ship_update].items():
                self.state.queueContent[size] = amount
            self.state.remaining_time = 0

        return self.state

    def timeAdvance(self):
        return self.state.remaining_time

    def outputFnc(self):
        # if self.out is None:
        #     return None
        # out = self.out
        # self.out = None
        # return out
        return {}

    def intTransition(self):
        ic(self.state)
        self.fill_lock()
        self.state.remaining_time = float("inf")
        return self.state


    def available_locks(self):
        return (i for i, value in enumerate(self.state.locks_status) if value != 0)

    def fill_lock(self):
        best = [-1,-1,float("inf")]
        for shipSize, amount in self.state.queueContent.items():
            if amount <= 0:
                continue

            locks = self.available_locks()
            while (i:= next(locks), -1) != -1:
                remaining = self.state.locks_status[i] - shipSize

                if remaining == 0:
                    return (i, shipSize)

                if remaining > 0 and remaining < best[2]:
                    best[0] = i
                    best[1] = shipSize
                    best[1] = remaining
        return best


class LoadBalancerState:
    def __init__(self, lock_capacities, ship_sizes):
        self.remaining_time = float("inf")
        self.locks_cap = copy(lock_capacities)
        self.locks_status = copy(lock_capacities)
        self.queueContent = {cap: 0 for cap in ship_sizes}

    def __repr__(self):
        return f"{self.remaining_time}\n"\
               f"{self.locks_status} / {self.locks_cap}\n"\
                f"{self.queueContent}"



class Lock(AtomicDEVS):
    def __init__(self,
                 capacity=2, # lock capacity (2 means: 2 ships of size 1 will fit, or 1 ship of size 2)
                 max_wait_duration=60.0,
                 passthrough_duration=60.0*15.0, # how long does it take for the lock to let a ship pass through it
                 ):
        super().__init__("Lock")
        self.in_lock = self.addInPort("in_lock")
        self.state = LockState()
    def extTransition(self, inputs):
        ic(inputs)
        return self.state

    # def timeAdvance(self):
    #     pass

    # def outputFnc(self):
    #     pass

    def intTransition(self):
        return self.state

class LockState:
    def __init__(self):
        self.remaining_time = float("inf")

    def __repr__(self):
        return f"lock"



PRIORITIZE_BIGGER_SHIPS = 0
PRIORITIZE_SMALLER_SHIPS = 1