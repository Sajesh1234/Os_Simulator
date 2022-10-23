from Storage import Storage
def __init__(self):

        
        self.Storage = Storage(self)
        file = int(input("enter 1 or 2"))
                
        if file == 1:
                print(self.Storage.generate_from_file('Template/program_file1.xml'))
                
        if file == 2: 
                  print(self.Storage.generate_from_file('Template/program_file1.xml'))
                  
        