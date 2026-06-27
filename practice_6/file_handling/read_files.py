from pathlib import Path

file_path = Path("../example.txt")

with open(file_path, "r") as file:
    content = file.read()
    print(content)