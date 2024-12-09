from pico2d import * 
import gfw

from fighter import Fighter
from enemy import EnemyGen
from item import UpgradeItem  # 아이템 클래스 가져오기
from c_check import CollisionChecker
from boss import *
from ui import FighterUI
import pause_scene


world = gfw.World(['bg', 'fighter', 'bullet', 'missile', 'enemy', 'controller', 'player_bullet', 'enemy_bullet', 'item','boss','boss_bullet','ui'])

canvas_width = 625
canvas_height = 1100
shows_bounding_box = False
shows_object_count = True

def enter():
    global fighter, fighter_ui
    # 배경 추가
    world.append(gfw.VertFillBackground('res/background.png', -40), world.layer.bg)
    
    # Fighter와 FighterUI 생성
    fighter = Fighter()
    fighter_ui = FighterUI(fighter)

    world.append(fighter, world.layer.fighter)
    world.append(fighter_ui, world.layer.ui)

    # EnemyGen 생성
    enemy_gen = EnemyGen(fighter)
    world.append(enemy_gen, world.layer.controller)

    # 충돌 체크 추가
    collision_checker = CollisionChecker(fighter)
    world.append(collision_checker, world.layer.controller)
    
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
    if e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        gfw.push(pause_scene)
        return True

def update():
    world.update()

def draw():
    world.draw()

if __name__ == '__main__':
    gfw.start_main_module() 