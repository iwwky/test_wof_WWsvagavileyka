import json
import os

from settings import DATA_DIR

SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
ACHIEVEMENTS_FILE = os.path.join(DATA_DIR, "achievements.json")

DEFAULT_SETTINGS = {
    "music": True,
    "sounds": True,
    "difficulty": "СРЕДНЯЯ",
    "fullscreen": False,
}


def load_settings():

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, value in DEFAULT_SETTINGS.items():
            data.setdefault(key, value)

        return data

    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict):

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)
