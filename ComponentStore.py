import pygame
import Component


class ComponentStore:
    def __init__(self, screen: pygame.display, size, b_width, sprites: dict):
        self.screen = screen
        self.rect = pygame.Rect(size[0] - b_width, 0, size[0], size[1])
        self.font2 = pygame.font.SysFont('lucidaconsole', 20)
        self.bg_colour = (100, 100, 100)
        y_offset = 150
        # sprites' main images should be _0 as these are used for display
        # self.sprites = [sprite for sprite in sprites if sprite.endswith('_0')]
        print(sprites)
        self.sprites = {key[:-2]: value for (key, value) in sprites.items() if key.endswith('_0')}
        print(self.sprites)
        # point not rect rn
        self.areas = {name: pygame.Rect((self.rect.x, y_offset + i * 50), (b_width, 50)) for (i, name) in (enumerate(self.sprites.keys()))}
        print(self.areas)

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_colour, self.rect)
        for i, (name, sprite) in enumerate(self.sprites.items()):
            self.screen.blit(sprite, (self.rect.x, 155 + i*50))
            # print all names and cut off trailing "_0"
            self.screen.blit(self.font2.render(name, False, (0, 0, 0)),
                             (self.rect.x + sprite.get_width() + 10, 155 + i*50))
            pygame.draw.rect(self.screen, (255, 0, 0), self.areas[name], width=1)

    """Get first frame of all main components, as well as their target names"""
    def get_valid_components(self):
        pass

    """Checks mouse is in bounds of area"""
    def in_bounds(self, mpos):
        return self.rect.collidepoint(mpos)
        # TODO: make collision and scrolling capabilities

    def grab_component(self, mpos):
        for item in self.areas.items():
            if item[1].collidepoint(mpos):
                print(f'attr: {getattr(Component, item[0])}')
                return getattr(Component, item[0])


class SearchBar:
    pass

