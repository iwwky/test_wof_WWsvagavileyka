import json
import os

SETTINGS_FILE = "settings.json"
ACHIEVEMENTS_FILE = "achievements.json"

DEFAULT_SETTINGS = {
    "music": True,
    "sounds": True,
    "difficulty": "СРЕДНЯЯ"
}

DEFAULT_ACHIEVEMENTS = {
    "first_blood": False,
    "boss_killer": False,
    "rich": False,
    "immortal": False,
    "score_10000": False
}


def load_settings():
    """Загрузить настройки игры."""

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Если появились новые настройки в будущем —
        # автоматически добавить их.
        for key, value in DEFAULT_SETTINGS.items():
            data.setdefault(key, value)

        return data

    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict):
    """Сохранить настройки игры."""

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)


def load_achievements():
    """Загрузить достижения."""

    if not os.path.exists(ACHIEVEMENTS_FILE):
        save_achievements(DEFAULT_ACHIEVEMENTS)
        return DEFAULT_ACHIEVEMENTS.copy()

    try:
        with open(ACHIEVEMENTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, value in DEFAULT_ACHIEVEMENTS.items():
            data.setdefault(key, value)

        return data

    except Exception:
        save_achievements(DEFAULT_ACHIEVEMENTS)
        return DEFAULT_ACHIEVEMENTS.copy()


def save_achievements(data: dict):
    """Сохранить достижения."""

    with open(ACHIEVEMENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)