from pico2d import *
import gfw

class Fighter(gfw.Sprite):
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-1, 0),
        (SDL_KEYDOWN, SDLK_RIGHT): (1, 0),
        (SDL_KEYUP, SDLK_LEFT):    (1, 0),
        (SDL_KEYUP, SDLK_RIGHT):   (-1, 0),
        (SDL_KEYDOWN, SDLK_UP):    (0, 1),
        (SDL_KEYDOWN, SDLK_DOWN):  (0, -1),
        (SDL_KEYUP, SDLK_UP):      (0, -1),
        (SDL_KEYUP, SDLK_DOWN):    (0, 1),
    }
    LASER_INTERVAL = 0.25
    MISSILE_INTERVAL = 0.5
    SPECIAL_LASER_INTERVAL = 0.5
    SPARK_INTERVAL = 0.05
    SPARK_OFFSET = 28
    MISSILE_MAX_SHOTS = 3
    MISSILE_COOLDOWN = 3.0

    def __init__(self):
        super().__init__('res/fighter.png', get_canvas_width() // 2, 80)
        self.layer_index = gfw.top().world.layer.fighter
        self.dx = 0
        self.dy = 0
        self.speed = 320  # 초당 320 픽셀
        self.width = 72
        half_width = self.width // 2
        self.min_x = half_width
        self.max_x = get_canvas_width() - half_width
        half_height = self.image.h // 2
        self.min_y = half_height
        self.max_y = get_canvas_height() - half_height
        self.laser_time = 0
        self.missile_time = 0
        self.special_laser_time = 0
        self.firing_laser = False
        self.firing_missile = False
        self.spark_image = gfw.image.load('res/fire0.png')
        self.missile_count = Fighter.MISSILE_MAX_SHOTS
        self.missile_cooldown_elapsed = 0
        self.hp = 100
        self.level = 1
        self.item_count = 0  # 아이템 획득 카운트
        self.bullet_power = 10  # 기본 탄환 공격력
        self.missile_power = 100 
        self.damage = self.calculate_damage()
        self.missile_max_shots = Fighter.MISSILE_MAX_SHOTS

    def calculate_damage(self):
        """현재 레벨에 따라 데미지를 계산합니다."""
        self.missile_max_shots = Fighter.MISSILE_MAX_SHOTS + (self.level - 1)  # 레벨 2부터 미사일 추가
        return 10 + (self.level - 1) * 5

    def level_up(self):
        """전투기의 레벨을 증가시킵니다. 최대 레벨은 3입니다."""
        if self.level >= 3:
            print("Max Level reached! No further leveling up.")
            return
        self.level += 1
        self.damage = self.calculate_damage()
        self.bullet_power += 5  # 탄환 공격력 증가
        self.missile_power += 50  # 미사일 공격력 증가
        self.missile_count = self.missile_max_shots
        print(f"Level Up! Current level: {self.level}, Damage: {self.damage}")

    def collect_item(self):
        """아이템을 수집했을 때 호출됩니다."""
        self.item_count += 1
        print(f"Item Collected! Current item count: {self.item_count}")
        if self.item_count >= 5:  # 아이템 5개 단위로 레벨 업
            self.item_count = 0  # 카운트 초기화
            self.level_up()



    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Fighter.KEY_MAP:
            dx, dy = Fighter.KEY_MAP[pair]
            self.dx += dx
            self.dy += dy
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_z:
                self.firing_laser = True
            elif e.key == SDLK_x:
                self.firing_missile = True
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_z:
                self.firing_laser = False
            elif e.key == SDLK_x:
                self.firing_missile = False

    def update(self):
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        self.x = clamp(self.min_x, self.x, self.max_x)
        self.y = clamp(self.min_y, self.y, self.max_y)

        self.laser_time += gfw.frame_time
        self.special_laser_time += gfw.frame_time
        if self.firing_laser and self.laser_time >= Fighter.LASER_INTERVAL:
            self.fire()
            self.laser_time = 0

        self.missile_time += gfw.frame_time
        if self.firing_missile and self.missile_count > 0 and self.missile_time >= Fighter.MISSILE_INTERVAL:
            self.launch_missile()
            self.missile_time = 0
            self.missile_count -= 1

            if self.missile_count == 0:
                self.missile_cooldown_elapsed = 0

        if self.missile_count == 0:
            self.missile_cooldown_elapsed += gfw.frame_time
            if self.missile_cooldown_elapsed >= Fighter.MISSILE_COOLDOWN:
                self.missile_count = self.missile_max_shots 

    def draw(self):
        super().draw()
        if self.laser_time < Fighter.SPARK_INTERVAL:
            self.spark_image.draw(self.x, self.y + Fighter.SPARK_OFFSET)

    def fire(self):
        """플레이어가 발사하는 탄환을 생성"""
        world = gfw.top().world

    # 기본 탄환 발사
        world.append(Bullet(self.x, self.y, self.bullet_power), world.layer.bullet)

    # 레벨 2 이상이면 대각선 탄환 추가
        if self.level >= 2:
            diagonal_power = self.bullet_power // 2
            world.append(DiagonalBullet(self.x - 10, self.y, dx=-100, attack_power=self.bullet_power))  # 왼쪽 대각선
            world.append(DiagonalBullet(self.x + 10, self.y, dx=100, attack_power=self.bullet_power))   # 오른쪽 대각선

        if self.level == 3:
            if self.special_laser_time >= Fighter.SPECIAL_LASER_INTERVAL:
                special_bullet_power = int(self.bullet_power * 1.5)  # 특수 탄환 공격력
                world.append(SpecialBullet(self.x, self.y, special_bullet_power), world.layer.bullet)
                self.special_laser_time = 0  # 특수 탄 발사 시간 초기화
        # 레벨 3에서는 정면 탄환에 새로운 이미지 사용
        else:
        # 정면 탄환 (레벨 1 및 2)
            world.append(Bullet(self.x, self.y, self.bullet_power), world.layer.bullet)


            print(f"Fired bullets at level {self.level}")
        if self.level >= 3:
            print(f"Special bullets with attack power: {self.bullet_power}")
        elif self.level >= 2:
            print(f"Diagonal bullets with attack power: {diagonal_power}")

    def launch_missile(self):
        world = gfw.top().world
        world.append(Missile(self.x, self.y, self.missile_power), world.layer.bullet)
        print(f"Missile launched with attack power: {self.missile_power}")
    def get_bb(self):
        r = 10  # 커다란 투사체 충돌 영역 반경
        return self.x - r, self.y - r, self.x + r, self.y + r

class Bullet(gfw.Sprite):
    def __init__(self, x, y, attack_power):
        super().__init__('res/fire1.png', x, y)
        self.speed = 400  # 초당 400 픽셀
        self.max_y = get_canvas_height() + self.image.h
        self.attack_power = attack_power
        self.layer_index = gfw.top().world.layer.bullet

    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y > self.max_y:
            gfw.top().world.remove(self)
    def get_bb(self):
        r = 5  # 충돌 영역 반경
        return self.x - r, self.y - r, self.x + r, self.y + r

class DiagonalBullet(gfw.Sprite):
    def __init__(self, x, y, dx, attack_power):
        super().__init__('res/fire2.png', x, y)
        self.dx = dx  # 탄환의 x축 이동 속도
        self.speed = 400  # y축 이동 속도
        self.max_y = get_canvas_height() + self.image.h
        self.attack_power = attack_power
        self.layer_index = gfw.top().world.layer.bullet

    def update(self):
        self.x += self.dx * gfw.frame_time
        self.y += self.speed * gfw.frame_time
        if self.y > self.max_y or self.x < 0 or self.x > get_canvas_width():
            gfw.top().world.remove(self)

    def get_bb(self):
        r = 5
        return self.x - r, self.y - r, self.x + r, self.y + r
class SpecialBullet(gfw.Sprite):
    def __init__(self, x, y, attack_power):
        super().__init__('res/fire3.png', x, y)  # 레벨 3에서 사용할 새로운 이미지
        self.speed = 500  # 레벨 3 탄환은 더 빠르게
        self.attack_power = attack_power
        self.max_y = get_canvas_height() + self.image.h
        self.layer_index = gfw.top().world.layer.bullet

    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y > self.max_y:
            gfw.top().world.remove(self)

    def get_bb(self):
        r = 7  # 충돌 영역 크기
        return self.x - r, self.y - r, self.x + r, self.y + r


class Missile(gfw.Sprite):
    def __init__(self, x, y, attack_power):
        super().__init__('res/missile.png', x, y)
        self.speed = 600  # 초당 600 픽셀
        self.attack_power = attack_power
        self.max_y = get_canvas_height() + self.image.h
        self.layer_index = gfw.top().world.layer.bullet

    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y > self.max_y:
            gfw.top().world.remove(self)