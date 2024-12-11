from pico2d import *

import time

_running = True
_stack = []

def start(scene):
    import gfw

    w, h = 625, 1100
    if hasattr(scene, 'canvas_width'): w = scene.canvas_width
    if hasattr(scene, 'canvas_height'): h = scene.canvas_height

    open_canvas(w=w, h=h, sync=True)

    gfw.shows_bounding_box = getattr(scene, 'shows_bounding_box', False)
    gfw.shows_object_count = getattr(scene, 'shows_object_count', False)
    if gfw.shows_object_count: 
        _load_system_font()

    push(scene)

    global frame_time
    last_time = time.time()

    while _running:
        now = time.time()
        gfw.frame_time = now - last_time
        last_time = now

        # update() 수행
        if hasattr(_stack[-1], 'world') and _stack[-1].world is not None:
            _stack[-1].world.update()

        # draw() 수행
        clear_canvas()
        if hasattr(_stack[-1], 'world') and _stack[-1].world is not None:
            _stack[-1].world.draw()
        else:
            if hasattr(_stack[-1], 'draw'):
                _stack[-1].draw()  # world 없는 경우 개별 draw 호출
        update_canvas()

        # event 처리
        for e in get_events():
            handled = _stack[-1].handle_event(e)
            if not handled:
                if e.type == SDL_QUIT:
                    quit()
                elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
                    pop()

    while _stack:
        _stack.pop().exit()

    close_canvas()

def start_main_module():
    import sys
    scene = sys.modules['__main__'] 
    # 시스템으로부터 __main__ 이라는 이름을 가진 module 객체를 얻어낸다

    start(scene)

def change(scene):
    if _stack:
        _stack.pop().exit()

    _stack.append(scene)
    print(f'current_scene={scene}')
    scene.enter()

def push(scene):
    if _stack:
        _stack[-1].pause()

    _stack.append(scene)
    print(f'current_scene={scene}')
    scene.enter()

def pop():
    _stack.pop().exit()
    if not _stack:
        quit()
        return

    scene = _stack[-1]
    print(f'current_scene={scene}')
    scene.resume()

def quit():
    global _running
    _running = False

def top():
    return _stack[-1]

def _load_system_font():
    import gfw
    gfw._system_font = None
    paths = [ 'artie-sans.ttf', 'res/artie-sans.ttf', 'C:/Users/ktx39/OneDrive/사진/바탕 화면/2dprogramming/resartie-sans.ttf' ]
    for path in paths:
        try:
            font = load_font(path, 20)
            print(f'System Font Loaded: {path}')
            gfw._system_font = font
            # print(f'{gfw.shows_object_count=} and {gfw._system_font=}')
            break
        except:
            pass
