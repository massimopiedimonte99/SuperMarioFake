import pygame as pg

from Player import Player
from Obstacles import Wall, Tube, QuestionBlock, BronzeWall, Flag
from Background import Background, Cloud, Hill
from Enemy import Goomba

from settings import *
from os import path

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        
        pg.mixer.init()
        
        self.running = True

        self.dirname = path.dirname(__file__)
        self.img_dir = path.join(self.dirname, 'img')

        self.font_name = path.join(path.join(self.dirname, "font"), FONT_NAME)
        
        self.tries = 0

        self.load_data()

    def load_data(self):
        self.tilemap = []
        
        # loading tilemap into "self.tilemap" array
        with open(path.join(self.dirname, 'map.txt'), 'r+') as f:
            for l in f:
                self.tilemap.append(l)
        
        self.snd_dir = path.join(self.dirname, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump.wav'))
        self.coin_sound = pg.mixer.Sound(path.join(self.snd_dir, 'coin.wav'))
        self.bump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'bump.wav'))

    def new_game(self):
        self.playing = True
        self.sprites = pg.sprite.LayeredUpdates()
        self.obstacles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bg_elements = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        pg.mixer.music.load(path.join(self.snd_dir, 'theme.mp3'))

        self.score = 0
        
        # camera settings
        self.cameraLeft = 0
        self.cameraRight = WIDTH

        # blit objects according to tilemap
        for x, tileline in enumerate(self.tilemap):
            for y, tile in enumerate(tileline):
                if tile == '1':
                    Wall(self, y, x)
                if tile == 'A':
                    w = Wall(self, y, x)
                    self.ground.add(w)
                if tile == 'Q':
                    QuestionBlock(self, y, x)
                if tile == 'E':
                    Enemy(self, y, x)
                if tile == 't':
                    Tube('small', self, y, x)
                if tile == 'T':
                    Tube('medium', self, y, x)
                if tile == 'Y':
                    Tube('big', self, y, x)
                if tile == 'F':
                    Flag(self, y, x)
                if tile == 'b':
                    BronzeWall(self, y, x)
                if tile == 'G':
                    Goomba(self, y, x)
                if tile == 'C':
                    Cloud(self, y, x)
                if tile == 'H':
                    Hill('big', self, y, x)
                if tile == 'h':
                    Hill('small', self, y, x)
                if tile == 'P':
                    self.player = Player(self, y, x)


        self.run()

    def events(self):
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            
            # checking controls
            if evt.type == pg.KEYDOWN:
                if evt.key == pg.K_LEFT:
                    self.player.move_left = True
                if evt.key == pg.K_RIGHT:
                    self.player.move_right = True
                if evt.key == pg.K_SPACE:
                    self.player.jump()
            if evt.type == pg.KEYUP:
                if evt.key == pg.K_LEFT:
                    self.player.move_left = False
                if evt.key == pg.K_RIGHT:
                    self.player.move_right = False

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.header()
        self.sprites.draw(self.screen)
        
        pg.display.flip()
    
    def update(self):
        self.sprites.update()

        # scrolling camera (if we're not reaching the starting/ending point)
        if self.player.pos.x > WIDTH//2:
            self.player.pos.x -= abs(self.player.vel.x)
            for obstacle in self.obstacles:
                obstacle.rect.x -= abs(self.player.vel.x)
            for bg_element in self.bg_elements:
                bg_element.rect.x -= abs(self.player.vel.x)
            for enemy in self.enemies:
                enemy.rect.x -= abs(self.player.vel.x)
            
            self.cameraLeft += abs(self.player.vel.x)
            self.cameraRight += abs(self.player.vel.x)
        
        elif self.player.pos.x <= WIDTH//2 and self.cameraLeft > 0 and self.cameraRight > WIDTH:
            self.player.pos.x += abs(self.player.vel.x)
            for obstacle in self.obstacles:
                obstacle.rect.x += abs(self.player.vel.x)
            for bg_element in self.bg_elements:
                bg_element.rect.x += abs(self.player.vel.x)
            for enemy in self.enemies:
                enemy.rect.x += abs(self.player.vel.x)
            

            self.cameraLeft -= abs(self.player.vel.x)
            self.cameraRight -= abs(self.player.vel.x)
        
        # adding boundaries (quite glitchy)
        if self.cameraLeft == 0 and self.cameraRight == WIDTH and self.player.pos.x <= 0:
            self.player.pos.x = 0
            self.player.vel.x = 0
            self.player.rect.x = self.player.pos.x
    
    def header(self):
        self.draw_text("MARIO", 20, WHITE, 60, 10)
        self.draw_text(str(self.score).zfill(10), 20, WHITE, 90, 30)


    def show_start_screen(self):
        self.screen.fill(BG_COLOR)
        self.intro = pg.image.load(path.join(self.img_dir, 'intro.png'))
        self.intro = pg.transform.scale(self.intro, (self.intro.get_rect().width//2, self.intro.get_rect().height//2))
        self.intro_rect = self.intro.get_rect()
        self.intro_rect.x = (WIDTH // 2) - (self.intro_rect.width // 2)
        self.intro_rect.y = (HEIGHT // 2) - (self.intro_rect.height // 2)
        self.draw_text("Press a key to start", 20, WHITE, WIDTH // 2, HEIGHT - 250)
        self.screen.blit(self.intro, self.intro_rect)
        pg.display.flip()
        self.wait_for_key()


    def show_gameover_screen(self):
        if not self.running:
            return

        self.screen.fill(BLACK)
        self.header()
        self.draw_text("x" + str(self.tries).zfill(2), 20, WHITE, WIDTH // 2, HEIGHT // 2)
        pg.display.flip()
        self.wait_for_key()


    # draw_text and wait_for_key are grabbed from: https://github.com/kidscancode/pygame_tutorials/blob/master/platform/part%2018/main.py
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            pg.time.Clock().tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    
    def run(self):
        pg.mixer.music.play(loops=-1)
        while self.playing:
            pg.time.Clock().tick(FPS)  
            
            self.events()
            self.update()
            self.draw()