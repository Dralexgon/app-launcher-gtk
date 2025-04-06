import os
from pathlib import Path

desktop_dirs = []
for d in os.environ["XDG_DATA_DIRS"].split(":"):
    desktop_dirs.append(Path(d) / "applications")

# List to store found .desktop files
desktop_files = []

for directory in desktop_dirs:
    if directory.exists():
        for file in directory.glob("*.desktop"):
            desktop_files.append(file)

# Print the paths
for file in desktop_files:
    print(file)