from storage import Storage

class Test:
    def __init__(self):
        self.Storage = Storage()
    def printeverything1(self):
        print (self.Storage.generate('Template/Program_files1.xml'))
        
    def printeverything2(self):
        print (self.Storage.generate('Template/Program_files2.xml'))
        
y = int(input("enter a number between 1 or 2"))

if y == 1:
    x = Test()
    x.printeverything1()
if y == 2:
    x = Test()
    x.printeverything2()


 
    


        
                  
        