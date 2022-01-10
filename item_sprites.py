import pygame as pg, sys, random
from pygame_functions import *
from settings import *
from hero import *
from hud import *
from pygame.locals import *
from item_sprites import *


soulsprite = makeSprite('data/img/pyramid.png')
addSpriteImage(soulsprite, 'data/img/crhvnchair.png')
hpboost = makeSprite('data/img/crhvn lamp.png')
addSpriteImage(hpboost, 'data/img/crhvnchair.png')
moveSprite(hpboost,random.randint(0, 640) , random.randint(0, 800))
moveSprite(soulsprite, 500, 500)
#showSprite(hpboost)

soulsprite_touched = False
#if soulsprite_touched == False:
    #showSprite(soulsprite)