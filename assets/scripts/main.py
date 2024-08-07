import pygame
from settings import *
from level import Level
from menu import Menu
import sys

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Starless Maze')
        self.clock = pygame.time.Clock()
        self.menu = Menu(self)
        self.level = None

    def run(self):
        self.menu.show_intro()
        while True:
            action = self.menu.run()
            if action == 'start_game':
                self.menu.show_story()
                self.start_game()

    def start_game(self):
        self.level = Level(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()

            if self.level.restart == True:
                self.run()
                return

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()