import pygame, sys
import Constantes

pygame.init()

pygame.display.set_caption("Crucigrama") 

Ventana = pygame.display.set_mode(Constantes.Coordenadas)
"""Resumen: En esta sección se inicializa, se le heredan coordenadas y se le otorga un nombre a la ventana 
"""


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Se ha cerrado correctamente")
            sys.exit()

