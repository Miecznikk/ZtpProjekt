import pygame

class InputBox:

    def __init__(self, x, y, w, h,surface, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (120,120,120)
        self.text = text
        self.surface = surface
        self.font = pygame.font.Font('assets/font/slkscr.ttf',32)
        self.txt_surface = self.font.render(text, True,self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (255,255,255) if self.active else (120,120,120)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_SPACE:
                    pass
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        pass

    def draw(self):
        # Blit the text.
        self.surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(self.surface, self.color, self.rect, 2)