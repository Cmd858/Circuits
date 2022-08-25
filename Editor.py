import pygame


class Editor:
    def __init__(self, screen, component_list):
        self.screen = screen
        self.component_list = component_list
        self.rect = pygame.Rect((0, 0), (600, 600))
        self.selecting = False
        self.select_pos = (0, 0)
        self.selected_area = pygame.Rect(0, 0, 0, 0)

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

    def select_up(self):
        self._check_select_collision()
        self.selecting = False

    def draw_select(self):
        if self.selecting:
            self.selected_area.update(*(*self.select_pos,  # below does subtraction from pos
                                        *(j - i for i, j in zip(self.select_pos, pygame.mouse.get_pos()))))
            self.selected_area.normalize()
            pygame.draw.rect(self.screen,
                             (100, 100, 100),
                             self.selected_area,
                             1)

    def run(self):
        #self.get_selected()
        self.draw_select()

    def _check_select_collision(self):
        for component in self.component_list:
            if self.selected_area.colliderect(component.rect):
                component.selected = True
