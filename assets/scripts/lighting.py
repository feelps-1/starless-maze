import pygame

class Lighting:
    def __init__(self, surface):
        self.surface = surface
        self.darkness = pygame.Surface(self.surface.get_size()).convert_alpha()
        self.darkness.fill((0, 0, 0, 220))  # Aumenta a opacidade para um efeito mais forte

        self.light_radius = 150
        self.light_surface = pygame.Surface((self.light_radius * 2, self.light_radius * 2)).convert_alpha()
        self.light_surface.fill((0, 0, 0, 0))  # Torna a superfície completamente transparente
        pygame.draw.circle(self.light_surface, (0, 0, 0, 0), (self.light_radius, self.light_radius), self.light_radius)
        for i in range(self.light_radius, 0, -1):
            alpha = (self.light_radius - i) * 255 // self.light_radius
            pygame.draw.circle(self.light_surface, (0, 0, 0, alpha), (self.light_radius, self.light_radius), i)

    def apply_lighting(self, light_position):
        self.surface.blit(self.darkness, (0, 0))
        light_rect = self.light_surface.get_rect(topleft=light_position)
        self.surface.blit(self.light_surface, light_rect, special_flags=pygame.BLEND_RGBA_SUB)

