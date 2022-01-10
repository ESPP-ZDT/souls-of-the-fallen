import pygame as pg, sys, random
from pygame_functions import *

from particles import *

hero = makeSprite('data/img/hero.png')
addSpriteImage(hero, 'data/img/death coin.png')
showSprite(hero)
xpos = 400
ypos = 320
xspeed = 0
yspeed = 0
#stats
lifestatus = True
hero_health = 100
mana = 100
mana_potions = 1
souls = 1
hero_pos =[xpos,ypos]

hero_weapon = makeSprite('data/img/mad war axe.png')
#weapon_rect = pg.Rect(50, 50, hero_weapon.get_width(), hero_weapon.get_height())
hero_weapon.x = 400
hero_weapon.y = 280
hero_weapon.xbasic = 400
hero_weapon.xbasicatright = 350
hero_weapon.xbasicatleft = 320
hero_weapon.ybasic = 280
hero_weapon.ybasicatdown = 250
hero_weapon.xspeed = 0
hero_weapon.yspeed = 0
hero_weapon_attack = random.randint(5,20)
moveSprite(hero_weapon, hero_weapon.x, hero_weapon.y, True)

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.magic = makeSprite('data/img/scalony.png')
        self.magic.x = 400
        self.magic.y = 340
    def create_bullet(self):
        return Bullet(xpos,ypos)
    def update(self):
        self.rect.y += 10

bullet = Bullet(xpos, ypos)


bullet_group = pg.sprite.Group()