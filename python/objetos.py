import pygame
import texturas
class Rocas:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.rocas = 5
        
    def draw(self, screen):
        pygame.draw.rect(screen, texturas.gris, (self.x, self.y, self.size, self.size))

class Mineral_calcita:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.calcita = 5

    def draw(self, screen):
        pygame.draw.rect(screen, texturas.rojo, (self.x, self.y, self.size, self.size))




    