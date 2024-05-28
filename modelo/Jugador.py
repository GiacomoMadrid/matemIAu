from datetime import datetime
from vista.frm_Principal import Ventana
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite) 
        
        # Sprites       
        self.SPRITE_JUGADOR = "imagenes/jugador.png" 
        self.SPRITE_JUGADOR_DERROTA = "imagenes/jugador_derrota.png"
        self.SPRITE_JUGADOR_VICTORIA = "imagenes/jugador_victoria.png" 

        self.LISTA_NUMEROS_JUGADOR = [2, 3, 5, 7]
        self.GRAVEDAD = 2 # Gravedad (para los saltos)

        #Los archivos de efectos de sonido deben estar en formato .ogg
        self.SONIDO_MOVIMIENTO = "sonidos/motion.ogg" 
        
        self.image = pygame.image.load(self.SPRITE_JUGADOR).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = (Ventana().ANCHO_VENTANA)/2 - self.rect.width/2
        self.rect.y = Ventana().ALTO_VENTANA - self.rect.height
        self.velocidad_x = 0
        self.velocidad_y = 0
    
    def update(self):
        # Cambio de velocidad en el eje Y producto de la gravedad (para que caiga cuando salte)
        if self.rect.x <  Ventana().ANCHO_VENTANA - self.rect.width:
            self.velocidad_y = self.velocidad_y + self.GRAVEDAD
        
        # Verificar que no se salga de los limites de la pantalla en el eje X
        if self.rect.x + self.velocidad_x < 0 or Ventana().ANCHO_VENTANA - self.rect.width < self.rect.x + self.velocidad_x:
            self.velocidad_x = 0
        
        # Verificar que no se salga de los limites inferiores de la pantalla en el eje Y
        if Ventana().ALTO_VENTANA - self.rect.height < self.rect.y + self.velocidad_y:
            self.velocidad_y = 0
        
        # Verificar que no se salga de los limites superiores de la pantalla en el eje Y 
        if self.rect.y + self.velocidad_y < 0:
            self.velocidad_y = -self.velocidad_y

        # Movimiento
        self.rect.x = self.rect.x + self.velocidad_x
        self.rect.y = self.rect.y + self.velocidad_y
    
    def actualizar_sprite_derrota(self):
        self.image = pygame.image.load(self.SPRITE_JUGADOR_DERROTA).convert_alpha()

    def actualizar_sprite_victoria(self):
        self.image = pygame.image.load(self.SPRITE_JUGADOR_VICTORIA).convert_alpha()

    def asignar_numero(self): # Se asigna el numero cuyos multiplos debemos buscar
        # Numero
        #self.number = random.randint(NUMERO_MIN_JUGADOR, NUMERO_MAX_JUGADOR)
        self.number = random.choice(self.LISTA_NUMEROS_JUGADOR)
        fuente = pygame.font.SysFont("Arial", 30, bold=True)
        texto_numero = fuente.render(str(self.number), 1, (0,0,0))
        W = texto_numero.get_width()
        H = texto_numero.get_height()
        self.image.blit(texto_numero, [self.rect.width/2 - W/2, self.rect.height/2 - H/3 +20])

        # Simbolo de multiplo
        simbolo_multiplo = fuente.render("°", 1, (0,0,0))
        W = simbolo_multiplo.get_width()
        H = simbolo_multiplo.get_height()
        self.image.blit(simbolo_multiplo, [self.rect.width/2 - W/2, self.rect.height/2 - 2*H/3 +20])
