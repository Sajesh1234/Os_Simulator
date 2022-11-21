import random

class Operation:
    def __init__(self, name, min, max, critical):
        self.operation_name = name
        self.min = min
        self.mac = max
        self.critical = critical
        self.cycle_length = random.randrange(min, max, 1)

    def get_cycle_length (self):
        return self.cycle_length

    def decrement_cycle_length(self):
        self.cycle_length -= decrement

    def get_name(self):
        return self.operation_name

    def isCritical(self):
        return self.critical
