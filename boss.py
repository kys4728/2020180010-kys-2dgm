from pico2d import *
import gfw
import random
from item import UpgradeItem

class Boss(gfw.Sprite):
    WIDTH = 113
    HEIGHT = 800
    MOVE_SPEED = 100  # 좌우 이동 속도
    
    MAX_BULLETS = 10
    HP = 1000  # 보스 체력
    SCALE = 1.75  # 보스 크기 확대 배율
    gauge = None
    BASE_BIG_BULLET_INTERVAL = 2.0  # 기본 커다란 투사체 발사 간격
    FAST_BIG_BULLET_INTERVAL = 1.0  # 체력이 낮을 때 커다란 투사체 발사 간격
    BASE_SHOOT_INTERVAL = 1.5  # 기본 총알 발사 간격
    FAST_SHOOT_INTERVAL = 0.8  # 체력이 낮을 때 빠른 발사 간격
    IMAGE_RECTS = [
        (0, 0, 114, 114),
        (0, 114, 114, 228),
        (0, 228, 114, 342),
        (0, 342, 114, 456),
        (0, 456, 114, 570),
        (0, 570, 114, 684),
        (0, 684, 114, 800),
        ]

    def __init__(self, target):
        x = get_canvas_width() // 2
        y = get_canvas_height() - Boss.HEIGHT // 2
        super().__init__('res/bosses.png', x, y)
        self.layer_index = gfw.top().world.layer.boss
        self.speed = -50  # 아래로 내려오는 속도 (느리게)
        self.move_dir = 1  # 좌우 이동 방향 (1: 오른쪽, -1: 왼쪽)
        self.shoot_time = 0
        self.target = target  # 플레이어 객체
        self.bullet_count = 0
        self.hp = Boss.HP
        self.max_health = 50  # 적의 최대 체력
        self.health = self.max_health  # 현재 체력
        self.big_bullet_time = 0  # 커다란 투사체 발사 타이머
        if Boss.gauge == None:
            Boss.gauge = gfw.Gauge('res/bossfg2.png', 'res/bossbg2.png')
        
        self.frame_index = 0  # 현재 프레임 인덱스
        self.frame_time = 0  # 프레임 변경 시간 관리
        self.shoot_interval = Boss.BASE_SHOOT_INTERVAL

    def update(self):
        # 좌우 이동
        self.x += self.move_dir * Boss.MOVE_SPEED * gfw.frame_time
        if self.x < Boss.WIDTH // 2:
            self.x = Boss.WIDTH // 2  # 위치 조정
            self.move_dir = 1  # 오른쪽으로 방향 전환
        elif self.x > get_canvas_width() - Boss.WIDTH // 2:
            self.x = get_canvas_width() - Boss.WIDTH // 2  # 위치 조정
            self.move_dir = -1  # 왼쪽으로 방향 전환

         # 프레임 업데이트
        self.frame_time += gfw.frame_time
        if self.frame_time > 0.1:  # 0.1초마다 프레임 변경
            self.frame_time = 0
            self.frame_index = (self.frame_index + 1) % len(Boss.IMAGE_RECTS)

        # 체력 기반 공격 속도 조정
        if self.hp <= Boss.HP * 0.3:  # 체력이 30% 이하일 때
            self.shoot_interval = Boss.FAST_SHOOT_INTERVAL
            self.big_bullet_interval =  Boss.FAST_BIG_BULLET_INTERVAL
        else:
            self.shoot_interval = Boss.BASE_SHOOT_INTERVAL
            self.big_bullet_interval = Boss.BASE_BIG_BULLET_INTERVAL

        # 총알 발사
        self.shoot_time += gfw.frame_time
        if self.shoot_time >= self.shoot_interval:
            self.shoot_time = 0
            self.shoot_bullets()

        self.big_bullet_time += gfw.frame_time
        if self.big_bullet_time >= self.big_bullet_interval:
            self.big_bullet_time = 0
            self.shoot_big_bullet()

        # 체력이 0 이하라면 제거
        if self.hp <= 0:
            self.remove()
    def draw(self):
        
        # 현재 프레임의 클리핑 영역 설정
        src_x, src_y, src_width, src_height = Boss.IMAGE_RECTS[self.frame_index]
        self.image.clip_draw(
            src_x, src_y, src_width - src_x, src_height - src_y,
            self.x, self.y,  # 위치
            (src_width - src_x) * Boss.SCALE,  # 너비 조정
            (src_height - src_y) * Boss.SCALE  # 높이 조정
        )
        # 체력바를 화면 상단에 고정
        canvas_width = get_canvas_width()
        rate = max(0, self.hp / Boss.HP) # 체력 비율
        bar_x = canvas_width // 2
        bar_y = get_canvas_height() - 30  # 화면 상단에서 30픽셀 아래
        bar_width = canvas_width - 20    # 화면 폭에 맞춰 너비 설정
        
        self.gauge.draw(bar_x, bar_y, bar_width, rate)

    def decrease_health(self, damage):
        self.health -= damage
        print(f"Enemy Health: {self.health}/{self.max_health}")
        if self.health <= 0:
            self.remove()          

    def shoot_bullets(self):
        for angle in range(0, 360, 45):  # 원형으로 총알 발사
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            bullet = BossBullet(self.x, self.y, dx, dy)
            gfw.top().world.append(bullet)

    def shoot_big_bullet(self):
        print("Boss is firing a big bullet!")
        bullet = BigBossBullet(self.x, self.y, self.target.x, self.target.y)
        gfw.top().world.append(bullet)

    def take_damage(self, damage):
        """보스 체력 감소 처리"""
        self.hp -= damage
        self.health -= damage
        print(f"Boss HP: {self.hp}")
        if self.hp <= 0:
            print("Boss Defeated!")
            self.remove()
    def get_bb(self):
        r = int(Boss.WIDTH // 4 * Boss.SCALE)
        return self.x - r, self.y - r, self.x + r, self.y + r

    def take_damage(self, damage):
        self.hp -= damage

    def remove(self):
        print("Boss removed")
        gfw.top().world.remove(self)
        
        # 적 생성 재개
        enemy_gen = gfw.top().world.objects_at(gfw.top().world.layer.controller)[0]
        if isinstance(enemy_gen, EnemyGen):
            enemy_gen.reactivate()

class BossBullet(gfw.Sprite):
    SPEED = 100  # 총알 속도

    def __init__(self, x, y, dx, dy):
        super().__init__('res/enemyfire.png', x, y)
        self.vx, self.vy = BossBullet.SPEED * dx, BossBullet.SPEED * dy
        self.layer_index = gfw.top().world.layer.enemy_bullet
        self.is_boss_bullet = True 

    def update(self):
        self.x += self.vx  * gfw.frame_time
        self.y += self.vy  * gfw.frame_time
        if self.x < 0 or self.x > get_canvas_width() or self.y < 0 or self.y > get_canvas_height():
            gfw.top().world.remove(self)

    def get_bb(self):
        r = 10  # 충돌 영역 반경
        return self.x - r, self.y - r, self.x + r, self.y + r

class BigBossBullet(gfw.Sprite):
    SPEED = 300  # 커다란 투사체 속도
    ROTATE_SPEED = 180

    def __init__(self, x, y, target_x, target_y):
        super().__init__('res/bossbigfire.png', x, y)
        # 플레이어를 향한 방향 벡터 계산
        dx, dy = target_x - x, target_y - y
        distance = (dx**2 + dy**2)**0.5
        self.vx, self.vy = BigBossBullet.SPEED * dx / distance, BigBossBullet.SPEED * dy / distance
        self.angle = 0  # 초기 각도
        self.layer_index = gfw.top().world.layer.boss_bullet
        self.is_boss_bullet = True

    def update(self):
        self.x += self.vx * gfw.frame_time
        self.y += self.vy * gfw.frame_time
        self.angle = (self.angle + BigBossBullet.ROTATE_SPEED * gfw.frame_time) % 360
        # 화면 밖으로 나가면 제거
        if self.x < 0 or self.x > get_canvas_width() or self.y < 0 or self.y > get_canvas_height():
            gfw.top().world.remove(self)

    def get_bb(self):
        r = 20  # 커다란 투사체 충돌 영역 반경
        return self.x - r, self.y - r, self.x + r, self.y + r

    def draw(self):
        # 회전된 이미지 그리기
        self.image.composite_draw(math.radians(self.angle), '', self.x, self.y)
        draw_rectangle(*self.get_bb())  # 디버깅용 충돌 박스
