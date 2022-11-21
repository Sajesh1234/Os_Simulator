class ProcessControlBlock:
    def __init__(self, pointer, state, pid, program_counter, registers, memory, clock_timer):
        self.pointer = pointer
        self.state = state
        self.pid = pid
        self.program_counter = program_counter
        self.registers = registers
        self.memory = memory
        self.clock_timer = clock_timer
