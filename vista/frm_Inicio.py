from datetime import datetime
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

from vista.frm_Principal import Ventana
from controlador.Controlador_Principal import Controlador_Principal
from modelo.GestorEscenas import Gestor_Escenas

class Frm_Inicial:
    def __init__(self):
        pygame.init()
        
        #------- Configuraciones de ventana:
        self.ICONO_VENTANA = "imagenes/icono.png"
        self.ANCHO_VENTANA = 900
        self.ALTO_VENTANA = 600        
        self.FONDO = "imagenes/fondo_menu.png"
        self.ventana = pygame.display.set_mode([self.ANCHO_VENTANA, self.ALTO_VENTANA])        
        icono = pygame.image.load(self.ICONO_VENTANA)
        pygame.display.set_icon(icono)
        pygame.display.set_caption("MatemIAu - Menu")
        self.fondo = pygame.image.load(self.FONDO)

        #------- Íconos de botones:
        self.LOGO_JUGAR = "imagenes/btnJugar.png"
        self.LOGO_JUGAR2 = "imagenes/btnJugar2.png"
        self.LOGO_PERSONAJE = "imagenes/btnPersonaje.png"
        self.LOGO_PERSONAJE2 = "imagenes/btnPersonaje2.png"
        self.LOGO_SALIR = "imagenes/btnSalir.png"
        self.LOGO_SALIR2 = "imagenes/btnSalir2.png"

        self.logo_btn_jugar = pygame.image.load(self.LOGO_JUGAR).convert_alpha()
        self.logo_btn_personaje = pygame.image.load(self.LOGO_PERSONAJE).convert_alpha()        
        self.logo_btn_salirr = pygame.image.load(self.LOGO_SALIR).convert_alpha()  

        #------- Otros atributos:
        self.personaje = 'maya'
        self.gestor = Gestor_Escenas('menu')
        self.diccionario_estados = {'play': self.play(self, self.personaje), 'personaje': self.elegir_personaje(self)}




    def display_frame(self):
        self.ventana.blit(self.fondo, [0, 0]) # Dibujar el fondo
        self.ventana.blit(self.logo_btn_jugar, [self.ANCHO_VENTANA/2, self.ALTO_VENTANA/2 - 120])
        self.ventana.blit(self.logo_btn_jugar, [self.ANCHO_VENTANA/2, self.ALTO_VENTANA/2])
        self.ventana.blit(self.logo_btn_jugar, [self.ANCHO_VENTANA/2, self.ALTO_VENTANA/2 + 120])
        

    #def play(self, personaje):
        #self.ventana.fill('black')
        #pygame.display.set_caption("MatemIAu con "+personaje)
        #vista = Ventana()
        #controlador_principal = Controlador_Principal(vista)
        #controlador_principal.run()
        

    def restaurar_logos(self):
        self.logo_btn_jugar = pygame.image.load(self.LOGO_JUGAR).convert_alpha()
        self.logo_btn_personaje = pygame.image.load(self.LOGO_PERSONAJE).convert_alpha()        
        self.logo_btn_salirr = pygame.image.load(self.LOGO_SALIR).convert_alpha()        


    def elegir_personaje(self):
        self.personaje = ''


    
    def point_in_box(self, p, box):
        x, y, w, h = box[0], box[1], box[2], box[3]
        if x<p[0] and p[0]<x+w and y<p[1] and p[1]<y+h:
            return True
        else:
            return False

    def fingers_in_box(self, finger_list, box):
        cont = 0
        for i in range(len(finger_list)):
            if self.point_in_box(finger_list[i], box) == False:
                return False
        return True
    
    def process_camera(self, hands):
        image = self.webcam.read()
        if image is not None:
            height, width, _ = image.shape
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            self.webcam_image = image
            results = hands.process(image) # Procesador de hands
            
            margin = 10

            x_up, y_up, w_up, h_up = int(width/3)+margin, margin, int(width/3)-2*margin, int(height/2)-2*margin
            sub_image = image[y_up:y_up+h_up, x_up:x_up+w_up]
            BLANCO_rect = np.ones(sub_image.shape, dtype=np.uint8) * 255
            image[y_up:y_up+h_up, x_up:x_up+w_up] = cv2.addWeighted(sub_image, self.alpha_up, BLANCO_rect, 1-self.alpha_up, 1.0)
            
            x_down, y_down, w_down, h_down = int(width/3)+margin,  int(height/2)+margin,  int(width/3)-2*margin, int(height/2)-2*margin
            sub_image = image[y_down:y_down+h_down, x_down:x_down+w_down]
            BLANCO_rect = np.ones(sub_image.shape, dtype=np.uint8) * 255
            image[y_down:y_down+h_down, x_down:x_down+w_down] = cv2.addWeighted(sub_image, self.alpha_down, BLANCO_rect, 1-self.alpha_down, 1.0)

            x_left, y_left, w_left, h_left = margin, int(height/2)+margin, int(width/3)-2*margin, int(height/2)-2*margin
            sub_image = image[y_left:y_left+h_left, x_left:x_left+w_left]
            BLANCO_rect = np.ones(sub_image.shape, dtype=np.uint8) * 255
            image[y_left:y_left+h_left, x_left:x_left+w_left] = cv2.addWeighted(sub_image, self.alpha_left, BLANCO_rect, 1-self.alpha_left, 1.0)

            x_right, y_right, w_right, h_right = int(2*width/3)+margin, int(height/2)+margin, int(width/3)-2*margin, int(height/2)-2*margin
            sub_image = image[y_right:y_right+h_right, x_right:x_right+w_right]
            BLANCO_rect = np.ones(sub_image.shape, dtype=np.uint8) * 255
            image[y_right:y_right+h_right, x_right:x_right+w_right] = cv2.addWeighted(sub_image, self.alpha_right, BLANCO_rect, 1-self.alpha_right, 1.0)
            
            box_up = [x_up, y_up, w_up, h_up]
            box_left = [x_left, y_left, w_left, h_left]
            box_right = [x_right, y_right, w_right, h_right]            
            box_down = [x_down, y_down, w_down, h_down]

            if results.multi_hand_landmarks is not None:

                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(255,255,0), thickness=4, circle_radius=5),
                        self.mp_drawing.DrawingSpec(color=(255,0,255), thickness=4))
                    
                    # Posicion del dedo pulgar
                    x1 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x * width)
                    y1 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y * height)
                    # Posicion del dedo indice
                    x2 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                    y2 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                    # Posicion del dedo medio
                    x3 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)
                    y3 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)
                    # Posicion del dedo anular
                    x4 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].x * width)
                    y4 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y * height)
                    # Posicion del dedo mennique
                    x5 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP].x * width)
                    y5 = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y * height)

                    fingers = [[x1,y1], [x2,y2], [x3,y3], [x4,y4], [x5,y5]]                    

                    self.detect_hands_movement(fingers, box_up, box_left, box_right, box_down)
                
            k = cv2.waitKey(1) & 0xFF
        
    def detect_hands_movement(self, fingers, box_up, box_left, box_right, box_down):
        if self.fingers_in_box(fingers, box_up) == True:
            self.jugador.velocidad_y = -1*self.VELOCIDAD_MOVIMIENTO
            self.jugador.velocidad_x = 0
            self.alpha_up = 0.2
        else:
            self.alpha_up = 0.5

        if self.fingers_in_box(fingers, box_down) == True:
            self.jugador.velocidad_y = self.VELOCIDAD_MOVIMIENTO
            self.jugador.velocidad_x = 0
            self.box_down = 0.2
        else:
            self.box_down = 0.5

        if self.fingers_in_box(fingers, box_left) == True:
            self.jugador.velocidad_x = -1*self.VELOCIDAD_MOVIMIENTO
            self.jugador.velocidad_y = 0
            self.alpha_left = 0.2
        else:
            self.alpha_left = 0.5
        
        if self.fingers_in_box(fingers, box_right) == True:
            self.jugador.velocidad_x = self.VELOCIDAD_MOVIMIENTO
            self.jugador.velocidad_y = 0
            self.alpha_right = 0.2
        else:
            self.alpha_right = 0.5
   
    def render_camera(self):
        # Limpiar coordenadas del cuadro de la cara
        if self.face_left_x < 0: self.face_left_x = 0
        if self.face_right_x > 1: self.face_right_x = 1
        if self.face_top_y < 0: self.face_top_y = 0
        if self.face_bottom_y > 1: self.face_bottom_y = 1
        
        face_surf = pygame.image.frombuffer(self.webcam_image, (int(self.webcam.width()), int(self.webcam.height())), "BGR")
        
        # Se redimensiona la imagen del la webcam en el lienzo
        height = face_surf.get_rect().height
        width = face_surf.get_rect().width
        face_ratio = height / width

        face_area_width = 200
        face_area_height = face_area_width * face_ratio

        face_surf = pygame.transform.scale(face_surf, (int(face_area_width),int(face_area_height)))
        #self.vista.ventana.blit(face_surf, [(self.vista.ANCHO_VENTANA)/2-face_area_height/2, (self.vista.ALTO_VENTANA)-face_area_height])
        self.vista.ventana.blit(face_surf, [(self.vista.ANCHO_VENTANA)/2-face_area_height/2, (self.vista.ALTO_VENTANA)-face_area_height])
       
        

    
    


        


    
