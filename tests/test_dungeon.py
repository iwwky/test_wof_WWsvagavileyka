import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from core.dungeon import Dungeon, generate_room_matrix
from settings import *


class DungeonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    def test_generate_room_has_walls(self):
        matrix = generate_room_matrix(["top", "bottom"], "spawn", (0, 0))
        self.assertEqual(matrix[0][0], TILE_WALL)
        self.assertEqual(matrix[ROWS - 1][COLS - 1], TILE_WALL)

    def test_boss_door_locked_until_arenas_cleared(self):
        dungeon = Dungeon()
        dungeon.current_pos = (0, 1)
        dungeon.boss_unlocked = False

        top_door_y = TILE_SIZE // 2
        blocked = dungeon.check_collision(COLS // 2 * TILE_SIZE, top_door_y, TANK_SIZE)
        self.assertTrue(blocked)

        dungeon.boss_unlocked = True
        dungeon.doors_locked = False
        free = dungeon.check_collision(COLS // 2 * TILE_SIZE, top_door_y, TANK_SIZE)
        self.assertFalse(free)

    def test_unlock_room_marks_cleared(self):
        dungeon = Dungeon()
        room_pos = (-1, 0)
        dungeon.current_pos = room_pos
        self.assertFalse(dungeon.rooms[room_pos]["cleared"])

        dungeon.unlock_doors()
        self.assertTrue(dungeon.rooms[room_pos]["cleared"])

    def test_static_layouts_are_deterministic(self):
        first = generate_room_matrix(["right"], "arena", (-1, 0))
        second = generate_room_matrix(["right"], "arena", (-1, 0))
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
