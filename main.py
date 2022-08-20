import pygame
import sys
import ctypes

from pygame.locals import *
from Component import ResistorStandard
from Editor import Editor
from Container import Container


def maximise():
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)


def do_events(components):
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('mdown')
            mpos = pygame.mouse.get_pos()
            for component in components:
                if component.touched(mpos):
                    print('omg')
                    component.drag_set()
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            for component in components:
                if component.touched(mpos):
                    component.dragging = False
                    break


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

    container = Container([ResistorStandard(00, 00, screen), ResistorStandard(100,100,screen)])
    editor = Editor(screen, container.components)


    while 1:
        clock.tick(60)
        screen.fill((220, 220, 220))
        #screen.blit(font.render('yay', False, (0, 0, 0)), (20, 20))
        container.tick()
        editor.run()
        do_events(container.components)
        pygame.display.update()


if __name__ == '__main__':
    main()
