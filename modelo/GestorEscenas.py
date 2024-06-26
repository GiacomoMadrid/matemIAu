import pygame

class Gestor_Escenas:
    def __init__(self, estado_Actual):
        self.estado = estado_Actual
    
    def get_estado(self):
        return self.estado

    def set_estado(self, estado):
        self.estado = estado