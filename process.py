import ProcessControlBlock as pcb

class Process:


    def __init__(self, pid, memory, pointer, fn):
        time_passed = 0
        program_c=0
        registers = []
        process_state = "NEW"
        memory_required = memory
        page_size = 64
        self.pages_need = memory_required // page_size
        self.page_table = []
        self.pcb = pcb.ProcessControlBlock(pointer, process_state, pid, program_c, registers, memory_required, time_passed)
        self.operations = []
        self.file_name = fn

    def add_operation(self, operation):
        self.operations.append(operation)

    def set_ready(self):
        self.pcb.state = "READY"

    def set_run(self):
        self.pcb.state = "RUN"

    def set_wait(self):
        self.pcb.state = "WAIT"

    def set_exit(self):
        self.pcb.state = "EXIT"

    def get_pid(self):
        return self.pcb.pid

    def get_memory(self):
        return self.pcb.memory

    def increment_clock_time(self, increment):
        self.pcb.clock_timer += increment

    def get_clock_time(self):
        return self.pcb.clock_timer

    def get_time_required(self):
        seconds = 0
        for o in self.operations:
            seconds += o.get_cycle_length()
        return seconds
    def print(self):
        print(f"\nProcess #{self.get_pid()}")
        print(f"Memory: {self.get_memory()}")
        for o in self.operations:
            if o.isCritical():
                print("Critical")
            operation_name = o.get_name()
            operation_cycle_length = str(o.get_cycle_length())
            s = "%10s:\t%s" % (operation_name, operation_cycle_length)
            print(s.center(20, ' '))
