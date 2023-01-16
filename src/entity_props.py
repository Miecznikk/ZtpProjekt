import pygame
from .game_object import GameObject

class Bullet(GameObject):
    def __init__(self,position,velocity,sprite,surface):
        super(Bullet, self).__init__(position,velocity,sprite,surface)

    def draw(self):
        self.surface.blit(self.sprite,(self.posX,self.posY))

    def update(self):
        self.posY += self.velY
        if self.posY < 0 or self.posY > 600:
            return False
        return True

class TripleBullet(Bullet):
    def __init__(self,position,velocity,sprite,surface):
        super(TripleBullet, self).__init__(position,velocity,sprite,surface)
        
    def draw(self):
        super(TripleBullet, self).draw()
    
    def update(self):
        return super(TripleBullet, self).update()

class HealthBar:

    bar_colors = {
        'green': (0,255,0),
        'yellow': (255,255,0),
        'red': (255,0,0)
    }

    def __init__(self,position,surface):
        self.posX,self.posY = position[0],position[1]
        self.surface = surface
        self.color = self.bar_colors['green']
        self.rect = pygame.Rect(self.posX,self.posY,64,10)

    def update(self,position,health_percantage):
        self.rect.x, self.rect.y = position[0],position[1]
        self.rect.w = 64 * health_percantage
        if health_percantage > .8:
            self.color = self.bar_colors['green']
        elif health_percantage > .4:
            self.color = self.bar_colors['yellow']
        else:
            self.color = self.bar_colors['red']

    def draw(self):
        pygame.draw.rect(self.surface,self.color,self.rect)