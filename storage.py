import json
import os
from models import FinanceManager

DATA_FILE = "finance_data.json"

def load_data(filepath = DATA_FILE):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                return FinanceManager.from_dict(data)
            
        except json.JSONDecodeError:
            print("Error! Corrupted save file detected.")
            backup_file = filepath + ".back"
            if os.path.exists(filepath):
                os.rename(filepath, backup_file)
                print(f"Backed up corrupted file to '{backup_file}'. ")

    return FinanceManager()

def save_data(manager: FinanceManager, file_path = DATA_FILE):
    data = manager.to_dict()
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)