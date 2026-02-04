import pygame 
import sys
from personajes_infinito import Personaje
import texturas
from mundo_infinito import WorldInfinito
from inventario import Inventory  

pygame.init()

ventana = pygame.display.set_mode((texturas.width, texturas.height))
pygame.display.set_caption("Mi Juego - Mundo Infinito")


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

    # Crear mundo infinito
    mundo = WorldInfinito(texturas.width, texturas.height)
    
    # Crear personaje en el spawn (centro del mundo)
    personaje = Personaje(0, 0)
    
    inventario = Inventory(texturas.width, texturas.height)
    
    inventario.agregar_item("Pico", 1)
    inventario.agregar_item("Combustible", 3)
    

    dialogos = [
        "Escribe tu nombre (usa ENTER para continuar)...",
        "Soy , la IA que te guiará en tu misión.",
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

    boton_panel = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inventario.guardar_inventario("partida_guardada.json")
                pygame.quit()
                sys.exit()

            
            if mostrar_mundo:
                inventario.handle_event(event)
    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    item_en_mano = inventario.get_item_seleccionado()
                    pico_equipado = item_en_mano is not None and item_en_mano.nombre == "Pico"
                    
                    # Obtener objetos cercanos
                    objetos_cercanos = mundo.obtener_objetos_cercanos(personaje.screen_x, personaje.screen_y, radio=50)
                    
                    # PRIORIDAD 1: Calcita (Requiere Pico)
                    for c in objetos_cercanos['calcita']:
                        if personaje.esta_cerca(c, mundo):
                            if pico_equipado:
                                if inventario.agregar_item("Calcita", 1):
                                    mundo.remover_objeto(c)
                                    print("✓ Calcita minada con el pico")
                                else:
                                    print("⚠ Inventario lleno")
                            else:
                                print("¡Necesitas equipar el Pico para minar Calcita!")
                            break
                    
                    # PRIORIDAD 2: Rocas (sin herramienta)
                    else:
                        for roca in objetos_cercanos['rocas']:
                            if personaje.esta_cerca(roca, mundo):
                                if inventario.agregar_item("Roca", 1):
                                    mundo.remover_objeto(roca)
                                    print("✓ Recogido: Roca")
                                else:
                                    print("⚠ Inventario lleno!")
                                break
            
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
                            print("Adiós")
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
            
            # Dibujar el mundo con la cámara centrada en el jugador
            mundo.draw(ventana, personaje.world_x, personaje.world_y)
            
            # Dibujar el personaje (siempre en el centro)
            personaje.draw(ventana)

            # Movimiento del personaje
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                personaje.move(-5, 0, mundo)
            if keys[pygame.K_d]:
                personaje.move(5, 0, mundo)
            if keys[pygame.K_w]:
                personaje.move(0, -5, mundo)
            if keys[pygame.K_s]:
                personaje.move(0, 5, mundo)
            
            # Instrucciones
            font_instruc = pygame.font.SysFont("Arial", 14)

            render_mouse = font_instruc.render("1-0: Hotbar | Mouse: Arrastrar items", True, (150, 255, 150))
            ventana.blit(render_mouse, (10, 555))

            render_recoger = font_instruc.render("E: Recoger objetos | I: Inventario", True, (150, 255, 150))
            ventana.blit(render_recoger, (10, 540))

            # Mostrar coordenadas del jugador (opcional)
            font_coords = pygame.font.SysFont("Arial", 12)
            texto_coords = font_coords.render(f"Pos: ({int(personaje.world_x)}, {int(personaje.world_y)})", True, (255, 255, 255))
            ventana.blit(texto_coords, (10, 10))
            
            # Mostrar cantidad de chunks cargados
            texto_chunks = font_coords.render(f"Chunks: {len(mundo.chunks)}", True, (255, 255, 255))
            ventana.blit(texto_chunks, (10, 25))

            # Item equipado
            item_equipado = inventario.get_item_hotbar(inventario.hotbar_seleccionado)
            if item_equipado:
                font_equipado = pygame.font.SysFont("Arial", 16, bold=True)
                texto_eq = font_equipado.render(f"Equipado: {item_equipado.nombre}", True, (255, 215, 0))
                ventana.blit(texto_eq, (texturas.width // 2 - 70, texturas.height - 100))
       
            inventario.draw(ventana)
      

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()