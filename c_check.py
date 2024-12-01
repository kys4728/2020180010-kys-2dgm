import gfw
from item import UpgradeItem  # 아이템 클래스 가져오기
from boss import Boss
from enemy import *

class CollisionChecker:
    def __init__(self, fighter):
        self.fighter = fighter
        self.kill_count = 0  # 적 처치 횟수 추적

    def draw(self):
        pass

    def update(self):
        # 충돌 체크 로직
        self.check_enemy_collision()
        self.check_enemy_bullet_collision()
        self.check_boss_collision()
        self.check_item_collision()
        self.check_boss_bullet_collision()  # 보스 투사체 충돌 확인 추가
        self.check_enemy_enemy_collision()

    def check_enemy_enemy_collision(self):
        enemies = gfw.top().world.objects_at(gfw.top().world.layer.enemy)
        for i, enemy1 in enumerate(enemies):
            for j, enemy2 in enumerate(enemies):
                if i >= j:  # 같은 적 또는 이미 확인한 쌍은 무시
                    continue
                if self.is_colliding(enemy1, enemy2):
                    enemy1.move_dir *= -1  # 충돌한 적의 X 방향 반전
                    enemy2.move_dir *= -1
    def check_enemy_collision(self):
        enemies = gfw.top().world.objects_at(gfw.top().world.layer.enemy)
        for e in enemies:
            if not isinstance(e, Enemy):  # 적 객체만 처리
                continue

            collided = False
            bullets = gfw.top().world.objects_at(gfw.top().world.layer.bullet)
            for b in bullets:
                if gfw.collides_box(b, e):
                    
                    gfw.top().world.remove(e)
                    gfw.top().world.remove(b)
                    self.drop_item(e.x, e.y)
                    self.kill_count += 1
                    print(f"Kill Count: {self.kill_count}")
                    self.check_boss_spawn()
                    collided = True
                    break

            if collided:
                continue

            if gfw.collides_box(self.fighter, e):
                gfw.top().world.remove(e)
                self.fighter.hp -= 10
                print(f"Fighter HP: {self.fighter.hp}")
                if self.fighter.hp <= 0:
                    print("Game Over!")
                    gfw.quit()
                break

    def check_enemy_bullet_collision(self):
        enemy_bullets = gfw.top().world.objects_at(gfw.top().world.layer.enemy_bullet)
        for b in enemy_bullets:
            if gfw.collides_box(b, self.fighter):
                gfw.top().world.remove(b)
                self.fighter.hp -= 1
                print(f"Fighter HP: {self.fighter.hp}")
                if self.fighter.hp <= 0:
                    print("Game Over!")
                    gfw.quit()
                break

    def check_boss_collision(self):
        bosses = gfw.top().world.objects_at(gfw.top().world.layer.boss)
        for boss in bosses:
            if gfw.collides_box(self.fighter, boss):
                self.fighter.hp -= 20
                print(f"Fighter HP: {self.fighter.hp}")
                if self.fighter.hp <= 0:
                    print("Game Over!")
                    gfw.quit()
                break

            bullets = gfw.top().world.objects_at(gfw.top().world.layer.bullet)
            for b in bullets:
                if gfw.collides_box(b, boss):
                    boss.take_damage(10)
                    gfw.top().world.remove(b)
                    if boss.hp <= 0:
                        print("Boss defeated!")
                        gfw.top().world.remove(boss)
                        self.drop_item(boss.x, boss.y)
                    break
    def check_boss_bullet_collision(self):
        boss_bullets = gfw.top().world.objects_at(gfw.top().world.layer.boss_bullet)
        for b in boss_bullets:
            if gfw.collides_box(b, self.fighter):
                gfw.top().world.remove(b)
                self.fighter.hp -= 5  # 보스 투사체에 맞으면 체력 5 감소
                print(f"Fighter HP: {self.fighter.hp}")
                if self.fighter.hp <= 0:
                    print("Game Over!")
                    gfw.quit()

    def check_item_collision(self):
        items = gfw.top().world.objects_at(gfw.top().world.layer.item)
        for item in items:
            if isinstance(item, UpgradeItem) and gfw.collides_box(item, self.fighter):
                item.apply_effect(self.fighter)  # 아이템 효과를 적용
                gfw.top().world.remove(item)

    def drop_item(self, x, y):
        # 고정 효과 아이템 생성
        effect_type = 'damage'  # 항상 'damage' 효과로 설정 (레벨업 관련)
        print(f"Item dropped with effect: {effect_type}")
        gfw.top().world.append(UpgradeItem(x, y, effect_type), gfw.top().world.layer.item)

    def check_boss_spawn(self):
        if self.kill_count >= 20:
            print("Boss Spawned!")
            boss = Boss(self.fighter)
            gfw.top().world.append(boss, gfw.top().world.layer.boss)

            enemy_gen = gfw.top().world.objects_at(gfw.top().world.layer.controller)[0]
            if isinstance(enemy_gen, EnemyGen):
                enemy_gen.deactivate()

            self.kill_count = 0
    def is_colliding(self, obj1, obj2):
        """두 객체 간 충돌 감지 (박스 기반)"""
        ax1, ay1, ax2, ay2 = obj1.get_bb()
        bx1, by1, bx2, by2 = obj2.get_bb()
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)