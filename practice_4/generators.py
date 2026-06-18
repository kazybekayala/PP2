#exercise 1, generator that generates squares up to N

def square_generator(n):
    for i in range(n + 1):
        yield i ** 2

n = int(input("Enter N: "))
print("Squares:")
for num in square_generator(n):
    print(num)

#exercise 2, even numbers between 0 and n in comma-separated form

n = int(input("\nEnter N for even numbers: "))
evens = (str(i) for i in range(n + 1) if i % 2 == 0)
print(",".join(evens))

#exercise 3, numbers divisible by both 3 and 4 (i.e. by 12)

def divisible_by_12(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

n = int(input("\nEnter N for numbers divisible by 3 and 4: "))
for num in divisible_by_12(n):
    print(num)

#exercise 4, squares from a to b

def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

a = int(input("\nEnter a: "))
b = int(input("Enter b: "))
for value in squares(a, b):
    print(value)

#exercise 5, generator from n down to 0

def countdown(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input("\nEnter N for countdown: "))
for num in countdown(n):
    print(num)