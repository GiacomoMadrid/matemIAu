import mediapipe as mp
import cv2
import math
import pygame as pg
import random

# -------------------------------------- CONSTANTES ----------------------------------------------

ANCHO_VENTANA = 1200
ALTO_VENTANA = 800

TIEMPO_MAXIMO = 60 # Tiempo en segundos
LISTA_RESPUESTAS = [0, 1, 2, 3, 4, 5]


#---------------------------------------- SPRITES -----------------------------------------------
SPRITE_JUGADOR = "sprites/Corazon50x50.png"
SPRITE_PARED = "sprites/Corazon50x50.png"
SPRITE_PUERTA = "sprites/Corazon50x50.png"
SPRITE_CASITA = "sprites/Corazon50x50.png"

#---------------------------------------- CLASES -------------------------------------------------

class Jugador(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(SPRITE_JUGADOR).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_VENTANA/2 - self.rect.width/2
        self.rect.y = ALTO_VENTANA - self.rect.height
        self.vida_inicial = 4
        self.velocidad_x = 0
        self.velocidad_y = 0
    
    def update(self):
        #Verificar que el jugador no se salga de los limites del escenario
        if (self.rect.x + self.velocidad_x < 0) or (ANCHO_VENTANA - self.rect.width < self.rect.x + self.velocidad_x):
            self.velocidad_x = 0
        
        if (ALTO_VENTANA - self.rect.height < self.rect.y + self.velocidad_y):
            self.velocidad_y = 0
        
        if (self.rect.y + self.velocidad_y < 0):
            self.velocidad_y = -self.velocidad_y

        #Actualizar hitbox
        self.rect.x = self.rect.x + self.velocidad_x
        self.rect.y = self.rect.y + self.velocidad_y

class Pared(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(SPRITE_PARED).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_VENTANA/2 - self.rect.width/2
        self.rect.y = ALTO_VENTANA - self.rect.height

class Puerta(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(SPRITE_PUERTA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_VENTANA/2 - self.rect.width/2
        self.rect.y = ALTO_VENTANA - self.rect.height
        self.estado = False
    
    def asignar_resta(self):
        n = random.randint(0, 20)
        m  = n + random.choice(LISTA_RESPUESTAS)
        return m-n
    
    def asignar_suma(self):
        n = random.choice(LISTA_RESPUESTAS) 
        m = random.randint(0, (5-n))
        return n+m
    
    def asignar_operacion(self):
        opera = random.randint(1,100)

        if (opera%2 == 0):
            self.asignar_resta()
        else:
            self.asignar_suma



#----------------------------------------- MAIN --------------------------------------------------