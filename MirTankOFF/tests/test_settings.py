import unittest

from settings import (
    DIFFICULTY_SETTINGS,
    get_boss_hp,
    get_boss_shoot_cooldown,
    get_difficulty_settings,
    get_enemy_hp,
    get_enemy_speed_mult,
    get_heal_cost,
    get_player_max_hp,
    GAME_SETTINGS,
)


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.original_difficulty = GAME_SETTINGS["difficulty"]

    def tearDown(self):
        GAME_SETTINGS["difficulty"] = self.original_difficulty

    def test_difficulty_player_hp(self):
        GAME_SETTINGS["difficulty"] = "ЛЕГКАЯ"
        self.assertEqual(get_player_max_hp(), 5)

        GAME_SETTINGS["difficulty"] = "СРЕДНЯЯ"
        self.assertEqual(get_player_max_hp(), 4)

        GAME_SETTINGS["difficulty"] = "СЛОЖНАЯ"
        self.assertEqual(get_player_max_hp(), 3)

    def test_difficulty_enemy_hp(self):
        GAME_SETTINGS["difficulty"] = "ЛЕГКАЯ"
        self.assertEqual(get_enemy_hp(), 2)

        GAME_SETTINGS["difficulty"] = "СРЕДНЯЯ"
        self.assertEqual(get_enemy_hp(), 4)

        GAME_SETTINGS["difficulty"] = "СЛОЖНАЯ"
        self.assertEqual(get_enemy_hp(), 4)

    def test_difficulty_boss_hp(self):
        GAME_SETTINGS["difficulty"] = "ЛЕГКАЯ"
        self.assertEqual(get_boss_hp(), 15)

        GAME_SETTINGS["difficulty"] = "СРЕДНЯЯ"
        self.assertEqual(get_boss_hp(), 20)

        GAME_SETTINGS["difficulty"] = "СЛОЖНАЯ"
        self.assertEqual(get_boss_hp(), 25)

    def test_hard_enemy_speed_multiplier(self):
        GAME_SETTINGS["difficulty"] = "СЛОЖНАЯ"
        self.assertEqual(get_enemy_speed_mult(), 1.3)

        GAME_SETTINGS["difficulty"] = "СРЕДНЯЯ"
        self.assertEqual(get_enemy_speed_mult(), 1.0)

    def test_heal_cost_depends_on_difficulty(self):
        GAME_SETTINGS["difficulty"] = "ЛЕГКАЯ"
        self.assertEqual(get_heal_cost(), 3)

        GAME_SETTINGS["difficulty"] = "СЛОЖНАЯ"
        self.assertEqual(get_heal_cost(), 8)

    def test_boss_shoot_cooldown_depends_on_difficulty(self):
        GAME_SETTINGS["difficulty"] = "ЛЕГКАЯ"
        self.assertEqual(get_boss_shoot_cooldown(), 100)

        GAME_SETTINGS["difficulty"] = "СРЕДНЯЯ"
        self.assertEqual(get_boss_shoot_cooldown(), 70)

        GAME_SETTINGS["difficulty"] = "СЛОЖНАЯ"
        self.assertEqual(get_boss_shoot_cooldown(), 50)

    def test_get_difficulty_settings_fallback(self):
        GAME_SETTINGS["difficulty"] = "НЕИЗВЕСТНАЯ"
        settings = get_difficulty_settings()
        self.assertEqual(settings, DIFFICULTY_SETTINGS["СРЕДНЯЯ"])


if __name__ == "__main__":
    unittest.main()
