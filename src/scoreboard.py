import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """Klasa przeznaczona do przechowywania informacji o punktacji"""

    def __init__(self, ai_game):
        """Inicjalizacja atrybutów dotyczących punktacji"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Ustawienie czcionki dla informacji dotyczących punktacji
        self.text_color = (30, 30, 200)
        self.font = pygame.font.SysFont(None, 48)

        # Przygotowanie początkowych obrazów z punktacją
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Przekształcenie punktacji na wygenerowany obraz"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Konwerja najlepszego wyniku w grze na wygenerowany obraz"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)

        # Wyświetlenie high score na środku ekranu przy górnej krawędzi
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Konwersja numeru poziomu na wygenerowany obraz"""
        level_str = "lvl: " + str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, None)

        # Numer poziomu jest wyświetlany pod aktualną punktacją
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Wyświetlanie liczby statków jakie pozostały graczowi"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 5)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Wyświetlenie punktacji na ekranie, poziomu oraz statków"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_timer(self):
        """Konwersja czasu gry na wygenerowany obraz"""
        time_str = f"Time: {int(self.stats.game_time)}s"
        self.timer_image = self.font.render(
            time_str, True, self.text_color, self.settings.bg_color)

        # Wyświetlenie czasu po lewej stronie ekranu przy górnej krawędzi
        self.timer_rect = self.timer_image.get_rect()
        self.timer_rect.left = self.screen_rect.left + 20
        self.timer_rect.top = self.screen_rect.top + 60

    def check_high_score(self):
        """Sprawdzenie, czy mamy najlepszy wynik osiągnięty dotąd w grze"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
