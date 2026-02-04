import pygame
import texturas

class Personaje:
    def __init__(self, x, y):
        # Posición en el mundo (coordenadas absolutas)
        self.world_x = x
        self.world_y = y
        
        # Posición en pantalla (siempre en el centro)
        self.screen_x = texturas.width // 2
        self.screen_y = texturas.height // 2
        
        self.size = 20 
        self.inventory = {"Roca": 0, "Calcita": 0} 
        
    def draw(self, screen): 
        # El jugador siempre se dibuja en el centro de la pantalla
        pygame.draw.rect(screen, texturas.negro, (self.screen_x, self.screen_y, self.size, self.size))
            
    def move(self, dx, dy, mundo_infinito):
        """Mueve al personaje en el mundo infinito"""
        nueva_world_x = self.world_x + dx
        nueva_world_y = self.world_y + dy
        
        # Obtener objetos cercanos para detectar colisiones
        objetos = mundo_infinito.obtener_objetos_cercanos(self.screen_x, self.screen_y, radio=100)
        
        # Verificar colisiones con rocas
        colision = False
        for roca in objetos['rocas']:
            if self.check_collision_world(nueva_world_x, nueva_world_y, roca, mundo_infinito):
                colision = True
                break
        
        # Si no hay colisión, mover
        if not colision:
            self.world_x = nueva_world_x
            self.world_y = nueva_world_y
            
            # Actualizar chunks según nueva posición
            mundo_infinito.actualizar(self.world_x, self.world_y)
            
    def check_collision_world(self, world_x, world_y, obj, mundo_infinito):
        """Verifica colisión usando coordenadas del mundo"""
        return (world_x < obj.x + obj.size and 
                world_x + self.size > obj.x and 
                world_y < obj.y + obj.size and 
                world_y + self.size > obj.y)
            
    def esta_cerca(self, objeto, mundo_infinito, distancia=40):
        """Verifica si el personaje está cerca de un objeto en el mundo"""
        dist_x = abs(self.world_x - objeto.x)
        dist_y = abs(self.world_y - objeto.y)
        return dist_x < distancia and dist_y < distancia
    
    def recolectar(self, lista_objetos, inventario_sistema, nombre_item, mundo_infinito):
        """Recolecta objetos del mundo infinito"""
        for objeto in lista_objetos[:]:
            if self.esta_cerca(objeto, mundo_infinito):
                if inventario_sistema.agregar_item(nombre_item, 1):
                    mundo_infinito.remover_objeto(objeto)
                    print(f"Has recogido: {nombre_item}")
                    return True
                else:
                    print("¡Inventario lleno!")
                    return False
        return False