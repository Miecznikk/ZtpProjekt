from .upgrades import HealthUpgrade, AttackUpgrade, TripleShot
import random
from imports.constants import FRAMES,UPGRADE_SPRITES

class Upgrader:

    possible_upgrades = [HealthUpgrade,AttackUpgrade,TripleShot]
    possible_upgrades_sprites = [UPGRADE_SPRITES['health'],UPGRADE_SPRITES['attack'],UPGRADE_SPRITES['triple_shot']]
    drop_interval = 5.5*FRAMES

    def __init__(self,player,surface):
        self.player = player
        self.drop_counter = self.drop_interval
        self.upgrades = []
        self.surface = surface

    def choose_upgrade(self):
        possible = [1]

        if self.player.health < self.player.max_health:
            possible.append(0)
        if not self.player.triple_shot:
            possible.append(2)

        choose = random.choice(possible)
        self.upgrades.append(self.possible_upgrades[choose]((random.randint(48,800-48),-32),(0,2),self.possible_upgrades_sprites[choose],self.surface))

    def update(self):
        self.drop_counter -= 1
        if self.drop_counter <= 0:
            self.drop_counter = self.drop_interval
            self.choose_upgrade()
        for upgrade in self.upgrades:
            if not upgrade.update(self.player):
                self.upgrades.remove(upgrade)

    def draw(self):
        for upgrade in self.upgrades:
            upgrade.draw()