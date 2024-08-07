import pygame
import pygame.mixer
from settings import *
from tile import Tile
from collectible import Collectible
from player import Player
from support import *
from random import choice

class Level():
    def __init__(self, screen):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.collectibles_sprites = pygame.sprite.Group()
        self.collectibles_stars = pygame.sprite.Group()
        self.collectibles_nebulae = pygame.sprite.Group()
        self.collectibles_bombs = pygame.sprite.Group()

        self.screen = screen

        self.create_map()

        self.music = pygame.mixer.Sound('assets/audio/firelink.wav')
        self.music.set_volume(0.1)
        self.music.play(-1)
        self.restart = False

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('assets/maps/positions/collisionmaze1_Collision.csv'),
            'grass': import_csv_layout('assets/maps/positions/collisionmaze1_Grass.csv'),
            'objects': import_csv_layout('assets/maps/positions/collisionmaze1_Objects.csv'),
            'collectibles': import_csv_layout('assets/maps/positions/collisionmaze1_Collectibles.csv'),
            'entities': import_csv_layout('assets/maps/positions/collisionmaze1_Entities.csv') 
        }
        graphics = {
            'grass': import_folder('assets/tiles/grass'),
            'objects': import_folder('assets/tiles/objects'),
            'collectibles': import_folder('assets/collectible/')
        }

        collectibles = {
            1: 'Nebulae',
            2: 'Stars',
            3: 'Bomb'
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                    
                        if style == 'boundary':
                            Tile((x,y), [self.collision_sprites], 'invisible')

                        if style == 'grass':
                            random_grass = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites], 'grass', random_grass)

                        if style == 'objects':
                            surface = graphics['objects'][int(col)-2]
                            Tile((x, y), [self.collision_sprites, self.visible_sprites], 'object', surface)

                        if style == 'collectibles':
                            surface = graphics['collectibles'][int(col)-1]
                            Collectible((x, y), [self.visible_sprites, self.collectibles_sprites], collectibles[int(col)], surface)
                        
                        if style == 'entities':
                            self.player = Player((x, y), [self.visible_sprites], self.collision_sprites, self.collectibles_sprites, self.screen)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update() 
        if self.player.restart == True:
            self.restart = True
            self.music.stop()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('assets/maps/maze1.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)



