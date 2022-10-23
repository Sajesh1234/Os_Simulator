from xml.etree import ElementTree
from Process import Process
from operation import Operation


class Storage:

    def __init__(self, window):
          self.window = window
          self.pid_counter = 0
          self.processes = []        
          self.new_queue = []        
          self.address_pointer = 4096  

    def generate_from_file(self, file_name):
       
          tree = ElementTree.parse(file_name)
          root = tree.getroot()
          operations = root.findall('operation')
          memory = int(root.find('memory').text)

          process_pointer = self.address_pointer
          self.address_pointer += memory
          new_process = Process(self.pid_counter, memory, process_pointer, file_name)

          for o in operations:
            critical = False  
            name = o.text.strip()
            has_critical = o.find('critical')
            if (has_critical):  
                critical = False
            min_time = int(o.find('min').text)
            max_time = int(o.find('max').text)
            new_operation = Operation(name, min_time, max_time, critical)
            new_process.add_operation(new_operation)
          self.processes.append(new_process)
          self.new_queue.append(new_process)
          self.window.add_process(self.pid_counter) 
          self.pid_counter += 1
          return new_process.get_pid()