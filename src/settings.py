class Settings:
    """Klasa przeznaczona do przechowywania wszystkich ustawień gry"""

    def __init__(self):
        """Inicjalizacja ustawień gry"""
        # Ustawienia dotyczące ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        # self.bg_color = (230, 230, 230)

        # Ustawienia dotyczące statku
        self.ship_limit = 3

        # Ustawienia dotyczące pocisku
        self.bullet_width = 3
        # self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (230, 230, 230)
        self.bullets_allowed = 3

        # Ustawienia dotyczące obcego
        self.fleet_drop_speed = 10 #org 10
        
        # Łatwia zmiana szybkości gry
        self.speedup_scale = 1.05
        # Ilość punktów po zastrzeleniu obcego
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicjalizacja ustawień, które ulegają zmianie w trakcie gry"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.5

        self.fleet_direction = 1 # 1 oznacza prawo, -1 lewo

        # Punktacja
        self.alien_points = 50

    def increase_speed(self):
        """Zmiana ustawień dt szybkości"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        