class GameStats:
    """Monitorowanie danych statystycznych gry"""

    def __init__(self, ai_game):
        """Inicjalizacja danych statystycznych"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Uruchomienie gry w stanie nieaktywnym
        self.game_active = False

        # Najlepszy wynik nie powinnien być zerowany
        self.high_score = 0

    def reset_stats(self):
        """Inicjalizacja danych statystycznych, które mogą się
        zmieniać w trakcie gry"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        