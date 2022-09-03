import pygame


class BaseComponent:
    def __init__(self, x, y, screen: pygame.display, sprites, target):
        self.x = x
        self.y = y
        self.image = None
        self.screen = screen
        self.bidirectional = True  # default behaviour
        self.connections = []
        self.dragging = False
        self.offset = [0, 0]
        self.selected = False
        self.rect = pygame.Rect((0, 0, 0, 0))  # Base has no proper rect
        self.sprites = self.load_sprites(sprites, target)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        if not self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 1)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), self.rect, 1)

    def load_sprites(self, sprites: dict, target: str):  # will probs mis-order if more that 10 unless hex
        self.sprites = [sprites[i] for i in sprites if i.startswith(target)]  # don't ask lol it works
        return self.sprites

        # refactor to make it only trigger on events instead of all the time
    def drag(self):
        if self.dragging:
            pos = pygame.mouse.get_pos()
            self.x = pos[0] - self.offset[0]
            self.y = pos[1] - self.offset[1]  # maybe constant update for bb idk
            self._bb()  # update bb only when acc dragging

    def drag_set(self):
        self.dragging = True
        self.selected = True
        pos = pygame.mouse.get_pos()
        self.offset = [pos[0] - self.x, pos[1] - self.y]

    def drag_release(self):
        self.dragging = False
        self._bb()

    def touched(self, mpos):
        return self.rect.collidepoint(mpos)

    def _bb(self):
        """Re-grab bounding box"""
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        return self.rect


class ResistorStandard(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'ResistorStandard'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        # refactor to make container reference, let container handle sprites
        self.image = self.sprites[0]  # only has one image
        #self.image = pygame.transform.scale(self.image, (68, 20))
        # self.image = pygame.transform.scale(self.image, [i * 4 for i in self.image.get_size()])
        # scale factr 4

        self.rect = self._bb()



