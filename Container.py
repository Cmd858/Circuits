from Component import *
import os

class Container:
    def __init__(self, components: [BaseComponent] = None):
        self.components = components if components is not None else []
        self.dragging = False
        self.offx = 0
        self.offy = 0
        self.sprites = {}

    def tick(self):
        for component in self.components:
            component.draw()
            #component.select()
            component.drag()

    def drag_set(self):
        for component in self.components:
            if component.selected:
                component.drag_set()

    def deselect_all(self):
        for component in self.components:
            component.selected = False

    """Puts all sprite images into dict and scales them to hardcoded factor"""
    @staticmethod
    def get_sprites():  # using underscores in names to separate name from frame
        sprites = {}

        for path in os.listdir('Images/'):  # have fun refactoring this for proper logic
            if path.endswith('.png'):  # will not work with more than one frame lmao
                sprites[path[:path.rindex('.')]] = pygame.image.load(f'Images/{path}').convert_alpha()
        for key, sprite in sprites.items():
            sprites[key] = pygame.transform.scale(sprite, [i * 4 for i in sprite.get_size()])
        return sprites

