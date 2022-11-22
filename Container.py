import pygame.draw
import pickle

from Component import *
from Editor import Editor
from ComponentStore import ComponentStore
# from Wirepath import Wirepath, Node
from WireMatrix import WireMatrix

import os


class Container:
    def __init__(self, screen, components: [BaseComponent] = None):
        self.components = components if components is not None else []
        self.wire_matrix = WireMatrix(len(self.components))
        for i, component in enumerate(self.components):
            self.components[i].cid = i
            self.wire_matrix.add_node(component)
        self.cids = [component.cid for component in self.components]
        self.dragging = False
        self.offx = 0
        self.offy = 0
        self.sprites = self.get_sprites()
        # start wire used for finding the component and it's
        self.start_wire = None
        self.wires = []  # ((component1, box_index1), (component2, box_index2)), box_index is of wire_box list
        self.wire_paths = []

        self.screen = screen
        scr_w, scr_h = screen.get_size()

        self.editor = Editor(screen, self.components, (scr_w / 5 * 4, scr_h))
        self.comp_store = ComponentStore(screen, (scr_w, scr_h), scr_w / 5, self.sprites)

    def tick(self):
        for component in self.components:
            component.draw()
            # component.select()
            component.drag()
            self.draw_wires()

    def drag_set(self):
        for component in self.components:
            if component.selected:
                component.drag_set()

    def deselect_all(self):
        for component in self.components:
            component.selected = False

    def add_wire(self, component, box_index, first=True):
        """Adds a wire to the matrix"""
        if first:
            self.start_wire = self.wire_matrix.get_nid(component.cid, box_index)
        else:
            self.wires.append(((component, box_index), self.start_wire))
            self.wire_matrix.connect_nodes(1, 1)

    def draw_wires(self):
        for wire in self.wires:
            # lol no screen
            pygame.draw.line(self.screen, (0, 0, 0),
                             wire[0][0].box_pos(wire[0][0].wire_boxes[wire[0][1]]),
                             wire[1][0].box_pos(wire[1][0].wire_boxes[wire[1][1]]))

    def delete_selected(self):
        i = 0
        while i < len(self.components):
            if self.components[i].selected:
                j = 0
                while j < len(self.wires):
                    if self.components[i] in self.wires[j][0] or self.components[i] in self.wires[j][1]:
                        self.wires.pop(j)
                        j -= 1
                    j += 1
                self.components.pop(i)
                i -= 1
            i += 1

    def append_component(self, mpos):
        """Major bugs here lol"""
        self.components.append(component := self.comp_store.grab_component(mpos)(mpos[0],
                                                                                 mpos[1],
                                                                                 self.screen,
                                                                                 self.sprites
                                                                                 ))
        component.selected = True
        component.dragging = True
        component.cid = self._get_id(component)

    def _get_id(self, component):
        """Get the ID of a new component, only create a new one if there is space"""
        for i, cid in enumerate(self.cids):
            if i != cid:
                self.cids.insert(i, i)
                return i
        self.cids.append(len(self.cids))
        self.wire_matrix.add_node(component)
        return len(self.cids) - 1  # -1 bc of append

    def save(self):
        """Currently unused save function"""
        name = 'save1'
        with open(name, 'wb') as f:
            pickle.dump(self, f)

    def load(self):
        """Currently unused load function"""
        name = 'save1'
        with open(name, 'rb') as f:
            self.__dict__.clear()
            self.__dict__.update(pickle.load(f).__dict__)


    @staticmethod
    def get_sprites():  # using underscores in names to separate name from frame
        sprites = {}
        scale = 4
        for path in os.listdir('Images/'):  # have fun refactoring this for proper logic
            if path.endswith('.png'):  # will not work with more than one frame lmao
                sprites[path[:path.rindex('.')]] = pygame.image.load(f'Images/{path}').convert_alpha()
        for key, sprite in sprites.items():
            sprites[key] = pygame.transform.scale(sprite, [i * scale for i in sprite.get_size()])
        return sprites
