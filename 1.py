import pygame, sys, random, time
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, RED)

background = pygame.image.load("road1.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
car_image = pygame.image.load("ya1.png")
car_image = pygame.transform.scale(car_image, (40, 80))
enemy_image = pygame.image.load("vstrechka1.png")
enemy_image = pygame.transform.scale(enemy_image, (40, 80))
coin_square = pygame.Surface((40, 30))
coin_square.fill(YELLOW)
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(5, WIDTH - 5), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 0
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_square
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(5, WIDTH - 5), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(20, WIDTH - 20), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

coins = pygame.sprite.Group()

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, YELLOW)
    DISPLAYSURF.blit(scores, (10, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)

        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if random.randint(0, 2000) < 10:
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)

    for coin in coins:
        DISPLAYSURF.blit(coin.image, coin.rect)
        coin.move()

    if pygame.sprite.spritecollideany(P1, coins):
       #pygame.mixer.Sound('coin_collect.mp3').play()
        SCORE += 10
        coin.kill()

    pygame.display.update()
    FramePerSec.tick(FPS)
