from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self,position,velocity,sprite,surface):
        self.posX=position[0]
        self.posY=position[1]

        self.velX=velocity[0]
        self.velY=velocity[1]

        self.sprite = sprite
        self.sprite_rect = self.sprite.get_rect()
        self.surface = surface

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self,*args,**kwargs):
        pass