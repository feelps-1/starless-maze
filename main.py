import pygame
import math
from settings import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Starless Maze')
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load('./assets/spr_bg.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = {
            'down': [pygame.transform.rotozoom(pygame.image.load(f"./assets/player/front/spr_playerfront{i}.png").convert_alpha(), 0, PLAYER_SCALE) for i in range(1, 6)],
            'up': [pygame.transform.rotozoom(pygame.image.load(f"./assets/player/up/spr_playerup{i}.png").convert_alpha(), 0, PLAYER_SCALE) for i in range(0, 5)],
            'left': [pygame.transform.rotozoom(pygame.image.load(f"./assets/player/left/spr_playerleft{i}.png").convert_alpha(), 0, PLAYER_SCALE) for i in range(1, 6)],
            'right': [pygame.transform.rotozoom(pygame.image.load(f"./assets/player/right/spr_playerright{i}.png").convert_alpha(), 0, PLAYER_SCALE) for i in range(0, 5)]
        }
        self.current_animation = 'down' 
        self.animation_frame = 0
        self.image = self.animations[self.current_animation][self.animation_frame]
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED
        self.last_update = pygame.time.get_ticks()
        self.moving = False

    def resize(self, scale_factor):
        self.image = pygame.transform.rotozoom(self.original_image, 0, scale_factor)

    def user_input(self, keys):
        self.velX = 0
        self.velY = 0

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.moving = True
        else:
            self.moving = False
            self.image = self.animations[self.current_animation][0]

        if keys[pygame.K_w]:
            self.velY = -PLAYER_SPEED
            self.current_animation = 'up'
        if keys[pygame.K_s]:
            self.velY = PLAYER_SPEED
            self.current_animation = 'down'
        if keys[pygame.K_d]:
            self.velX = PLAYER_SPEED
            self.current_animation = 'right'
        if keys[pygame.K_a]:
            self.velX = -PLAYER_SPEED
            self.current_animation = 'left'

        if self.velX != 0 and self.velY != 0:
            self.velX /= math.sqrt(2)
            self.velY /= math.sqrt(2)

    def animate(self):
        if self.moving:
            now = pygame.time.get_ticks()
            if now - self.last_update > ANIMATION_TIME * 1000:
                self.last_update = now
                self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.current_animation])
                self.image = self.animations[self.current_animation][self.animation_frame]


    def move(self):
        self.pos += pygame.math.Vector2(self.velX, self.velY)

    def update(self, keys):
        self.user_input(keys)
        self.animate()
        self.move()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./assets/tiles/spr_tilebrick.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player()


while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
 

    screen.blit(background, (0, 0))
    screen.blit(player.image, player.pos)
    player.update(keys)

    pygame.display.update()
    clock.tick(FPS)