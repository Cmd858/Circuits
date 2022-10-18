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
        # wire boxes stored as top left relative to sprite
        self.wire_boxes = []
        self.cid = None
        self.font = pygame.font.SysFont('lucidaconsole', 30)

        self.resistance = 10

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        if not self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 1)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), self.rect, 1)
        for wire_box in self.wire_boxes:
            pygame.draw.rect(self.screen, (200, 200, 0), (self.x + wire_box[0], self.y + wire_box[1], 10, 10), 1)
        self.screen.blit(self.font.render(f'{self.resistance}', False, (0, 0, 0)), (self.x, self.y))

    def load_sprites(self, sprites: dict, target: str):  # will probs mis-order if more than 10 unless hex
        self.sprites = [sprites[i] for i in sprites if i.startswith(target)]  # don't ask lol it works
        return self.sprites

        # refactor to make it only trigger on events instead of all the time

    def drag(self):
        if self.dragging:
            pos = pygame.mouse.get_pos()
            self.x = pos[0] - self.offset[0]
            self.y = pos[1] - self.offset[1]  # maybe constant update for bb idk
            self.get_bb()  # update bb only when acc dragging

    def drag_set(self):
        self.dragging = True
        self.selected = True
        pos = pygame.mouse.get_pos()
        self.offset = [pos[0] - self.x, pos[1] - self.y]

    def drag_release(self):
        self.dragging = False
        self.get_bb()

    def touched(self, mpos):
        return self.rect.collidepoint(mpos)

    def touched_wires(self, mpos):
        for i, wire_box in enumerate(self.wire_boxes):
            if self.x + wire_box[0] < mpos[0] < self.x + wire_box[0] + 10 \
                    and self.y + wire_box[1] < mpos[1] < self.y + wire_box[1] + 10:
                return i  # index of wire box
        return None

    def box_pos(self, box_pos):
        """Modifies box position to absolute from relative, +5 for centering"""
        return self.x + box_pos[0] + 5, self.y + box_pos[1] + 5

    def get_bb(self):
        """Re-grab bounding box"""
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        return self.rect

    def get_wb(self):
        """Grab wire boxes"""
        pass


class ResistorStandard(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'ResistorStandard'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        # refactor to make container reference, let container handle sprites
        self.image = self.sprites[0]  # only has one image
        # self.image = pygame.transform.scale(self.image, (68, 20))
        # self.image = pygame.transform.scale(self.image, [i * 4 for i in self.image.get_size()])
        # scale factr 4

        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]


class Cell(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'Cell'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        # refactor to make container reference, let container handle sprites
        self.image = self.sprites[0]  # only has one image

        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]

        self.path = None

    def build_model(self):
        """Build a model of all connections to the cell"""
        # self.path = Wirepath()
        pass


class EmitterLamp(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'EmitterLamp'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        self.image = self.sprites[0]
        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]


class EmitterLED(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'EmitterLED'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        self.image = self.sprites[0]
        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]


class ResistorLight(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'ResistorLight'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        self.image = self.sprites[0]
        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]


class ResistorThermal(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'ResistorThermal'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        self.image = self.sprites[0]
        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]


class ResistorVariable(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'ResistorVariable'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        self.image = self.sprites[0]
        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]


class SwitchSPST(BaseComponent):
    def __init__(self, x, y, screen: pygame.display, sprites: dict):
        self.sprite_name = 'SwitchSPST'
        super().__init__(x, y, screen, sprites, self.sprite_name)
        self.image = self.sprites[0]
        self.rect = self.get_bb()
        self.wire_boxes = [(-5, 5), (64, 5)]
