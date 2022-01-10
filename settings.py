import pygame as pg, sys, random
from pygame_functions import *
from settings import *

from pygame.locals import *

pg.init()
WIDTH = 640
HEIGHT = 800
screenSize(HEIGHT,WIDTH)
setAutoUpdate(False)
setBackgroundImage('data/img/tile 3.png')
main_clock = pg.time.Clock()