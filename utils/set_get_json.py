import json
import os

# Path to the status JSON file, located in the same directory as this script
STATUS_FILE = os.path.join(os.path.dirname(__file__), "status.json")


def load_status():
    if not os.path.exists(STATUS_FILE):
        return {}
    with open(STATUS_FILE, "r") as f:
        return json.load(f)


def get_status(key):
    """
    Retrieve a single value from the status dict by key.
    """
    status = load_status()
    return status.get(key)


def set_status(clave, valor):
    status = load_status()
    status[clave] = valor
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=4)
