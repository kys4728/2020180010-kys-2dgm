from pico2d import * 
import gfw

from fighter import Fighter
from enemy import *
from item import UpgradeItem  # 아이템 클래스 가져오기

world = gfw.World(['bg', 'fighter', 'bullet', 'missile', 'enemy', 'controller', 'player_bullet', 'enemy_bullet', 'item'])

canvas_width = 625
canvas_height = 1100
shows_bounding_box = True
shows_object_count = True

def enter():
    world.append(gfw.VertFillBackground('res/background.png', -40), world.layer.bg)
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
    def draw(self):
        pass

    def update(self):
        # 적과 플레이어 투사체 간 충돌 확인
        enemies = gfw.top().world.objects_at(gfw.top().world.layer.enemy)
        for e in enemies:
            if not isinstance(e, Enemy):  # 적 객체만 처리
                continue

            collided = False
            bullets = gfw.top().world.objects_at(gfw.top().world.layer.bullet)
            for b in bullets:
                if gfw.collides_box(b, e):
                    gfw.top().world.remove(e)  # 적 제거
                    gfw.top().world.remove(b)  # 투사체 제거
                    self.drop_item(e.x, e.y)  # 아이템 드랍
                    collided = True
                    break
            if collided:
                continue

            # 적과 플레이어 충돌 확인
            if gfw.collides_box(fighter, e):
                gfw.top().world.remove(e)
                fighter.hp -= 10  # 체력 감소
                print(f"Fighter HP: {fighter.hp}")
                if fighter.hp <= 0:
                    print("Game Over!")
                    gfw.quit()
                break

        # 적의 투사체와 플레이어 충돌 확인
        enemy_bullets = gfw.top().world.objects_at(gfw.top().world.layer.enemy_bullet)
        for b in enemy_bullets:
            if gfw.collides_box(b, fighter):
                gfw.top().world.remove(b)
                fighter.hp -= 1  # 체력 감소
                print(f"Fighter HP: {fighter.hp}")
                if fighter.hp <= 0:
                    print("Game Over!")
                    gfw.quit()
                break

        # 아이템과 플레이어 충돌 확인
        items = gfw.top().world.objects_at(gfw.top().world.layer.item)
        for item in items:
            if isinstance(item, UpgradeItem) and gfw.collides_box(item, fighter):
                self.apply_item_effect(item.effect_type)  # 아이템 효과 적용
                if item in gfw.top().world.objects_at(gfw.top().world.layer.item):  # 존재 여부 확인
                    gfw.top().world.remove(item)

    def drop_item(self, x, y):
        """적 제거 시 아이템을 드랍"""
        import random
        if random.random() < 0.5:  # 50% 확률로 아이템 드랍
            effect_type = random.choice(['health', 'damage'])
            gfw.top().world.append(UpgradeItem(x, y, effect_type), gfw.top().world.layer.item)

    def apply_item_effect(self, effect_type):
        if effect_type == 'health':
            fighter.hp = min(100, fighter.hp + 10)  # 체력 회복 (최대 100)
            print(f"Health increased: {fighter.hp}")
        elif effect_type == 'damage':
            fighter.increase_damage()  # 데미지 증가 (Fighter 클래스에 메서드 추가 필요)
            print("Damage increased!")

if __name__ == '__main__':
    gfw.start_main_module()
