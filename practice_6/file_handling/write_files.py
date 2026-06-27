from pathlib import Path

file_path = Path("../example.txt")

#write mode - creates file or overwrites it
with open(file_path, "w") as file:
    file.write("Python Practice 6\n")
    file.write("File handling example\n")

#append mode - adds new information
with open(file_path, "a") as file:
    file.write("New appended line\n")
print("Data written successfully")