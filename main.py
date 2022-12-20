import sys
import ctypes

from pygame.locals import *
from Component import *
from Container import Container


def maximise():
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)


def do_events(container):
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left button down
                mpos = pygame.mouse.get_pos()
                if container.editor.in_bounds(mpos):
                    for component in container.components:
                        if (wire_box_index := component.touched_wires(mpos)) is not None:
                            print(wire_box_index)
                            container.editor.set_wire_draw(mpos)
                            container.add_wire(component, wire_box_index, True)
                            break
                        elif component.touched(mpos):
                            if not component.selected and not pygame.key.get_pressed()[pygame.K_LCTRL]:
                                container.deselect_all()
                            component.drag_set()
                            container.drag_set()
                            break
                    else:
                        container.editor.select_down(mpos)
                        if not pygame.key.get_pressed()[pygame.K_LCTRL]:
                            container.deselect_all()
                elif container.comp_store.in_bounds(mpos):
                    container.append_component(mpos)

            elif event.button == 2:  # right button down
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            if event.button == 1:  # left button up
                if container.editor.in_bounds(mpos):
                    for component in container.components:
                        if (wire_box_index := component.touched_wires(mpos)) is not None:
                            container.add_wire(component, wire_box_index, False)
                            break
                    for component in container.components:
                        component.drag_release()
                    container.editor.select_up()
                if container.comp_store.in_bounds(mpos):
                    container.delete_selected()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE or event.key == pygame.K_PERIOD:
                container.delete_selected()
            elif event.key == pygame.K_k:
                # container.build_paths()
                m = container.wire_matrix.copy_matrix()
                print(container.wire_matrix.reduce_matrix(m))
            """
            elif event.key == pygame.K_l:
                container.load()
            elif event.key == pygame.K_s:
                container.save()
            """


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
    container = Container(screen,
                          [ResistorStandard(00, 00, screen, sprites),
                           ResistorStandard(100, 100, screen, sprites),
                           ResistorStandard(00, 00, screen, sprites),
                           Cell(00, 00, screen, sprites)])
    # editor = Editor(screen, container.components, (scr_w/5*4, scr_h))
    # comp_store = ComponentStore(screen, (scr_w, scr_h), scr_w/5, sprites)
    # screen.get_size()
    # container.components[0].load_sprites(container.sprites)

    while 1:
        clock.tick(60)
        screen.fill((220, 220, 220))
        container.comp_store.draw()
        # screen.blit(font.render('yay', False, (0, 0, 0)), (20, 20))
        container.tick()

        container.editor.run()
        do_events(container)

        # disp fps to check performance
        # screen.blit(font2.render(str(clock.get_fps()), False, (20, 20, 20)), (100, 100))
        pygame.display.update()


if __name__ == '__main__':
    main()

# TODO 1: comp store  `
# TODO 2: wires  `
# TODO 3: simulation
# TODO 4: scrolling around

# finish trees and do wire boxes with images

# maybe tally up resistances, calc current and distribute voltage IDK
