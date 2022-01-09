
import pygame
from pygame import *
from pygame import gfxdraw


def add_img(path: str, scale=0):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    return img


def get_info(info, remaining_time, screen):
    current_info_str = "|GAME LEVEL: " + str(info.get('game_level')) + " | MOVES: " + str(info.get(
        "moves")) + " | POINTS: " + str(info.get("grade")) + " | REMAINING TIME: " + remaining_time + "|"
    INFO_FONT = font.SysFont("Arial", 20, bold=True)
    info_surface = INFO_FONT.render(current_info_str, True, Color(255, 255, 255))
    info_scale = info_surface.get_rect(
        center=(screen.get_width() - (info_surface.get_width()), screen.get_height() - 10))
    return info_surface, info_scale
