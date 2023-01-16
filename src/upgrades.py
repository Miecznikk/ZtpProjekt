from .game_object import GameObject
from abc import ABC, abstractmethod

class Upgrade(GameObject,ABC):
    def __init__(self,position,velocity,sprite,surface):
        super(Upgrade, self).__init__(position,velocity,sprite,surface)

    @abstractmethod
    def upgrade_method(self,player):
        pass
    
    def draw(self):
        self.surface.blit(self.sprite, (self.posX, self.posY))
    
    def update(self,player):
        self.posX += self.velX
        self.posY += self.velY

        if self.posY + self.sprite_rect.h > player.posY:
            if player.posX < self.posX < player.posX + player.sprite_rect.w or player.posX < self.posX + self.sprite_rect.w < player.posX + player.sprite_rect.w:
                self.upgrade_method(player)
                return False
        if self.posY>600:
            return False
        return True

class HealthUpgrade(Upgrade):
    def __init__(self,position,velocity,sprite,surface):
        super(HealthUpgrade, self).__init__(position,velocity,sprite,surface)
        self.health = 25

    def upgrade_method(self,player):
        player.heal(self.health)

    def draw(self):
        super(HealthUpgrade, self).draw()

    def update(self,player):
        return super(HealthUpgrade, self).update(player)

class AttackUpgrade(Upgrade):
    def __init__(self,position,velocity,sprite,surface):
        super(AttackUpgrade, self).__init__(position,velocity,sprite,surface)
        self.attack = 5

    def upgrade_method(self,player):
        player.upgrade_attack(self.attack)

    def draw(self):
        super(AttackUpgrade, self).draw()

    def update(self,player):
        return super(AttackUpgrade, self).update(player)

class TripleShot(Upgrade):
    def __init__(self,position,velocity,sprite,surface):
        super(TripleShot, self).__init__(position,velocity,sprite,surface)

    def upgrade_method(self,player):
        player.toggle_triple_shot()

    def draw(self):
        super(TripleShot, self).draw()

    def update(self,player):
        return super(TripleShot, self).update(player)
