import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from core.dungeon import Dungeon
from entities.bullet import Bullet
from settings import *


class BulletTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    def test_bullet_hits_obstacle(self):
        dungeon = Dungeon()
        dungeon.current_pos = (0, 0)
        matrix = dungeon.get_matrix()

        row, col = 5, 5
        matrix[row][col] = TILE_OBSTACLE
        bullet = Bullet(col * TILE_SIZE + 8, row * TILE_SIZE + 8, "right", True)

        bullet.update(dungeon)
        self.assertFalse(bullet.active)
        self.assertEqual(matrix[row][col], TILE_EMPTY)

    def test_bullet_deactivates_on_wall(self):
        dungeon = Dungeon()
        bullet = Bullet(-10, TILE_SIZE, "left", True)
        bullet.update(dungeon)
        self.assertFalse(bullet.active)


if __name__ == "__main__":
    unittest.main()
