from vista.frm_Principal import Ventana
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

class Comida_danninna(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.LISTA_COMIDA = ["imagenes/lata_1.png", "imagenes/lata_2.png", "imagenes/lata_3.png", "imagenes/lata_4.png", "imagenes/lata_dorada.png"]
        self.SPRITES_COMIDA = [pygame.image.load(imagen) for imagen in self.LISTA_LATAS]

        # Los efectos de sonido deben estaren formato .ogg
        self.SONIDO_ERROR = "sonidos/error.ogg"

        self.VELOCIDAD_Y_MIN = 3
        self.VELOCIDAD_Y_MAX = 5

        self.imagen_aleatoria = random.choice(self.SPRITES_COMIDA)
        self.image = self.imagen_aleatoria.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, (Ventana().ANCHO_VENTANA) - self.rect.width)
        self.rect.y = 0
        self.velocidad_x = 3*random.randint(-1, 1)
        self.velocidad_y = random.randint(self.VELOCIDAD_Y_MIN, self.VELOCIDAD_Y_MAX)
        

    