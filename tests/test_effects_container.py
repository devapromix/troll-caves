from mobs.effects.effect import Effect
from mobs.effects.effects_container import EffectsContainer
from mobs.player import *
from tests.test_effect import create_mock


class TestEffect(Effect):
    modifier = create_mock()
    max_turns = 5


def test_effects_container_effect_lifetime():
    mob = Player(0, FIGHTER)
    effects = EffectsContainer(mob)
    effect = TestEffect()

    effects.add(effect)
    assert effect in effects
    for _ in range(0, 4):
        effects.act()
    assert effect in effects
    for _ in range(0, 4):
        effects.act()
    assert effect not in effects
