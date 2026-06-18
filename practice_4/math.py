import math

#exercise 1, convert degree to radian

degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)

print("Output radian:", round(radian, 6))
print("-" * 40)

#exercise 2, area of a trapezoid

height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area_trapezoid = ((base1 + base2) * height) / 2

print("Expected Output:", area_trapezoid)
print("-" * 40)

#exercise 3, area of a regular polygon

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area_polygon = (n * s ** 2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", round(area_polygon))
print("-" * 40)

#exercise 4, area of a parallelogram

base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area_parallelogram = base * height

print("Expected Output:", float(area_parallelogram))