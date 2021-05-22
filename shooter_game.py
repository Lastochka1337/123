import pygame
from pygame import *
from random import randint
import time

pygame.init()

window = display.set_mode((700, 500))

display.set_caption('Поняшки')

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

FPS = 100

class GameSprite(sprite.Sprite):  
    def __init__(self, player_image, player_x, player_y, player_speed,width,height):
        super().__init__()
        self.w = width
        self.h = height
        self.image = transform.scale(image.load(player_image), (self.w, self.h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_d] and self.rect.x <= 620:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed
    def fire(self):
        firem.play()
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10,15,15)
        bullets.add(bullet)

lives = 3
lost = 0
kills = 0
num_b = 0
reload_on = False
ka = 0
i = 0

class Enemie(GameSprite):
    def update(self):
        global lost
        global i
        self.rect.y += speed
        
        if self.rect.y >= 500:
            lost += 1
            i -= 1
            self.rect.y = ycor
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        global ka
        self.rect.y += self.speed
        if self.rect.y >= 500:
            ka -= 1
            self.rect.y = ycor
            self.kill()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

mixer.init()
mixer.music.load("space.ogg")
firem = mixer.Sound('fire.ogg')
mixer.music.play()

a = 420

rocketa = Player("rocket.png", 350, a, 5,65,65)

lose_game = False
win_game = False
run = True
while run:
    check_time = time.time()
    key_pressed = key.get_pressed()
    myfont = font.SysFont("Arial", 30)
    myfont3 = font.SysFont("Arial", 60)
    kill_l = myfont.render("Счёт:" + str(kills), 1, (255, 255, 255))
    label = myfont.render("Пропущенно:" + str(lost), 1, (255, 255, 255))
    lives_label = myfont3.render(str(lives), 1, (255, 15, 87))
    reload_label = myfont.render("Перезарядка..." ,1, (255, 0, 0))
    myfont1 = font.SysFont("Arial", 100)
    label1 = myfont1.render("You lose!!", 1, (255, 0, 0))
    label2 = myfont1.render("You win!!", 1, (255, 191, 28))
    window.blit(background, (0, 0))
    rocketa.reset()
    window.blit(lives_label,(670,0))
    window.blit(kill_l,(0,0))
    window.blit(label,(0,30))
    while i != 5:
        ycor = randint(-50,0)
        xcor = randint(80, 620)
        speed = randint(1,2) 
        monster = Enemie('ufo.png', xcor, ycor,speed,65,65)
        monsters.add(monster)
        i += 1
    
    while ka != 3:
        ycor = randint(-100,0)
        xcor = randint(80,620)
        speed = randint(2,3)
        asteroid = Asteroid('asteroid.png', xcor,ycor,speed,65,65)
        asteroids.add(asteroid)
        ka +=1

    rocketa.update()
    bullets.draw(window)
    monsters.draw(window)
    asteroids.draw(window)

    if sprite.groupcollide(monsters,bullets,True,True):
        i-=1
        kills+=1
    
    if sprite.spritecollide(rocketa,monsters,True) or sprite.spritecollide(rocketa,asteroids,True):
        lives -=1
        ka -= 1
    if sprite.groupcollide(monsters,asteroids,True,False):
        i -= 1
    if sprite.groupcollide(bullets,asteroids,True,False):
        pass

    if key_pressed[K_SPACE] and reload_on == False:
        num_b +=1
        rocketa.fire()
        if num_b == 5:
            reload_on = True
            start_time = time.time()
            end_time = int(start_time) + 3

    for u in bullets:
        u.update()

    if reload_on == True:
        window.blit(reload_label,(300,450))
        if check_time >= end_time:
            num_b = 0
            reload_on = False

    for o in asteroids:
        o.update()

    for m in monsters:
        m.update()

    for e in event.get():
        if e.type == QUIT:
            run = False

    if lost == 10 or lives == 0:
        lose_game=True

    while lose_game:
        window.blit(label1, (200, 250))
        for e in event.get():
            if e.type == QUIT:
                lose_game = False
                run = False
            key_pressed = key.get_pressed()
            if key_pressed[K_SPACE]:
                kills = 0
                lost = 0
                i = 0
                run = True
                lose_game = False
        display.update()

    if kills == 5:
        win_game=True

    while win_game:
        window.blit(label2, (200, 250))
        for e in event.get():
            if e.type == QUIT:
                win_game = False
                run = False
            key_pressed = key.get_pressed()
            if key_pressed[K_SPACE]:
                kills = 0
                lost = 0
                i = 0
                run = True
                win_game = False
        display.update()

    display.update()
