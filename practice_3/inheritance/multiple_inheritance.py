#first parent class
class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname
    def printname(self):
        print(f"Name: {self.firstname} {self.lastname}")

#second parent class
class University:
    def __init__(self, uni_name, major):
        self.university = uni_name
        self.major = major
    def print_studies(self):
        print(f"Study in: {self.university}, Speciality: {self.major}")

#child class
class Student(Person, University):
    def __init__(self, fname, lname, uni_name, major):
        Person.__init__(self, fname, lname)
        University.__init__(self, uni_name, major)
x = Student("Mike", "Olsen", "MIT", "Computer Science")

#add methods
x.printname()
x.print_studies()