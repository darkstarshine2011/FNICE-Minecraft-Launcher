import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fnice_config.json")

DEFAULT_CONFIG = {
    "last_username": "FNICE_Player",
    "last_mc_version": "",
    "last_modloader": "vanilla",
    "last_modloader_version": "",
}

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return {**DEFAULT_CONFIG, **data}
    except:
        return DEFAULT_CONFIG.copy()

def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Config save error: {e}")