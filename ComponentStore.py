import pygame


class ComponentStore:
    def __init__(self, screen: pygame.display, size, b_width, sprites: dict):
        self.screen = screen
        self.rect = pygame.Rect(size[0] - b_width, 0, size[0], size[1])
        self.font2 = pygame.font.SysFont('lucidaconsole', 20)
        self.bg_colour = (100, 100, 100)
        # sprites' main images should be _0 as these are used for display
        # self.sprites = [sprite for sprite in sprites if sprite.endswith('_0')]
        print(sprites)
        self.sprites = {key: value for (key, value) in sprites.items() if key.endswith('_0')}
        print(self.sprites)

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_colour, self.rect)
        for i, (name, sprite) in enumerate(self.sprites.items()):
            self.screen.blit(sprite, (self.rect.x, 150 + i*50))
            # print all names and cut off trailing "_0"
            self.screen.blit(self.font2.render(name[:-2], False, (0, 0, 0)),
                             (self.rect.x + sprite.get_width() + 10, 150 + i*50))

    """Get first frame of all main components, as well as their target names"""
    def get_valid_components(self):
        pass

    """Check each component for selection"""
    def collide(self):
        pass
        # TODO: make collision and scrolling capabilities


class SearchBar:
    pass

