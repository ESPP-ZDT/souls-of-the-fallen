import pygame as pg, sys, random
from pygame_functions import *
from settings import *
from hero import *
from pygame.locals import *


#hud
hpcolor = "red"
display_health = makeLabel(str(hero_health),40,10,10,hpcolor,"Agency FB")
manacolor = "blue"
display_mana = makeLabel(str(mana),40,60,10,manacolor,"Agency FB")
soulscolor = "white"
display_souls = makeLabel(str(souls),40,120,10,soulscolor,"Agency FB")
display_manapotions = makeLabel(str(mana_potions),40, 160, 10, manacolor, 'Agency FB')


def huddisplay():
    showLabel(display_health)
    showLabel(display_mana)
    showLabel(display_souls)
    showLabel(display_manapotions)


