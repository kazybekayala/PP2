#create a parent class
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname
  def printname(self):
    print(self.firstname, self.lastname)
#use the person class to create an object, and then execute the printname method:
x = Person("John", "Doe")
x.printname()

#create a child class
class Student(Person):
  pass
x = Student("Mike", "Olsen")
x.printname()