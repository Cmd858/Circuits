import pygame
import sys
import ctypes

from pygame.locals import *
from Component import ResistorStandard
from Editor import Editor


def maximise():
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Circuits")
    dispinfo = pygame.display.Info()
    screen = pygame.display.set_mode((700, 600), RESIZABLE)  # normally 700x600
    maximise()
    scr_w = screen.get_width()
    scr_h = screen.get_height()
    font = pygame.font.SysFont('lucidaconsole', 60)
    font2 = pygame.font.SysFont('lucidaconsole', 20)
    components = []
    components.append(ResistorStandard(00, 00, screen))
    components.append(ResistorStandard(100,100,screen))

    editor = Editor(screen, components)


    while 1:
        clock.tick(60)
        screen.fill((220, 220, 220))
        #screen.blit(font.render('yay', False, (0, 0, 0)), (20, 20))
        for component in components:
            component.draw()
            component.select()
        editor.run()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        pygame.display.update()


if __name__ == '__main__':
    main()
