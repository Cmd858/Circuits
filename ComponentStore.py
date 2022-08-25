import pygame
import os


class ComponentStore:
    def __init__(self, screen, size, b_width):
        self.screen = screen
        ## rect is no longer pygame.Rect, refactor
        self.rect = pygame.Rect(size[0] - b_width, 0, size[0], size[1])
        self.bg_colour = (100, 100, 100)

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_colour, self.rect)

    """Get first frame of all main components, as well as their target names"""
    def get_valid_components(self):
        pass




class SearchBar:
    pass

