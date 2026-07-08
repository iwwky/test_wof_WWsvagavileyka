import os
import tempfile
import unittest

import pygame

from data.save_manager import load_settings, save_settings, DEFAULT_SETTINGS


class SaveManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.settings_file = os.path.join(self.temp_dir.name, "settings.json")

        import data.save_manager as save_module
        self.original_file = save_module.SETTINGS_FILE
        save_module.SETTINGS_FILE = self.settings_file

    def tearDown(self):
        import data.save_manager as save_module
        save_module.SETTINGS_FILE = self.original_file
        self.temp_dir.cleanup()

    def test_save_and_load_settings(self):
        data = DEFAULT_SETTINGS.copy()
        data["difficulty"] = "СЛОЖНАЯ"
        data["fullscreen"] = True
        save_settings(data)

        loaded = load_settings()
        self.assertEqual(loaded["difficulty"], "СЛОЖНАЯ")
        self.assertTrue(loaded["fullscreen"])

    def test_load_creates_defaults(self):
        loaded = load_settings()
        self.assertEqual(loaded["music"], True)
        self.assertEqual(loaded["sounds"], True)


if __name__ == "__main__":
    unittest.main()
