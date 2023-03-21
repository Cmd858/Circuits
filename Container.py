import pygame.draw
import pickle
from copy import deepcopy

from Component import *
from Editor import Editor
from ComponentStore import ComponentStore
# from Wirepath import Wirepath, Node
from WireMatrix import WireMatrix

import os


class Container:
    def __init__(self, screen, components: [BaseComponent] = None):
        self.components: [BaseComponent] = components if components is not None else []
        self.wire_matrix = WireMatrix(len(self.components))
        for i, component in enumerate(self.components):
            component.cid = i
            print(f'component, i: {component, i}')
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

    def add_wire(self, component, box_index: int, first=True):
        """Adds a wire to the matrix"""
        if first:
            self.start_wire = self.wire_matrix.get_nid(component.cid, box_index)
        elif self.start_wire != (wire2 := self.wire_matrix.get_nid(component.cid, box_index)):
            if wire2 != None and self.start_wire != None:
                self.wires.append((wire2, self.start_wire))
                self.wire_matrix.connect_nodes(*self.wires[-1])

    def draw_wires(self):
        """Draw all wires"""
        for wire in self.wires:
            # lol no screen
            #print(self.wires)
            #print(self.wire_matrix.nodes)
            #print(self.wire_matrix.get_wirebox_pos_from_nid(wire[0]),
            #      self.wire_matrix.get_wirebox_pos_from_nid(wire[1]))
            pygame.draw.line(self.screen, (0, 0, 0),
                             self.wire_matrix.get_wirebox_pos_from_nid(wire[0]),
                             self.wire_matrix.get_wirebox_pos_from_nid(wire[1]))

    def delete_selected(self):
        """Remove a component and wires connecting to it"""
        i = 0
        print(f'Wires: {self.wires}')
        while i < len(self.components):
            if self.components[i].selected:
                j = 0
                while j < len(self.wires):
                    print(self.wires, self.components, i, j)
                    nids = self.wire_matrix.get_nids(self.components[i].cid)
                    print(nids)
                    for wire in self.wires[j]:
                        if wire in nids:
                            self.wires.pop(j)
                            j -= 1
                            break
                    j += 1
                self.components.pop(i)
                i -= 1
            i += 1
        print(f'Wires: {self.wires}')

    def append_component(self, mpos):
        """Adds a component to the list and matrix, if a valid component was selected"""
        component = self.comp_store.grab_component(mpos)  # returns class object to be initialised
        if component is not None:
            self.components.append(component(mpos[0],
                                             mpos[1],
                                             self.screen,
                                             self.sprites
                                             ))
            self.components[-1].selected = True
            self.components[-1].dragging = True
            self.components[-1].cid = self._get_id(self.components[-1])

    def _get_id(self, component):
        """Get the ID of a new component, only create a new one if there is space"""
        for i, cid in enumerate(self.cids):
            if i != cid:
                self.cids.insert(i, i)
                return i
        self.cids.append(len(self.cids))
        self.wire_matrix.add_node(component)
        return len(self.cids) - 1  # -1 bc of append

    """
    def save(self):
        "Currently unused save function"
        name = 'save1'
        savedict = {'Cmps': [], 'Matrix': None}
        for cmp in self.components:
            savedict['Cmps'].append({'Obj': cmp.__class__, 'xy': (cmp.x, cmp.y), 'cid': cmp.cid})
        savedict['Matrix'] = self.wire_matrix
        with open(name, 'wb') as f:
            pickle.dump(savedict, f)

    def load(self):
        "Currently unused load function"
        name = 'save1'
        self.components = []
        self.wire_matrix = None
        with open(name, 'rb') as f:
            loaddict = pickle.load(f)
        for cmp in loaddict['Cmps']:
            self.components.append()
    """
    def save(self):
        name='save1'

        sprites = self.sprites
        screen = self.screen
        self.sprites = []
        self.screen = None
        self.editor = None
        self.comp_store = None
        with open(name, 'wb') as f:
            pickle.dump(self, f)
        self.sprites = sprites
        self.screen = screen

    @staticmethod
    def get_sprites():  # using underscores in names to separate name from frame
        """Load sprites into a dictionary and return it"""
        sprites = {}
        scale = 4
        for path in os.listdir('Images/'):  # have fun refactoring this for proper logic
            if path.endswith('.png'):  # will not work with more than one frame lmao
                sprites[path[:path.rindex('.')]] = pygame.image.load(f'Images/{path}').convert_alpha()
        for key, sprite in sprites.items():
            sprites[key] = pygame.transform.scale(sprite, [i * scale for i in sprite.get_size()])
        return sprites
