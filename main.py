import pygame
import sys
import random

from pygame import display, Surface

pygame.init()

WIDTH, HEIGHT = 1400, 900
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            'up': pygame.image.load('up.png').convert(),
            'down': pygame.image.load('dw.png').convert(),
            'left': pygame.image.load('l.png').convert(),
            'right': pygame.image.load('rt.png').convert()
        }

        self.image = self.images['up']
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5
        self.direction = "up"
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.image = self.images['left']
            self.direction = 'left'
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.image = self.images['right']
            self.direction = 'right'
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.image = self.images['up']
            self.direction = 'up'
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.image = self.images['down']
            self.direction = 'down'
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            'up': pygame.image.load('IMG_4350-removebg-preview.png').convert(),
            'down': pygame.image.load('en_down.png').convert(),
            'left': pygame.image.load('en_left.png').convert(),
            'right': pygame.image.load('IMG_4351-removebg-preview.png').convert()
        }

        self.image = self.images['up']
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(0, HEIGHT - 50)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x = -self.speed_x
            self.image = self.images['left'] if self.speed_x < 0 else self.images['right']
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y = -self.speed_y
            self.image = self.images['up'] if self.speed_y < 0 else self.images['down']

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('bullets.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.speed = 20
        self.direction = player.direction
        self.move = ''
    def update(self):
        if self.direction == 'up':
            self.move = 'up'
        if self.direction == 'down':
            self.move = 'down'
        if self.direction == 'left':
            self.move = 'left'
        if self.direction == 'right':
            self.move = 'right'
        if self.move == 'up':
            self.rect.y -= self.speed
        if self.move == 'down':
            self.rect.y += self.speed
        if self.move == 'left':
            self.rect.x -= self.speed
        if self.move == 'right':
            self.rect.x += self.speed
        if self.rect.y < 0 or self.rect.y < HEIGHT - 50 or self.rect.x < 0 or self.rect.x > WIDTH - 50:
            self.kill()
class Wall(pygame.sprite.Sprite):
    def __init__(self, color_r, color_g, color_b, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_r, color_g, color_b))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Шутер")

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
walls = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(1):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

wall1 = Wall(154, 205, 50, 100, 210, 300, 100)
wall2 = Wall(154, 205, 50, 100, 450, 300, 110)
wall3 = Wall(154, 205, 50, 100, 210, 110, 300)
wall4 = Wall(154, 205, 50, 200, 150, 110, 300)
wall5 = Wall(154, 205, 50, 300, 20, 110, 300)
wall6 = Wall(154, 205, 50, 400, 150, 110, 300)
wall7 = Wall(154, 205, 50, 500, 150, 110, 300)
wall8 = Wall(154, 205, 50, 200, 210, 300, 110)
wall9 = Wall(154, 205, 50, 200, 450, 300, 110)
all_sprites.add(wall1, wall2)
walls.add(wall1, wall2)


clock = pygame.time.Clock()
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_e:
                bullet = Bullet(player)
                all_sprites.add(bullet)
                bullets.add(bullet)
    all_sprites.update()

    hits_player_walls = pygame.sprite.spritecollide(player, walls, False)
    if hits_player_walls:
        player.rect.x = player.rect.x - player.speed
        player.rect.y = player.rect.y - player.speed

    hits_enemies_walls = pygame.sprite.groupcollide(enemies, walls, False, False)
    for enemy in hits_enemies_walls:
        enemy.speed_x = -enemy.speed_x
        enemy.speed_y = -enemy.speed_y

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
