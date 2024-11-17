from pico2d import *
import gfw
import random
from item import UpgradeItem 

class Enemy(gfw.Sprite):
    WIDTH = 100
    HEIGHT = 100
    MOVE_SPEED = 50  # 좌우 이동 속도
    SHOOT_INTERVAL = 1.5  # 총알 발사 간격
    MAX_BULLETS = 3
    ITEM_DROP_CHANCE = 0.3  # 30% 확률로 아이템 드랍

    def __init__(self, index, target):
        x = self.WIDTH * index + self.WIDTH // 2
        y = get_canvas_height() + self.WIDTH // 2
        super().__init__('res/enemy1.png', x, y)
        self.layer_index = gfw.top().world.layer.enemy
        self.speed = -100  # 아래로 내려가는 속도
        self.move_dir = 1  # 좌우 이동 방향 (1: 오른쪽, -1: 왼쪽)
        self.shoot_time = 0
        self.target = target  # 플레이어 객체
        self.bullet_count = 0

    def update(self):
        # 좌우 이동
        self.x += self.move_dir * Enemy.MOVE_SPEED * gfw.frame_time
        if self.x < self.WIDTH // 2 or self.x > get_canvas_width() - self.WIDTH // 2:
            self.move_dir *= -1  # 벽에 닿으면 방향 반전

        # 아래로 이동
        self.y += self.speed * gfw.frame_time
        if self.y < -self.WIDTH:
            gfw.top().world.remove(self)

        # 총알 발사
        if self.bullet_count < Enemy.MAX_BULLETS:
            self.shoot_time += gfw.frame_time
            if self.shoot_time >= Enemy.SHOOT_INTERVAL:
                self.shoot_time = 0
                bullet = Bullet(self.x, self.y, self.target.x, self.target.y)
                gfw.top().world.append(bullet)
                self.bullet_count += 1  # 발사된 총알 수 증가

    def drop_item(self):
        if random.random() < Enemy.ITEM_DROP_CHANCE:  # 30% 확률
            effect_type = random.choice(['health', 'damage'])  # 아이템 효과 랜덤 선택
            item = UpgradeItem(self.x, self.y, effect_type)  # 아이템 생성
            gfw.top().world.append(item)

    def get_bb(self):
        r = 42
        return self.x - r, self.y - r, self.x + r, self.y + r
    def remove(self):
        self.drop_item()  # 적이 제거될 때 아이템 드랍 시도
        gfw.top().world.remove(self)

class EnemyGen:
    GEN_INTERVAL = 5.0

    def __init__(self, target):
        self.time = 0
        self.target = target  # 플레이어 객체

    def draw(self):
        pass

    def update(self):
        self.time += gfw.frame_time
        if self.time < self.GEN_INTERVAL:
            return
        for i in range(3):  # 3개의 적을 생성
            gfw.top().world.append(Enemy(i, self.target))
        self.time -= self.GEN_INTERVAL


class Bullet(gfw.Sprite):
    SPEED = 400  # 총알 속도

    def __init__(self, x, y, target_x, target_y):
        super().__init__('res/fire2.png', x, y)
        dx, dy = target_x - x, target_y - y
        distance = (dx**2 + dy**2) ** 0.5
        self.vx, self.vy = Bullet.SPEED * dx / distance, Bullet.SPEED * dy / distance
        self.layer_index = gfw.top().world.layer.enemy_bullet
        self.is_projectile = True  # 투사체로 식별

    def update(self):
        self.x += self.vx * gfw.frame_time
        self.y += self.vy * gfw.frame_time
        if self.x < 0 or self.x > get_canvas_width() or self.y < 0 or self.y > get_canvas_height():
            gfw.top().world.remove(self)

    def get_bb(self):
        r = 5  # 총알 크기
        return self.x - r, self.y - r, self.x + r, self.y + r
