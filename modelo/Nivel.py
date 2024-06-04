from datetime import datetime
from vista.frm_Principal import Ventana
from modelo.Jugador import Jugador
from modelo.Lata import Lata
from modelo.webcam import Webcam
from modelo.comida_dannina import Comida_dannina
from modelo.Vida import Vida
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

class Nivel:
    def __init__(self, 
                 id, # Identificador del nivel
                 fondo, #Fondo base
                 fondo_victoria, #Fondo Victoria
                 fondo_derrota, #Fondo Derrota
                 velocidad_min, #Velocidad minima de  los objetos
                 velocidad_max, #Velocidad maxima de los objetos
                 tiempo_inicial, #Tiempo inicial del nivel
                 tiempo_extra, #Tiempo extra por acierto
                 ):
        
        #Fondos:        
        self.FONDO = fondo 
        self.FONDO_VICTORIA = fondo_victoria
        self.FONDO_DERROTA = fondo_derrota

        #Tiempo
        self.TIEMPO_TOTAL = tiempo_inicial        
        self.TIEMPO_EXTRA = tiempo_extra

        #Objetos
        self.VELOCIDAD_MIN = velocidad_min
        self.VELOCIDAD_MAX = velocidad_max  

        #Generalidades:        
        self.nombre = id
        self.PUNTUACION_GANADORA = 10 # Define cuándo gana el jugador  


