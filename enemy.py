from pico2d import *
import gfw
import random
from item import UpgradeItem 

class Enemy(gfw.Sprite):
    WIDTH = 140
    HEIGHT = 800
    SHOOT_INTERVAL = 0.6  # 초기 총알 발사 간격
    MIN_SHOOT_INTERVAL = 0.1  # 최소 총알 발사 간격
    MAX_BULLETS = 5
    ITEM_DROP_CHANCE = 0.1  # 30% 확률로 아이템 드랍
    HP = 50  # 적 체력
    SCALE = 0.75
    gauge = None
    IMAGE_RECTS = [
    (0, 0, 140, 160),
    (0, 160, 140, 320),
    (0, 320, 140, 480),
    (0, 480, 140, 640),
    (0, 640, 140, 800),
    ]

    def __init__(self, x, target):
        y = get_canvas_height() + int(self.WIDTH * self.SCALE // 2)
        super().__init__('res/enemys.png', x, y)
        self.layer_index = gfw.top().world.layer.enemy
        self.speed = random.uniform(-80, -120)
        self.x_speed = random.uniform(50, 150)
        self.move_dir = random.choice([-1, 1])  # 랜덤 방향 (왼쪽 또는 오른쪽)
        self.shoot_time = 0
        self.target = target  # 플레이어 객체
        self.bullet_count = 0
        self.frame_index = 0  # 현재 프레임 인덱스
        self.frame_time = 0  # 프레임 변경 시간 관리
        self.hp = Enemy.HP
        self.shoot_interval = Enemy.SHOOT_INTERVAL

        def apply_damage(self, damage):
            self.hp -= damage
            print(f"Enemy hit! Remaining HP: {self.hp}")
            if self.hp <= 0:
                print("Enemy destroyed!")
                gfw.top().world.remove(self)

    def update(self):


        # 아래로 이동
        self.x += self.move_dir * self.x_speed * gfw.frame_time
        self.y += self.speed * gfw.frame_time
        # 화면 가장자리에 닿으면 X 방향 반전
        if self.x < self.WIDTH * self.SCALE // 2:
            self.x = self.WIDTH * self.SCALE // 2
            self.move_dir = 1
        elif self.x > get_canvas_width() - self.WIDTH * self.SCALE // 2:
            self.x = get_canvas_width() - self.WIDTH * self.SCALE // 2
            self.move_dir = -1

        # 적이 화면 아래로 사라지면 제거
        if self.y < -self.WIDTH * self.SCALE:
            gfw.top().world.remove(self)

         # 프레임 업데이트
        self.frame_time += gfw.frame_time
        if self.frame_time > 0.1:  # 0.1초마다 프레임 변경
            self.frame_time = 0
            self.frame_index = (self.frame_index + 1) % len(Enemy.IMAGE_RECTS)
            
        # 총알 발사
        if self.bullet_count < Enemy.MAX_BULLETS:
            self.shoot_time += gfw.frame_time
            if self.shoot_time >= Enemy.SHOOT_INTERVAL:
                self.shoot_time = 0
                bullet = Bullet(self.x, self.y, self.target.x, self.target.y)
                gfw.top().world.append(bullet)
                self.bullet_count += 1  # 발사된 총알 수 증가
    
    def draw(self):
    # 현재 프레임의 클리핑 영역 설정
        src_x, src_y, src_width, src_height = Enemy.IMAGE_RECTS[self.frame_index]
        self.image.clip_draw(
            src_x, src_y, src_width - src_x, src_height - src_y,
            self.x, self.y,  # 위치
            (src_width - src_x) * Enemy.SCALE,  # 너비 조정
            (src_height - src_y) * Enemy.SCALE  # 높이 조정
        )
    def take_damage(self, damage):
        """적에게 데미지를 입히는 함수"""
        self.hp -= damage
        print(f"Enemy hit! Remaining HP: {self.hp}")
        if self.hp <= 0:
            self.remove()
          
    def drop_item(self):
        if random.random() < Enemy.ITEM_DROP_CHANCE:  # 30% 확률
            item = UpgradeItem(self.x, self.y)  # 아이템 생성
            gfw.top().world.append(item)

    def get_bb(self):
        r = int(30 * Enemy.SCALE)
        return self.x - r, self.y - r, self.x + r, self.y + r
    def remove(self):
        self.drop_item()  # 적이 제거될 때 아이템 드랍 시도
        gfw.top().world.remove(self)

class EnemyGen:
    GEN_INTERVAL = 4.0
    ENEMY_SPACING = 100  # 적끼리의 간격 (픽셀 단위)
    MIN_GEN_INTERVAL = 1.0  # 최소 생성 간격 (난이도 증가에 따라 줄어듦)
    DIFFICULTY_INCREASE_INTERVAL = 10.0

    def __init__(self, target):
        self.time = 0
        self.difficulty_time = 0
        self.target = target  # 플레이어 객체
        self.active = True
        self.gen_interval = EnemyGen.GEN_INTERVAL  # 현재 생성 간격
        self.enemy_positions = []  # 현재 생성된 적들의 위치 목록

    def draw(self):
        pass

    def update(self):
        if not self.active:  # 보스 등장 중이면 적 생성 중지
            return
        self.time += gfw.frame_time
        self.difficulty_time += gfw.frame_time
         # 난이도 증가: 일정 시간이 지나면 생성 간격 줄이기
        if self.difficulty_time >= EnemyGen.DIFFICULTY_INCREASE_INTERVAL:
            self.difficulty_time = 0
            self.gen_interval = max(self.gen_interval - 0.5, EnemyGen.MIN_GEN_INTERVAL)
            Enemy.SHOOT_INTERVAL = max(Enemy.SHOOT_INTERVAL - 0.2, Enemy.MIN_SHOOT_INTERVAL)
            print(f"난이도 증가: 생성 간격 {self.gen_interval}, 발사 간격 {Enemy.SHOOT_INTERVAL}")

    # 적 생성
        if self.time >= self.gen_interval:
            self.spawn_random_enemies()
            self.time = 0

    def spawn_random_enemies(self):
        """랜덤 위치와 개수로 적 생성"""
        screen_width = get_canvas_width()
        num_enemies = random.randint(3, 7)  # 랜덤한 적 수 (1~5개 생성)
        self.enemy_positions = []  # 적 위치 초기화

        for _ in range(num_enemies):
            for attempt in range(10):  # 최대 10번 시도
                x = random.randint(
                    int(Enemy.WIDTH * Enemy.SCALE // 2), 
                    screen_width - int(Enemy.WIDTH * Enemy.SCALE // 2)
                )
                if self.is_position_valid(x):
                    self.enemy_positions.append(x)
                    gfw.top().world.append(Enemy(x, self.target))
                    break
    def is_position_valid(self, x):
        """새로운 x 좌표가 기존 적들과 겹치지 않는지 확인"""
        for existing_x in self.enemy_positions:
            if abs(x - existing_x) < self.ENEMY_SPACING:
                return False
        return True
    def deactivate(self):
        """적 생성을 중지"""
        self.active = False

class Bullet(gfw.Sprite):
    SPEED = 800  # 총알 속도

    def __init__(self, x, y, target_x, target_y):
        super().__init__('res/enemyfire.png', x, y)
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
        