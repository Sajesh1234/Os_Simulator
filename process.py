import ProcessControlBlock as pcb


class Process(object):

  def __init__(self, pid, file_name):
          process_state = "NEW"
          self.pcb = pcb.ProcessControlBlock(process_state, pid)

  def set_ready(self):
          self.pcb.state = "READY"

  def set_run(self):
          self.pcb.state = "RUN"

  def set_wait(self):
          self.pcb.state = "WAIT"

  def set_exit(self):
          self.pcb.state = "EXIT"

  def get_state(self):
          return self.pcb.state
  
  def get_pid(self):
          return self.pcb.pid

  def print(self):
          print(f"\nProcess #{self.get_pid()}")
          for o in self.operations:
              if o.is_critical():
                print("Critical")
              operation_name = o.get_name()
              operation_cycle_length = str(o.get_cycle_length())
              s = "%10s:\t%s" % (operation_name, operation_cycle_length)
              print(s.center(20, ' '))

	


