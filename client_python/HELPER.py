import pygame
from pygame import *
from pygame import gfxdraw


def add_img(path: str, scale=0):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    return img
