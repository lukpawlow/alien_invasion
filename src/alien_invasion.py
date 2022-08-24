import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Ogólna klasa polegająca na zarządzaniu zasobami i działaniem gry"""

    def __init__(self, fullscreen=False):
        """Inicjalizacja gry i utworzenie jej zasobów"""
        pygame.init()
        self.settings = Settings()

        if fullscreen:
            # fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Inwazja obcych")

        # Utworzenie egzemplarza przechowującego dane statystyczne gry
        # oraz utworzenie egzemplarza klasy Scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Utworzenie przycisku Gra
        self.play_button = Button(self, "Graj")

    def run_game(self):
        """Rozpoczęcie pętli głównej gry"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Reakcja na zdarzenia generowane przez klawisze lub mysz"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Rozpoczęcie nowej gry po kliknięciu myszką w przycisk Graj"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """Uruchomienie nowej gry"""
        # Wyzerowanie danych statystycznych gry
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Usunięcie zawartości list aliens i bullets
        self.aliens.empty()
        self.bullets.empty()

        # Utworzenie nowej floty i wyśrodkowanie statku
        self._create_fleet()
        self.ship.center_ship()

        # Wyzerowanie ustawień dotyczących gry
        self.settings.initialize_dynamic_settings()

        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Reakcja na naciśnięcie klawisza"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_g:
            self._start_game()

    def _check_keyup_events(self, event):
        """Reakcja na zwolnienie klawisza"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Utworzenie nowego pocisku i dodanie go do grupy pocisków"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """uaktualnienie położenia pocisków i usunięcie tych niewidocznych
        na ekranie"""
        # Uaktualnienie położenia pocisków
        self.bullets.update()

        # Usunięcie pocisków, które znajdują się poza ekranem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets)) # dubug czy bullets są usuwane

        self._check_bullet_alien_colision()

    def _check_bullet_alien_colision(self):
        """Reakcja na kolizję między pociskiem i obcym"""
        # Sprawdzenie czy którykolwiek pocisk trafił któregokolwiek obcego
        # Jeżeli tak usuwamy zarówno pocisk jak i obcego
        collision = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collision:
            for alien in collision.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()
            
        # Po zastrzeleniu wszystkich obcych,
        # usunięcie pozostałych pocisków i utworzenie nowej floty
        # i przyspieszenie gry
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Inkrementacja numeru poziomu
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """Sprawdzenie czy obcy znajduje się przy krawędzi a następnie,
        Uaktualnienie położenia wszystkich obcych we flocie"""
        self._check_fleet_edges()
        self.aliens.update()

        # Wykrywanie kolizji między obcym i statkiem
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Wykrywanie obcych docierających do dolnej krawędzi ekranu
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Utworzenie pełnej floty obcych"""
        # Utworzenie obcego i ustalenie liczby obcych, które zmieszczą się
        # na ekranie
        # Odległość między obcymi jest równa szerokości obcego
        alien = Alien(self)
        alien_width, alien_hight = alien.rect.size

        # Ustalenie ile obcych w rzędzie
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Ustalenie ile rzędów obnych na ekranie
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             3 * alien_hight - ship_height)
        number_rows = available_space_y // (2 * alien_hight)

        # Utworzenie pełnej floty obcych
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Utworzenie obcego i umieszczenie go w rzędzie
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien_height + 2 * alien_height * row_number) + 10
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Przesunięcie całej floty w dół i zmiana kiernku w którym się 
        ona porusza"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Reakcja na uderzenie obcego w statek"""
        if self.stats.ships_left > 1:
            # Zmniejszenie wartości w ship_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()

            # Utworzenie nowej floty i wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()

            # Pauza
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Spr, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu"""
        # Odświeżenie ekranu w trakcie każdej iteracji pętli
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Wyświetlenie informacji o punktacji
        self.sb.show_score()

        # Wyświetlenie przycisku tylko gdy gra jest niekatywna
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Wyświetlenie ostatio zmodyfikowanego ekranu
        pygame.display.flip()


if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion(False)
    ai.run_game()
