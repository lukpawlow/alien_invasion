import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Klasa przeznaczona do zarządzania statkiem kosmicznym"""

    def __init__(self, ai_game):
        """Inicjalizacja statku kosmicznego i jego położenia początkowego"""
        super().__init__()

        # Wczytanie powierzchni gry i jej prostokąta
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Wczytanie obrazu statku i pobranie jego prostokąta
        self.image = pygame.image.load('images/white_ship.bmp')
        self.rect = self.image.get_rect()

        # Każdy nowy statek pojawia się na dole ekranu
        self.rect.midbottom = self.screen_rect.midbottom

        # Położenie poziome statku jest przechowywane we float
        self.x = float(self.rect.x)

        # Opcje początkowe wskazujące na poruszanie się statku
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Uaktualnienie położenie statku na podstawie opcji
        wskazujących na jego ruch"""
        # Uaktualnianie wartości współrzednej X a nie jego prostokąta
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
    
        # Uaktualnienie obiektu rect na podstawie wartości self.x
        self.rect.x = self.x

    def blitme(self):
        """Wyświetlenie statku kosmicznego w jego aktualnym położeniu"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Umieszczenie statku na środku przy dolnej krawędzi"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    