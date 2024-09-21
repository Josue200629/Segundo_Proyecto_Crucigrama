import pygame 
import Constantes


pygame.init()

Ventana = pygame.display.set_mode((Constantes.Ancho,Constantes.Alto))
run = True
while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.QUIT()

            
