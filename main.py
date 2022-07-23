import pygame
import sys
import ctypes

from pygame.locals import *


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

    while 1:
        clock.tick(60)
        screen.fill((255, 255, 255))
        screen.blit(font.render('yay', False, (0, 0, 0)), (20, 20))

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        pygame.display.update()

if __name__ == '__main__':
    main()