import os
from pathlib import Path

folder = Path("practice_folder/subfolder")

#create nested directories
folder.mkdir(parents=True, exist_ok=True)

print("Current directory:")
print(os.getcwd())
print("Files:")
print(os.listdir())