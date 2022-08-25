import pygame
import sys
import ctypes

from pygame.locals import *
import pygame
from Component import *
from ComponentStore import ComponentStore
from Editor import Editor
from Container import Container


def maximise():
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)


def do_events(container, editor):
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left button down
                mpos = pygame.mouse.get_pos()
                for component in container.components:
                    if component.touched(mpos):
                        if not component.selected:
                            container.deselect_all()
                        component.drag_set()
                        container.drag_set()
                        break
                else:
                    editor.select_down(mpos)
                    container.deselect_all()
            elif event.button == 2:  # right button down
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # left button up
                for component in container.components:
                    component.drag_release()
                editor.select_up()
            elif event.button == 2:  # right button up
                pass



def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Circuits")
    dispinfo = pygame.display.Info()
    scr_w, scr_h = dispinfo.current_w, dispinfo.current_h
    screen = pygame.display.set_mode((scr_w, scr_h), RESIZABLE)  # normally 700x600
    maximise()
    # scr_w = screen.get_width()
    # scr_h = screen.get_height()
    font = pygame.font.SysFont('lucidaconsole', 60)
    font2 = pygame.font.SysFont('lucidaconsole', 20)

    sprites = Container.get_sprites()
    container = Container([ResistorStandard(00, 00, screen, sprites), ResistorStandard(100, 100, screen, sprites)])
    editor = Editor(screen, container.components)
    comp_store = ComponentStore(screen, (scr_w, scr_h), scr_w/5)
    # container.components[0].load_sprites(container.sprites)


    while 1:
        clock.tick(60)
        screen.fill((220, 220, 220))
        #screen.blit(font.render('yay', False, (0, 0, 0)), (20, 20))
        container.tick()
        editor.run()
        do_events(container, editor)
        comp_store.draw()
        # disp fps to check performance
        # screen.blit(font2.render(str(clock.get_fps()), False, (20, 20, 20)), (100, 100))
        pygame.display.update()


if __name__ == '__main__':
    main()


# TODO 1: comp store
# TODO 2: wires
# TODO 3: simulation
# TODO 4: scrolling around
