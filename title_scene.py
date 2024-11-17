from gfw import *
from pico2d import *
import main_scene  # 게임 시작 버튼 클릭 시 이동할 씬

import sys
self = sys.modules[__name__]

canvas_width = 625  # 캔버스 크기 설정
canvas_height = 1100
button_gap = 100  # 버튼 간격

center_x = canvas_width // 2
center_y = canvas_height // 2

world = World(2)  # 버튼과 배경을 위한 레이어 생성

class Button(Sprite):
    def __init__(self, bg_image, title, x, y, width, height, on_click):
        super().__init__(None, x, y)
        self.bg = bg_image
        self.width, self.height = width, height
        self.title = title
        self.font = load_font('res/artie-sans.ttf', 30)  
        self.on_click = on_click

    def draw(self):
        # 버튼 배경 그리기
        self.bg.draw(self.x, self.y, self.width, self.height)
        # 버튼 텍스트 그리기
        text_x = self.x - (self.width // 6)  # 대략적인 중앙 위치
        text_y = self.y - 5
        self.font.draw(text_x, text_y, self.title, (255, 255, 255))

    def handle_event(self, e):
        if e.type == SDL_MOUSEBUTTONDOWN and e.button == SDL_BUTTON_LEFT:
            if self.is_inside(e.x, e.y):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def is_inside(self, x, y):
        return (
            self.x - self.width // 2 <= x <= self.x + self.width // 2 and
            self.y - self.height // 2 <= y <= self.y + self.height // 2
        )

def start_game():
    gfw.push(main_scene)  # 게임 씬으로 전환

def quit_game():
    gfw.quit()  # 프로그램 종료

def enter():
    global button_bg
    world.append(Background('res/background.png'), 0)

    title_sprite = Sprite('res/titlename.png', center_x, canvas_height - 150)  # 화면 상단에 위치
    world.append(title_sprite, 0)  # 배경 레이어와 동일하게 설정
    
    # 버튼 배경 이미지 로드
    button_bg = load_image('res/smrec.png')

    # 시작 버튼 추가
    start_button = Button(
        button_bg, "Start", center_x, center_y + button_gap, 400, 80, quit_game
    )
    world.append(start_button, 1)

    # 종료 버튼 추가
    quit_button = Button(
        button_bg, " Quit", center_x, center_y - button_gap, 400, 80, start_game
    )
    world.append(quit_button, 1)

def exit():
    world.clear()

def update():
    pass

def draw():
    world.draw()

def handle_event(e):
    if e.type in [SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP]:
        for btn in world.objects_at(1):
            if btn.handle_event(e):
                return True

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    gfw.start_main_module()
