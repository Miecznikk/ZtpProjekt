import pygame
from src.entities import Player
from src.level import Level

from .game_props import InputBox

from imports.constants import FRAMES
from src.textfield import TextField
from .scoreboard import ScoreBoard


class Game:
    is_running = False

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.username = ''

        self.surface = pygame.display.set_mode((800, 600))

        self.passed_screen_textfields = [
            TextField((0, 0), (800, 400), 'LEVEL PASSED', 60,self.surface),
            TextField((0,0),(800,600),'press enter to continue',30,self.surface)
        ]

        self.paused_screen_textfields = [
            TextField((0,0),(800,400),'GAME PAUSED',60,self.surface),
            TextField((0,0),(800,600),'press escape to continue',30,self.surface)
        ]

        self.clock = pygame.time.Clock()

        self.levels = [
            Level(Player.getInstance((368,500),(0,0),pygame.image.load('assets/images/player.png'),self.surface,50,10),self.surface,3,15,0),
            Level(Player.getInstance(),self.surface,2,15,1),
            Level(Player.getInstance(),self.surface,2,15,2)
        ]
        self.current_level = 0

        self.is_running = True
        self.game_state = 'MAIN_MENU'

        self.main_menu_textfields = [
            TextField((0,0),(800,400),'ENTER YOUR USERNAME',50,self.surface),
            TextField((0, 0), (800, 500), 'AND PRESS ENTER', 50, self.surface)
        ]
        self.input_box = InputBox(200,300,400,40,self.surface)
        self.scoreboard = ScoreBoard(self.surface)

    def run(self):
        self.update()
        self.draw()

        self.clock.tick(FRAMES)

    def update(self):
        if self.game_state == 'MAIN_MENU':
            self.main_menu()

        elif self.game_state=='PLAY':
            if self.levels[self.current_level].state == 'PLAYING':
                self.levels[self.current_level].update()
            elif self.levels[self.current_level].state == 'PASSED':
                if self.current_level < len(self.levels) - 1:
                    self.game_state = 'PASSED_LVL'
                    self.current_level += 1
                else:
                    self.scoreboard.append_file(f'{self.username} {self.levels[self.current_level].player.points}\n')
                    self.game_state = 'SCOREBOARD'
            elif self.levels[self.current_level].state == 'GAME_OVER':
                self.scoreboard.append_file(f'{self.username} {self.levels[self.current_level].player.points}\n')
                self.game_state = 'SCOREBOARD'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = 'PLAY' if self.game_state == 'PAUSED' else 'PAUSED'

    def draw(self):
        if self.game_state == 'PLAY':
            self.surface.fill((30,30,30))
            self.levels[self.current_level].draw()
        elif self.game_state == 'PAUSED':
            self.paused_screen()
        elif self.game_state == 'PASSED_LVL':
            self.passed_screen()
        elif self.game_state == 'SCOREBOARD':
            self.scoreboard_screen()
        pygame.display.update()

    def passed_screen(self):
        keys = pygame.key.get_pressed()
        self.surface.fill((0,0,0))
        for textfield in self.passed_screen_textfields:
            textfield.draw()
        if keys[pygame.K_RETURN]:
            self.levels[self.current_level].reset_player()
            self.game_state = 'PLAY'

    def paused_screen(self):
        self.surface.fill((0,0,0))
        for textfield in self.paused_screen_textfields:
            textfield.draw()

    def main_menu(self):
        self.surface.fill((0, 0, 0))
        for event in pygame.event.get():
            if self.input_box.handle_event(event) is not None:
                self.username = self.input_box.handle_event(event)
                self.game_state = 'PLAY'
            if event.type == pygame.QUIT:
                self.is_running = False
        for textfield in self.main_menu_textfields:
            textfield.draw()
        self.input_box.draw()
        self.input_box.update()
        pygame.display.update()

    def scoreboard_screen(self):
        self.surface.fill((0,0,0))
        self.scoreboard.draw()
        pygame.display.update()
