import pygame
import texturas
from objetos import Rocas
import mundo

class Personaje:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20 
        self.inventory = {"Roca": 0, "Calcita": 0} 
        
    def draw(self, screen): 
        pygame.draw.rect(screen, texturas.negro, (self.x, self.y, self.size, self.size))
            
    def move(self, dx, dy, mundo):
        variable_x = self.x + dx
        variable_y = self.y + dy
        
        for rocas in mundo.rocas:
            if self.check_collision(variable_x, variable_y, rocas):
                return
            
        self.x = variable_x
        self.y = variable_y
        self.x = max(0, min(self.x, texturas.width - self.size))
        self.y = max(0, min(self.y, texturas.height - self.size))
            
    def check_collision(self, x, y, obj):
        return (x < obj.x + obj.size and x + self.size > obj.x and y < obj.y + obj.size and y + self.size > obj.y)       
            