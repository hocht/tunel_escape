import sys
from time import sleep

import pygame
from pygame.display import set_allow_screensaver
from pygame.event import pump

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from gamepad import controlador
from bullet import Bullet
from alien import Alien

class TunnelEscape:
    """Overall class to manage game assets and behaivor"""

    def __init__(self):
        """ initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.controlador = controlador()

        #lo uso para pruebas de terminal
        #self.screen = pygame.display.set_mode(
            #(self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Tunnel escape") 

        # Create an instance to store game statics,
        # And create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Crea una nueva nave a partir de la clase
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """check for new events"""
        for event in pygame.event.get():
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self,event):
        """ respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """ respond to keyReleased"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_axis_events(self,event):
        """ respond to analog stick events"""
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
        """ respond to buttonpresses gamepad events"""
        if event.button == 6:
            sys.exit()
        elif event.button == 0:
            self._fire_bullet()
        elif event.button == 7:

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
             # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fllet and center
            self._create_fleet
            self.ship.center_ship()

            # hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_buttonUp_events(self,event):
        """ respond to buttonReleased gamepad events"""
    
    def _check_play_button(self,mouse_pos):
        """ Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fllet and center
            self._create_fleet
            self.ship.center_ship()

            # hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # update bullet positions.
        self.bullets.update()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

            # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-allien collisions."""
        # Remove any bullets and aliens that have collide
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,
                                                True,True)
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level.
            self.stats.level += 1
            self.sb.prep_level()


        if collisions:
            for aliens in collisions.values():  
                self.stats.score += self.settings.alien_points * len(aliens) 
            self.sb.prep_score()
            self.sb.check_high_score()

    def _update_aliens(self):
        """ check if the fleet is at an edge, then update the position of
         aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for an alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        # Look for aliens hiting the bottom of the screen.
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -=1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """create the fleet of aliens"""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size

        # Determine the number of columns of aliens that fit in the screen.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x //(2 * alien_width)

        # Determine the number of rows of aliens that fit in the screen.
        ship_height = self.ship.rect.height
        avaiable_space_y = (self.settings.screen_height-(3*alien_height)
                            -ship_height)
        number_rows = avaiable_space_y//(2*alien_height)

        #create the full flate of aliens
        for row_number in range(number_rows):

        #create the first row of aliens.
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        """ Create an alien and place it in the row"""        
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """make the most recently drawn screen visible."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # make the most recently drawn screen visible
        pygame.display.flip()

# make a game instance and run the game
if __name__ == '__main__':
    ai = TunnelEscape()
    ai.run_game()