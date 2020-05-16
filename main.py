'''
font:     https://www.dafont.com/it/vcr-osd-mono.font
assets:   https://www.spriters-resource.com/nes/supermariobros/
sounds and music:   http://www.orangefreesounds.com/mario-coin-sound/
                    https://www.myinstants.com/instant/mario-jump/
                    https://downloads.khinsider.com/game-soundtracks/album/super-mario-bros

@author: Massimo Piedimonte
'''

import pygame as pg
from Game import Game
from settings import *

pg.init()

g = Game()

g.show_start_screen()
while g.running:
    g.new_game()
    g.show_gameover_screen()