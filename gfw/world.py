from pico2d import *
from functools import reduce

class World:
    def __init__(self, layer_count=1):
        if isinstance(layer_count, list):
            layer_names = layer_count
            layer_count = len(layer_count)
            index = 0
            self.layer = lambda: None
            for name in layer_names:
                self.layer.__dict__[name] = index
                index += 1

        self.objects = [[] for _ in range(layer_count)]

    def append(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        self.objects[layer_index].append(go)

    def remove(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        if go in self.objects[layer_index]:
            self.objects[layer_index].remove(go)

    def clear(self):
        layer_count = len(self.objects)
        self.objects = [[] for _ in range(layer_count)]

    def update(self):
        for go in self.all_objects():
            go.update()

    def draw(self):
        for go in self.all_objects():
            go.draw()
            #if hasattr(go, 'get_bb'):
                #draw_rectangle(*go.get_bb())
    def all_objects(self):
        for objs in self.objects:
            for go in objs:
                yield go

    def objects_at(self, layer_index):
        return self.objects[layer_index]

def collides_box(a, b):
    if getattr(a, 'is_projectile', False) and getattr(b, 'is_projectile', False):
        return False
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()
    return not (la > rb or ra < lb or ba > tb or ta < bb)
