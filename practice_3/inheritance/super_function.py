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

#use the super() function
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)

#add properties
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
    self.graduationyear = 2019
class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year
x = Student("Mike", "Olsen", 2019)

#add methods
class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year
  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)