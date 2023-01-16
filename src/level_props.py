import pygame

class Background:
    def __init__(self,surface):
        self.surface = surface

        self.image1 = pygame.image.load('assets/images/background.jpg')
        self.image2 = pygame.image.load('assets/images/background.jpg')

        self.posY1 = -600
        self.posY2 = 0

    def draw(self):
        self.surface.blit(self.image1,(0,self.posY1))
        self.surface.blit(self.image2,(0,self.posY2))

    def update(self):
        self.posY1 += 1
        self.posY2 += 1
        if self.posY1 >= 600:
            self.posY1 = -600
        if self.posY2 >= 600:
            self.posY2 = -600