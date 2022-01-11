import pygame as pg, sys, random, math
from pygame_functions import *
from settings import *
from hud import *
from pygame.locals import *
from deathscreen import *

#setAutoUpdate(False)

#drzewo
dtheta = math.pi / 4
ratio = 0.7

#fraktal
def line(screen, x, y, len, theta):
    if (len >= 1):
        x2 = int(x - len * math.cos(theta))
        y2 = int(y - len * math.sin(theta))
        pygame.draw.line(screen, (len, 255 / len, 0), (x, y), (x2, y2))
        line(screen, x2, y2, len * ratio, theta - dtheta)
        line(screen, x2, y2, len * ratio, theta + dtheta)

enemies = []
healing =[]
particles = []
boss_score = 0


for x in range(40):#boss
    ronexadas = makeSprite('data/img/apparotion.png')
    addSpriteImage(ronexadas, 'data/img/death coin.png')
    transformSprite(ronexadas, 90, 1)
    ronexadas_hp = 1000
    ronexadas.x = random.randint(380, 700) # w jakim miejscu sie spawnuje x
    ronexadas.y = random.randint(-3000, -1000) # w jakim miejscu sie spawnuje y
    ronexadas.xspeed = random.randint(1,2)/2
    ronexadas.yspeed = random.randint(1,3)/2
    ronexadas_speed = 3
    moveSprite(ronexadas, ronexadas.x, ronexadas.y, True)#to musi zostac
    min_dist = 1000
    showSprite(ronexadas)
    #pg.draw.rect(screen, (255,255,255),(ronexadas.x , ronexadas.y + 15, 30,10))

    enemies.append(ronexadas)

#tego nie da sie przerzucic do innych plikow
for x in range(5):#hpboosts
    hpboost = makeSprite('data/img/crhvn lamp.png')
    transformSprite(hpboost, 90, 1)
    hpboost.x = random.randint(1,300) # w jakim miejscu sie spawnuje x
    hpboost.y = random.randint(1,200)  # w jakim miejscu sie spawnuje y
    hpboost.xspeed = random.randint(0,0)
    hpboost.yspeed = random.randint(0,0)
    moveSprite(hpboost, hpboost.x, hpboost.y, True)
    showSprite(hpboost)
    healing.append(hpboost)

while True:
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[1][1] += particle[1][1]
        particle[2] -= 0.2
        pg.draw.circle(screen, (255, 0, 10), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)


    #soul
    if keyPressed("x") and souls > 0:
        souls -= 1
        hero_health = hero_health + 100
        mana = mana + 100
        print(' used soul ' +' mana '+ str(mana)+ ' hero_health ' + str(hero_health))
        # display change
        changeLabel(display_health, str(hero_health), hpcolor)
        changeLabel(display_mana, str(mana), manacolor)
        changeLabel(display_souls, str(souls), soulscolor)
    #mana potion
    if keyPressed("z") and mana_potions > 0:
        mana_potions -= 1
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
    for ronexadas in enemies:
        if touching(hero,ronexadas):
            if ronexadas_hp > 0:
                hero_health = hero_health - 1
                boss_score += 1
                print('boss score'+str(boss_score))
                changeLabel(display_health, str(hero_health), hpcolor)
                print('you have been hit by enemy -1hero_health')
            updateDisplay()
            if ronexadas_hp <= 0:
                ronexadas_speed = 0
                killSprite(ronexadas)
                enemies.remove(ronexadas)
                hideTextBox(boss_damage)

        if touching(hero_weapon, ronexadas):
            if ronexadas_hp > 0:
                ronexadas_hp -= hero_weapon_attack
                boss_score += -1
                boss_damage = makeTextBox(ronexadas.x, ronexadas.y + 10, 40, 0, str(ronexadas_hp), 10, 12)
                showTextBox(boss_damage)
                updateDisplay()
            else:
                changeSpriteImage(ronexadas, 1)
                ronexadas.xspeed = 0# to nie dziala
                ronexadas.yspeed = 0#to nie dziala
                #updateDisplay()
                #problem jest taki ze jak zabije jednego enemy, ruszaja sie dalej, zabijajac dalej trawiam na takiego, ktory sprawia ze przestaja sie ruszac

#basic hero movement and keys
    if keyPressed("up"):
        changeSpriteImage(hero, 0)
        transformSprite(hero, -180, 1)
        scrollBackground(0,10)
        for enemy in enemies:
            enemy.y  = enemy.y + 10
            moveSprite(enemy, enemy.x, enemy.y, True)
        for hpboost in healing:
            hpboost.y = hpboost.y + 10
            moveSprite(hpboost, hpboost.x, hpboost.y, True)
            updateDisplay()
    elif keyPressed("down"):
        changeSpriteImage(hero, 0)
        transformSprite(hero, 360, 1)
        scrollBackground(0,-10)
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
        for enemy in enemies:
            enemy.x = enemy.x - 10
            moveSprite(enemy, enemy.x, enemy.y, True)
        for hpboost in healing:
            hpboost.x = hpboost.x - 10
            moveSprite(hpboost, hpboost.x, hpboost.y, True)
    elif keyPressed("left"):
        changeSpriteImage(hero, 0)
        transformSprite(hero, 90, 1)
        #xspeed -= 2
        scrollBackground(10, 0)
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

    updateDisplay()
    #ruch potworow, bossow np if heropos jest blisko costam, wtedy:

    def getheroypos():
        return int(ypos)
    def getheroxpos():
        return int(xpos)
    def getronxpos():
        return int(ronexadas.x)
    def getronypos():
        return int(ronexadas.y)

    for boss in enemies:
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
    if hero_health <= 0:
        changeSpriteImage(hero, 1)
        yspeed = 0
        lifestatus = False
        print('game over')
        showSprite(endscreen)
        break
    huddisplay()
    tick(60)
    updateDisplay()

endWait()
