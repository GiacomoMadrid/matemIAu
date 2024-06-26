from datetime import datetime
import mediapipe as mp
import pygame, random
import numpy as np
import cv2
from frm_Inicio import Frm_Inicial 
from modelo.GestorEscenas import Gestor_Escenas

class Frm_Personaje:
    def __init__(self, Frm_Inicial, Gestor_Escenas):
        pygame.init()
        self.personaje = 'maya'
        self.ventana = Frm_Inicial.ventana
        self.gestor = Gestor_Escenas('personaje')
        self.FONDO_1 = "imagenes/fondo_dia.png"
        self.fondo = pygame.image.load(self.FONDO_1) 

    def run(self):        
        self.ventana.fill('black')
        self.ventana.display.set_caption('Seleción de Personaje')
        

    def dibujar_pantalla(self):
        self.ventana.blit(self.fondo, [0, 0]) # Se dibuja el fondo

    
    def get_personaje(self):
        return self.personaje
    
    