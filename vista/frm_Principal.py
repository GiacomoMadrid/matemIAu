from datetime import datetime
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

class Ventana:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption("Multi-Game (con Maya :3)")

        self.ICONO_VENTANA = "imagenes/icono.png"
        self.ANCHO_VENTANA = 900
        self.ALTO_VENTANA = 600

        icono = pygame.image.load(self.ICONO_VENTANA)

        self.ventana = pygame.display.set_mode([self.ANCHO_VENTANA, self.ALTO_VENTANA])
        pygame.display.set_icon(icono)
        

    