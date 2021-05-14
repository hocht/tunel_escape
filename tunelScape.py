import sys
import pygame

from settings import Settings
class TunnelEscape:
    """Overall class to manage game assets and behaivor"""
    def __init__(self):
        """ initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Tunnel escape") 



        def run_game(self):
            """start the main loop for the game"""
            while True:
                #watch for keyboard and mouse events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                #make the most recently drawn screen visible.
                self.screen.fill(self.settings.bg_color)
                # make the most recently drawn screen visible
                pygame.display.flip()
if __name__ == '__main__':
    # make a game instance and run the game
    ai = TunnelEscape()
    ai.run_game()

            
            

        

