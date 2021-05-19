import sys

import pygame

from settings import Settings
from ship import Ship
from Gamepad import controlador

class TunnelEscape:
    """Overall class to manage game assets and behaivor"""
    
    def __init__(self):
        """ initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.controlador = controlador()

        #lo uso para pruebas de terminal
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Tunnel escape") 

        self.ship = Ship(self)

    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            
    def _check_events(self):
        """check for new events"""
        for event in pygame.event.get():
            #imprime el tipo de eventos

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.JOYAXISMOTION:
                self._check_axis_events(event)
            elif event.type == pygame.JOYBUTTONDOWN:
                self._check_buttonDown_events(event)
            elif event.type == pygame.JOYBUTTONUP:
                self._check_buttonUp_events(event)
    
    def _check_keydown_events(self,event):
        """ respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_axis_events(self,event):
        if event.axis == 1:
            if self.controlador.gamepad.get_axis(0) > 0.1:
                self.ship.moving_left = False
                self.ship.moving_right = True
            elif self.controlador.gamepad.get_axis(0) < -0.1:
                self.ship.moving_right = False
                self.ship.moving_left = True
            elif self.controlador.gamepad.get_axis(0) == 0:
                self.ship.moving_right = False
                self.ship.moving_left = False
    
    def _check_buttonDown_events(self,event):
        if event.button == 6:
            sys.exit()
        print(event.button,"fue pulsado")
    
    def _check_buttonUp_events(self,event):
        print(event.button,"fue liberado")

    def _update_screen(self):
    #make the most recently drawn screen visible.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # make a game instance and run the game
    ai = TunnelEscape()
    ai.run_game()
            
            

        

