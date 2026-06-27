from functools import reduce

numbers = [1,2,3,4,5]

#map
squared = list(map(lambda x: x*x, numbers))
print(squared)

#filter
even = list(filter(lambda x: x%2==0, numbers))
print(even)

#reduce
total = reduce(lambda x,y: x+y, numbers)
print(total)