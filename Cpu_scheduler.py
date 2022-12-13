import random
from Memory import *
import threading
from op import Operation
from process import Process
from threading import *
import time

class CpuSchedule:

    quantum = 25

    def __init__(self, gui, gen):
        self.gui = gui
        self.gen = gen
        self.ready_queue = []
        self.waiting_queue = []
        self.lock_critical = Lock()
        self.pid_counter = 0
        self.semaphore = Semaphore(4)
        self.memory = Memory(self.gui, self.gen, self)

    def mem_con(self, memory):
        self.memory = memory

    def rr(self):
        while True:
            time.sleep(0.01)
            if len(self.ready_queue) > 0:
                with self.semaphore:
                    process = self.ready_queue.pop(0)
                    pid = process.get_pid()
                    self.gen.processes[pid].set_run()
                    self.gui.running(pid)
                    self.run_pro(pid)

    def run_pro(self, pid):
        operation = self.gen.processes[pid].operations.pop(0)
        if operation.isCritical():
            with self.lock_critical:
                #print("Process %d's is critical for %s operation" % (pid, operation.get_name()))
                self.gui.log(f"\nRunning Process {pid} in critical for {operation.get_name()} operation")
                self.run_operation(pid, operation)
        else:
            #print("Process %d: %s operation" % (pid, operation.get_name()))
            self.gui.log("\nProcess %d in %s operation" % (pid, operation.get_name()))
            self.run_operation(pid, operation)

        if len(self.gen.processes[pid].operations) == 0:
            self.gen.processes[pid].set_exit()
            self.memory.free_mem(pid)
            self.gui.finish(pid)
            #print("Process %d has finished in %f cycles" % (pid, self.gen.processes[pid].get_clock_time()))
            self.gui.log(f"\nProcess {pid} has finished in" f" {self.gen.processes[pid].get_clock_time()} cycles")
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
                #print("Process %d finished CALCULATE in %f" %(pid, duration))
                self.gui.log(f"\nProcess {pid} finished CALCULATE")
            else:
                duration = self.quantum
                self.in_cpu(pid, duration)
                operation.decrement_cycle_length(duration)
                self.gen.processes[pid].operations.insert(0, operation)
        elif operation.get_name() == "I/O":
            self.interrupt(pid, duration)
            #print("Process %d finished I/O  in %f " % (pid, duration))
            self.gui.log(f"\nProcess {pid} finished I/O")

    def in_cpu(self, pid, duration):
        count = duration
        while count > 0:
            time.sleep(.01)
            self.gen.processes[pid].increment_clock_time(1)
            if random.random() <= 0.01:
                self.interrupt(pid, random.randint(1, 10))
                #print("Process %d is interrupted" % pid)
                self.gui.log(f"\nProcess {pid} interupted")
            count -= 1

    def interrupt(self, pid, duration):
        self.gen.processes[pid].set_wait()
        self.gui.wait(pid)
        time.sleep(duration * 0.01) 
        #print("Process %d finished I/O in %f " % (pid, duration))
        #self.gui.log(f"\n Process {pid} finished I/O in {duration}")

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
