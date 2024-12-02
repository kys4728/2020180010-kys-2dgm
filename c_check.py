import gfw
from item import UpgradeItem  # 아이템 클래스 가져오기
from boss import *
from enemy import *
from fighter import *

class CollisionChecker:
    def __init__(self, fighter):
        self.fighter = fighter
        self.kill_count = 0  # 적 처치 횟수 추적

    def draw(self):
        pass

    def update(self):
        # 충돌 처리에 필요한 객체 가져오기 (한 번만 호출)
        self.enemies = gfw.top().world.objects_at(gfw.top().world.layer.enemy)
        self.bullets = gfw.top().world.objects_at(gfw.top().world.layer.bullet)
        self.enemy_bullets = gfw.top().world.objects_at(gfw.top().world.layer.enemy_bullet)
        self.bosses = gfw.top().world.objects_at(gfw.top().world.layer.boss)
        self.items = gfw.top().world.objects_at(gfw.top().world.layer.item)
        # 충돌 체크 로직
        self.check_enemy_collision()
        self.check_enemy_bullet_collision()
        self.check_boss_collision()
        self.check_item_collision()
        self.check_boss_bullet_collision()  # 보스 투사체 충돌 확인 추가
        self.check_enemy_enemy_collision()

    def check_enemy_enemy_collision(self):
        for i, enemy1 in enumerate(self.enemies):
            for j, enemy2 in enumerate(self.enemies):
                if i >= j:  # 같은 적 또는 이미 확인한 쌍은 무시
                    continue
                if self.is_colliding(enemy1, enemy2):
                    overlap = (enemy1.get_bb()[2] - enemy2.get_bb()[0]) / 2
                    enemy1.x -= overlap
                    enemy2.x += overlap
                    enemy1.move_dir *= -1  # 충돌한 적의 X 방향 반전
                    enemy2.move_dir *= -1

    def handle_projectile_collision(self, projectile, target):
        if gfw.collides_box(projectile, target):
            target.take_damage(projectile.attack_power)
            gfw.top().world.remove(projectile)
            if target.hp <= 0:
                self.drop_item(target.x, target.y)
                if isinstance(target, Enemy):
                    self.kill_count += 1
                    self.check_boss_spawn()
                elif isinstance(target, Boss):
                    print("Boss defeated!")
                    gfw.top().world.remove(target)
            return True
        return False    

    def check_enemy_collision(self):
        for e in self.enemies:
            for b in self.bullets:
                if self.handle_projectile_collision(b, e):
                    break  # 적이 제거되었으므로 다음 적으로 이동

            if gfw.collides_box(self.fighter, e):
                gfw.top().world.remove(e)
                self.fighter.hp -= 10
                print(f"Fighter HP: {self.fighter.hp}")
                if self.fighter.hp <= 0:
                    self.game_over()
                break

    def check_enemy_bullet_collision(self):
        for b in self.enemy_bullets:
            if not isinstance(b, BossBullet) and gfw.collides_box(b, self.fighter):
                print("Fighter hit by Enemy Bullet!")
                gfw.top().world.remove(b)
                self.fighter.hp -= 1  # 일반 적 투사체에 맞으면 체력 1 감소
                print(f"Fighter HP: {self.fighter.hp}")
            if self.fighter.hp <= 0:
                self.game_over()
                break


    def check_boss_collision(self):
        for boss in self.bosses:
            for b in self.bullets:
                if self.handle_projectile_collision(b, boss):
                    break  # 보스가 제거되었으므로 다음 보스로 이동

            if gfw.collides_box(self.fighter, boss):
                self.fighter.hp -= 20
                print(f"Fighter HP: {self.fighter.hp}")
                if self.fighter.hp <= 0:
                    self.game_over()
                break

    def check_boss_bullet_collision(self):
        for b in self.enemy_bullets:
            if isinstance(b, BossBullet) and gfw.collides_box(b, self.fighter):
                print("Fighter hit by Boss Bullet!")
                gfw.top().world.remove(b)
                self.fighter.hp -= 5  # 보스 투사체에 맞으면 더 큰 데미지
            if isinstance(b, BigBossBullet) and gfw.collides_box(b, self.fighter):
                print("Fighter hit by Big Boss Bullet!")
                gfw.top().world.remove(b)
                self.fighter.hp -= 20    
                print(f"Fighter HP: {self.fighter.hp}")
            if self.fighter.hp <= 0:
                self.game_over()
                break


    def check_item_collision(self):
        for item in self.items:
            if isinstance(item, UpgradeItem) and gfw.collides_box(item, self.fighter):
                item.apply_effect(self.fighter)  # 아이템 효과를 적용
                gfw.top().world.remove(item)

    def drop_item(self, x, y):
        # 고정 효과 아이템 생성
        effect_type = 'damage'  # 항상 'damage' 효과로 설정 (레벨업 관련)
        print(f"Item dropped with effect: {effect_type}")
        gfw.top().world.append(UpgradeItem(x, y, effect_type), gfw.top().world.layer.item)

    def check_boss_spawn(self):
        if self.kill_count >= 1:
            existing_bosses = gfw.top().world.objects_at(gfw.top().world.layer.boss)
            if existing_bosses:
                return  # 이미 보스가 존재하면 스폰하지 않음

            print("Boss Spawned!")
            boss = Boss(self.fighter)
            gfw.top().world.append(boss, gfw.top().world.layer.boss)

            # 보스 생성 시 적 스폰 중지
            enemy_gen = gfw.top().world.objects_at(gfw.top().world.layer.controller)[0]
            if isinstance(enemy_gen, EnemyGen):
                enemy_gen.deactivate()

            self.kill_count = 0

    def game_over(self):
        print("Game Over!")
        gfw.quit()

    def is_colliding(self, obj1, obj2):
        """두 객체 간 충돌 감지 (박스 기반)"""
        ax1, ay1, ax2, ay2 = obj1.get_bb()
        bx1, by1, bx2, by2 = obj2.get_bb()
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)