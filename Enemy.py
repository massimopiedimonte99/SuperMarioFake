import pygame as pg
import random

from Spritesheet import *
from os import path
from settings import *

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ENEMY_LAYER
        self.groups = game.sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
    
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()

        self.last_update = 0
        self.current_frame = 0

        self.acc = pg.math.Vector2(0, GRAVITY)
        
        self.vel = pg.math.Vector2(random.choice([GOOMBA_SPPED, -GOOMBA_SPPED]))
        self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE)

        self.rect.x = self.pos.x 
        self.rect.y = self.pos.y 

    def update(self): 
        self.animate()
        self.vel += self.acc

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        self.rect.y = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.ground, False)
        if hits:
            if self.vel.y > 0:
                self.pos.y = hits[0].rect.top - self.rect.height
            self.vel.y = 0
            self.rect.y = self.pos.y
        
        self.rect.x += self.vel.x
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)

        if hits:
            self.vel = -self.vel
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
            self.image = self.walking_frames[self.current_frame]
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

class Goomba(Enemy):
    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y)
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, 'enemies.png'))

        self.load_images()
        self.image = self.walking_frames[1]
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
    
    def load_images(self):
        self.walking_frames =   [ 
                                    self.spritesheet.get_image(0, 0, 16, 16),
                                    self.spritesheet.get_image(16, 0, 16, 16)
                                ]
        
        for frame in self.walking_frames:
            frame.set_colorkey(WHITE)