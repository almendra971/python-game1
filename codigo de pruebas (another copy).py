import pygame
import sys
from personajes import Personaje
import c
import texturas
from mundo import World

pygame.init()

ventana = pygame.display.set_mode((texturas.width, texturas.height))
pygame.display.set_caption("prueba juego")


def dibujar_texto(surface, texto, tamaño, x, y, color=texturas.blanco):
    font = pygame.font.SysFont(None, tamaño)
    render = font.render(texto, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)


def dibujar_boton(surface, texto, x, y, w, h, color=texturas.azul, texto_color=texturas.blanco):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, color, rect, border_radius=10)

    font = pygame.font.SysFont("Arial", 30)
    render = font.render(texto, True, texto_color)
    texto_rect = render.get_rect(center=rect.center)
    surface.blit(render, texto_rect)

    return rect


def main():
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
    mostrar_nave = False
    mostrar_mundo = False
    nombre = ""
    decision = None

    boton_panel = None  

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
                            print("adios")
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_y:
                            print("Comienza tu misión")
                            mostrar_dialogos = False
                            mostrar_nave = True

           
            if mostrar_nave and not mostrar_mundo:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_panel and boton_panel.collidepoint(event.pos):
                        print("Panel abierto. Cargando mundo…")
                        mostrar_nave = False
                        mostrar_mundo = True

      

        if mostrar_dialogos:
            ventana.fill((0, 0, 0))

            if capturando_nombre:
                dibujar_texto(ventana, dialogos[0], 35, texturas.width // 2, texturas.height // 2 - 40)
                dibujar_texto(ventana, nombre, 40, texturas.width // 2, texturas.height // 2)
            else:
                dibujar_texto(ventana, dialogos[indice], 35, texturas.width // 2, texturas.height // 2)

        elif mostrar_nave and not mostrar_mundo:
            ventana.fill((20, 20, 30))

            boton_panel = dibujar_boton(
                ventana,
                "Abrir panel de control",
                texturas.width // 2 - 150,
                texturas.height // 2 - 50,
                300,
                80
            )

        elif mostrar_mundo:
            ventana.fill((0, 0, 0))
            mundo.draw(ventana)
            personaje.draw(ventana)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                personaje.move(-5, 0, mundo)
            if keys[pygame.K_d]:
                personaje.move(5, 0, mundo)
            if keys[pygame.K_w]:
                personaje.move(0, -5, mundo)
            if keys[pygame.K_s]:
                personaje.move(0, 5, mundo)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

