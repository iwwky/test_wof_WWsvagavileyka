# core/audio_manager.py
import array
import math
import os

import pygame

from settings import SOUNDS_DIR, MUSIC_DIR, sound_path


class AudioManager:
    """Менеджер звука: загружает файлы из assets/sounds/ и assets/music/."""

    SOUND_FILES = {
        "shoot": ("shoot", ("shoot.ogg", "shoot.wav", "выстрел.ogg", "выстрел.wav")),
        "hit": ("hit", ("hit.ogg", "hit.wav", "попадание.ogg", "попадание.wav")),
        "coin": ("coin", ("coin.ogg", "coin.wav", "монета.ogg", "монета.wav")),
        "heal": ("heal", ("heal.ogg", "heal.wav", "лечение.ogg", "лечение.wav")),
        "menu": ("menu", ("menu.ogg", "menu.wav", "меню.ogg", "меню.wav")),
    }

    MUSIC_FILES = ("music.ogg", "music.wav", "theme.ogg", "theme.wav", "фон.ogg", "фон.wav")

    def __init__(self):
        self.enabled = False
        self.music_loaded = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
        except pygame.error:
            self.enabled = False

        self.sounds = {}
        if self.enabled:
            for name, (_, candidates) in self.SOUND_FILES.items():
                loaded = self._load_sound_file(candidates)
                if loaded is not None:
                    self.sounds[name] = loaded
                else:
                    self.sounds[name] = self._make_beep(self._fallback_frequency(name), 80)

            self._load_music()

    def _load_sound_file(self, candidates):
        for filename in candidates:
            path = sound_path(filename)
            if os.path.isfile(path):
                try:
                    return pygame.mixer.Sound(path)
                except pygame.error:
                    continue
        return None

    def _load_music(self):
        for filename in self.MUSIC_FILES:
            path = os.path.join(MUSIC_DIR, filename)
            if os.path.isfile(path):
                try:
                    pygame.mixer.music.load(path)
                    self.music_loaded = True
                    return
                except pygame.error:
                    continue

    @staticmethod
    def _fallback_frequency(name):
        return {
            "shoot": 880,
            "hit": 220,
            "coin": 660,
            "heal": 520,
            "menu": 440,
        }.get(name, 440)

    def _make_beep(self, frequency, duration_ms):
        sample_rate = 22050
        sample_count = int(sample_rate * duration_ms / 1000)
        buffer = array.array("h")

        for i in range(sample_count):
            fade = 1.0 - (i / max(sample_count - 1, 1))
            value = int(12000 * fade * math.sin(2 * math.pi * frequency * i / sample_rate))
            buffer.append(value)
            buffer.append(value)

        return pygame.mixer.Sound(buffer=buffer)

    def play(self, name):
        from settings import GAME_SETTINGS

        if not self.enabled or not GAME_SETTINGS.get("sounds", True):
            return

        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def play_music(self, loop=-1):
        from settings import GAME_SETTINGS

        if not self.enabled or not GAME_SETTINGS.get("music", True) or not self.music_loaded:
            return

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loop)

    def stop_music(self):
        if self.enabled and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def update_music_state(self):
        from settings import GAME_SETTINGS

        if not self.enabled:
            return

        if GAME_SETTINGS.get("music", True):
            self.play_music()
        else:
            self.stop_music()
