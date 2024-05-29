from datetime import datetime
from vista.frm_Principal import Ventana
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

class Lata(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.LISTA_LATAS = ["imagenes/lata_1.png", "imagenes/lata_2.png", "imagenes/lata_3.png", "imagenes/lata_4.png", "imagenes/lata_dorada.png"]
        self.SPRITES_LATAS = [pygame.image.load(imagen) for imagen in self.LISTA_LATAS]

        #Los archivos de efectos de sonido deben estar en formato .ogg
        self.SONIDO_LATA = "sonidos/coin.ogg" 
        self.SONIDO_ERROR = "sonidos/error.ogg" 
        
        self.VELOCIDAD_Y_MIN = 2
        self.VELOCIDAD_Y_MAX = 4
                
        self.imagen_aleatoria = random.choice(self.SPRITES_LATAS)
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
        if Ventana().ALTO_VENTANA - self.rect.width < self.rect.y + self.velocidad_y:
            self.rect.y = Ventana().ALTO_VENTANA - self.rect.height
            self.velocidad_y = 0
        
        # Movimiento
        self.rect.x = self.rect.x + self.velocidad_x
        self.rect.y = self.rect.y + self.velocidad_y
    
    def tocar_piso(self):
        if self.rect.y == Ventana().ALTO_VENTANA - self.rect.height:
            return True
        else:
            return False
    
    def asignar_numero(self):
        self.number = random.randint(0,25)
        font = pygame.font.SysFont("Arial", 30, bold=True)
        texto_numero = font.render(str(self.number), 1, (255, 255, 255))
        W = texto_numero.get_width()
        H = texto_numero.get_height()
        self.image.blit(texto_numero, [self.rect.width/2 - W/2, self.rect.height/2 - H/2 + 10])

    def asignar_numero_correcto(self, num):
        self.number = num
        font = pygame.font.SysFont("Arial", 30, bold=True)
        texto_numero = font.render(str(self.number), 1, (255, 255, 255))
        W = texto_numero.get_width()
        H = texto_numero.get_height()
        self.image.blit(texto_numero, [self.rect.width/2 - W/2, self.rect.height/2 - H/2 + 10])

    def es_dorada(self):
        if self.imagen_aleatoria == self.SPRITES_LATAS[4]:
            return True
        else:
            return False
