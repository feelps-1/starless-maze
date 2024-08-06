import pygame
import sys
from settings import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        
        self.font = pygame.font.Font('assets/menu/d_font.ttf', 12)  
        self.options = ["Iniciar Jogo", "Sair"]
        self.selected_option = 0
        
        self.background_image = pygame.image.load('assets/menu/background.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.arrow_image = pygame.image.load('assets/menu/seta.png').convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (30, 30))

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        
        for idx, option in enumerate(self.options):
            color = 'grey' if idx == self.selected_option else 'grey'
            
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + idx * 60))
            self.screen.blit(text, rect)
            
            if idx == self.selected_option:
                
                if idx == 0:
                    arrow_x = SCREEN_WIDTH / 2 - 100
                else:
                    arrow_x = SCREEN_WIDTH / 2 - 50  
                arrow_rect = self.arrow_image.get_rect(center=(arrow_x, SCREEN_HEIGHT / 2 + idx * 60))
                self.screen.blit(self.arrow_image, arrow_rect)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:  
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    if event.key == pygame.K_s:  
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    if event.key == pygame.K_RETURN or event.key == pygame.K_d: 
                        if self.selected_option == 0:
                            return 'start_game'
                        if self.selected_option == 1:
                            pygame.quit()
                            sys.exit()
            
            self.draw()
            self.clock.tick(FPS)

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
        pygame.time.wait(2500)

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
        pygame.time.wait(10000)