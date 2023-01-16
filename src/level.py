from src.entities import Enemy
from random import randint

from src.strategy import EasyStrategy, MediumStrategy, HardStrategy
from src.textfield import TextField
from .level_props import Background
from .upgrader import Upgrader
from imports.constants import FRAMES,TMP_SPRITE

class Level:

    enemy_types = [EasyStrategy,MediumStrategy,HardStrategy]

    def __init__(self,player,surface,enemy_generate_interval,time_to_play,difficulty):
        self.player = player
        self.surface = surface
        self.state = 'PLAYING'
        self.time_to_play = time_to_play * FRAMES
        self.enemy_generate_interval = enemy_generate_interval * FRAMES
        self.generate_enemy_counter = 0
        self.enemies = []
        self.upgrader = Upgrader(self.player,self.surface)
        self.background = Background(self.surface)

        if difficulty > 2 or difficulty < 0:
            self.difficulty = 2
        else:
            self.difficulty = difficulty

        self.time_to_play_textfield = TextField((400,0),(400,50),f'Time remaining:{self.time_to_play // FRAMES}',30,self.surface)
        self.points_textfield = TextField((0,0),(200,50),f'Points:{self.player.points}',30,self.surface)

    def update(self):
        self.time_to_play -= 1
        self.generate_enemy_counter -= 1

        self.background.update()

        self.state = 'PASSED' if self.time_to_play <= 0 else self.state
        self.update_enemies()
        self.player.update()

        self.upgrader.update()

        self.time_to_play_textfield.update(f'Time remaining: {self.time_to_play // FRAMES}')
        self.points_textfield.update(f'Points: {self.player.points}')
        self.generate_enemy()

    def draw(self):
        self.background.draw()
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.time_to_play_textfield.draw()
        self.points_textfield.draw()
        self.upgrader.draw()

    def update_enemies(self):
        for enemy in self.enemies:
            if enemy.player_collider(self.player):
                self.state = 'GAME_OVER'
            enemy.update()
            if enemy.bullet_collider(self.player):
                self.state = 'GAME_OVER'
            if self.player.bullet_collider(enemy):
                if enemy.take_damage(self.player.attack * self.player.damage_multiplier):
                    self.player.add_points(enemy.points)
                    self.enemies.remove(enemy)
            if enemy.out_of_screen():
                self.enemies.remove(enemy)

    def generate_enemy(self):
        if self.generate_enemy_counter <=0:
            self.enemies.append(Enemy((randint(100,700),-64),(0,1),TMP_SPRITE,self.surface,self.enemy_types[randint(0,self.difficulty)]()))
            self.generate_enemy_counter = self.enemy_generate_interval

    def reset_player(self):
        self.player.reset()
