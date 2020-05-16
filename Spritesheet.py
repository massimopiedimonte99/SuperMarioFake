import pygame as pg
from settings import *

class Spritesheet():
    def __init__(self, path):
        self.spritesheet = pg.image.load(path).convert()

    def get_image(self, x, y, w, h):
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        return image