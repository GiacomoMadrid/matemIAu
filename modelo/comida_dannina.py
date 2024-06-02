from vista.frm_Principal import Ventana
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

class Comida_dannina(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.LISTA_COMIDA = ["imagenes/chocolate_1.png", "imagenes/chocolate_2.png", "imagenes/chocolate_3.png", "imagenes/chocolate_4.png"]
        self.SPRITES_COMIDA = [pygame.image.load(imagen) for imagen in self.LISTA_COMIDA]

        # Los efectos de sonido deben estaren formato .ogg
        self.SONIDO_ERROR = "sonidos/error.ogg"

        self.VELOCIDAD_Y_MIN = 2
        self.VELOCIDAD_Y_MAX = 3

        self.imagen_aleatoria = random.choice(self.SPRITES_COMIDA)
        self.image = self.imagen_aleatoria.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, (Ventana().ANCHO_VENTANA) - self.rect.width)
        self.rect.y = 0
        self.velocidad_x = 3*random.randint(-1, 1)
        self.velocidad_y = random.randint(self.VELOCIDAD_Y_MIN, self.VELOCIDAD_Y_MAX)

    def update(self):
        # Verificar que no se salga de los limites de la pantalla en el eje X
        if self.rect.x + self.velocidad_x < 0 or Ventana().ANCHO_VENTANA - self.rect.width < self.rect.x + self.velocidad_x:
            self.velocidad_x = -self.velocidad_x
        
        # Verificar que no se salga de los limites de la pantalla en el eje Y
        if Ventana().ALTO_VENTANA - self.rect.height- 150 < self.rect.y + self.velocidad_y:
            self.rect.y = Ventana().ALTO_VENTANA - self.rect.height - 150
            self.velocidad_y = 0
        
        # Movimiento
        self.rect.x = self.rect.x + self.velocidad_x
        self.rect.y = self.rect.y + self.velocidad_y
    
    def tocar_piso(self):
        if self.rect.y == Ventana().ALTO_VENTANA - self.rect.height - 150:
            return True
        else:
            return False  

    