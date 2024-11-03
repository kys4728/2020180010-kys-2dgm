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
    SPARK_INTERVAL = 0.05
    SPARK_OFFSET = 28
    MISSILE_MAX_SHOTS = 3  # 최대 미사일 발사 횟수
    MISSILE_COOLDOWN = 3.0 # 쿨다운 시간

    def __init__(self):
        super().__init__('res/fighter.png', get_canvas_width() // 2, 80)
        self.dx = 0
        self.dy = 0
        self.speed = 320  # 초당 320 픽셀
        half_width = self.image.w // 2
        self.min_x = half_width
        self.max_x = get_canvas_width() - half_width
        half_height = self.image.h // 2
        self.min_y = half_height
        self.max_y = get_canvas_height() - half_height
        self.laser_time = 0
        self.missile_time = 0
        self.firing_laser = False
        self.firing_missile = False
        self.spark_image = gfw.image.load('res/fire0.png')        
        self.missile_count = Fighter.MISSILE_MAX_SHOTS  # 미사일 카운트 초기화
        self.missile_cooldown_elapsed = 0  # 쿨다운 시간 경과 추적 변수

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
        if self.firing_laser and self.laser_time >= Fighter.LASER_INTERVAL:
            self.fire()
            self.laser_time = 0

        # 미사일 발사 관리
        self.missile_time += gfw.frame_time
        if self.firing_missile and self.missile_count > 0 and self.missile_time >= Fighter.MISSILE_INTERVAL:
            self.launch_missile()
            self.missile_time = 0
            self.missile_count -= 1

            # 모든 미사일을 발사한 경우 쿨다운 초기화
            if self.missile_count == 0:
                self.missile_cooldown_elapsed = 0

        # 쿨다운 시간 경과 누적
        if self.missile_count == 0:
            self.missile_cooldown_elapsed += gfw.frame_time
            if self.missile_cooldown_elapsed >= Fighter.MISSILE_COOLDOWN:
                self.missile_count = Fighter.MISSILE_MAX_SHOTS  # 미사일 카운트 초기화

    def draw(self):
        super().draw()
        if self.laser_time < Fighter.SPARK_INTERVAL:
            self.spark_image.draw(self.x, self.y + Fighter.SPARK_OFFSET)

    def fire(self):
        world = gfw.top().world
        world.append(Bullet(self.x, self.y), world.layer.bullet)

    def launch_missile(self):
        world = gfw.top().world
        world.append(Missile(self.x, self.y), world.layer.bullet)

class Bullet(gfw.Sprite):
    def __init__(self, x, y):
        super().__init__('res/fire1.png', x, y)
        self.speed = 400  # 초당 400 픽셀
        self.max_y = get_canvas_height() + self.image.h
        self.layer_index = gfw.top().world.layer.bullet

    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y > self.max_y:
            gfw.top().world.remove(self)

class Missile(gfw.Sprite):
    def __init__(self, x, y):
        super().__init__('res/missile.png', x, y)
        self.speed = 600  # 초당 600 픽셀
        self.max_y = get_canvas_height() + self.image.h
        self.layer_index = gfw.top().world.layer.bullet

    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y > self.max_y:
            gfw.top().world.remove(self)