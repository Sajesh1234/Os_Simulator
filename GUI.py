import tkinter as tk
import tkinter.scrolledtext as tks
from Cpu_scheduler import *
from Memory import *
from Gen import *
from threading import *
from process import *

class gui:

    def __init__(self):
        self.gen = gen(self)
        self.cpu = CpuSchedule(self, self.gen)
        self.memory = Memory(self, self.gen, self.cpu)
        self.cpu.mem_con(self.memory)
        self.processes = []
        self.frames = []

        root = tk.Tk()
        root.configure(background="gray")
        root.title ("Operating System Simulator")
        
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

        Label_Template = tk.Label(text="Click on one of the files to create a Process:")
        Label_Template.grid(row = 0, column = 0, padx=10, pady=10,)

        button1 = tk.Button(master=root, text="Program File One", bd = '5',
                          command=lambda: self.gen.from_files(r'C:\Users\Sajesh\OneDrive\Desktop\templates\program_file.xml'))
        button1.grid(row= 0, column=1, padx=10, pady= 3)

        button2 = tk.Button(master=root, text="Program File Two", bd = '5',
                          command=lambda: self.gen.from_files(r'C:\Users\Sajesh\OneDrive\Desktop\templates\program_file_2.xml'))
        button2.grid(row=0, column=2, padx=30, pady= 3)

        self.process_frame = tk.Frame(master = root, width = 90, height = 90, relief = tk.SUNKEN)
        self.process_frame.grid_propagate(False)
        self.process_frame.grid(row=2, column=0, columnspan=3)

        self.page_entries = []
        self.pf = tk.Frame(master=root, height=400, width=200, relief=tk.SUNKEN)
        self.pf.grid(row = 4, column=0)
        self.pf.grid_columnconfigure(0, weight = 1)
        self.pf.grid_columnconfigure(1, weight = 1)
        
        self.nf = tk.Frame (master=self.pf, width = 100)
        self.nf.config(background= "red")
        self.nf.grid(row =0, column=0)
        self.pn = tk.Frame(master = self.pf, width = 100)
        self.pn.config(background= "blue")
        self.pn.grid(row =0, column=1)

        for o in range (16):
            table = tk.Label(master = self.nf, text=f"FRAME {o}", height =1, width= 8)
            table.config(background="white")
            table.grid(row = o, column= 0, padx=1, pady=1)
        
        for i in range (16):
            page = tk.Label(master = self.pn, text=f"None", height =1, width= 12, padx=1, pady=1)
            page.config(background="white")
            page.grid(row = i, column= 1, padx=1, pady=1)
            self.page_entries.append(page)




        run_but = tk.Button(master=root, text="Run", command=self.run)
        run_but.grid(row=3, column=1, pady=10)

        self.console = tks.ScrolledText(master=root, relief=tk.SUNKEN)
        self.console.grid(row=4, column=1)
        self.console.config(background="gray")

        root.mainloop()
    def run(self):
        memory_thread = Thread(target=self.memory.load_mem)
        cpu_thread = Thread(target=self.cpu.rr)
        memory_thread.start()
        cpu_thread.start()

    def add_process(self, pid):
        k = tk.Frame(master=self.process_frame, background= "red")
        i = tk.Text(master = k, width= 10, height= 5)
        i.insert(1.0, f"Process {pid}")
        i.pack(side = tk.LEFT, padx =1, pady=1)
        k.pack(side=tk.LEFT)
        self.processes.append(i)
        self.frames.append(k)

    def update_page_table(self, frame, page):
        self.page_entries[frame].config(text=f"Page {page}")

    def log(self, string):
        self.console.insert('end', string)
        print(string)

    def running(self, pid):
        self.frames[pid].config(background="green")
    def wait(self, pid):
        self.frames[pid].config(background="red")
    def finish(self, pid):
        self.frames[pid].config(background="blue")

    
app = gui()
