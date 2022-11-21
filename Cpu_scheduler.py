import random
from Memory import *

class CpuSchedule:
    quantum = 20
    def __init__(self, gen):
        self.gen = gen
        self.ready_queue = []
        self.new_queue = []
        self.wait_queue = []
        self.lock_critical = Lock()
        self.semaphore = Semaphore(4)
        self.pid_count = 0
        self.semaphore = Semaphore(4)
        self.memory = Memory(self.gen, self)

    def mem_con(self, memory):
        self.memory = memory

    def rr(self):
        while True:
            if len(self.ready_queue) > 0:
                with self.semaphore:
                    process = self.ready_queue.pop(0)
                    pid = process.get_pid()
                    self.gen.processes[pid].set_run()
                    self.run_process(pid)

    def run_process(self, pid):
        operation = self.gen.processes[pid].operations.pop(0)
        if operation.isCritical():
            with self.lock_critical:
                print("Process %d's is critical for %s operation" % (pid, operation.get_name()))
                self.run_operation(pid, operation)
        else:
            print("Process %d: %s operation" % (pid, operation.get_name()))
            self.run_operation(pid, operation)

        if len(self.gen.processes[pid].operations) == 0:
            self.gen.processes[pid].set_exit()
            self.memory.free_mem(pid)
            print("Process %d has finished in %f cycles" % (pid, self.gen.processes[pid].get_clock_time()))
            with self.memory.mem_condition:
                self.memory.mem_condition.notify()
        else:
            self.ready_queue.append(self.gen.processes[pid])

    def run_operation(self, pid, operation):
        duration = operation.get_cycle_length()
        if operation.get_name() == "CALCULATE":
            if duration <= self.quantum:
                self.in_cpu(pid, duration)
                operation.decrement_cycle_length(duration)
                print("process %d finished CALCULATE in %f" %(pid, duration))
            else:
                duration = self.quantum
                self.in_cpu(pid, duration)
                operation.decrement_cycle_length(duration)
                self.gen.processes[pid].operations.insert(0, operation)
        elif operation.get_name() == "I/O":
            self.interrupt(pid, duration)
            print("Process %d finished I/O  in %f " % (pid, duration))

    def in_cpu(self, pid, duration):
        count = duration
        while count > 0:
            self.gen.processes[pid].increment_clock_time(1)
            if random.random() <= 0.01:
                self.interrupt(pid, random.randint(1, 10))
                print("Process %d is interrupted" % pid)
            count -= 1

    def interrupt(self, pid, duration):
        self.gen.processes[pid].set_wait()
        self.gen.processes[pid].set_wait()
        print("Process %d finished I/O in %f " % (pid, duration))

    def get_process_id(self, process):
        return self.gen.processes.index(process)

    def print(self):
        for p in self.gen.processes:
            print("\nProcess #", self.get_process_id(p))
            for o in p.operations:
                operation_name = o.get_name()
                operation_cycle_length = str(o.get_cycle_length())
                s = "%10s:\t%s" % (operation_name, operation_cycle_length)
                print(s.center(20, ' '))
