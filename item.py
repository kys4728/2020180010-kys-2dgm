from pico2d import *
import gfw

class UpgradeItem(gfw.Sprite):
    SPEED = 100  # 아래로 떨어지는 속도

    def __init__(self, x, y, effect_type='health'):  # 기본값으로 'health' 설정
        super().__init__('res/item.png', x, y)
        self.effect_type = effect_type  # 고정된 아이템 효과 유형
        self.layer_index = gfw.top().world.layer.item  # 레이어 인덱스 설정

    def update(self):
        self.y -= UpgradeItem.SPEED * gfw.frame_time
        if self.y < 0:
            gfw.top().world.remove(self)

    def get_bb(self):
        r = 15  # 아이템 크기
        return self.x - r, self.y - r, self.x + r, self.y + r

    def apply_effect(self, player):
        """아이템 효과 적용"""
        if self.effect_type == 'health':
            player.hp = min(player.hp + 10, 100)  # 체력 최대값은 100
            print(f"Health item collected! Health increased: {player.hp}")
        elif self.effect_type == 'damage':
            player.collect_item()  # 아이템 수집 처리
            print(f"Damage item collected! Current item count: {player.item_count}")
