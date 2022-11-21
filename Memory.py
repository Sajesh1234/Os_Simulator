from threading import *

class Memory:
    def __init__(self, gen, cpu):
        self.gen = gen
        self.mem_available = 512
        self.mem_lock = Lock()
        self.mem_condition = Condition(self.mem_lock)
        self.frames = []
        self.available_frames = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.p_number = 0
        for frame in range(12):
            self.frames.append(None)
        self.ready_queue = []
        self.cpu = cpu

    def load_mem(self):
        while True:
            if len(self.cpu.new_queue) > 0:
                process = self.cpu.new_queue.pop(0)
                with self.mem_condition:
                    while not self.loaded_mem(process.get_pid()):
                        self.mem_condition.wait()


    def loaded_mem(self, pid):
        if self.cpu.processes[pid].get_memory() < self.get_mem_available():
            for page in range(self.gen.processes[pid].pages_needed):
                page_num = self.p_number
                self.gen.processes[pid].page_table.append((page_num, self.assign_frame(page_num)))
                self.p_number = (self.p_number + 1) % 12

            self.gen.processes[pid].set_ready()
            self.gen.processes[pid].print()
            self.cpu.ready_queue.append(self.gen.processes[pid])
            self.mem_available -= self.gen.processes[pid].get_memory()
            print("Process %d is in memory"% pid)
            return True

        else:
            print("Process %d is waiting for memory to be free" % pid)
            return False
    def get_mem_available(self):
        return self.mem_available

    def free_mem(self,pid):
        self.mem_available += self.gen.processes[pid].get_memory()
        for entry_list in self.gen.processes[pid].page_table:
            frame_index = entry_list[1]
            self.frames[frame_index] = None
            self.available_frames.append(frame_index)
            print("frame % is free" % frame_index)
    def assign_frame(self, p_number):
        if len(self.available_frames) > 0:
            frame = self.available_frames.pop(0)
            self.frames[frame] = p_number
            return frame
        else:
            print("no")
            return None

    def remove_page(self, p_number):
        frame_index = self.get_frame(p_number)
        self.frames[frame_index] = 0
        self.available_frames.append(frame_index)

    def h_page(self, p_number):
        for frame in self.frames:
            if frame == p_number:
                return True
        else:
            return False

    def get_frame(self, p_number):
        for frame_index in range(len(self.frames)):
            if self.frames[frame_index] == p_number:
                return frame_index
        return 0
    
