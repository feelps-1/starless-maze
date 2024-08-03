import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, collectibles_sprites, screen, controller):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/player/front/spr_playerfront1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -7)

        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        self.colision_sprites = collision_sprites
        self.collectibles_sprites = collectibles_sprites
        self.screen = screen

        self.stars = 0
        self.controller = controller
        
    def input(self, controller):
        controls = {
            1: [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a],
            2: [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT],
        }


        keys = pygame.key.get_pressed()

        if keys[controls[controller][0]]:
            self.direction.y = -1
        elif keys[controls[controller][1]]:
            self.direction.y = 1
        else: 
            self.direction.y = 0

        if keys[controls[controller][2]]:
            self.direction.x = 1
        elif keys[controls[controller][3]]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.colision_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left

                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.colision_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        
        for collectibles in self.collectibles_sprites:
            if collectibles.hitbox.colliderect(self.hitbox):
                self.collectibles_sprites.remove(collectibles)
                collectibles.kill()
                self.stars += 1

    def count(self, stars):
        self.fonte = pygame.font.Font(None, 20)
        self.contador = self.fonte.render(f'Estrelas coletadas: {stars}', False, 'Yellow')
        self.screen.blit(self.contador, (0,0))

    def dark(self, stars):
        self.escuro = pygame.image.load(f'./assets/maps/tocha{stars}.png').convert_alpha()
        self.escuro = pygame.transform.scale(self.escuro, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(self.escuro, (0,0))
            
    def update(self):
        self.input(self.controller)
        self.move(self.speed)
        self.collision(self.direction)
        self.count(self.stars)
        self.dark(self.stars)
        
