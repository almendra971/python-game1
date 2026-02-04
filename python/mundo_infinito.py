import texturas
import pygame
import c
from objetos import Rocas, Mineral_calcita
import random
import os

class Chunk:
    """Representa un chunk (trozo) del mundo"""
    def __init__(self, chunk_x, chunk_y, chunk_size=800):
        self.chunk_x = chunk_x  # Coordenada del chunk en la cuadrícula
        self.chunk_y = chunk_y
        self.chunk_size = chunk_size
        
        # Posición real en píxeles
        self.world_x = chunk_x * chunk_size
        self.world_y = chunk_y * chunk_size
        
        # Semilla única para este chunk (genera el mismo contenido siempre)
        self.seed = hash((chunk_x, chunk_y))
        
        # Generar objetos del chunk
        self.rocas = []
        self.calcita = []
        self._generar_contenido()
    
    def _generar_contenido(self):
        """Genera rocas y calcita para este chunk"""
        # Usar la semilla del chunk para generar siempre el mismo contenido
        random.seed(self.seed)
        
        # Generar rocas (10 por chunk)
        for _ in range(10):
            x = self.world_x + random.randint(0, self.chunk_size - 40)
            y = self.world_y + random.randint(0, self.chunk_size - 40)
            self.rocas.append(Rocas(x, y))
        
        # Generar calcita (20 por chunk)
        for _ in range(20):
            x = self.world_x + random.randint(0, self.chunk_size - 32)
            y = self.world_y + random.randint(0, self.chunk_size - 40)
            self.calcita.append(Mineral_calcita(x, y))
        
        # Restaurar semilla aleatoria normal
        random.seed()


class WorldInfinito:
    """Mundo infinito con generación procedural de chunks"""
    
    def __init__(self, screen_width, screen_height, chunk_size=800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.chunk_size = chunk_size
        
        # Diccionario de chunks cargados {(chunk_x, chunk_y): Chunk}
        self.chunks = {}
        
        # Camera offset (desplazamiento de la cámara)
        self.camera_x = 0
        self.camera_y = 0
        
        # Cargar textura del suelo
        suelo_path = os.path.join('imagenes', 'fondos', 'suelo.jpg')
        self.suelo_image = pygame.image.load(suelo_path).convert()
        self.suelo_image = pygame.transform.scale(self.suelo_image, (texturas.suelo, texturas.suelo))
        
        # Generar chunks iniciales alrededor del spawn (0, 0)
        self._generar_chunks_alrededor(0, 0)
    
    def _get_chunk_coords(self, world_x, world_y):
        """Convierte coordenadas del mundo a coordenadas de chunk"""
        chunk_x = int(world_x // self.chunk_size)
        chunk_y = int(world_y // self.chunk_size)
        return (chunk_x, chunk_y)
    
    def _generar_chunks_alrededor(self, chunk_x, chunk_y, radio=2):
        """Genera chunks en un radio alrededor de un chunk central"""
        for dx in range(-radio, radio + 1):
            for dy in range(-radio, radio + 1):
                cx = chunk_x + dx
                cy = chunk_y + dy
                
                # Solo generar si no existe
                if (cx, cy) not in self.chunks:
                    self.chunks[(cx, cy)] = Chunk(cx, cy, self.chunk_size)
    
    def actualizar(self, jugador_x, jugador_y):
        """Actualiza los chunks según la posición del jugador"""
        # Calcular en qué chunk está el jugador
        jugador_chunk_x, jugador_chunk_y = self._get_chunk_coords(
            jugador_x + self.camera_x, 
            jugador_y + self.camera_y
        )
        
        # Generar chunks alrededor del jugador
        self._generar_chunks_alrededor(jugador_chunk_x, jugador_chunk_y)
        
        # Opcional: Eliminar chunks muy lejanos para ahorrar memoria
        self._limpiar_chunks_lejanos(jugador_chunk_x, jugador_chunk_y, radio_max=4)
    
    def _limpiar_chunks_lejanos(self, jugador_chunk_x, jugador_chunk_y, radio_max=4):
        """Elimina chunks que están muy lejos del jugador"""
        chunks_a_eliminar = []
        
        for (cx, cy) in self.chunks.keys():
            distancia = max(abs(cx - jugador_chunk_x), abs(cy - jugador_chunk_y))
            if distancia > radio_max:
                chunks_a_eliminar.append((cx, cy))
        
        for coords in chunks_a_eliminar:
            del self.chunks[coords]
    
    def draw(self, screen, jugador_x, jugador_y):
        """Dibuja el mundo con la cámara centrada en el jugador"""
        # Actualizar posición de la cámara para seguir al jugador
        self.camera_x = jugador_x - self.screen_width // 2
        self.camera_y = jugador_y - self.screen_height // 2
        
        # Dibujar suelo (solo las tiles visibles)
        inicio_x = int(self.camera_x // texturas.suelo) * texturas.suelo
        inicio_y = int(self.camera_y // texturas.suelo) * texturas.suelo
        
        for y in range(inicio_y, inicio_y + self.screen_height + texturas.suelo, texturas.suelo):
            for x in range(inicio_x, inicio_x + self.screen_width + texturas.suelo, texturas.suelo):
                screen_x = x - self.camera_x
                screen_y = y - self.camera_y
                screen.blit(self.suelo_image, (screen_x, screen_y))
        
        # Dibujar objetos de los chunks visibles
        for chunk in self.chunks.values():
            # Solo dibujar chunks que estén en pantalla
            chunk_screen_x = chunk.world_x - self.camera_x
            chunk_screen_y = chunk.world_y - self.camera_y
            
            # Verificar si el chunk está visible
            if (chunk_screen_x + self.chunk_size >= 0 and chunk_screen_x <= self.screen_width and
                chunk_screen_y + self.chunk_size >= 0 and chunk_screen_y <= self.screen_height):
                
                # Dibujar rocas
                for roca in chunk.rocas:
                    screen_x = roca.x - self.camera_x
                    screen_y = roca.y - self.camera_y
                    
                    # Solo dibujar si está en pantalla
                    if -40 <= screen_x <= self.screen_width and -40 <= screen_y <= self.screen_height:
                        pygame.draw.rect(screen, texturas.gris, (screen_x, screen_y, roca.size, roca.size))
                
                # Dibujar calcita
                for calcita in chunk.calcita:
                    screen_x = calcita.x - self.camera_x
                    screen_y = calcita.y - self.camera_y
                    
                    # Solo dibujar si está en pantalla
                    if -20 <= screen_x <= self.screen_width and -20 <= screen_y <= self.screen_height:
                        pygame.draw.rect(screen, texturas.rojo, (screen_x, screen_y, calcita.size, calcita.size))
    
    def obtener_objetos_cercanos(self, x, y, radio=200):
        """Obtiene todos los objetos cercanos a una posición"""
        # Convertir a coordenadas del mundo
        world_x = x + self.camera_x
        world_y = y + self.camera_y
        
        objetos_cercanos = {
            'rocas': [],
            'calcita': []
        }
        
        # Buscar en chunks cercanos
        chunk_x, chunk_y = self._get_chunk_coords(world_x, world_y)
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cx = chunk_x + dx
                cy = chunk_y + dy
                
                if (cx, cy) in self.chunks:
                    chunk = self.chunks[(cx, cy)]
                    
                    # Buscar rocas cercanas
                    for roca in chunk.rocas:
                        dist_x = abs(world_x - roca.x)
                        dist_y = abs(world_y - roca.y)
                        if dist_x < radio and dist_y < radio:
                            objetos_cercanos['rocas'].append(roca)
                    
                    # Buscar calcita cercana
                    for calcita in chunk.calcita:
                        dist_x = abs(world_x - calcita.x)
                        dist_y = abs(world_y - calcita.y)
                        if dist_x < radio and dist_y < radio:
                            objetos_cercanos['calcita'].append(calcita)
        
        return objetos_cercanos
    
    def remover_objeto(self, objeto):
        """Remueve un objeto del mundo"""
        # Buscar en qué chunk está el objeto
        chunk_x, chunk_y = self._get_chunk_coords(objeto.x, objeto.y)
        
        if (chunk_x, chunk_y) in self.chunks:
            chunk = self.chunks[(chunk_x, chunk_y)]
            
            # Intentar remover de rocas
            if objeto in chunk.rocas:
                chunk.rocas.remove(objeto)
                return True
            
            # Intentar remover de calcita
            if objeto in chunk.calcita:
                chunk.calcita.remove(objeto)
                return True
        
        return False