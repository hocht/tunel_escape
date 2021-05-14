import sys

import pygame

class TunnelEscape:
    """Overall class to manage game assets and behaivor"""
    def __init__(self):
        """ initialize the game, and create game resources"""
        pygame.init()
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Tunnel escape")
        #set the background color
        self.bg_color = (230,230,230)
        
        def run_game(self):
            """start the main loop for the game"""
            while True:
                #watch for keyboard and mouse events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                #make the most recently drawn screen visible.
                self.screen.fill(self.bg_color)
                # make the most recently drawn screen visible
                pygame.display.flip()
if __name__ == '__main__':
    # make a game instance and run the game
    ai = TunnelEscape()
    ai.run_game()

            
            

        

