from pico2d import *
import gfw
import title_scene
import main_scene
import boss
import c_check
def enter():
    global game_over_image, font, font_large
    
    game_over_image = gfw.image.load('res/gameover.png')
    font = gfw.font.load('res/artie-sans.ttf', 25)
    font_large = gfw.font.load('res/artie-sans.ttf', 30)

    # world 객체 초기화
    gfw.world = gfw.World()

def start_game():
    gfw.change(title_scene)  # 타이틀 화면으로 이동

def quit_game():
    gfw.quit()  # 프로그램 종료

def exit():
    global game_over_image, font, font_large
    del game_over_image
    del font
    del font_large

def update():
    pass  # 게임 오버 화면에서는 업데이트 필요 없음

def draw():
    clear_canvas()
    game_over_image.draw(625 // 2, 1100 // 2)  # 화면 중앙에 이미지 출력

    # "Thanks for playing!" 텍스트
    over_text = "Thanks for playing!"
    x = (625 - len(over_text) * 15) // 5  # 글자당 약 15픽셀로 텍스트 중앙 정렬
    y = 1100 * 3 // 4  # 화면 상단 3/4 위치
    font_large.draw(x, y, over_text, (25, 215, 150))

    # "Press R to title" 텍스트
    main_text = "Press R to title"
    x = (625 - len(main_text) * 15) // 2.5  # 글자당 약 15픽셀로 텍스트 중앙 정렬
    y = 1100 // 2  # 화면 중앙
    font.draw(x, y, main_text, (255, 255, 255))
    update_canvas()

def handle_event(e):
    if e.type == SDL_QUIT:
        quit_game()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_r:
            start_game()

def pause():
    pass

def resume():
    pass

if __name__ == "__main__":
    gfw.start_main_module()
