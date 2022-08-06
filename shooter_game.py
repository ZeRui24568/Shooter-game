from pygame import*
from random import randint
mixer.init()
#mixer.music.load("")
#mixer.music.play ()

shoot_sound = mixer.Sound('fire.ogg')
font.init()
score = 0

life = 10
WIDTH = 700
HEIGHT = 500


img_back = 'galaxy.jpg'
img_hero = 'space_ship.png'

class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
    
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
    
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #method drawing the character on the window
    def draw(self,surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
		
        if keys[K_DOWN] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_UP] and self.rect.x < HEIGHT - 80:
            self.rect.y += self.speed
def fire():
    b = Bullet("ninjastar.png", ship.rect.centerx,ship.rect.centery,16,20,10)

    bullets.add(b)
    shoot_sound.play()
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:

            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH-self.rect.width)
class TextSprite(sprite.Sprite):
    def __init__(self,text,color,pos,Font_size):
        self.font = font.SysFont('Arial', Font_size)
        self.color = color
        self.pos = pos
        self.update_text(text)
        self.rect = self.image.get_rect()
    def update_text(self,new_text):
        self.image = self.font.render(new_text,True, self.color)
    def draw(self,surface):
        surface.blit(self.image,self.pos)

scoreboard = TextSprite(text = 'Score:0'  , color='white',pos=(40,40), Font_size=22)
lifeboard = TextSprite(text = 'Life:0'  , color='white',pos=(40,60), Font_size=22)


display.set_caption('shooting game')
window = display.set_mode((WIDTH,HEIGHT))
clock = time.Clock()

background = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))
win = transform.scale(image.load("win.png"), (WIDTH, HEIGHT))
loose = transform.scale(image.load("loose.png"), (WIDTH, HEIGHT))
bullets = sprite.Group()
ship = Player(img_hero, 5, HEIGHT - 100, 80 , 100 , 10)
finish = False
run = True

enemies = sprite.Group()
for _ in range(5):
    e1 = Enemy("ufo.png", randint(0, WIDTH-30), -60, 60, 60, randint(3, 7))
    enemies.add(e1)

 
while run:
    for ev in event.get():
        if ev.type == QUIT:
            run = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE and finish == False:    
                fire()
            elif ev.key == K_r and finish == True:
                score = 0
                life = 10
                finish = False
                enemies.empty()
                bullets.empty()
                for _ in range(5):
                    e1 = Enemy("ufo.png", randint(0, WIDTH-30), -60, 60, 60, randint(3, 7))
                    enemies.add(e1)

    if not finish:

        window.blit(background, (0,0))
        ship.update()
        enemies.update()
        bullets.update()


        ship.draw(window)
        scoreboard.draw(window)
        lifeboard.draw(window)

        hits = sprite.groupcollide(bullets,enemies,False,True)
        for hit in hits:
            e1 = Enemy("ufo.png", randint(0, WIDTH-30), -60, 60, 60, randint(3, 7))
            enemies.add(e1)
            score +=1
            scoreboard.update_text("Score"+str(score))

        shiphits = sprite.spritecollide(ship,enemies,True)
        for hit in shiphits:
            e1 = Enemy("ufo.png", randint(0, WIDTH-30), -60, 60, 60, randint(3, 7))
            enemies.add(e1)
            life -=1
            lifeboard.update_text("Life"+str(life))

        if score >= 150:
            finish = True
        if life <= 0:
            finish = True

        bullets.draw(window)
        
        enemies.draw(window)

    else:
        if score >= 150:
            window.blit(win,(0,0))
        if life <=0:
            window.blit(loose,(0,0))

    display.update()
    clock.tick(60)

