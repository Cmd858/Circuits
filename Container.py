class Container:
    def __init__(self, components = []):
        self.components = components

    def tick(self):
        for component in self.components:
            component.draw()
            #component.select()
            component.drag()

    def drag_set(self):
        pass
