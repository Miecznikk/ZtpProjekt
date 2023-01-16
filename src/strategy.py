from abc import ABC, abstractmethod
from imports.constants import FRAMES,ENEMY_SPRITES

class Strategy(ABC):
    @abstractmethod
    def set_values(self,enemy):
        pass

    @abstractmethod
    def move_method(self,enemy):
        pass


class EasyStrategy(Strategy):

    def set_values(self,enemy):
        enemy.sprite = ENEMY_SPRITES['easy']
        enemy.sprite_rect = enemy.sprite.get_rect()
        enemy.points = 10
        enemy.health = 30
        enemy.max_health = 30

    def move_method(self,enemy):
        enemy.posY += enemy.velY

class MediumStrategy(Strategy):

    def __init__(self):
        self.shoot_interval = 2.5 * FRAMES
        self.shoot_counter = 0

    def set_values(self,enemy):
        enemy.sprite = ENEMY_SPRITES['medium']
        enemy.sprite_rect = enemy.sprite.get_rect()
        enemy.points = 20
        enemy.health = 75
        enemy.max_health = 75
        enemy.attack = 20

    def move_method(self,enemy):
        self.shoot_counter -= 1
        enemy.posY += enemy.velY
        if self.shoot_counter <= 0:
            enemy.shoot()
            self.shoot_counter = self.shoot_interval


class HardStrategy(Strategy):

    def __init__(self):
        self.shoot_interval = 2.5 * FRAMES
        self.shoot_counter = 0

        self.turn_interval = 1 * FRAMES
        self.turn_counter = 0

        self.horizontal_vel = -1

    def set_values(self,enemy):
        enemy.sprite = ENEMY_SPRITES['hard']
        enemy.sprite_rect = enemy.sprite.get_rect()
        enemy.points = 30
        enemy.health = 150
        enemy.max_health = 150
        enemy.attack = 30

    def move_method(self,enemy):
        self.shoot_counter -= 1
        self.turn_counter -= 1

        enemy.posY += enemy.velY
        enemy.posX += self.horizontal_vel

        if self.shoot_counter <= 0:
            enemy.shoot()
            self.shoot_counter = self.shoot_interval

        if self.turn_counter <= 0:
            self.horizontal_vel *= -1
            self.turn_counter = self.turn_interval