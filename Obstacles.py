import pygame as pg
from os import path
from settings import *

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = OBSTACLE_LAYER
        self.groups = game.sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        
        self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE)
        self.rect.x = self.pos.x 
        self.rect.y = self.pos.y 

class Wall(Obstacle):
    def __init__(self, game, x, y):
        Obstacle.__init__(self, game, x, y)
    
        self.image = pg.image.load(path.join(self.game.img_dir, 'wall.png')).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

class QuestionBlock(Obstacle):
    def __init__(self, game, x, y):
        Obstacle.__init__(self, game, x, y)
    
        self.image = pg.image.load(path.join(self.game.img_dir, 'question_block.png')).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

        self.hitted = False
    
    def update(self):
        if self.hitted:
            self.image = pg.image.load(path.join(self.game.img_dir, 'question_block_hitted.png')).convert()
            self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

class Tube(Obstacle):
    def __init__(self, type_of_tube, game, x, y):
        self._layer = TUBE_LAYER
        Obstacle.__init__(self, game, x, y)

        if type_of_tube == 'small':
            self.image = pg.image.load(path.join(self.game.img_dir, 'small_tube.png')).convert()
            self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 3))
            self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE - 50)
        
        if type_of_tube == 'medium':
            self.image = pg.image.load(path.join(self.game.img_dir, 'medium_tube.png')).convert()
            self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 4))
            self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE - 90)
        
        if type_of_tube == 'big':
            self.image = pg.image.load(path.join(self.game.img_dir, 'big_tube.png')).convert()
            self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 5))
            self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE - 120)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x 
        self.rect.y = self.pos.y 

class BronzeWall(Obstacle):
    def __init__(self, game, x, y):
        Obstacle.__init__(self, game, x, y)
    
        self.image = pg.image.load(path.join(self.game.img_dir, 'bronze_wall.png')).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

class Flag(Obstacle):
    def __init__(self, game, x, y):
        Obstacle.__init__(self, game, x, y)
    
        self.image = pg.image.load(path.join(self.game.img_dir, 'flag.png')).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE + 20, TILESIZE * 10))
        self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE - 285)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x 
        self.rect.y = self.pos.y 
