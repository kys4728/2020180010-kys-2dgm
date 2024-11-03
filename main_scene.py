from pico2d import * 
import gfw

from fighter import Fighter
#from enemy import EnemyGen

world = gfw.World(['bg', 'fighter', 'bullet', 'missile'])

canvas_width = 625
canvas_height = 1100
shows_bounding_box = True
shows_object_count = True

def enter():
    world.append(gfw.VertFillBackground('res/background.jpeg', -30), world.layer.bg)
    global fighter
    fighter = Fighter()
    world.append(fighter, world.layer.fighter)

def exit():
    world.clear()
    print('[main.exit()]')

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
    fighter.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

