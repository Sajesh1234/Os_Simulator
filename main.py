from Cpu_scheduler import *
from Memory import *
from Gen import *
from threading import *
from process import *

class main:
    def __init__(self):

        self.gen = gen()
        self.cpu = CpuSchedule(self.gen)
        self.memory = Memory(self.gen, self.cpu)
        self.cpu.mem_con(self.memory)
        self.processes = []

        n = int(input('Enter the No. of Processes: '))

        while n > 0:
            file_use = int(input('Select from templates 1 or 2 '))
            if file_use == 1 or file_use == 2:
                if file_use == 1:
                    fn = (r'C:\Users\Sajesh\Desktop\templates\program_file.xml')
                elif file_use == 2:
                    fn = (r'C:\Users\Sajesh\Desktop\templates\program_file_2.xml')
                self.gen.from_files(fn)
                n -= 1
            else:
                print("invalid template")

        self.cpu.print()
        print("\nBeginning schedule processes\n")

    def run(self):
        memory_thread = Thread(target=self.memory.load_mem)
        cpu_thread = Thread(target=self.cpu.rr)
        memory_thread.start()
        cpu_thread.start()
        
t = main()
print(t.run())
