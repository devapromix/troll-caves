from graphics.color import Color
from mobs.abilities.ability import Ability

class BashChests(Ability):
    def __init__(self, player):
        from mobs.player import Classes
        super().__init__(player)
        self.game_class = Classes.FIGHTER
        self.need_mana = 3
        
    def use(self):
        from common.game import message
        from maps.objects import Container
        if super().use():
            return
        if self.player.tile.obj == None or not isinstance(self.player.tile.obj, Container):
            message('Stand on the chest to break it.', Color.ERROR.value)
            return
        self.player.tile.obj.bash(self.player)

















