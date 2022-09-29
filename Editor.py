import pygame


class Editor:
    def __init__(self, screen, component_list, dimensions):
        self.screen = screen
        self.component_list = component_list
        self.rect = pygame.Rect((0, 0), dimensions)
        self.selecting = False
        self.select_pos = (0, 0)
        self.selected_area = pygame.Rect(0, 0, 0, 0)
        self.wire_draw = False
        self.wire_draw_loc = (0, 0)

    # possible use for generator to yield data idk
    
    def get_selected(self):
        if not self.selecting:
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed(3)[0] and self.rect.collidepoint(pos):
                self.select_pos = pos
                self.selecting = True
        else:
            if not pygame.mouse.get_pressed(3)[0]:
                self.selecting = False
                self._check_select_collision()

        ###
        if self.selecting:
            pass

    def select_down(self, mpos):
        self.selecting = True
        self.select_pos = mpos

    def set_wire_draw(self, pos):
        self.wire_draw_loc = pos
        self.wire_draw = True

    def select_up(self):
        self._check_select_collision()
        self.selecting = False
        self.wire_draw = False

    def draw_select_box(self):
        if self.selecting:
            self.selected_area.update(*(*self.select_pos,  # below does subtraction from pos
                                        *(j - i for i, j in zip(self.select_pos, pygame.mouse.get_pos()))))
            self.selected_area.normalize()
            pygame.draw.rect(self.screen,
                             (100, 100, 100),
                             self.selected_area,
                             1)

    def draw_select_wires(self):
        if self.wire_draw:
            pygame.draw.line(self.screen, (0, 0, 0), self.wire_draw_loc, pygame.mouse.get_pos())

    def run(self):
        #self.get_selected()
        self.draw_select_box()
        self.draw_select_wires()

    def in_bounds(self, mpos):
        # print(f'{mpos}, {self.rect}')
        return self.rect.collidepoint(mpos)

    def _check_select_collision(self):
        for component in self.component_list:
            if self.selected_area.colliderect(component.rect):
                component.selected = True
