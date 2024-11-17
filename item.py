from pico2d import *
import gfw

class UpgradeItem(gfw.Sprite):
    def __init__(self, x, y, effect_type):
        super().__init__('res/item.png', x, y)
        self.effect_type = effect_type  # 효과 유형 ('health', 'damage')
        self.speed = 100  # 아이템이 아래로 내려가는 속도
        self.layer_index = gfw.top().world.layer.item

    def update(self):
        self.y -= self.speed * gfw.frame_time
        if self.y < 0:  # 화면 밖으로 나가면 제거
            gfw.top().world.remove(self)

    def get_bb(self):
        r = 20  # 충돌 영역 크기
        return self.x - r, self.y - r, self.x + r, self.y + r
