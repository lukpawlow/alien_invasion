import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Klasa przedstawiajaca pojedyńczego obcego we flocie"""

    def __init__(self, ai_game):
        """Inicjalizacja obcego i zdefiniowanie jego położenia początkowego"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.points = self.settings.alien_points

        # Wczytanie obrazu obcego i zdefiniowanie jego atrybutu rect
        self.image = pygame.image.load('images/alien_orange.bmp')
        self.rect = self.image.get_rect()

        # Umieszczenie nowego obcego w poliżu górnego rogu ekranu
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Przechowywanie dokładnego poziomego położenia ekranu
        self.x = float(self.rect.x)

    def check_edges(self):
        """Zwraca True gdy obcy znajduje się przy krawędzi ekranu"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Przesunięcie obcego w prawo lub w lewo"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

class ToughAlien(Alien):
    """Klasa przedstawiająca wytrzymałego obcego"""
    def __init__(self, ai_game):
        super().__init__(ai_game)

        # Wczytanie innego obrazu dla wytrzymałego obcego
        self.image = pygame.image.load('images/alien_tough.bmp')
        self.rect = self.image.get_rect()

        # Większa wartość punktowa
        self.points = self.settings.alien_points * 5

        # Licznik trafień potrzebnych do zniszczenia
        self.hits_required = 10
        self.hits = 0

    def hit(self):
        """Obsługa trafienia obcego"""
        self.hits += 1
        return self.hits >= self.hits_required
