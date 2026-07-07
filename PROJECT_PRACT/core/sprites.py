import pygame
from settings import DIRECTION_ANGLES


def sprite_for_direction(image, direction):
    return pygame.transform.rotate(image, DIRECTION_ANGLES[direction])


def blit_tank(screen, image, x, y, size, direction):
    """Draw a tank sprite centered on its grid cell."""
    rotated = sprite_for_direction(image, direction)
    rect = rotated.get_rect(center=(x + size // 2, y + size // 2))
    screen.blit(rotated, rect)
