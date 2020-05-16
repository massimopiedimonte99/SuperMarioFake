import pygame as pg
import random

from Spritesheet import *

from os import path
from settings import *

class Background(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = BG_LAYER
        self.groups = game.sprites, game.bg_elements
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        
        self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE)
        self.rect.x = self.pos.x 
        self.rect.y = self.pos.y 
        
class Cloud(Background):
    def __init__(self, game, x, y):
        Background.__init__(self, game, x, y)
        self.image = pg.image.load(path.join(self.game.img_dir, 'cloud.png')).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE * 4, TILESIZE * 4))
        self.image.set_colorkey(BLACK)
    
class Hill(Background):
    def __init__(self, type, game, x, y):
        Background.__init__(self, game, x, y)
        self.image = pg.image.load(path.join(self.game.img_dir, 'big_hill.png')).convert()
        
        if type == 'big':
            self.image = pg.transform.scale(self.image, (TILESIZE * 6, TILESIZE * 3))
            self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE - 60)
        else:
            self.image = pg.transform.scale(self.image, (TILESIZE * 4, TILESIZE *  2))
            self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE - 30)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x 
        self.rect.y = self.pos.y 

        