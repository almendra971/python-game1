import pygame
import sys
from personajes import Personaje
import c
import texturas
from mundo import World

pygame.init()

ventana = pygame.display.set_mode((texturas.width, texturas.height))
pygame.display.set_caption("prueba juego")


def dibujar_texto(surface, texto, tamaño, x, y, color=(255,255,255)): #aparcer el tenxto inicial
    font = pygame.font.SysFont(None, tamaño)
    render = font.render(texto, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)


def main():      #def principal donde va todo
    clock = pygame.time.Clock()
    mundo = World(texturas.width, texturas.height) 
    personaje = Personaje(texturas.width // 2, texturas.height // 2)

    
    dialogos = [ 
        "Escribe tu nombre (usa ENTER para continuar)...",
        "Soy Sara, la IA que te guiará en tu misión.",
        "Has sido elegido para pilotar hacia XH-3892...",
        "Debes encontrar rastros del anterior viaje de exploración.",
        "¿Deseas dirigir la misión?",
        "Usa n para NO   |   y para SI"
    ]

    indice = 0
    mostrar_dialogos = True
    capturando_nombre = True
    nombre = ""
    decision = None

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

           
            if mostrar_dialogos:

                if capturando_nombre:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            capturando_nombre = False
                            indice = 1  
                        elif event.key == pygame.K_BACKSPACE:
                            nombre = nombre[:-1]
                        else:
                            nombre += event.unicode

               
                elif 1 <= indice <= 4:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        indice += 1

               
                elif indice == 5:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_n:
                            decision = "NO"
                            print("adios")
                            pygame.quit()
                            sys.exit()
                            mostrar_dialogos = False  
                        elif event.key == pygame.K_y:
                            decision = "SI"
                            print("Comienza tu misión")
                            mostrar_dialogos = False

        if not mostrar_dialogos: #control personaje
            llaves = pygame.key.get_pressed()
            if llaves[pygame.K_a]:
                personaje.move(-5, 0, mundo)
            if llaves[pygame.K_d]:
                personaje.move(5, 0, mundo)
            if llaves[pygame.K_w]:
                personaje.move(0, -5, mundo)
            if llaves[pygame.K_s]:
                personaje.move(0, 5, mundo)

       
        mundo.draw(ventana)
        personaje.draw(ventana)

       
        if mostrar_dialogos:
            ventana.fill((0, 0, 0))

            if capturando_nombre:
                dibujar_texto(ventana, dialogos[0], 35,
                              texturas.width//2, texturas.height//2 - 40)
                dibujar_texto(ventana, nombre, 40,
                              texturas.width//2, texturas.height//2)

            else:
                dibujar_texto(ventana, dialogos[indice], 35,
                              texturas.width//2, texturas.height//2)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
