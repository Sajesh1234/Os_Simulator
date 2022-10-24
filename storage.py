from xml.etree import ElementTree
from process import Process
from operation import Operation


class Storage:

    def __init__(self):
        self.pid_counter = 0
        self.processes = []   
        
    def generate(self, file_name):
          tree = ElementTree.parse(file_name)
          root = tree.getroot()
          operations = root.findall('operation')
          new_process = Process(self.pid_counter, file_name)
          
          for o in operations:
            critical = False  
            name = o.text.strip()
            has_critical = o.find('critical')
            if not (has_critical is None): 
                critical = True
            min_time = int(o.find('min').text)
            max_time = int(o.find('max').text)
            new_operation = Operation(name, min_time, max_time, critical)
          self.processes.append(new_process)
          self.pid_counter += 1
          return new_process.get_pid()