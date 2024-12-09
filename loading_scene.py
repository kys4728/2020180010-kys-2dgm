import gfw
from pico2d import *
import title_scene
import time
import sys

self = sys.modules[__name__]

canvas_width = title_scene.canvas_width
canvas_height = title_scene.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

world = gfw.World(2)

def enter():
    self.gauge = gfw.Gauge('res/pgfg.png', 'res/pgbg.png')
    self.font = load_font('res/artie-sans.ttf', 10)

    world.append(gfw.Sprite('res/ldback.png', center_x, center_y), 0)
    world.append(self, 1)

    self.image_index = 0
    self.image_count = len(IMAGE_FILES)
    self.images = iter(IMAGE_FILES)
    self.file = ''
    self.progress_y = canvas_height // 2
    self.progress_w = canvas_width * 2 // 3
    self.other_x = center_x - self.progress_w // 2
    self.color = (87, 41, 138) #57298a
    # print(len(list(images)))

def update():
    self.file = next(images, None)
    if file is None:
        gfw.change(title_scene)
        return
    print(f'Loading {file=}')
    gfw.image.load(file)
    time.sleep(0.01)
    self.image_index += 1

def draw():
    progress = image_index / image_count
    gauge.draw(center_x, progress_y, progress_w, progress)
    font.draw(other_x, progress_y - 10, self.file, self.color)
    font.draw(other_x, progress_y + 10, '%.1f%%' % (progress * 100), self.color)

def exit():
    gfw.image.unload('res/ldback.png')
    gfw.image.unload('res/pgbg.png')
    gfw.image.unload('res/pgfg.png')
    world.clear()
    del self.font

def handle_event(e):
    pass
IMAGE_FILES = [
    "res/background.png",
    "res/boss.png",
    "res/bossbigfire.png",
    "res/bossfg2.png",
    "res/bossbg2.png",
    "res/enemy.png",
    "res/enemys.png",
    "res/enemyfire.png",
    "res/fighiter.png",
    "res/fighter.png",
    "res/fire0.png",
    "res/fire1.png",
    "res/fire2.png",
    "res/fire3.png",
    "res/healthbar.png",
    "res/item.png",
    "res/ldback.png",
    "res/missile.png",
    "res/number.png",
    "res/pgbg.png",
    "res/pgfg.png",
    "res/wreck.png",
    "res/smrec.png",
    "res/titlename.png",
]
if __name__ == '__main__':
    gfw.start_main_module()