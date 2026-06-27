import shutil
from pathlib import Path

file = Path("../example.txt")
destination = Path("../moved_example.txt")

shutil.move(file, destination)
print("File moved")