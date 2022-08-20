import pygame


class BaseComponent:
    def __init__(self, x, y, screen: pygame.display):
        self.x = x
        self.y = y
        self.screen = screen
        self.bidirectional = True  # default behaviour
        self.connections = []
        self.dragging = False
        self.offset = [0, 0]
        self.selected = False
        self.rect = pygame.Rect((0, 0, 0, 0))  # Base has no proper rect


class ResistorStandard(BaseComponent):
    def __init__(self, x, y, screen: pygame.display):
        super().__init__(x, y, screen)
        self.image = pygame.image.load('Images/ResistorStandard.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (68, 20))
        self.rect = self._bb()

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        if not self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 1)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), self.rect, 1)

        # make image cropper for lazy auto-crop via lines of alpha values

    # refactor to make it only trigger on events instead of all the time
    def drag(self):
        if self.dragging:
            pos = pygame.mouse.get_pos()
            self.x = pos[0] - self.offset[0]
            self.y = pos[1] - self.offset[1]  # maybe constant update for bb idk

    def drag_set(self):
        self.dragging = True
        pos = pygame.mouse.get_pos()
        self.offset = [pos[0] - self.x, pos[1] - self.y]

    def drag_release(self):
        pass

    def touched(self, mpos):
        return self.rect.collidepoint(mpos)

    def _bb(self):
        """Re-grab bounding box"""
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        return self.rect
