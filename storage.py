import json
import os

DATA_FILE = "finance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading file")
            backup_file = DATA_FILE + ".backup"
            os.rename(DATA_FILE, backup_file)
            print(f"Backed up corrupted file to {backup_file}")

    return {"transactions" : [], "budgets": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)