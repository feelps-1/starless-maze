import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, collectibles_sprites, screen):
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
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else: 
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
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
    

    def dark(self, stars):
        self.escuro = pygame.image.load(f'./assets/maps/tocha{stars}.png').convert_alpha()
        self.escuro = pygame.transform.scale(self.escuro, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(self.escuro, (0,0))

    def count_stars(self, stars):
        max_stars = 2
        bar_width = 100
        #Titulo do coletável
        self.fonte = pygame.font.Font(None, 20)
        self.contador = self.fonte.render(f'ESTRELAS: {stars}', False, 'White')
        self.screen.blit(self.contador, (20, 10))
        #Barra interior, que representa o vazio
        rect_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        rect_position = (20, 25)
        rect_color = (255, 255, 255) #White
        self.score = pygame.draw.rect(rect_surface, rect_color, (0, 0, bar_width, 20))
        self.screen.blit(rect_surface, rect_position)
        #Barra exterior, que representa a quantidade
        filling = (stars / max_stars) * bar_width
        if stars > 2:
            filling = bar_width
        rect_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        rect_position = (20, 25)
        rect_color = (0, 0, 255) #Blue
        self.score = pygame.draw.rect(rect_surface, rect_color, (0, 0, filling, 20))
        self.screen.blit(rect_surface, rect_position)

    def count_nebula(self,stars):
        max_nebulae = 2
        bar_width = 100
        #Titulo do coletável
        self.fonte = pygame.font.Font(None, 20)
        self.contador = self.fonte.render(f'NEBULOSAS: {stars}', False, 'White')
        self.screen.blit(self.contador, (190,10))
        #Barra interior, que representa o vazio
        rect_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        rect_position = (190, 25)
        rect_color = (255, 255, 255) #White
        self.score = pygame.draw.rect(rect_surface, rect_color, (0, 0, bar_width, 20))
        self.screen.blit(rect_surface, rect_position)
        #Barra exterior, que representa a quantidade
        filling = (stars / max_nebulae) * bar_width
        if stars > 2:
            filling = bar_width
        rect_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        rect_position = (190, 25)
        rect_color = (75, 0, 130) #Indigo
        self.score = pygame.draw.rect(rect_surface, rect_color, (0, 0, filling, 20))
        self.screen.blit(rect_surface, rect_position)

    def count_life(self, stars):
        max_life = 5
        bar_width = 100
        #Titulo do coletável
        self.fonte = pygame.font.Font(None, 20)
        self.contador = self.fonte.render(f'VIDA: {max_life - stars}', False, 'White')
        self.screen.blit(self.contador, (360,10))
        #Barra interior, que representa a perda de vida
        rect_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        rect_position = (360, 25)
        rect_color = (255, 255, 255) #White
        self.score = pygame.draw.rect(rect_surface, rect_color, (0, 0, bar_width, 20))
        self.screen.blit(rect_surface, rect_position)
        #Barra exterior, que representa a perda de vida
        filling = ((max_life - stars )/max_life) * bar_width
        rect_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        rect_position = (360, 25)
        rect_color = (0, 100, 0) #Dark Green
        self.score = pygame.draw.rect(rect_surface, rect_color, (0, 0, filling, 20))
        self.screen.blit(rect_surface, rect_position)
            
    def update(self):
        self.input()
        self.move(self.speed)
        self.collision(self.direction)
        self.dark(self.stars)
        self.count_stars(self.stars)
        self.count_nebula(self.stars)
        self.count_life(self.stars)

