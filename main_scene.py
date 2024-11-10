from pico2d import * 
import gfw

from fighter import Fighter
from enemy import EnemyGen

world = gfw.World(['bg', 'fighter', 'bullet', 'missile', 'enemy','controller','player_bullet', 'enemy_bullet'])

canvas_width = 625
canvas_height = 1100
shows_bounding_box = True
shows_object_count = True

def enter():
    world.append(gfw.VertFillBackground('res/background.jpeg', -40), world.layer.bg)
    global fighter
    fighter = Fighter()
    world.append(fighter, world.layer.fighter)
    
    # EnemyGen 생성 시 Fighter 객체를 전달
    enemy_gen = EnemyGen(fighter)
    world.append(enemy_gen, world.layer.controller)
    world.append(CollisionChecker(), world.layer.controller)

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
class CollisionChecker:
    def draw(self): pass
    def update(self):
        enemies = world.objects_at(world.layer.enemy)
        for e in enemies: # reversed order
            collided = False
            bullets = world.objects_at(world.layer.bullet)
            for b in bullets: # reversed order
                if gfw.collides_box(b, e):
                    world.remove(e)
                    world.remove(b)
                    collided = True
                    break
            if collided: break
            if gfw.collides_box(fighter, e):
                world.remove(e)
                # decrease fighter HP here?
                break

if __name__ == '__main__':
    gfw.start_main_module()
