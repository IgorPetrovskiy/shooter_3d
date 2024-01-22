import pygame
import sys
import random

from pygame import *

pygame.init()

WIDTH, HEIGHT = 1400, 900
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pause_font = pygame.font.Font(None, 50)
pause_menu = pygame.Surface((300, 200))
pause_menu.fill((100, 100, 100))
pygame.draw.rect(pause_menu, (255, 255, 255), (50, 50, 200, 50))  # Resume button
pygame.draw.rect(pause_menu, (255, 255, 255), (50, 120, 200, 50))  # Exit button
resume_text = pause_font.render('Resume', True, (0, 0, 0))
exit_text = pause_font.render('Exit', True, (0, 0, 0))
pause_menu.blit(resume_text, (120 - resume_text.get_width() // 2, 65))
pause_menu.blit(exit_text, (120 - exit_text.get_width() // 2, 135))


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
            self.direction = "left"
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.image = self.images['right']
            self.direction = "right"
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.image = self.images['up']
            self.direction = "up"
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.image = self.images['down']
            self.direction = "down"
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
        self.rect.x = random.randint(200, WIDTH - 50)
        self.rect.y = random.randint(200, HEIGHT - 50)
        self.speed_x = random.choice([-1, 1])
        self.speed_y = random.choice([-1, 1])

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
    def __init__(self, plaeyer):
        super().__init__()
        self.images = {
            'up': pygame.transform.scale(pygame.image.load('bullets.png'), (15, 50)),
            'down': pygame.transform.scale(pygame.image.load('bullet_d.png'), (15, 50)),
            'left': pygame.transform.scale(pygame.image.load('bullet_l.png'), (50, 15)),
            'right': pygame.transform.scale(pygame.image.load('bullet_r.png'), (50, 15))
        }
        self.image = pygame.transform.scale(pygame.image.load('bullets.png'), (15, 50))  #
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.speed = 20
        self.direction = player.direction
        self.move = ""

    def update(self):
        if self.direction == 'up':
            self.move = "up"
            self.image = self.images['up']

        if self.direction == 'down':
            self.move = "down"
            self.image = self.images['down']

        if self.direction == 'left':
            self.move = "left"
            self.image = self.images['left']

        if self.direction == 'right':
            self.move = "right"
            self.image = self.images['right']

        if self.move == "up":
            self.rect.y -= self.speed
        if self.move == "down":
            self.rect.y += self.speed
        if self.move == "left":
            self.rect.x -= self.speed
        if self.move == "right":
            self.rect.x += self.speed

        if self.rect.y < 0 or self.rect.y > HEIGHT - 50 or self.rect.x < 0 or self.rect.x > WIDTH - 15:
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
class Background(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()

pygame.display.set_caption("2D Шутер")

all_sprites = pygame.sprite.Group()

background = Background('D:\shooter_2d\lock_floor.jpg')
background.image = pygame.transform.scale(background.image, (WIDTH, HEIGHT))
background.rect = background.image.get_rect()
all_sprites.add(background)

enemies = pygame.sprite.Group()
walls = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
pygame.mixer.init()
pygame.mixer.music.load('dark_souls_22. Gwyn, Lord of Cinder.mp3')
pygame.mixer.music.play(-1)
fire = pygame.mixer.Sound('fire.mp3')
fire.set_volume(0.1)
hit = pygame.mixer.Sound('hits.mp3')
for i in range(3):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

clock = pygame.time.Clock()
running = True
finish = False
keys = pygame.key.get_pressed()
pygame.font.init()
font = pygame.font.Font(None, 50)


def pause_game():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = ev.pos
                x -= WIDTH // 2 - 150
                y -= HEIGHT // 2 - 100
                if 50 <= x <= 250 and 50 <= y <= 100:
                    return
                elif 50 <= x <= 250 and 120 <= y <= 170:
                    pygame.quit()
                    sys.exit()

        screen.blit(pause_menu, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        pygame.display.update()
        clock.tick(60)


def start_game():
    start1 = font.render('All time when you kill all enemy', True, (255, 255, 255))
    start2 = font.render('in next time he was respawn and there will be more of them.', True, (255, 255, 255))
    start3 = font.render('Type on Q to start', True, (255, 255, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
            if event.type == pygame.QUIT:
                exit()
        screen.blit(start1, (50, 200))
        screen.blit(start2, (50, 250))
        screen.blit(start3, (50, 300))
        pygame.display.update()


a = 3


def reset_game():
    global enemyset
    enemyset = 3
    for b in bullets:
        b.kill()
    for e in enemies:
        e.kill()
    for i in all_sprites:
        i.kill()
    time.delay(1000)
    for i in range(3):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    player.rect.center = (WIDTH // 2, HEIGHT - 50)
    all_sprites.add(player)


enemyset = 3
an = 0
while running:
    if an == 0:
        start_game()
        an = 1
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_e:
                fire.play()
                bullet = Bullet(player)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif ev.key == pygame.K_ESCAPE:
                pause_game()
    if not finish:
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
            finish = True
        hits_enemy_with_bullets = pygame.sprite.groupcollide(bullets, enemies, False, True)
        if hits_enemy_with_bullets:
            enemyset -= 1
            hit.play()
        if enemyset <= 0:
            finish = True
            reset_game()
        screen.fill((0, 0, 0))

        all_sprites.draw(screen)
    else:
        finish = False
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()
        for i in all_sprites:
            i.kill()
        time.delay(1000)
        all_sprites.add(background)
        for i in range(3):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        player = Player()
        all_sprites.add(player)

    display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
