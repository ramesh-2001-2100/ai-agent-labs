import os
from pathlib import Path


folder = Path(r"C:\Users\lrame\Downloads\temp")
for file in folder.glob("*.txt"):
    new_name = file.with_suffix(".md")
    file.rename(new_name)
    print(f"Renamed: {file.name} -> {new_name.name}")
