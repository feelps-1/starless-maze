import pygame
from settings import *
from level import Level
import sys

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Starless Maze')
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.fonte = pygame.font.Font(None, 20)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        

            self.screen.fill('black')
            self.level.run()
            
            n_coletadas = 1
            self.escuro = pygame.image.load(f'./assets/maps/tocha{n_coletadas}.png').convert_alpha()
            self.screen.blit(self.escuro, (0,0))
            self.contador = self.fonte.render(f'Estrelas coletadas: {n_coletadas}', False, 'Yellow')
            self.screen.blit(self.contador, (0,0))
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()

    game.run()
