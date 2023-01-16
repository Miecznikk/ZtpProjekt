import pygame

class TextField:
    def __init__(self,position,size,text,font_size,surface,text_color = (250,250,250)):
        self.font = pygame.font.Font('assets/font/slkscr.ttf',font_size)
        self.rect = pygame.Rect(position,size)
        self.text = self.font.render(text,True,text_color)
        self.text_rect = self.text.get_rect(center = self.rect.center)
        self.text_color = text_color
        self.surface = surface

    def draw(self):
        self.surface.blit(self.text,self.text_rect)

    def update(self,new_text=None):
        if new_text is not None:
            self.text = self.font.render(new_text,True,self.text_color)
