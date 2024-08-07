import pygame
import pygame.mixer
from settings import *
from hud import *
from support import *
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, collectibles_sprites, collectibles_stars, collectibles_nebulae, collectibles_bombs, screen):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/player/down/spr_playerdown0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -7)
        self.hitbox = self.rect.inflate(0, -7)

        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        self.colision_sprites = collision_sprites
        self.collectibles_sprites = collectibles_sprites
        self.collectibles_stars = collectibles_stars
        self.collectibles_nebulae = collectibles_nebulae
        self.collectibles_bombs = collectibles_bombs
        self.screen = screen
        self.restart = False

        self.import_player_assets()
        self.state = 'down'
        self.frame_index = 0
        self.animation_speed = 0.12

        self.health= 5
        self.stars = 0
        self.nebulae = 0

        self.healthcounter = Counter('Health', self.health, 5, self.screen, (20, 25), COUNTER_BACKGROUND, (255, 0, 0))
        self.starscounter = Counter('Stars', self.stars, 3, self.screen, (190, 25), COUNTER_BACKGROUND, (255, 243, 70))
        self.nebulaecounter = Counter('Nebulae', self.nebulae, 3,self.screen, (360, 70), COUNTER_BACKGROUND, (132, 0, 200))

    def import_player_assets(self):
        character_path = './assets/player/'

        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}
        
        for animation in self.animations.keys():
            full_path = character_path+animation
            self.animations[animation] = import_folder(full_path)
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.state = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.state = 'down'
        else: 
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.state = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.state = 'left'
        else:
            self.direction.x = 0

    def get_state(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.state:
                self.state = self.state + '_idle'
    
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
                if collectibles in self.collectibles_stars:
                    self.collectibles_sprites.remove(collectibles)
                    collectibles.kill()
                    self.stars += 1
                    pygame.mixer.music.load('assets/audio/ds_item.wav')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(1)
                elif collectibles in self.collectibles_nebulae:
                    self.collectibles_sprites.remove(collectibles)
                    collectibles.kill()
                    if 3 > self.nebulae:
                        self.nebulae += 1
                    if 5 > self.health:
                        self.health += 1
                    pygame.mixer.music.load('assets/audio/ds_item.wav')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(1)
                elif collectibles in self.collectibles_bombs:
                    self.collectibles_sprites.remove(collectibles)
                    collectibles.kill()
                    self.health -= 1
                    pygame.mixer.music.load('assets/audio/bomba.wav')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(1)         

    def animate(self):
        animation = self.animations[self.state]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def dark(self, stars):
        if stars < 3:
            self.escuro = pygame.image.load(f'./assets/maps/tocha{stars}.png').convert_alpha()
            self.escuro = pygame.transform.scale(self.escuro, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(self.escuro, (0,0))
        else: 
            pass

    def game_over_screen(self):
        font = pygame.font.Font("assets/menu/d_font.ttf", 36)
        text = font.render("Você morreu", True, (255, 0, 0))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()
        
        pygame.time.wait(2000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.restart = True

    def win_screen(self):
        font = pygame.font.Font("assets/menu/d_font.ttf", 36)
        text = font.render("Nix salva", True, (255, 255, 0))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()
        
        pygame.time.wait(2000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.restart = True

    def check_end(self):
        if self.health <= 0:
            self.game_over_screen()

        if self.nebulae == 3 and self.stars == 3:
            self.win_screen()
        
    def update(self):
        self.input()
        self.move(self.speed)
        self.collision(self.direction)
        self.dark(self.stars)
        self.get_state()
        self.animate()
        self.check_end()

        self.healthcounter.drawCounter('Health', self.health, 5, self.screen, (20, 25), COUNTER_BACKGROUND, (255, 0, 0))
        self.nebulaecounter.drawCounter('Nebulae', self.nebulae, 3,self.screen, (190, 25), COUNTER_BACKGROUND, (132, 0, 200))
        self.starscounter.drawCounter('Stars', self.stars, 3, self.screen, (360, 25), COUNTER_BACKGROUND, (255, 243, 70))
        
