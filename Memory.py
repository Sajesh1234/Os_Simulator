from threading import *
import time

class Memory:
    def __init__(self, gui, gen, cpu):
        self.gui = gui
        self.gen = gen
        self.mem_available = 512
        self.mem_lock = Lock()
        self.mem_condition = Condition(self.mem_lock)

        self.available_frames = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.frames = []
        self.p_number = 0

        for frame in range(16):
            self.frames.append(None)

        self.cpu = cpu
        self.ready_queue = []
        #self.page_entries = []

    def load_mem(self):
        while True:
            time.sleep(.01)
            if len(self.gen.new_queue) > 0:
                process = self.gen.new_queue.pop(0)
                with self.mem_condition:
                    while not self.loaded_mem(process.get_pid()):
                        self.mem_condition.wait()


    def loaded_mem(self, pid):
        if self.gen.processes[pid].get_memory() < self.get_mem_available():
            for page in range(self.gen.processes[pid].pages_need):
                page_num = self.p_number
                self.gen.processes[pid].page_table.append((page_num, self.assign_frame(page_num)))
                self.p_number = (self.p_number + 1) % 16

            self.gen.processes[pid].set_ready()
            self.gen.processes[pid].print()
            self.cpu.ready_queue.append(self.gen.processes[pid])
            self.mem_available -= self.gen.processes[pid].get_memory()
            #print("Process %d is in memory"% pid)
            self.gui.log(f"\nProcess {pid} Loaded on to the Memory")
            return True

        else:
            #print("Process %d is waiting for memory to be free" % pid)
            self.gui.log(f"\nProcess {pid} is waiting for free memory")
            return False
    def get_mem_available(self):
        return self.mem_available

    def free_mem(self, pid):
        self.mem_available += self.gen.processes[pid].get_memory()
        for entry_tuple in self.gen.processes[pid].page_table:
            frame_index = entry_tuple[1]
            self.frames[frame_index]=None
            self.available_frames.append(frame_index)
            #self.update_page_table(frame_index, "FREE")
            self.gui.update_page_table(frame_index, "None")
            
    def assign_frame(self, p_number):
        if len(self.available_frames) > 0:
            frame = self.available_frames.pop(0)
            self.frames[frame] = p_number
            self.gui.update_page_table(frame, p_number)
            return frame
        else:
            print("BUSY\n")
            return None

    def remove_page(self, p_number):
        frame_index = self.get_frame(p_number)
        self.frames[frame_index] = 0
        self.available_frames.append(frame_index)

    def h_page(self, p_number):
        for o in self.frames:
            if o == p_number:
                return True
        return False

    def get_frame(self, p_number):
        for o in range(len(self.frames)):
            if self.frames[o] == p_number:
                return o
        return 0
    #def update_page_table(self, frame, page):
        #for o in self.page_entries:
            #self.page_entries[frame] = page
    
