from .LightSource import LightSource
from .Weapon import *
from .Weapon import Weapon
from .Item import Item
from .Equipment import Equipment
from common.spells import *

# --- DAGGER --- #

class Dagger(Weapon):
    ABSTRACT = True
    poison = 0

    def __init__(self):
        super(Dagger, self).__init__()
        if rand(1, 5) == 1:
            if self.suffix("rogues"):
                self.speed += 1
        if rand(1, 9) == 1:
            if self.suffix("assassins"):
                a, b, c = self.dice
                b += rand(1, 2)
                self.dice = a, b, c
        if rand(1, 15) == 1:
            if self.suffix("doom"):
                a, b, c = self.dice
                c += rand(2, 4)
                self.dice = a, b, c

    @property
    def mod_descr(self):    
        s = ''
        if self.speed != 0:
            s += ' %s%d speed' % ('+' if self.speed > 0 else '', self.speed)
        if self.poison > 0:
            s += ' poisons'
        return " " + s.strip()

    def on_equip(self, player):
        if not player.can_use_dagger:
            message("You don't know how to use daggers!", COLOR_ERROR)
            return False
        super(Dagger, self).on_equip(player)
        player.holding_dagger = True
        player.poison = self.poison
        return True
        
    def on_unequip(self, player):
        super(Dagger, self).on_unequip(player)
        player.holding_dagger = False
        player.poison = 0
    
class EliteDagger(Dagger):
    ABSTRACT = True
    rarity = 10

class UniqueDagger(EliteDagger):
    ABSTRACT = True
    rarity = 15

# --- STAFF --- #

class Staff(Weapon):
    ABSTRACT = True
    mana = 0
    magic = 1
    
    def __init__(self):
        super(Staff, self).__init__()
        if rand(1, 3) == 1:
            if self.suffix("eclipse"):
                self.mana += rand(self.magic, self.magic * 3)
        if rand(1, 9) == 1:
            if self.suffix("wizards"):
                self.mana += rand(self.magic * 2, self.magic * 5)

    @property
    def mod_descr(self):    
        s = ''
        if self.mana != 0:
            s += ' %s%d mana' % ('+' if self.mana > 0 else '', self.mana)
        if self.speed != 0:
            s += ' %s%d speed' % ('+' if self.speed > 0 else '', self.speed)
        if self.magic != 0:
            s += ' %s%d magic' % ('+' if self.magic > 0 else '', self.magic)
        return " " + s.strip()
        
    def on_equip(self, player):
        if not player.can_use_staff:
            message("You don't know how to use staves!", COLOR_ERROR)
            return False
        super(Staff, self).on_equip(player)
        player.mana.inc(self.mana)
        player.magic += self.magic
        return True
    
    def on_unequip(self, player):    
        super(Staff, self).on_unequip(player)
        player.mana.dec(self.mana)
        player.magic -= self.magic

class EliteStaff(Staff):
    ABSTRACT = True
    rarity = 10

class UniqueStaff(EliteStaff):
    ABSTRACT = True
    rarity = 15

# --- ARMOR --- #

class Armor(Equipment):
    ABSTRACT = True
    armor = 0

    def __init__(self):
        super(Armor, self).__init__()
        if rand(1, 5) == 1:
            if self.suffix("defense"):
                self.armor = self.armor + rand(round(self.armor / 5), round(self.armor / 3))
        if rand(1, 11) == 1:
            if self.suffix("protection"):
                self.armor = self.armor + rand(round(self.armor / 3), round(self.armor / 2))

    @property
    def descr(self):
        return '%s (%s)' % (self.name, self.mod_descr)

    @property
    def mod_descr(self):
        s = ''
        if self.armor != 0:
            s += ' %s%d armor' % ('+' if self.armor > 0 else '', self.armor)
        return s.strip()

    def on_equip(self, player):
        player.armor += self.armor
        return True

    def on_unequip(self, player):
        player.armor -= self.armor

# --- CLOTH ARMOR --- #

class ClothArmor(Armor):
    ABSTRACT = True
    slot = 'a'
    mana = 0
    magic = 1

    def __init__(self):
        super(ClothArmor, self).__init__()
        if rand(1, 3) == 1:
            if self.suffix("thought"):
                self.mana += rand(round(self.mana / 3), round(self.mana / 2))
        if rand(1, 6) == 1:
            if self.suffix("moon"):
                self.mana += rand(round(self.mana / 2), self.mana)

    def on_equip(self, player):
        if not player.can_wear_cloth_armor:
            message("You don't know how to use cloth armor!", COLOR_ERROR)
            return False
        super(ClothArmor, self).on_equip(player)
        player.mana.inc(self.mana)
        return True

    def on_unequip(self, player):    
        super(ClothArmor, self).on_unequip(player)
        player.mana.dec(self.mana)

    @property
    def mod_descr(self):    
        s = ''
        if self.armor != 0:
            s += ' %s%d armor' % ('+' if self.armor > 0 else '', self.armor)
        if self.mana != 0:
            s += ' %s%d mana' % ('+' if self.mana > 0 else '', self.mana)
        if self.speed != 0:
            s += ' %s%d speed' % ('+' if self.speed > 0 else '', self.speed)
        if self.magic != 0:
            s += ' %s%d magic' % ('+' if self.magic > 0 else '', self.magic)
        return s.strip()
        
class EliteClothArmor(ClothArmor):
    ABSTRACT = True
    rarity = 10

class UniqueClothArmor(EliteClothArmor):
    ABSTRACT = True
    rarity = 15

# --- LEATHER ARMOR --- #

class LeatherArmor(Armor):
    ABSTRACT = True
    slot = 'a'

    def on_equip(self, player):
        if not player.can_wear_leather_armor:
            message("You don't know how to use leather armor!", COLOR_ERROR)
            return False
        super(LeatherArmor, self).on_equip(player)
        return True

    def on_unequip(self, player):    
        super(LeatherArmor, self).on_unequip(player)

class EliteLeatherArmor(LeatherArmor):
    ABSTRACT = True
    rarity = 10

class UniqueLeatherArmor(EliteLeatherArmor):
    ABSTRACT = True
    rarity = 15

# --- MAIL ARMOR --- #

class MailArmor(Armor):
    ABSTRACT = True
    slot = 'a'

    def on_equip(self, player):
        if not player.can_wear_mail_armor:
            message("You don't know how to use mail armor!", COLOR_ERROR)
            return False
        super(MailArmor, self).on_equip(player)
        return True

    def on_unequip(self, player):    
        super(MailArmor, self).on_unequip(player)

class EliteMailArmor(MailArmor):
    ABSTRACT = True
    rarity = 10

class UniqueMailArmor(EliteMailArmor):
    ABSTRACT = True
    rarity = 15

# --- HELM --- #

class Helm(Armor):
    ABSTRACT = True
    slot = 'h'
    plural = True
    radius = 0

    def __init__(self):
        super(Helm, self).__init__()
        if rand(1, 5) == 1:
            if self.suffix("light"):
                self.radius += 1

    def on_equip(self, player):
        super(Helm, self).on_equip(player)
        player.radius += self.radius
        return True

    def on_unequip(self, player):    
        super(Helm, self).on_unequip(player)
        player.radius -= self.radius

class EliteHelm(Helm):
    ABSTRACT = True
    rarity = 10

    def __init__(self):
        super(EliteHelm, self).__init__()
        if rand(1, 9) == 1:
            if self.suffix("sun"):
                self.radius += 2

class UniqueHelm(EliteHelm):
    ABSTRACT = True
    rarity = 15

# --- BOOTS --- #

class Boots(Armor):
    ABSTRACT = True
    slot = 'b'
    plural = True

class EliteBoots(Boots):
    ABSTRACT = True
    rarity = 10

    def __init__(self):
        super(EliteBoots, self).__init__()
        if rand(1, 9) == 1:
            if self.suffix("speed"):
                self.speed += 1

class UniqueBoots(EliteBoots):
    ABSTRACT = True
    rarity = 15

# --- SHIELD --- #

class Shield(Armor):
    ABSTRACT = True
    slot = 'o'
    rarity = 5
    blocking = 10

    def __init__(self):
        super(Shield, self).__init__()

    @property
    def mod_descr(self):    
        s = ''
        s += ' +%d armor' % (self.armor)
        s += ' +%d blocking' % (self.blocking)
        return s.strip()

    def on_equip(self, player):
        if not player.can_use_shield:
            message("You don't know how to use shields!", COLOR_ERROR)
            return False
        super(Shield, self).on_equip(player)
        player.blocking += self.blocking
        return True
    
    def on_unequip(self, player):    
        super(Shield, self).on_unequip(player)
        player.blocking -= self.blocking

# --- BOOK --- #

class Book(Item):
    ABSTRACT = True

    def on_use(self, player):
        if player.try_learn_spell(self.spell):
            player.items.remove(self)

# --- CRAFT ITEM --- #

class CraftItem(Item):
    ABSTRACT = True
    
# --- POTION --- #

class Potion(Item):
    ABSTRACT = True

    def on_use(self, player):
        message('You drink the %s.' % self.name)
        player.items.remove(self)

# --- POISON POTION --- #

class PoisonPotion(Potion):
    ABSTRACT = True
    poison = 1

    def _failed(self):
        message("Failed attempt to make the weapon poisonous!", COLOR_ERROR)

    def on_use(self, player):
        from mobs.player import THIEF
        super(PoisonPotion, self).on_use(player)
        if player.game_class == THIEF:
            if player.holding_dagger:
                dagger = player.equipment['w']
                if dagger and dagger.suffix("venom"):
                    dagger.poison = self.poison
                    player.poison = dagger.poison
                    message("You smeared the dagger with poison!", COLOR_ALERT)
                else:
                    self._failed()
            else:
                self._failed()
        else:
            player.poisoned = self.poison

# --- SCROLL --- #

class Scroll(Item):
    ABSTRACT = True

    def on_use(self, player):
        if self.spell.on_use(self.spell(), player):
            player.items.remove(self)

# --- LIGHT SOURCES --- # 

class Torch(LightSource):
    name = 'torch'
    glyph = '|', T.dark_orange
    dungeons = 1, 12
    turns = 150
    light_range = 6

class Lamp(LightSource):
    name = 'lamp'
    glyph = 'o', T.dark_yellow
    dungeons = 4, 12
    rarity = 5
    turns = 300
    light_range = 8

class Lamp2(LightSource):
    name = 'lamp2'
    glyph = '0', T.light_yellow
    dungeons = 8, 12
    rarity = 15
    turns = 500
    light_range = 10

# --- DAGGERS --- #

class SmallDagger(Dagger):
    name = 'small dagger'
    glyph = '(', T.light_grey
    speed = 1
    dice = 1, 2, 1
    dungeons = 1, 2

class Dirk(Dagger):
    name = 'dirk'
    glyph = '(', T.light_pink
    speed = 1
    dice = 2, 2, 2
    dungeons = 3, 4

class Kris(Dagger):
    name = 'kris'
    glyph = '(', T.light_green
    speed = 1
    dice = 2, 3, 3
    dungeons = 5, 6

class Rondel(Dagger):
    name = 'rondel'
    glyph = '(', T.light_blue
    speed = 1
    dice = 3, 3, 3
    dungeons = 7, 8

class BloodDagger(Dagger):
    name = 'blood dagger'
    glyph = '(', T.red
    speed = 1
    dice = 4, 4, 0
    dungeons = 9, 10

class IceDagger(Dagger):
    name = 'ice dagger'
    glyph = '(', T.white
    speed = 1
    dice = 3, 5, 4
    dungeons = 11, 12

class BloodSpike(EliteDagger):
    name = 'blood spike'
    glyph = '(', T.light_red
    speed = 2
    dice = 3, 5, 1
    dungeons = 7, 9

class MithrilBlade(EliteDagger):
    name = 'mithril blade'
    glyph = '(', T.light_sky
    speed = 2
    dice = 4, 5, 0
    dungeons = 9, 11

class DivineStiletto(UniqueDagger):
    name = 'divine stiletto'
    glyph = '(', T.cyan
    speed = 3
    dice = 3, 5, 7
    dungeons = 11, 12

# --- MACES --- #

class Club(Weapon):
    name = 'club'
    glyph = '/', T.dark_orange
    speed = -1
    dice = 1, 3, 0
    dungeons = 1, 2

class KillerClub(Weapon):
    name = 'killer club'
    glyph = '/', T.dark_orange
    speed = -1
    dice = 1, 4, 3
    dungeons = 3, 4

class SpikedClub(Weapon):
    name = 'spiked club'
    glyph = '/', T.light_orange
    dice = 2, 4, 2
    dungeons = 5, 6

class Mace(Weapon):
    name = 'mace'
    glyph = '/', T.light_gray
    dice = 2, 5, 3
    dungeons = 7, 8

class Hammer(Weapon):
    name = 'hammer'
    glyph = '/', T.light_gray
    dice = 2, 6, 5
    dungeons = 9, 10

class FireHammer(Weapon):
    name = 'fire hammer'
    glyph = '/', T.light_red
    dice = 2, 8, 4
    dungeons = 11, 12

class DeathMace(EliteWeapon):
    name = 'death mace'
    glyph = '/', T.light_gray
    dice = 2, 5, 6
    dungeons = 7, 9

class ThunderMaul(EliteWeapon):
    name = 'thunder maul'
    glyph = '/', T.blue
    dice = 3, 5, 5
    dungeons = 9, 11

class LegendaryMallet(UniqueWeapon):
    name = 'legendary mallet'
    glyph = '/', T.cyan
    speed = 1
    dice = 3, 6, 5
    dungeons = 11, 12

# --- SWORDS --- #

class ShortSword(Weapon):
    name = 'short sword'
    glyph = '(', T.lighter_blue
    dice = 1, 3, 0
    dungeons = 1, 2

class Falchion(Weapon):
    name = 'falchion'
    glyph = '(', T.lighter_blue
    dice = 1, 6, 1
    dungeons = 3, 4

class BroadSword(Weapon):
    name = 'broad sword'
    glyph = '(', T.lighter_blue
    dice = 2, 4, 2
    dungeons = 5, 6

class CrusaderSword(Weapon):
    name = 'crusader sword'
    glyph = '(', T.lighter_green
    dice = 2, 5, 4
    dungeons = 7, 8

class HeroicSword(Weapon):
    name = 'heroic sword'
    glyph = '(', T.light_blue
    dice = 3, 5, 3
    dungeons = 9, 10

class WarSword(Weapon):
    name = 'war sword'
    glyph = '(', T.lighter_blue
    dice = 3, 6, 3
    dungeons = 11, 12

class RuneSword(EliteWeapon):
    name = 'rune sword'
    glyph = '(', T.dark_orange
    dice = 2, 5, 6
    dungeons = 7, 9

class MithrilSword(EliteWeapon):
    name = 'mithril sword'
    glyph = '(', T.light_sky
    dice = 3, 5, 6
    dungeons = 9, 11

class AncientSword(UniqueWeapon):
    name = 'ancient sword'
    glyph = '(', T.cyan
    speed = 1
    dice = 2, 8, 7
    dungeons = 11, 12

# --- AXES --- #

class HandAxe(Weapon):
    name = 'hand axe'
    glyph = '(', T.grey
    speed = -1
    dice = 1, 2, 1
    dungeons = 1, 2

class DoubleAxe(Weapon):
    name = 'double axe'
    glyph = '(', T.grey
    dice = 1, 3, 4
    dungeons = 3, 4

class WarAxe(Weapon):
    name = 'war axe'
    glyph = '(', T.grey
    dice = 1, 4, 6
    dungeons = 5, 6

class BattleAxe(Weapon):
    name = 'battle axe'
    glyph = '(', T.grey
    dice = 2, 4, 5
    dungeons = 7, 8

class GrandAxe(Weapon):
    name = 'grand axe'
    glyph = '(', T.grey
    dice = 2, 6, 5
    dungeons = 9, 10

class SupremeAxe(Weapon):
    name = 'supreme axe'
    glyph = '(', T.grey
    dice = 2, 7, 6
    dungeons = 11, 12

class GreatAxe(EliteWeapon):
    name = 'great axe'
    glyph = '(', T.light_gray
    dice = 2, 5, 6
    dungeons = 7, 9

class GiantAxe(EliteWeapon):
    name = 'giant axe'
    glyph = '(', T.blue
    dice = 2, 6, 7
    dungeons = 9, 11

class GloriousAxe(UniqueWeapon):
    name = 'glorious axe'
    glyph = '(', T.cyan
    speed = 1
    dice = 2, 7, 10
    dungeons = 11, 12

# --- SPEARS --- #

class HuntingSpear(Weapon):
    name = 'hunting spear'
    glyph = '/', T.light_orange
    dice = 1, 3, 0
    dungeons = 1, 2

class Pilum(Weapon):
    name = 'pilum'
    glyph = '/', T.light_orange
    dice = 1, 5, 2
    dungeons = 3, 4

class Harpoon(Weapon):
    name = 'harpoon'
    glyph = '/', T.light_orange
    dice = 2, 4, 2
    dungeons = 5, 6

class SerpentSpear(Weapon):
    name = 'serpent spear'
    glyph = '/', T.light_orange
    dice = 2, 5, 3
    dungeons = 7, 8

class WarSpear(Weapon):
    name = 'war spear'
    glyph = '/', T.light_orange
    dice = 2, 6, 5
    dungeons = 9, 10

class SacredSpear(Weapon):
    name = 'sacred spear'
    glyph = '/', T.light_orange
    dice = 2, 6, 8
    dungeons = 11, 12

class GhostSpear(EliteWeapon):
    name = 'ghost spear'
    glyph = '/', T.light_grey
    speed = 1
    dice = 2, 6, 4
    dungeons = 7, 9

class MithrilMancatcher(EliteWeapon):
    name = 'mithril mancatcher'
    glyph = '/', T.light_sky
    speed = 1
    dice = 2, 8, 4
    dungeons = 9, 11

class AncientPike(UniqueWeapon):
    name = 'ancient pike'
    glyph = '/', T.cyan
    speed = 2
    dice = 2, 9, 6
    dungeons = 11, 12

# --- STAVES --- #

class ShortStaff(Staff):
    name = 'short staff'
    glyph = '/', T.light_orange
    speed = -1
    magic = 1
    dice = 1, 2, 1
    mana = 3
    dungeons = 1, 2

class LongStaff(Staff):
    name = 'long staff'
    glyph = '/', T.lighter_blue
    speed = -1
    magic = 2
    dice = 1, 4, 3
    mana = 6
    dungeons = 3, 4

class EmeraldStaff(Staff):
    name = 'emerald staff'
    glyph = '/', T.lighter_green
    speed = -1
    magic = 3
    dice = 2, 4, 3
    mana = 9
    dungeons = 5, 6

class FireStaff(Staff):
    name = 'fire staff'
    glyph = '/', T.light_red
    speed = -1
    magic = 4
    dice = 2, 5, 3
    mana = 12
    dungeons = 7, 8

class WonderStaff(Staff):
    name = 'wonder staff'
    glyph = '/', T.pink
    speed = -1
    magic = 5
    dice = 2, 7, 4
    mana = 15
    dungeons = 9, 10

class SnowStaff(Staff):
    name = 'snow staff'
    glyph = '/', T.white
    speed = -1
    magic = 6
    dice = 2, 8, 5
    mana = 18
    dungeons = 11, 12

class BattleStaff(EliteStaff):
    name = 'battle staff'
    glyph = '/', T.light_grey
    magic = 6
    dice = 2, 6, 4
    mana = 14
    dungeons = 7, 9

class RuneStaff(EliteStaff):
    name = 'rune staff'
    glyph = '/', T.dark_orange
    magic = 7
    dice = 3, 5, 4
    mana = 17
    dungeons = 9, 11

class PowerStaff(UniqueStaff):
    name = 'power staff'
    glyph = '/', T.cyan
    speed = 1
    magic = 9
    dice = 4, 4, 7
    mana = 20
    dungeons = 11, 12

# --- SHIELDS --- #

class RoundShield(Shield):
    name = 'round shield'
    glyph = '0', T.light_green
    armor = 2
    blocking = 10
    dungeons = 1, 2

class SkullShield(Shield):
    name = 'skull shield'
    glyph = '0', T.light_grey
    armor = 4
    blocking = 15
    dungeons = 3, 4

class KnightShield(Shield):
    name = 'knight shield'
    glyph = '0', T.light_orange
    armor = 6
    blocking = 20
    dungeons = 5, 6

class PaladinShield(Shield):
    name = 'paladin shield'
    glyph = '0', T.yellow
    armor = 8
    blocking = 25
    dungeons = 7, 8

class RoyalShield(Shield):
    name = 'royal shield'
    glyph = '0', T.lightest_red
    armor = 10
    blocking = 30
    dungeons = 9, 10

class RuneShield(Shield):
    name = 'rune shield'
    glyph = '0', T.dark_orange
    armor = 12
    blocking = 35
    dungeons = 11, 12

# --- HELMS --- #

class FullHelm(Helm):
    name = 'full helm'
    glyph = '^', T.dark_orange
    armor = 1
    dungeons = 1, 2

class GuardianHelm(Helm):
    name = 'guardian helm'
    glyph = '^', T.dark_yellow
    armor = 2
    dungeons = 3, 4

class DefenderHelm(Helm):
    name = 'defender helm'
    glyph = '^', T.dark_orange
    armor = 3
    dungeons = 5, 6

class GreatHelm(Helm):
    name = 'great helm'
    glyph = '^', T.lightest_grey
    armor = 4
    dungeons = 7, 8

class WingedHelm(Helm):
    name = 'winged helm'
    glyph = '^', T.dark_yellow
    armor = 5
    dungeons = 9, 10

class HornedHelm(Helm):
    name = 'horned helm'
    glyph = '^', T.lighter_grey
    armor = 6
    dungeons = 11, 12

class AssaultHelmet(EliteHelm):
    name = 'assault helmet'
    glyph = '^', T.yellow
    armor = 5
    dungeons = 7, 9

class GuardianCrown(EliteHelm):
    name = 'guardian crown'
    glyph = '^', T.light_yellow
    armor = 6
    dungeons = 9, 11

class AvengerGuard(UniqueHelm):
    name = 'avenger guard'
    glyph = '^', T.cyan
    armor = 7
    dungeons = 11, 12

# --- BOOTS --- #

class LightBoots(Boots):
    name = 'light boots'
    glyph = '[', T.dark_orange
    armor = 1
    dungeons = 1, 2

class MeshBoots(Boots):
    name = 'mesh boots'
    glyph = '[', T.dark_red
    armor = 2
    dungeons = 3, 4

class SterlingBoots(Boots):
    name = 'sterling boots'
    glyph = '[', T.lighter_grey
    armor = 3
    dungeons = 5, 6

class ChainBoots(Boots):
    name = 'chain boots'
    glyph = '[', T.dark_grey
    armor = 4
    speed = -1
    dungeons = 7, 8

class ArmoredBoots(Boots):
    name = 'armored boots'
    glyph = '[', T.dark_grey
    armor = 5
    speed = -1
    dungeons = 9, 10

class HeavyBoots(Boots):
    name = 'heavy boots'
    glyph = '[', T.light_blue
    armor = 6
    speed = -2
    dungeons = 11, 12

class MirroredBoots(EliteBoots):
    name = 'mirrored boots'
    glyph = '[', T.light_green
    armor = 6
    speed = 1
    dungeons = 7, 9

class BattleBoots(EliteBoots):
    name = 'battle boots'
    glyph = '[', T.light_red
    armor = 7
    speed = 1
    dungeons = 9, 11

class WarBoots(UniqueBoots):
    name = 'war boots'
    glyph = '[', T.cyan
    armor = 8
    speed = 1
    dungeons = 11, 12

# --- CLOTH ARMORS --- #

class CultistRobe(ClothArmor):
    name = 'cultist robe'
    glyph = ']', T.blue
    armor = 2
    mana = 3
    speed = -1
    dungeons = 1, 2

class EnchanterRobe(ClothArmor):
    name = 'enchanter robe'
    glyph = ']', T.yellow
    armor = 4
    mana = 6
    speed = -1
    dungeons = 3, 4

class WitchRobe(ClothArmor):
    name = 'witch robe'
    glyph = ']', T.gray
    armor = 6
    mana = 9
    speed = -1
    dungeons = 5, 6

class MageRobe(ClothArmor):
    name = 'mage robe'
    glyph = ']', T.darker_orange
    armor = 8
    mana = 12
    dungeons = 7, 8

class WardenRobe(ClothArmor):
    name = 'warden robe'
    glyph = ']', T.light_green
    armor = 10
    mana = 15
    dungeons = 9, 10

class ArchonRobe(ClothArmor):
    name = 'archon robe'
    glyph = ']', T.green
    armor = 12
    mana = 18
    dungeons = 11, 12

class TemplarRobe(EliteClothArmor):
    name = 'templar robe'
    glyph = ']', T.light_blue
    armor = 12
    mana = 20
    magic = 2
    dungeons = 7, 9

class QuicksilverRobe(EliteClothArmor):
    name = 'quicksilver robe'
    glyph = ']', T.light_grey
    armor = 15
    mana = 24
    magic = 2
    dungeons = 9, 11

class DivineArmor(UniqueClothArmor):
    name = 'divine armor'
    glyph = ']', T.cyan
    armor = 20
    mana = 30
    magic = 3
    dungeons = 11, 12

# --- LEATHER ARMORS --- #

class QuiltedArmor(LeatherArmor):
    name = 'quilted armor'
    glyph = ']', T.dark_orange
    armor = 3
    dungeons = 1, 2

class ShadowArmor(LeatherArmor):
    name = 'shadow armor'
    glyph = ']', T.grey
    armor = 2
    dungeons = 1, 2

class StuddedLeatherArmor(LeatherArmor):
    name = 'studded leather armor'
    glyph = ']', T.darker_orange
    armor = 6
    dungeons = 3, 4

class DusterLeatherArmor(LeatherArmor):
    name = 'duster leather armor'
    glyph = ']', T.orange
    armor = 9
    speed = -1
    dungeons = 5, 6

class StuddedWardenArmor(LeatherArmor):
    name = 'studded warden armor'
    glyph = ']', T.darker_orange
    armor = 12
    speed = -1
    dungeons = 7, 8

class FlamescaleArmor(LeatherArmor):
    name = 'flamescale armor'
    glyph = ']', T.light_red
    armor = 15
    speed = -1
    dungeons = 9, 10

class DragonskinArmor(LeatherArmor):
    name = 'dragonskin armor'
    glyph = ']', T.green
    armor = 18
    speed = -2
    dungeons = 11, 12

class ChaosArmor(EliteLeatherArmor):
    name = 'chaos armor'
    glyph = ']', T.grey
    armor = 18
    dungeons = 7, 9

class SacredArmor(EliteLeatherArmor):
    name = 'sacred armor'
    glyph = ']', T.light_red
    armor = 20
    dungeons = 9, 11

class AncientArmor(UniqueLeatherArmor):
    name = 'ancient armor'
    glyph = ']', T.cyan
    armor = 25
    dungeons = 11, 12

# --- MAIL ARMORS --- #

class RingMail(MailArmor):
    name = 'ring mail'
    glyph = ']', T.light_grey
    armor = 4
    speed = -1
    dungeons = 1, 2

class ScaleMail(MailArmor):
    name = 'scale mail'
    glyph = ']', T.light_grey
    armor = 8
    speed = -1
    dungeons = 3, 4

class ChainMail(MailArmor):
    name = 'chain mail'
    glyph = ']', T.light_grey
    armor = 12
    speed = -1
    dungeons = 5, 6

class WardenSplintmail(MailArmor):
    name = 'warden splintmail'
    glyph = ']', T.light_grey
    armor = 16
    speed = -1
    dungeons = 7, 8

class DwarvenArmor(MailArmor):
    name = 'dwarven armor'
    glyph = ']', T.light_grey
    armor = 20
    speed = -1
    dungeons = 9, 10

class PlateArmor(MailArmor):
    name = 'plate armor'
    glyph = ']', T.light_grey
    armor = 24
    speed = -2
    dungeons = 11, 12

class AncientElvenArmor(EliteMailArmor):
    name = 'ancient elven armor'
    glyph = ']', T.light_blue
    armor = 25
    dungeons = 7, 9

class DwarvenGuardArmor(EliteMailArmor):
    name = 'dwarven guard armor'
    glyph = ']', T.light_red
    armor = 30
    dungeons = 9, 11

class DragonboneLegionArmor(UniqueMailArmor):
    name = 'dragonbone legion armor'
    glyph = ']', T.cyan
    armor = 40
    dungeons = 11, 12

# --- BOOKS --- #

class BookHealing(Book):
    glyph = '+', T.pink
    name = 'book of healing'
    spell = Heal
    dungeons = 1, 3
    rarity = 1
    
class BookTeleportation(Book):
    glyph = '+', T.lighter_blue
    name = 'book of teleportation'
    spell = Teleport
    dungeons = 2, 4
    rarity = 1
    
class BookBloodlust(Book):
    glyph = '+', T.red
    name = 'book of bloodlust'
    spell = Bloodlust
    dungeons = 3, 5
    rarity = 1
    
class BookConfuse(Book):
    glyph = '+', T.light_green
    name = 'book of confuse'
    spell = Confuse
    dungeons = 4, 7
    rarity = 1
    
# --- ALCHEMY --- #

class EmptyBottle(CraftItem):
    glyph = '!', T.light_gray
    name = 'empty bottle'
    dungeons = 1, 12
    rarity = 5

    def on_use(self, player):
        message('A simple bottle. You can brew a potion.')
    
# --- POTIONS --- #

class HealingPotion(Potion):
    glyph = '!', T.light_red
    name = 'healing potion'
    dungeons = 1, 12
    rarity = 1
    
    def on_use(self, player):
        super(HealingPotion, self).on_use(player)
        message('You feel healed.')
        player.life.fill()

class ManaPotion(Potion):
    glyph = '!', T.light_blue
    name = 'mana potion'
    dungeons = 1, 12
    rarity = 1
    
    def on_use(self, player):
        super(ManaPotion, self).on_use(player)
        message('You feel magical energies restoring.')
        player.mana.fill()

# --- POISON POTIONS --- #

class InstantPoisonPotion(PoisonPotion):
    glyph = '!', T.light_green
    name = 'instant poison potion'
    poison = 3
    dungeons = 1, 4
    rarity = 10

class ChokingPoisonPotion(PoisonPotion):
    glyph = '!', T.lighter_green
    name = 'choking poison potion'
    poison = 6
    dungeons = 5, 8
    rarity = 10
    
class RancidPoisonPotion(PoisonPotion):
    glyph = '!', T.light_yellow
    name = 'rancid poison potion'
    poison = 9
    dungeons = 9, 12
    rarity = 10

# --- SCROLLS --- #

class ScrollRedPortal(Scroll):
    ABSTRACT = True
    glyph = '?', T.light_red
    name = 'scroll of red portal'
    spell = RedPortal

class ScrollGreenPortal(Scroll):
    ABSTRACT = True
    glyph = '?', T.light_green
    name = 'scroll of green portal'
    spell = GreenPortal
        
class ScrollBluePortal(Scroll):
    ABSTRACT = True
    glyph = '?', T.light_blue
    name = 'scroll of blue portal'
    spell = BluePortal
        
class ScrollHealing(Scroll):
    glyph = '?', T.pink
    name = 'scroll of healing'
    spell = Heal
    dungeons = 1, 12
    rarity = 1

class ScrollTeleport(Scroll):
    glyph = '?', T.lighter_blue
    name = 'scroll of teleportation'
    spell = Teleport
    dungeons = 2, 12
    rarity = 1

class ScrollBloodlust(Scroll):
    glyph = '?', T.red
    name = 'scroll of bloodlust'
    spell = Bloodlust
    dungeons = 3, 12
    rarity = 1

class ScrollConfuse(Scroll):
    glyph = '?', T.light_green
    name = 'scroll of confuse'
    spell = Confuse
    dungeons = 4, 12
    rarity = 1
