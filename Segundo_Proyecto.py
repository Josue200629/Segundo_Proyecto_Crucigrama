import pygame, sys
import Constantes

#Creación de la ventana
pygame.init()
pygame.display.set_caption("Crucigrama") 
#Ventana = pygame.display.set_mode(Constantes.Coordenadas)
#Ventana.fill(Constantes.BLANCO)
#Actualiza la pantalla


screen = pygame.display.set_mode(Constantes.Coordenadas, pygame.RESIZABLE)

# Configura la fuente
font = pygame.font.Font(None, 36)

# Color del texto
text_color = pygame.Color('white')  # Cambia a tu color deseado


# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Se ha cerrado correctamente")
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en la caja de entrada
            if Constantes.input_box.collidepoint(event.pos):
                active = not Constantes.active  # Cambia el estado activo
            else:
                active = False
            Constantes.color = Constantes.color_active if active else Constantes.color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:  # Presiona Enter
                    print('Texto ingresado:', Constantes.text)
                    Constantes.palabras.append(Constantes.text)
                    Constantes.text = ''  # Limpia la entrada
                elif event.key == pygame.K_BACKSPACE:
                    text = Constantes.text[:-1]  # Eliminar el último carácter
                else:
                    Constantes.text += event.unicode  # Agrega el carácter ingresado
        
        if event.type == pygame.VIDEORESIZE:
            # Ajusta el tamaño de la ventana al nuevo tamaño
            size = (event.w, event.h)
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
 
    screen.fill((0, 128, 128))  # Color de fondo de la ventana
    pygame.draw.rect(screen, Constantes.color, Constantes.input_box, 2)  # Dibuja el borde de la caja de entrada

    # Renderiza el texto en el color deseado
    text_surface = font.render(Constantes.text, True, text_color)  # Cambia el color del texto aquí
    screen.blit(text_surface, (Constantes.input_box.x + 5, Constantes.input_box.y + 5))  # Dibuja el texto en la caja de entrada

    # Actualiza la pantalla
    pygame.display.flip()

"""Resumen:
"""
#Sección 2

"""Resumen:
"""
