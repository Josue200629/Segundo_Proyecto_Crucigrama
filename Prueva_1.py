import pygame
import sys

# Inicializa pygame
pygame.init()
size = (700, 700)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Título")

# Configura la fuente
font = pygame.font.Font(None, 36)

# Variables para la entrada de texto
input_box = pygame.Rect(100, 80, 200, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
palabras = []

# Color del texto
text_color = pygame.Color('white')  # Cambia a tu color deseado

# Función para convertir a binario
def texto_a_binario(texto):
    return ' '.join(format(ord(caracter), '08b') for caracter in texto)

# Variable para mostrar el texto en binario
binario_text = ''

running = True
# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en la caja de entrada
            if input_box.collidepoint(event.pos):
                active = not active  # Cambia el estado activo
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:  # Presiona Enter
                    print('Texto ingresado:', text)
                    palabras.append(text)
                    binario_text = texto_a_binario(text)
                    text = ''  # Limpia la entrada
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]  # Eliminar el último carácter
                else:
                    text += event.unicode  # Agrega el carácter ingresado
        
        if event.type == pygame.VIDEORESIZE:
            # Ajusta el tamaño de la ventana al nuevo tamaño
            size = (event.w, event.h)
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
 
    screen.fill((0, 128, 128))  # Color de fondo de la ventana
    pygame.draw.rect(screen, color, input_box, 2)  # Dibuja el borde de la caja de entrada

    # Renderiza el texto en el color deseado
    text_surface = font.render(text, True, text_color)  # Cambia el color del texto aquí
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))  # Dibuja el texto en la caja de entrada

    # Renderiza el texto en binario
    binario_surface = font.render(binario_text, True, text_color)
    screen.blit(binario_surface, (100, 150))  # Dibuja el texto en binario

    # Actualiza la pantalla
    pygame.display.flip()

pygame.quit()