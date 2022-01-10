import pygame as pg, sys, random, math
from pygame_functions import *
from settings import *
from hud import *
from pygame.locals import *
from item_sprites import *
from deathscreen import *
from bosses import *

# jak poruszac przeciwnikow wraz z backgroundem?
# co zrobic, zeby sprite przestal istniec? mimo ze znika, kolizje dalej zachodza.

setAutoUpdate(False)
"""
przeciwnicy nie musza sie poruszac z backgroundem
moga poruszac sie w wlasnych granicach, cos moze byc od 0, 10000 a cos moze byc (10000, 100000),
do tego wystarczajaca duzy background,
przedmioty ktore beda losowo sie pojawiac ale nie beda sie ruszac, i bedzie sie na nich blokowac bohater
np krzesla ***** 
moglbys teoretycznie zorbic wioske, gdzies na koordynatach porostu porozstawiac, a potem przesunac gdzies daleko
kompas tez bylby ok
przeciwnicy mogli by sie spawnowac ddalej, i potem wieksi w jeszcze dalszym zakresie, i idac do przodu byloby ich wiecej, niektorzy by sie konczyli itp.

"""

#drzewo
dtheta = math.pi / 4
ratio = 0.7



def line(screen, x, y, len, theta):
    if (len >= 1):
        x2 = int(x - len * math.cos(theta))
        y2 = int(y - len * math.sin(theta))
        pygame.draw.line(screen, (len, 255 / len, 0), (x, y), (x2, y2))
        line(screen, x2, y2, len * ratio, theta - dtheta)
        line(screen, x2, y2, len * ratio, theta + dtheta)


#reset
#reward
#play (action) - zwraca kierunek
#sprawdza klatke, iteracje gry
#prawdza if touching
#dla kierunku uzyje bossx i bossy zwiazany z bosem,
#dla tego co nie ma dotykac uzywam return? hero weaponx i y
#dla tego co chce dotykac uzywam hero xpos i ypos
bosses = []
enemies = []
healing =[]
crabs = []
particles = []
boss_score = 0

bosses = []

for x in range(40):#boss
    ronexadas = makeSprite('data/img/apparotion.png')
    addSpriteImage(ronexadas, 'data/img/death coin.png')
    transformSprite(ronexadas, 90, 1)
    ronexadas_hp = 1000
    ronexadas.x = random.randint(380, 700) # w jakim miejscu sie spawnuje x
    ronexadas.y = random.randint(-3000, -1000) # w jakim miejscu sie spawnuje y
    ronexadas.xspeed = random.randint(1,2)/21
    ronexadas.yspeed = random.randint(1,3)/21
    ronexadas_speed =3
    moveSprite(ronexadas, ronexadas.x, ronexadas.y, True)
    min_dist = 1000
    showSprite(ronexadas)
    pg.draw.rect(screen, (255,255,255),(ronexadas.x , ronexadas.y + 15, 30,10))
    bosses.append(ronexadas)
    boss_damage = makeTextBox(ronexadas.x, ronexadas.y + 10, 40, 0, str(ronexadas_hp), 10,
                              12)
for x in range(10):#golden saits
    fallen_star = makeSprite('data/img/Golden Saint.png')
    addSpriteImage(fallen_star, 'data/img/death coin.png')
    fallen_star.x = random.randint(0,350) # w jakim miejscu sie spawnuje x
    fallen_star.y = random.randint(400,450)  # w jakim miejscu sie spawnuje y
    fallen_star.xspeed = random.randint(0,0)
    fallen_star.yspeed = random.randint(0,0)
    moveSprite(fallen_star, fallen_star.x, fallen_star.y, True)
    showSprite(fallen_star)
    enemies.append(fallen_star)

for blade in range(10):#crab angels
    killer = makeSprite('data/img/blade from thelma l 3.png')
    addSpriteImage(killer, 'data/img/death coin.png')
    deadkiller = makeSprite('data/img/crawler.png')
    blade_hp = 100
    transformSprite(killer, 90, 1)
    killer.x = random.randint(300,510) # w jakim miejscu sie spawnuje x
    killer.y = random.randint(-1000,10)  # w jakim miejscu sie spawnuje y
    killer.xspeed = random.randint(0,0)
    killer.yspeed = random.randint(1,1)
    moveSprite(killer, killer.x, killer.y, True)
    showSprite(killer)
    enemies.append(killer)
#tego nie da sie przerzucic do innych plikow


for x in range(5):#hpboosts
    hpboost = makeSprite('data/img/crhvn lamp.png')
    transformSprite(hpboost, 90, 1)
    addSpriteImage(hpboost, 'data/img/crhvnchair.png')
    hpboost.x = random.randint(1,300) # w jakim miejscu sie spawnuje x
    hpboost.y = random.randint(1,200)  # w jakim miejscu sie spawnuje y
    hpboost.xspeed = random.randint(0,0)
    hpboost.yspeed = random.randint(0,0)
    moveSprite(hpboost, hpboost.x, hpboost.y, True)
    showSprite(hpboost)
    healing.append(hpboost)

while True:
    huddisplay()
    #soul
    if keyPressed("x") and souls > 0:
        souls = souls - 1
        hero_health = hero_health + 100
        mana = mana + 100
        print(' used soul ' +' mana '+ str(mana)+ ' hero_health ' + str(hero_health))
        # display change
        changeLabel(display_health, str(hero_health), hpcolor)
        changeLabel(display_mana, str(mana), manacolor)
        changeLabel(display_souls, str(souls), soulscolor)
    #mana potion
    if keyPressed("z") and mana_potions > 0:
        mana_potions = -1
        mana = mana + 50
        # display manachange
        changeLabel(display_mana, str(mana), manacolor)
        changeLabel(display_manapotions, str(mana_potions), manacolor)
        print(' used mana potion ' + 'manalevel is ' + str(mana))
    #magic attack
    if keyPressed("space") and mana !=0:
        mana = mana - 1
        line(screen, 400, 280, 20, math.pi / 2)
        updateDisplay()
        print('mana level' + str(mana))
        changeLabel(display_mana, str(mana), manacolor)
        line(screen, WIDTH / 2, HEIGHT, 10, math.pi / 2)
        fractal = line
        bullet_group.add(bullet.create_bullet())
    elif keyPressed("space") and mana == 0:
        print('no mana')
#atak
    if keyPressed("up") and keyPressed("c"):
        showSprite(hero_weapon)
        hero_weapon.yspeed = random.randint(-20,-1)
        moveSprite(hero_weapon, hero_weapon.x, hero_weapon.y, True)
        hero_weapon.y == hero_weapon.ybasic
        hero_weapon.y += hero_weapon.yspeed - 5


    elif keyPressed("down") and keyPressed("c"):
        showSprite(hero_weapon)
        hero_weapon.yspeed = random.randint(1,20)
        moveSprite(hero_weapon, hero_weapon.x, hero_weapon.y, True)
        hero_weapon.y == hero_weapon.ybasicatdown
        hero_weapon.y += hero_weapon.yspeed + 5
    elif keyPressed("right") and keyPressed("c"):
        showSprite(hero_weapon)
        hero_weapon.xspeed = random.randint(1, 20)
        moveSprite(hero_weapon, hero_weapon.x, hero_weapon.y, True)
        hero_weapon.x == hero_weapon.xbasic
        hero_weapon.x += hero_weapon.xspeed + 5
    elif keyPressed("left") and keyPressed("c"):
        showSprite(hero_weapon)
        hero_weapon.xspeed = random.randint(-20,-1)
        moveSprite(hero_weapon, hero_weapon.x, hero_weapon.y, True)
        hero_weapon.x == hero_weapon.xbasic
        hero_weapon.x += hero_weapon.xspeed - 5
    else:
        hero_weapon.x = hero_weapon.xbasic
        hero_weapon.y = hero_weapon.ybasic
        moveSprite(hero_weapon, hero_weapon.xbasic, hero_weapon.ybasic, True)
        killSprite(hero_weapon)
        updateDisplay()

    for killer in enemies:
        if touching(hero,killer):
            hero_health = hero_health - 1
            changeLabel(display_health, str(hero_health), hpcolor)
            updateDisplay()

            print('you have been hit by enemy -1hero_health')

        if touching(hero_weapon,killer):
            print(blade_hp)
            if blade_hp > 0:
                for killer in enemies:
                    blade_hp -= hero_weapon_attack
                    line(screen, 320, 400, 100, math.pi / 2)
                    updateDisplay()
                    for blade in range(random.randint(1, 2)):
                        killer.xspeed = killer.xspeed + random.randint(-1, 1) / 20

            else:
                for blade in range(random.randint(1,2)):
                    killer.xspeed = 0
                    killer.yspeed = 0
                    changeSpriteImage(killer, 1)

                updateDisplay()
    updateDisplay()
    #hpboost
    for hpboost in healing:
        if touching(hero, hpboost):
            hero_health = hero_health + 10
            changeLabel(display_health, str(hero_health), hpcolor)
            updateDisplay()
            print('you touched hpboost: + 10 hp ')
            killSprite(hpboost)
            healing.remove(hpboost)
#ronexadas collisions
    for ronexadas in bosses:
        if touching(hero,ronexadas):
            if ronexadas_hp > 0:
                hero_health = hero_health - 1
                boss_score += 1
                print('boss score'+str(boss_score))
                changeLabel(display_health, str(hero_health), hpcolor)
                print('you have been hit by enemy -1hero_health')

            updateDisplay()
            if ronexadas_hp < 0:
                ronexadas_speed = 0
                killSprite(ronexadas)


        if touching(hero_weapon,ronexadas):
            print('you have hit by enemy- it dies')
            ronexadas_hp = ronexadas_hp - hero_weapon_attack
            changeSpriteImage(killer, 1)
            boss_score += -1
            print('boss score' + str(boss_score))
            boss_damage = makeTextBox(ronexadas.x, ronexadas.y + 10, 40, 0, str(ronexadas_hp), 10,
                                      12)
            showTextBox(boss_damage)

            #hideTextBox(boss_damage)
            #ronexadas.xspeed = 0
            #ronexadas.yspeed = 0



        if touching(hero_weapon, ronexadas):
            print('you have hit by enemy- it dies')
            print(ronexadas_hp)
            if ronexadas_hp > 0:
                ronexadas_hp -= hero_weapon_attack

                updateDisplay()

            else:

                changeSpriteImage(ronexadas, 1)
                ronexadas.xspeed = 0
                ronexadas.yspeed = 0
                updateDisplay()

#basic hero movement and keys
    if keyPressed("up"):
        changeSpriteImage(hero, 0)
        transformSprite(hero, -180, 1)
        scrollBackground(0,10)
        for enemy in enemies:
            enemy.y  = enemy.y + 10
            moveSprite(enemy, enemy.x, enemy.y, True)
        for boss in bosses:
            boss.y  = boss.y + 10
            moveSprite(boss, boss.x, boss.y, True)
        for hpboost in healing:
            hpboost.y = hpboost.y + 10
            moveSprite(hpboost, hpboost.x, hpboost.y, True)

            updateDisplay()
    elif keyPressed("down"):
        changeSpriteImage(hero, 0)
        transformSprite(hero, 360, 1)
        scrollBackground(0,-10)
        for boss in bosses:
            boss.y  = boss.y -10
            moveSprite(boss, boss.x, boss.y, True)
        for enemy in enemies:
            enemy.y  = enemy.y - 10
            moveSprite(enemy, enemy.x, enemy.y, True)
        for hpboost in healing:
            hpboost.y  = hpboost.y -10
            moveSprite(hpboost, hpboost.x, hpboost.y, True)
    elif keyPressed("right"):
        changeSpriteImage(hero, 0)
        transformSprite(hero, -90, 1)
        scrollBackground(-10, 0)
        for boss in bosses:
            boss.x  = boss.x -10
            moveSprite(boss, boss.x, boss.y, True)
        for enemy in enemies:
            enemy.x  = enemy.x - 10
            moveSprite(enemy, enemy.x, enemy.y, True)
        for hpboost in healing:
            hpboost.x = hpboost.x - 10
            moveSprite(hpboost, hpboost.x, hpboost.y, True)
    elif keyPressed("left"):
        changeSpriteImage(hero, 0)
        transformSprite(hero, 90, 1)
        #xspeed -= 2
        scrollBackground(10, 0)
        moveSprite(killer,-5,0)
        for boss in bosses:
            boss.x  = boss.x +10
            moveSprite(boss, boss.x, boss.y, True)
        for enemy in enemies:
            enemy.x  = enemy.x + 10
            moveSprite(enemy, enemy.x, enemy.y, True)
        for hpboost in healing:
            hpboost.x  = hpboost.x + 10
            moveSprite(hpboost, hpboost.x, hpboost.y, True)

    moveSprite(hero, xpos, ypos, True)#hero movement
    #efekt przy ruchu broni
    particles.append([[hero_weapon.x, hero_weapon.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(2, 3)])
    #tworzy efekt przy broni
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[1][1] += particle[1][1]
        particle[2] -= 0.2
        pg.draw.circle(screen, (255, 0, 10), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)

    updateDisplay()
    #ruch potworow, bossow np if heropos jest blisko costam, wtedy:
    for enemy in enemies:
        enemy.x += killer.xspeed
        enemy.y += killer.yspeed


        moveSprite(enemy, enemy.x, enemy.y, True)
    def getheroypos():
        return int(ypos)
    def getheroxpos():
        return int(xpos)
    def getronxpos():
        return int(ronexadas.x)
    def getronypos():
        return int(ronexadas.y)

    for boss in bosses:
        boss.x += ronexadas.xspeed
        boss.y += ronexadas.yspeed
        delta_x = getheroxpos() - getronxpos()
        delta_y = getheroypos() - getronypos()
        if abs(delta_x) <= min_dist and abs(delta_y) <= min_dist:
            enemy_move_x = abs(delta_x) > abs(delta_y)
            if abs(delta_x) > boss.x and abs(delta_x) > boss.y:
                enemy_move_x = random.random() < 0.5
            enemy_move_x = random.random() < 0.5
            if enemy_move_x:
                boss.x += min(delta_x, ronexadas_speed) if delta_x > 0 else max(delta_x, -ronexadas_speed)
            else:
                boss.y += min(delta_y, ronexadas_speed) if delta_y > 0 else max(delta_y, -ronexadas_speed)

        moveSprite(boss, boss.x, boss.y, True)
    #game over, tylko czasem dziala
    if hero_health == 0:
        changeSpriteImage(hero, 1)
        yspeed = 0
        lifestatus = False
        print('game over')
        showSprite(endscreen)
        break


    bullet_group.draw(screen)
    bullet_group.update()


    tick(60)
    #print(getronxpos)
    #print(getronypos)
    #print(getheroxpos)
    #print(getheroypos)
    updateDisplay()

endWait()
