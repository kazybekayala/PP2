import shutil
from pathlib import Path

source = Path("../example.txt")
backup = Path("../backup_example.txt")

#copy file
shutil.copy(source, backup)
print("File copied")

#delete file
if backup.exists():
    backup.unlink()
    print("Backup deleted")