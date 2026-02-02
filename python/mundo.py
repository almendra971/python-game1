import texturas
import pygame
import c
from objetos import Rocas, Mineral_calcita
import random
import os
class World:
    
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        self.rocas = [Rocas(random.randint(0, width-40), random.randint(0, height-40)) for _ in range(10)]
        self.calcita = [Mineral_calcita(random.randint(0, width-32), random.randint(0, height-40)) for _ in range(20)]
    
        suelo_path = os.path.join('imagenes', 'fondos', 'suelo.png')
        self.suelo_image = pygame.image.load(suelo_path).convert()
        self.suelo_image = pygame.transform.scale(self.suelo_image, (texturas.suelo, texturas.suelo))
    
    
        
    def draw(self, screen):
        for y in range(0, self.height, texturas.suelo):
            for x in range(0, self.height, texturas.suelo):
                screen.blit(self.suelo_image, (x, y)) 
            
        
        for rocas in self.rocas:
            rocas.draw(screen)
        
        for calcita in self.calcita:
            calcita.draw(screen)