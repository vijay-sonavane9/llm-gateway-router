import os
from pathlib import Path

def create_structure(base_name="llm-gateway-router"):
    # Define the folders that need to be created inside the root
    folders = [
        "models",
        "data",
        "src",
        "ui"
    ]

    # Define the files that need to be created (including their sub-paths)
    files = [
        "requirements.txt",
        "generate_data.py",
        "train.py",
        "src/config.py",
        "src/extractor.py",
        "src/db.py",
        "src/main.py",
        "ui/app.py"
    ]

    # Create the root directory
    base_path = Path(base_name)
    base_path.mkdir(parents=True, exist_ok=True)
    print(f"Created root: {base_path}/")

    # Create all subdirectories
    for folder in folders:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {folder_path}/")

    # Create all empty files
    for file in files:
        file_path = base_path / file
        file_path.touch(exist_ok=True)
        print(f"Created file: {file_path}")

    print("\nProject structure generated successfully!")

if __name__ == "__main__":
    create_structure()