import ProcessControlBlock as pcb

class Process:
    def __init__(self, pid, memory, pointer, fn):
        time_passed = 0
        program_c=0
        registers = []
        process_state = "NEW"
        memory_required = memory
        page_size = 32
        self.pages_need = page_size
        self.page_table = []
        self.pcb = pcb.ProcessControlBlock(pointer, process_state, pid, program_c, registers, memory_required, time_passed)
        self.operations = []
        self.file_name = fn

    def add_operation(self, operation):
        self.operations.append(operation)

    def is_new(self):
        if self.pcb.state == "NEW":
            return True
        else:
            return False
    def set_ready(self):
        self.pcb.state = "READY"

    def is_ready(self):
        if self.pcb.state == "READY":
            return True
        else:
            return False

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
