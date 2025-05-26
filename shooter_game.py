from pygame import *
from random import randint
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_ufo = 'ufo.png'
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Space Shooter')
background = transform.scale(image.load(img_back), (win_width, win_height))


ship = Player(img_hero, 5, win_height-100, 80, 100, 10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()


for i in range(5):
    monster = Enemy(img_ufo, randint(0, win_width - 80), -40, 80, 80, randint(1,5))
    monsters.add(monster)
    asteroid = Asteroid('asteroid.png', randint(0, win_width - 80), -40, 80, 80, randint(1,5))
    asteroids.add(asteroid)

lost = 0
score = 0
font.init()
style = font.SysFont    (None, 36)
win = style.render('You Win!', True, (255, 255, 255))
lose = style.render('You Lose!', True, (100, 0, 0))
finish = False
run = True
life = 3
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                # fire_sound.play()

    if not finish:
        window.blit(background, (0, 0))

        text = style.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lost = style.render("Lost: " + str(lost), 1, (255,255,255)) 
        window.blit(text_lost, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = Enemy(img_ufo, randint(0, win_width - 80), -40, 80, 80, randint(1,5))
            monsters.add(monster)

            
        # collides_bullet_asteroid = sprite.groupcollide(bullets, asteroids, True, False)
        # for i in collides_bullet_asteroid:

        if sprite.spritecollide(ship, monsters, False) or lost > 2 or sprite.spritecollide(ship, asteroids, False):
            # window.blit(lose, (win_height/2, win_width/2))
            # finish = True
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if life == 0:
            window.blit(lose, (win_height/2, win_width/2))
            finish = True
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = style.render(str(life), 1, life_color)
        window.blit(text_life,(650, 10))

        if score >= 20:
            window.blit(win, (win_height/2, win_width/2))
            finish = True
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        display.update()

    time.delay(50)
