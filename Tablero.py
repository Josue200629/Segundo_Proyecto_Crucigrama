import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
size = 400  # Tamaño total de la ventana
border_width = 103  # Ancho del área para botones en el lado izquierdo
border_height = 103  # Altura del área para botones en la parte inferior
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("Cuadrícula con Botones")

# Tamaño del tablero
rows = 8
cols = 8
# Ajustar tamaño de los cuadrados
square_size = (size - border_width) // cols  # Tamaño de cada cuadrado

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(rows + 1):
        pygame.draw.line(screen, (255, 255, 255), (border_width, row * square_size), (size, row * square_size))
    for col in range(cols + 1):
        pygame.draw.line(screen, (255, 255, 255), (border_width + col * square_size, 0), (border_width + col * square_size, size - border_height))

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # Limpiar la pantalla con negro
    draw_grid()  # Dibujar la cuadrícula
    
    # Dibujar el área para botones en el lado izquierdo
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, border_width, size))  # Área de botones
    # Dibujar el área para botones en la parte inferior
    pygame.draw.rect(screen, (50, 50, 50), (0, size - border_height, size, border_height))  # Área de botones inferior
    
    pygame.display.flip()  # Actualizar la pantalla
