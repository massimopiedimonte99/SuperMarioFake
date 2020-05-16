import pygame as pg
import random

from Obstacles import Wall, QuestionBlock, BronzeWall, Flag
from Spritesheet import *

from os import path
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.won = False

        self.spritesheet = Spritesheet(path.join(self.game.img_dir, 'player.png'))

        self.walking = False
        self.last_update = 0
        self.current_frame = 0
        self.going_right = True

        self.load_images()
        self.image = self.standing_frames_r
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        
        self.rect = self.image.get_rect()

        self.move_left = self.move_right = False

        self.pos = pg.math.Vector2(x * TILESIZE, y * TILESIZE)
        self.acc = pg.math.Vector2(0, GRAVITY)
        self.vel = pg.math.Vector2(0, 0)
    
    def load_images(self):
        self.standing_frames_r = self.spritesheet.get_image(1, 1, 16, 16)
        self.standing_frames_r.set_colorkey(WHITE)

        self.standing_frames_l = pg.transform.flip(self.standing_frames_r, True, False)
        self.standing_frames_l.set_colorkey(WHITE)

        self.walking_frames_r = [   
                                    self.spritesheet.get_image(18, 1, 16, 16),
                                    self.spritesheet.get_image(35, 1, 16, 16),
                                    self.spritesheet.get_image(52, 1, 16, 16)
                                ]
        for frame in self.walking_frames_r:
            frame.set_colorkey(WHITE)

        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))
            frame.set_colorkey(WHITE)

    def jump(self):
        # if we stand on platforms, we can jump
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
        self.rect.y -= 1

        if hits:
            self.game.jump_sound.play()
            self.vel.y -= PLAYER_JUMP

    def collide_with_obstacles(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                    if isinstance(hits[0], Flag):
                        self.won = True
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                    if isinstance(hits[0], Wall):
                        hits[0].kill()
                        self.game.score += 50
                    if isinstance(hits[0], QuestionBlock) and hits[0].hitted == False:
                        self.game.coin_sound.play()
                        hits[0].hitted = True
                        self.game.score += 500
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.animate()
        self.vel.x = 0
        
        if self.move_left:
            self.vel.x = -PLAYER_SPEED
        if self.move_right:
            self.vel.x = PLAYER_SPEED

        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

        self.vel += self.acc

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # updating position for the two axis checking if they're colliding
        self.rect.x = self.pos.x
        self.collide_with_obstacles('x')
        self.rect.y = self.pos.y
        self.collide_with_obstacles('y')

        # collision with enemy
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)

        if hits:
            # check if player jumped on the enemy and if so delete the enemy
            if self.vel.y > 0:
                self.vel.y = -20
                self.game.bump_sound.play()
                hits[0].kill()
                self.game.score += 100
            
            # if player did not jump on the enemy, game over
            else:
                self.game.tries += 1
                self.game.show_gameover_screen()
                self.game.playing = False
        
        # gameover if player falls down
        if self.pos.y > HEIGHT:
            self.game.tries += 1
            self.game.show_gameover_screen()
            self.game.playing = False
        
        # exit if player touches flag
        if self.won:
            exit()
        
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                if self.vel.x > 0:
                    self.going_right = True
                    self.image = self.walking_frames_r[self.current_frame]
                elif self.vel.x < 0:
                    self.going_right = False
                    self.image = self.walking_frames_l[self.current_frame]
        
        else:
            if self.going_right:
                self.image = self.standing_frames_r
            else:
                self.image = self.standing_frames_l