from op import Operation
from xml.etree import ElementTree
from process import Process


class gen:
    def __init__ (self, gui):
        self.gui = gui
        self.pid_counter = 0
        self.processes = []
        self.new_queue = []
        #self.ready_queue = []
        #self.wait_queue = []
        #self.exit_queue = []
        self.address = 4096

    def from_files(self, file_name):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        operations = root.findall('operation')
        mem = int(root.find('memory').text)
        process_pointer = self.address
        self.address += mem
        new_process = Process(self.pid_counter, mem, process_pointer, file_name)

        for o in operations:
            critical = False
            name = o.text.strip()
            has_critical = o.find('critical')
            if not (has_critical is None):
                critical = True
            min = int(o.find('min').text)
            max = int(o.find('max').text)
            new_op = Operation(name, min, max, critical)
            new_process.add_operation(new_op)
        self.processes.append(new_process)
        self.new_queue.append(new_process)
        self.gui.add_process(self.pid_counter)
        self.pid_counter += 1
        return new_process.get_pid()
