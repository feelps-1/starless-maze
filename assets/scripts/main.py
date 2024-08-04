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

    def show_intro(self):
        intro_text = "Starless Maze"
        
        background_image = pygame.image.load('assets/menu/spr_bg.png').convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        font = pygame.font.Font('assets/menu/d_font.ttf', 24)  
        
        self.screen.blit(background_image, (0, 0))
        text_surface = font.render(intro_text, True, 'black')
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text_surface, text_rect)
        
        pygame.display.update()
        pygame.time.wait(5000)

    def show_story(self):
        story_text = ("Agora, ó herói, toda a esperança do mundo recai sobre vossos ombros, "
                      "até mesmo dos deuses imortais. Deveis desafiar o Starless Maze, "
                      "onde a escuridão habita densamente e com grande poder. Quebrai as prisões, "
                      "buscai as essências da Noite e fazei Nix voltar à sanidade, "
                      "devolvendo-lhe seus poderes e o mundo será salvo do escuro sem fim.")
        
        background_image = pygame.image.load('assets/menu/background2.jpg').convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        font = pygame.font.Font('assets/menu/d_font.ttf', 12)
        
        self.screen.blit(background_image, (0, 0))
        
        lines = story_text.split('. ')
        y_offset = 50
        line_height = 30
        
        for line in lines:
            words = line.split(' ')
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                text_surface = font.render(test_line, True, 'grey')
                if text_surface.get_width() > SCREEN_WIDTH - 40:
                    text_surface = font.render(current_line, True, 'grey')
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
                    self.screen.blit(text_surface, text_rect)
                    y_offset += line_height
                    current_line = word
                else:
                    current_line = test_line
            text_surface = font.render(current_line, True, 'grey')
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += line_height
        
        pygame.display.update()
        pygame.time.wait(20000)

    def run(self):
        self.show_intro()
        while True:
            action = self.menu.run()
            if action == 'start_game':
                self.show_story()
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

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()