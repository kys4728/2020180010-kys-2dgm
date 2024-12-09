from pico2d import *
import gfw
from fighter import Fighter

class FighterUI:
    def __init__(self, fighter):
        """Fighter의 상태를 화면에 표시할 UI 생성"""
        self.fighter = fighter
        try:
            self.ui_background_image = gfw.image.load('res/uibg.png')
        except Exception as e:
            print("Error loading UI background image:", e)
            self.ui_background_image = None

        try:
            self.font = load_font('res/artie-sans.ttf', 25)
            self.small_font = load_font('res/artie-sans.ttf', 15)
        except Exception as e:
            print("Error loading fonts:", e)
            self.font = None
            self.small_font = None

    def update(self):
        """FighterUI는 업데이트 로직이 필요 없으므로 빈 메서드로 처리"""
        pass

    def draw_ui_background(self):
        """UI 배경 이미지를 화면 하단에 그리기"""
        if self.ui_background_image:
            self.ui_background_image.draw(get_canvas_width() // 2, 50)

    def draw_health_bar(self):
        """플레이어 체력 게이지를 화면 하단에 표시"""
        canvas_width = get_canvas_width()
        if hasattr(Fighter, 'gauge'):
            rate = max(0, self.fighter.hp / self.fighter.max_hp)
            bar_x = canvas_width // 2
            bar_y = 30
            bar_width = canvas_width - 300
            Fighter.gauge.draw(bar_x, bar_y, bar_width, rate)
        else:
            print("Error: Fighter.gauge is not initialized!")

    def draw_lives(self):
        """플레이어의 남은 목숨을 화면 하단에 표시"""
        x = 20
        y = 30
        if self.small_font:
            self.small_font.draw(x, y, f"Lives: {self.fighter.lives}", (255, 0, 0))

    def draw_level(self):
        """플레이어 레벨을 화면 우측 하단에 표시"""
        canvas_width = get_canvas_width()
        x = canvas_width - 120
        y = 30
        if self.font:
            self.font.draw(x, y, f'Lv: {self.fighter.level}', (0, 120, 255))

    def draw_missile_count(self):
        """남은 미사일 개수를 화면 우측 하단에 표시"""
        canvas_width = get_canvas_width()
        x = canvas_width - 180
        y = 65
        if self.small_font:
            self.small_font.draw(x, y, f'Missiles: {self.fighter.missile_count}/{self.fighter.missile_max_shots}', (255, 255, 255))

    def draw(self):
        """UI를 그리는 메인 메서드"""
        self.draw_ui_background()
        self.draw_health_bar()
        self.draw_lives()
        self.draw_level()
        self.draw_missile_count()

