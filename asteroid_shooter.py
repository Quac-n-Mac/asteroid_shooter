import pygame, math, random, time
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((900,900))
playing = True

bg = pygame.image.load("images/s_bg.png")
bg = pygame.transform.scale(bg, (900,900))

player_img = pygame.image.load("images/player.png")
a_big = pygame.image.load("images/a_big.png")
a_med = pygame.image.load("images/a_med.png")
a_small = pygame.image.load("images/a_small.png")
ufo = pygame.image.load("images/ufo.png")
star = pygame.image.load("images/star.png")

bang_large = pygame.mixer.Sound("images/bangLarge.wav")
bang_small = pygame.mixer.Sound("images/bangSmall.wav")
shoot = pygame.mixer.Sound("images/shoot.wav")

score = 0
gameover = False
lives = 3
rapidFire = False
rfStart = -1
isSoundOn = True
highScore = 0

class Player(object):
    def __init__(self):
        self.img = player_img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = 900//2
        self.y = 900//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x,self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine *self.h//2)
    def draw(self,screen):
        screen.blit(self.rotatedSurf, self.rotatedRect)
    def turnLeft(self):
        self.angle +=5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x,self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine *self.h//2)
    def turnRight(self):
        self.angle -=5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x,self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine *self.h//2)
    def moveForward(self):
        self.x += self.cosine*6
        self.y -= self.sine*6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x,self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine *self.h//2)
    def updateLoc(self):
        if self.x > 900:
            self.x = 0
        elif self.x <0:
            self.x = 900
        elif self.y >900:
            self.y = 0
        elif self.y <0:
            self.y = 900

player = Player()

class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h=4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c*10
        self.yv = self.s*10
    def move(self):
        self.x += self.xv
        self.y -= self.yv
    def draw(self, screen):
        pygame.draw.rect(screen, "red", [self.x, self.y, self.w, self.h])
    def offScreen(self):
        if self.x < -50 or self.x > 950 or self.y < -50 or self.y > 950:
            return True

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if rank ==1:
            self.image = a_small
        elif rank ==2:
            self.image = a_med
        else:
            self.image = a_big
        self.w = 50*rank
        self.h = 50*rank
        self.x, self.y = random.randint(50,850), random.randint(50,850)
        if self.x <450:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y <450:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir*random.randrange(1,3)
        self.yv = self.ydir*random.randrange(1,3)
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))

playerBullets=[]
asteroids = []
count = 0
stars =[]
aliens = []
alienBullets =[]
run = True
player = Player()

clock = pygame.time.Clock()

def char_draw():
    player.draw(screen)
    for a in asteroids:
        a.draw(screen)
    for b in playerBullets:
        b.draw(screen)
    if rapidFire:
        pygame.draw.rect(screen, (0, 0, 0), [sw//2 - 51, 19, 102, 22])
        pygame.draw.rect(screen, (255, 255, 255), [sw//2 - 50, 20, 100 - 100*(count - rfStart)/500, 20])

while playing:
    clock .tick(60)
    count +=1
    screen.blit(bg, (0,0))
    if gameover == False:
        if count % 100==0:
            asteroids.append(Asteroid(random.randint(1,3)))
    player.updateLoc()
    for a in asteroids:
        a.x += a.xv
        a.y += a.yv
        if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
            if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                asteroids.pop(asteroids.index(a))
        for p in playerBullets:
            if (a.x >= p.x - p.w//2 and a.x <= p.x + p.w//2) or (a.x + a.w <= p.x + p.w//2 and a.x + a.w >= p.x - p.w//2):
                if(a.y >= p.y - p.h//2 and a.y <= p.y + p.h//2) or (a.y  +a.h >= p.y - p.h//2 and a.y + a.h <= p.y + p.h//2):
                    playerBullets.pop(playerBullets.index(p))
                    asteroids.pop(asteroids.index(a))
    char_draw()
    for p in playerBullets:
        p.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.turnLeft()
    if keys[pygame.K_RIGHT]:
        player.turnRight()
    if keys[pygame.K_UP]:
        player.moveForward()
    if keys[pygame.K_SPACE]:
        playerBullets.append(Bullet())
    pygame.display.update()