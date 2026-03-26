import pygame, math, random, time
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((900,900))
playing = True

bg = pygame.image.load("images/s_bg.png")

player = pygame.image.load("images/player.png")
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
        self.img = player
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
        self.y += self.yv
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


clock = pygame.time.Clock()

while playing:
    clock .tick(60)
    screen.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
    pygame.display.update()