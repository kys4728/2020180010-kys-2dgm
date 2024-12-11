from pico2d import * 
from gfw import *

import sys
self = sys.modules[__name__]

world = World(2)
transparent = True

def enter():
    global center_x, center_y
    center_x = get_canvas_width() // 2
    center_y = get_canvas_height() // 2

    global font
    font = gfw.font.load('res/artie-sans.ttf',30)

    world.append(Background('res/background.png'), 0)

    world.append(self, 1)

def exit():
    world.clear()

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_q:
        gfw.pop()
        gfw.pop()
        return True

def draw():
    gfw.font.draw_centered_text(font, 'Press ESC to Resume',     center_x, center_y + 60, (0, 126, 63))
    gfw.font.draw_centered_text(font, 'Press Q to Exit', center_x, center_y - 20, (126, 0, 0))

def update():
    pass

if __name__ == '__main__':
    gfw.start_main_module()


