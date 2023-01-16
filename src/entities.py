from .game_object import GameObject
from abc import ABC,abstractmethod
from imports.constants import BULLET_SPRITE,TRIPLE_BULLET_SPRITE
import pygame
from .entity_props import Bullet, HealthBar, TripleBullet


class Entity(GameObject,ABC):
    bullet_sprite = BULLET_SPRITE
    max_health = 0
    health = 0
    attack = 0

    def __init__(self,position,velocity,sprite,surface):
        super(Entity, self).__init__(position,velocity,sprite,surface)
        self.bullets = []

    @abstractmethod
    def shoot(self):
        pass

    def draw(self):
        self.surface.blit(self.sprite,(self.posX,self.posY))
        for bullet in self.bullets:
            bullet.draw()

    def update(self):
        for bullet in self.bullets:
            if not bullet.update():
                self.bullets.remove(bullet)

        self.posX += self.velX
        self.posY += self.velY

class Enemy(Entity):
    def __init__(self,position,velocity,sprite,surface,strategy):
        super(Enemy, self).__init__(position,velocity,sprite,surface)
        self.strategy = strategy
        self.strategy.set_values(self)
        self.health_bar = HealthBar((self.posX,self.posY - 8),self.surface)

    def draw(self):
        super(Enemy, self).draw()
        self.health_bar.draw()

    def update(self):
        super(Enemy, self).update()
        self.strategy.move_method(self)
        self.health_bar.update((self.posX,self.posY - 8),self.health/self.max_health)

    def bullet_collider(self,player):
        for bullet in self.bullets:
            if bullet.posY >= player.posY + 10 and (player.posX <= bullet.posX <= player.posX + player.sprite_rect.width):
                self.bullets.remove(bullet)
                if player.take_damage(self.attack):
                    return True
            return False

    def shoot(self):
        self.bullets.append(Bullet((self.posX + (self.sprite_rect.width / 2) - 3,self.posY + self.sprite_rect.height),(0,4),self.bullet_sprite,self.surface))

    def player_collider(self,player):
        player_vertical_range = range(player.posY+16,player.posY + player.sprite_rect.height)
        player_horizontal_range = range(player.posX,player.posX + player.sprite_rect.width)

        if self.posY + self.sprite_rect.height in player_vertical_range:
            if self.posX in player_horizontal_range or self.posX + self.sprite_rect.width in player_horizontal_range:
                return True
        return False

    def out_of_screen(self):
        return self.posY > 600

    def take_damage(self,damage):
        self.health -= damage
        return self.health <= 0

class Player(Entity):
    _instance = None
    reload_time = 0
    points = 0
    init_attack = 0
    triple_shot = False
    health_bar = None
    triple_bullet = TRIPLE_BULLET_SPRITE
    damage_multiplier = 1

    def __init__(self):
        raise RuntimeError('Use instance() method instead')

    @classmethod
    def getInstance(cls,*args):
        """ 0-position 1-velocity 2-sprite 3-surface 4-health 5-attack """
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.posX = args[0][0]
            cls._instance.posY = args[0][1]
            cls._instance.velX = args[1][0]
            cls._instance.velY = args[1][1]
            cls._instance.sprite = args[2]
            cls._instance.sprite_rect = args[2].get_rect()
            cls._instance.surface = args[3]
            cls._instance.max_health = args[4]
            cls._instance.health = args[4]
            cls._instance.init_attack = args[5]
            cls._instance.attack = args[5]
            cls._instance.bullets = []
            cls._instance.health_bar = HealthBar((cls._instance.posX,cls._instance.posY - 8),cls._instance.surface)
        return cls._instance

    def take_damage(self,attack):
        self.health-= attack
        if self.health <= 0:
            return True
        return False

    def heal(self,health_value):
        self.health += health_value
        if self.health > self.max_health:
            self.health = self.max_health

    def upgrade_attack(self,attack_value):
        self.attack += attack_value

    def update(self):
        super(Player, self).update()

        if self.posX < 0:
            self.posX = 0
        if self.posX + self.sprite_rect.width > 800:
            self.posX = 800 - self.sprite_rect.width
        self.health_bar.update((self.posX,self.posY + 72),self.health/self.max_health)
        self.reload_time -= 1

        self.handle_input()
        
    def draw(self):
        super(Player, self).draw()
        self.health_bar.draw()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velX = -4
        elif keys[pygame.K_RIGHT]:
            self.velX = 4
        else:
            self.velX = 0
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.reload_time <= 0:
            if not self.triple_shot:
                self.bullets.append(Bullet((self.posX + (self.sprite_rect.width / 2) - 3,self.posY - 5),(0,-8),self.bullet_sprite,self.surface))
            else:
                self.bullets.append(TripleBullet((self.posX + (self.sprite_rect.width / 2) - 3,self.posY - 5),(0,-8),self.triple_bullet,self.surface))
            self.reload_time = 20

    def bullet_collider(self,enemy):
        for bullet in self.bullets:
            if bullet.posY <= enemy.posY + enemy.sprite_rect.height - 20 and (enemy.posX <= bullet.posX <= enemy.posX + enemy.sprite_rect.width):
                self.bullets.remove(bullet)
                return True
            return False

    def add_points(self,enemy_points):
        self.points += enemy_points

    def reset(self):
        self.bullets = []
        self.health = self.max_health
        self.attack = self.init_attack
        self.triple_shot = False
        self.damage_multiplier = 1

    def toggle_triple_shot(self):
        self.triple_shot = True
        self.damage_multiplier = 3

