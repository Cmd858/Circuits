import pygame

"""
Removing this and waiting until I figure out what I want to do.

Probably will roll back to pygame 1.9.6 for embedding the window,
unless they fix the issue.
"""


class Menubar:
    def __init__(self, screen: pygame.display):
        ybuf = 0
        xbuf = 7
        # all including outer lines
        #text height 9
        #box height 18
        #7 pixel x buf
        #5 px off bottom inc line

        self.screen = screen
        self.fontsize = 12
        self.font = pygame.font.SysFont('segoeui', self.fontsize)
        self.font.bold = True

        self.rect = pygame.Rect(0, 0, screen.get_width(), self.font.size('adj')[1])
        self.buttonNames = ['File', 'Edit', 'View']
        self.buttons = []
        self.displacement = 5



        for name in self.buttonNames:
            self.buttons.append(Button(self.screen,
                                       name,
                                       (self.displacement, ybuf),
                                       self.font))
            self.displacement += self.font.size(name)[0] + xbuf

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
        for button in self.buttons:
            button.draw(True)


class Button:
    def __init__(self, screen: pygame.display, name, position, font):
        self.x = position[0]
        self.y = position[1]
        self.rect = pygame.Rect(position, font.size(name))
        self.name = name
        self.screen = screen
        self.font = font

    def draw(self, aa):
        self.screen.blit(self.font.render(self.name, aa, (0, 0, 0)), (self.x, 1))
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
