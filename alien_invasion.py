import sys
from time import sleep
import pygame as pg


from settings import Setting
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class Alien_Invesion():
    

    def __init__(self):
        
        pg.init()

        self.settings = Setting()
        self.screen = pg.display.set_mode((1600,900),pg.FULLSCREEN)

        pg.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        # Create an instance to store game statistics, and create a scoreboard
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self.play_Counter = 0

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play/Pause")

        # Start Alien Invasion in an active state.
        self.game_active = True
        

    def run_game(self):
        
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()

    def _check_events(self):
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        
        if event.key == pg.K_RIGHT:
            print("Right True")
            self.ship.moving_right = True

        elif event.key == pg.K_LEFT:
            print("left True")
            self.ship.moving_left = True

        elif event.key == pg.K_q:
            sys.exit()

        elif event.key == pg.K_SPACE:
            self._fire_bullet()
        
        elif event.key == pg.K_p:
            if self.stats.game_active == True:
                self.stats.game_active = False
            elif self.stats.game_active == False:
                self.stats.game_active = True
            self.play_Counter +=1
            print(self.play_Counter)



    def _check_keyup_events(self, event):
        
        if event.key == pg.K_RIGHT:
            print("Right False")
            self.ship.moving_right = False

        elif event.key == pg.K_LEFT:
            print("left False")
            self.ship.moving_left = False

    def _fire_bullet(self):
        
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

        self._check_bullet_alien_collisions()

        
    def _check_bullet_alien_collisions(self):
        
        # Remove any bullets and aliens that have collided.

        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            # self.stats.score += self.settings.alien_points
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()



    def _create_fleet(self):
        
        alien = Alien(self)
        
        alien_width, alien_height = alien.rect.size

      
        available_space_x = self.settings.screen_width - (2 * alien_width)

     
        number_aliens_x = available_space_x // (2 * alien_width)


        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    

    def _create_alien(self, alien_number,row_number):
        
        
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    
    def _update_aliens(self):
        
        
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()


        self._check_aliens_bottom()


    def _update_screen(self):
        
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw Alien
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pg.display.flip()
    
    def _ship_hit(self):
        
        if self.stats.ships_left > 0:
            
           
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.0
            sleep(0.5)

        else:
            print("Game over")
            sleep(5)   
            self.settings.initialize_dynamic_settings()


            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    
    def _check_play_button(self, mouse_pos):
        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
       
        if button_clicked and not self.stats.game_active :
            
            if not (self.play_Counter % 2) == 0:
            # Reset the game settings.
                self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pg.mouse.set_visible(False)
            # if 
        

if __name__ == '__main__':
    ai = Alien_Invesion()
    ai.run_game()
