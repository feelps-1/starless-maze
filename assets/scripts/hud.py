import pygame
from settings import *

class Counter():
    def __init__(self, item, quantity, screen):
        self.item = item
        self.quantity = quantity
        self.screen = screen

    def drawCounter(self, item, quantity, maxitems, screen, position, innercolor, outercolor):
        self.maxitems = maxitems
        self.screen = screen
        self.position = position
        self.innercolor = innercolor
        self.outercolor = outercolor
        bar_width = COUNTER_WIDTH
        self.font = pygame.font.Font(None, 18)
        self.contador = self.font.render(f'{item}: {quantity}', False, 'White')
        self.screen.blit(self.contador, (self.position[0], self.position[1]-15))
        rect_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.score = pygame.draw.rect(rect_surface, self.innercolor, (0, 0, bar_width, 15))
        self.screen.blit(rect_surface, self.position)
        filling = (quantity / maxitems) * bar_width
        if quantity > maxitems:
            filling = bar_width
        self.score = pygame.draw.rect(rect_surface, self.outercolor, (0, 0, filling, 15))
        self.screen.blit(rect_surface, self.position)
        self.icon = pygame.image.load(f'../icons/{item}.png')
        self.screen.blit(self.icon, (self.position[0]-20, self.position[1]-10))

    def drawSimple(self, item, quantity ,screen, position):
        self.font = pygame.font.Font(None, 30)
        self.contador = self.font.render(f'{quantity}', False, 'White')
        self.screen.blit(self.contador, position)
        self.icon = pygame.image.load(f'../icons/{item}.png').convert_alpha()
        self.screen.blit(self.icon, (position[0]-35, position[1]-12))