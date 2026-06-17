def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus")

def my_function(name): #name is a parameter
  print("Hello", name)
my_function("Emil") #Emil is an argument

#default parameter values
def my_function(name = "friend"):
  print("Hello", name)
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

#positional arguments
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("dog", "Buddy")

#switching the order changes the result
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("Buddy", "dog")