import sys

import pygame
from pygame.event import event_name

from settings import Settings
from ship import Ship

class TunnelEscape:
    """Overall class to manage game assets and behaivor"""
    
    def __init__(self):
        """ initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.joysticks = []
        # for al the connected joysticks
        for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
            self.joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
            self.joysticks[-1].init()
        # print a statement telling what the name of the controller is
            print ("Detected joystick '",self.joysticks[-1].get_name(),"'")

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
            #watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.JOYHATMOTION:
                    self._check_hat_events(event)
                    print("hola")
                elif event.type == pygame.JOYBUTTONDOWN:
                    print(event.type)
                elif event.type == pygame.JOYAXISMOTION:
                    print(event.type)
    
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

    def _check_hat_events(self,event):
       if self.joysticks[-1].get_hat(0) == (1,0):
          self.ship.moving_right = True
       elif self.joysticks[-1].get_hat(0) == (0,0):
           self.ship.moving_right = False

       if self.joysticks[-1].get_hat(0) == (-1,0):
          self.ship.moving_left = True
       elif self.joysticks[-1].get_hat(0) == (0,0):
           self.ship.moving_left = False


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
            
            

        

