from datetime import datetime
import mediapipe as mp
import pygame, random
import numpy as np
import cv2

from modelo.webcam import Webcam
#from modelo import Juego

#----------------------------------------- CONSTANTES DEL JUEGO --------------------------------------
# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

#Ventana
ANCHO_VENTANA = 900
ALTO_VENTANA = 600

#Constantes Generales
TIEMPO_TOTAL = 30 # En segundos
PUNTUACION_MAXIMA = 10 # Define cuándo gana el jugador
GRAVEDAD = 2 # Gravedad (para los saltos)

VELOCIDAD_Y_MIN_OBJETO = 2
VELOCIDAD_Y_MAX_OBJETO = 4

#Lista de posibles numeros con los cuales jugar (tendras que buscar los multiplos del que elijas)
LISTA_NUMEROS_JUGADOR = [2, 3, 5, 7]

#--------------------------------------------- SPRITES ----------------------------------------------

ICONO_VENTANA = "imagenes/icono.png"

FONDO_VICTORIA = "imagenes/fondo_victoria.png"
FONDO_DERROTA = "imagenes/fondo_derrota.png"
FONDO_1 = "imagenes/fondo_dia.png" 

SPRITE_JUGADOR = "imagenes/jugador.png" 
SPRITE_JUGADOR_DERROTA = "imagenes/jugador_derrota.png"
SPRITE_JUGADOR_VICTORIA = "imagenes/jugador_victoria.png" 
LISTA_LATAS = ["imagenes/lata_1.png", "imagenes/lata_2.png", "imagenes/lata_3.png", "imagenes/lata_4.png", "imagenes/lata_dorada.png"]
SPRITES_LATAS = [pygame.image.load(imagen) for imagen in LISTA_LATAS]

RELOJ = "imagenes/reloj.png"
LOGO_LATA = "imagenes/puntuacion.png"
#------------------------------------ MUSICA Y EFECTOS DE SONIDO -----------------------------------

#Los archivos de musica deben estar en formato .wav
MUSICA_JUEGO = "musica/music.wav" 
MUSICA_VICTORIA = "musica/winner.wav" 
MUSICA_DERROTA = "musica/gameover.wav" 

#Los archivos de efectos de sonido deben estar en formato .ogg
SONIDO_MOVIMIENTO = "sonidos/motion.ogg" 
SONIDO_LATA = "sonidos/coin.ogg" 
SONIDO_ERROR = "sonidos/error.ogg" 

#------------------------------------------- CLASES -------------------------------------------------

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)
        self.image = pygame.image.load(SPRITE_JUGADOR).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_VENTANA/2 - self.rect.width/2
        self.rect.y = ALTO_VENTANA - self.rect.height
        self.velocidad_x = 0
        self.velocidad_y = 0
    
    def update(self):
        # Cambio de velocidad en el eje Y producto de la gravedad (para que caiga cuando salte)
        if self.rect.x <  ANCHO_VENTANA - self.rect.width:
            self.velocidad_y = self.velocidad_y + GRAVEDAD
        
        # Verificar que no se salga de los limites de la pantalla en el eje X
        if self.rect.x + self.velocidad_x < 0 or ANCHO_VENTANA - self.rect.width < self.rect.x + self.velocidad_x:
            self.velocidad_x = 0
        
        # Verificar que no se salga de los limites inferiores de la pantalla en el eje Y
        if ALTO_VENTANA - self.rect.height < self.rect.y + self.velocidad_y:
            self.velocidad_y = 0
        
        # Verificar que no se salga de los limites superiores de la pantalla en el eje Y 
        if self.rect.y + self.velocidad_y < 0:
            self.velocidad_y = -self.velocidad_y

        # Movimiento
        self.rect.x = self.rect.x + self.velocidad_x
        self.rect.y = self.rect.y + self.velocidad_y
    
    def actualizar_sprite_derrota(self):
        self.image = pygame.image.load(SPRITE_JUGADOR_DERROTA).convert_alpha()

    def actualizar_sprite_victoria(self):
        self.image = pygame.image.load(SPRITE_JUGADOR_VICTORIA).convert_alpha()

    def asignar_numero(self): # Se asigna el numero cuyos multiplos debemos buscar
        # Numero
        #self.number = random.randint(NUMERO_MIN_JUGADOR, NUMERO_MAX_JUGADOR)
        self.number = random.choice(LISTA_NUMEROS_JUGADOR)
        fuente = pygame.font.SysFont("Arial", 30, bold=True)
        texto_numero = fuente.render(str(self.number), 1, NEGRO)
        W = texto_numero.get_width()
        H = texto_numero.get_height()
        self.image.blit(texto_numero, [self.rect.width/2 - W/2, self.rect.height/2 - H/3 +20])

        # Simbolo de multiplo
        simbolo_multiplo = fuente.render("°", 1, NEGRO)
        W = simbolo_multiplo.get_width()
        H = simbolo_multiplo.get_height()
        self.image.blit(simbolo_multiplo, [self.rect.width/2 - W/2, self.rect.height/2 - 2*H/3 +20])

class Lata(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)        
        #self.image = pygame.image.load(random.choice(LISTA_LATAS)).convert_alpha() # Elije aleatoriamente un modelo de lata
        self.imagen_aleatoria = random.choice(SPRITES_LATAS)
        self.image = self.imagen_aleatoria.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_VENTANA - self.rect.width)
        self.rect.y = 0
        self.velocidad_x = 3*random.randint(-1, 1)
        self.velocidad_y = random.randint(VELOCIDAD_Y_MIN_OBJETO, VELOCIDAD_Y_MAX_OBJETO)
    
    def update(self):
        # Verificar que no se salga de los limites de la pantalla en el eje X
        if self.rect.x + self.velocidad_x < 0 or ANCHO_VENTANA - self.rect.width < self.rect.x + self.velocidad_x:
            self.velocidad_x = -self.velocidad_x
        
        # Verificar que no se salga de los limites de la pantalla en el eje Y
        if ALTO_VENTANA - self.rect.width < self.rect.y + self.velocidad_y:
            self.rect.y = ALTO_VENTANA - self.rect.height
            self.velocidad_y = 0
        
        # Movimiento
        self.rect.x = self.rect.x + self.velocidad_x
        self.rect.y = self.rect.y + self.velocidad_y
    
    def tocar_piso(self):
        if self.rect.y == ALTO_VENTANA - self.rect.height:
            return True
        else:
            return False
    
    def asignar_numero(self):
        self.number = random.randint(1,256)
        font = pygame.font.SysFont("Arial", 30, bold=True)
        texto_numero = font.render(str(self.number), 1, BLANCO)
        W = texto_numero.get_width()
        H = texto_numero.get_height()
        self.image.blit(texto_numero, [self.rect.width/2 - W/2, self.rect.height/2 - H/2 + 10])

    def es_dorada(self):
        if self.imagen_aleatoria == SPRITES_LATAS[4]:
            return True
        else:
            return False

class Juego:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption("Multi-Game (con Maya :3)")

        icono = pygame.image.load(ICONO_VENTANA)
        pygame.display.set_icon(icono)

        self.ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
        self.fondo = pygame.image.load(FONDO_1)
        self.reloj_fps = pygame.time.Clock()

        self.lista_latas_correctas = pygame.sprite.Group() 
        self.lista_latas_incorrectas = pygame.sprite.Group() 
        self.lista_sprites = pygame.sprite.Group() 

        self.jugador = Jugador()
        self.jugador.asignar_numero()
        self.lista_sprites.add(self.jugador) 

        self.tiempo_restante = TIEMPO_TOTAL+1 
        self.puntuacion = 0 

        self.juego_iniciado = True 
        self.game_over = None 

        self.sonido_colision = pygame.mixer.Sound(SONIDO_LATA)
        self.sonido_movimiento = pygame.mixer.Sound(SONIDO_MOVIMIENTO)
        self.error_sound = pygame.mixer.Sound(SONIDO_ERROR)

        pygame.mixer.music.load(MUSICA_JUEGO)
        pygame.mixer.music.play(-1)

        # Hands de mediapipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.alpha_up = 0.5
        self.alpha_left = 0.5
        self.alpha_right = 0.5

        # Uso de webcam
        self.webcam = Webcam().start() 
        self.max_face_surf_height = 0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0
    
    def generar_latas(self):
        if self.game_over == None: # Verifica si el jugador aun no ha perdido ni ganado
            if random.randint(1, 100)%43 == 0: # Genera numeros aleatorios del 1 al 100 y crea una lata cada que salga un multiplo de 43
                lata = Lata()
                lata.asignar_numero()
                self.lista_sprites.add(lata) # Se agrega el lata a la lista de sprites del juego 
                
                # Agrega la lata generada a la lista correspondiente
                if self.es_lata_correcta(lata) == True:
                    self.lista_latas_correctas.add(lata)
                else:
                    self.lista_latas_incorrectas.add(lata)

    def procesar_eventos(self):
        for event in pygame.event.get(): # Captura los eventos para analizarlos
            if event.type == pygame.QUIT: # Verifica si el usuario cierra la pantalla
                self.juego_iniciado = False
            if event.type == pygame.KEYDOWN: # Verifica si presiona una tecla
                # Se analiza primero, el caso en que el jugador no ha ganado ni perdido (game_over = None)
                if self.game_over == None: 
                    if event.key == pygame.K_LEFT:
                        self.jugador.velocidad_x = -10
                        self.sonido_movimiento.play() # Se reproduce el sonido de movimiento
                    if event.key == pygame.K_RIGHT:
                        self.jugador.velocidad_x = 10
                        self.sonido_movimiento.play() # Se reproduce el sonido de movimiento
                    if event.key == pygame.K_SPACE:
                        self.jugador.velocidad_y = -20
                        self.sonido_movimiento.play() # Se reproduce el sonido de movimiento
                else: # Aqui se analiza el caso contrario, es decir cuando gano o perdio. Solo debe esperar el ENTER del usuario
                    if event.key == pygame.K_RETURN: # Verifica si presiona ENTER
                        if self.game_over != None: # Verifica si el jugador ha perdido o ha ganado (diferente de None)
                            self.__init__() # Se reinicia el juego
    
    def es_lata_correcta(self, lata):
        if lata.number%self.jugador.number == 0:
            return True
        else:
            return False

    def detectar_colisiones(self):
        # Correctas
        lista_latas_colisionadas = pygame.sprite.spritecollide(self.jugador, self.lista_latas_correctas, True)

        for lata in lista_latas_colisionadas:
            if lata.es_dorada(): #Si agarras una lata dorada correcta, ganas 1 punto extra
                self.puntuacion = self.puntuacion + 1

            self.lista_latas_correctas.remove(lata) # Se elimina de la lista de latas
            self.lista_sprites.remove(lata) # Se elimina de la lista de sprites (latas y jugador)

            self.puntuacion = self.puntuacion + 1 # Aumenta el puntaje
            self.sonido_colision.play() # Reproduce el sonido de la colision
            
        # Incorrectas
        lista_latas_colisionadas = pygame.sprite.spritecollide(self.jugador, self.lista_latas_incorrectas, True)

        for lata in lista_latas_colisionadas:
            self.lista_latas_incorrectas.remove(lata) # Se elimina de la lista de latas
            self.lista_sprites.remove(lata) # Se elimina de la lista de sprites (latas y jugador)

            self.puntuacion = self.puntuacion - 1 # Disminuye el puntaje
            self.error_sound.play() # Reproduce el sonido de la colision

    def eliminar_latas_del_suelo(self):
        # Eliminar las latas correctas que cayeron al suelo
        for lata in self.lista_latas_correctas:
            if lata.tocar_piso() == True:
                self.lista_sprites.remove(lata) # Se elimina de la lista de sprites (latas y jugador)
                self.lista_latas_correctas.remove(lata) # Se elimina de la lista de latas

        # Eliminar las latas incorrectas que cayeron al suelo
        for lata in self.lista_latas_incorrectas:
            if lata.tocar_piso() == True:
                self.lista_sprites.remove(lata) # Se elimina de la lista de sprites (latas y jugador)
                self.lista_latas_incorrectas.remove(lata) # Se elimina de la lista de latas

    def iniciar_logica(self):
        if self.juego_iniciado == True: # Se verifica que el juego este iniciado

            # Actualizar sprites
            self.lista_sprites.update()

            #Detectar colisiones y latas que cayeron al suelo
            self.detectar_colisiones() 
            self.eliminar_latas_del_suelo() 

            # Verificar que el puntaje no sea menor a 0
            if self.puntuacion < 0:
                self.puntuacion = 0

            # Si el jugador aun no ha ganado o perdido, verificamos que le pasa
            if self.game_over == None:
                self.tiempo_restante = self.tiempo_restante - 0.02 # Actualizamos el tiempo

                # Detecto si gana o pierde
                if int(self.tiempo_restante) > 0: # Si el tiempo es mayor a cero (tiene tiempo)
                    if self.puntuacion >= PUNTUACION_MAXIMA: # Verifica si el score es mayor o igual a la puntuacion maxima o mas, en ese caso gana
                        self.game_over = False # No ha perdido, es decir ha ganado
                        # Se reproduce sonido de game over
                        pygame.mixer.music.load(MUSICA_VICTORIA)
                        pygame.mixer.music.play(-1)
                        self.jugador.actualizar_sprite_victoria()
                else:
                    self.game_over = True # Ha perdido
                    # Se reproduce sonido de game over
                    pygame.mixer.music.load(MUSICA_DERROTA)
                    pygame.mixer.music.play(-1)
                    self.jugador.actualizar_sprite_derrota()

                # Se escribe el resultado del juego en los archivos
                self.guardar_resultados()
    
    def guardar_resultados(self):
        fecha_actual = datetime.now()
        # Se abre el archivo results para escritura
        archivo = open("resultados.txt", "a")
        # Se escribe el resultado en el archivo
        if self.game_over == False:
            archivo.write("Victoria: ,"+fecha_actual.strftime("%Y/%m/%d %H:%M:%S")+"\n")
        elif self.game_over == True:
            archivo.write("Derrota: ,"+fecha_actual.strftime("%Y/%m/%d %H:%M:%S")+"\n")
        # Se cierra el archivo
        archivo.close()
    
    def leer_resultados(self):
        # Se abre el archivo results para lectura
        archivo = open("resultados.txt", "r")
        # Se inicializan los contadores
        contador_victorias = 0
        contador_derrotas = 0
        # Se cuentan los resultados victorias y derrotas
        for line in archivo:
            line_split = line.split(',')
            if line_split[0] == "Victoria: ":
                contador_victorias = contador_victorias+1
            elif line_split[0] == "Derrota: ":
                contador_derrotas = contador_derrotas+1
        # Se retornan los resultados
        return contador_victorias, contador_derrotas

    def mostrar_informacion(self): # Se muestra la informacion en tiempo real
        fuente = pygame.font.SysFont('Showcard Gothic', 30, bold=False)
        texto_puntuacion = fuente.render(str(self.puntuacion)+" / "+str(PUNTUACION_MAXIMA), True, BLANCO)
        texto_tiempo = fuente.render(str("{:02}".format(int(self.tiempo_restante))), True, BLANCO)
        logo_reloj = pygame.image.load(RELOJ).convert_alpha()
        logo_puntuacion = pygame.image.load(LOGO_LATA).convert_alpha()

        self.ventana.blit(logo_puntuacion, (20, 20))
        self.ventana.blit(texto_puntuacion, (logo_puntuacion.get_width() + 30, 20))
        self.ventana.blit(texto_tiempo, (ANCHO_VENTANA - texto_tiempo.get_width() - 20, 20))        
        self.ventana.blit(logo_reloj, (ANCHO_VENTANA - logo_reloj.get_width() - texto_tiempo.get_width() - 30, 10))

    def pausar_movimientos(self):
        for sprite in self.lista_sprites:
            sprite.velocidad_x = 0
            sprite.velocidad_y = 0
        
        for lata in self.lista_latas_correctas:
            sprite.velocidad_x = 0
            sprite.velocidad_y = 0

        for lata in self.lista_latas_incorrectas:
            sprite.velocidad_x = 0
            sprite.velocidad_y = 0
    
    def display_frame(self):
        self.ventana.blit(self.fondo, [0, 0]) # Se dibuja el fondo
        self.lista_sprites.draw(self.ventana) # Se dibujan todos los srpites
        # Se dibuja la camara
        if self.webcam.lastFrame is not None:
            self.render_camera()
        self.mostrar_informacion() # Se dibujan los textos (puntos y tiempo)
        
        if self.game_over == False: #Si se gano el juego
            self.fondo = pygame.image.load(FONDO_VICTORIA)
            font = pygame.font.SysFont('Comic Sans', 30, bold=True)
            text = font.render("¡Ganaste!", True, BLANCO)
            # Posicion del texto
            text_x = ANCHO_VENTANA/2 - text.get_width()/2
            text_y = ALTO_VENTANA/2 - text.get_height()/2
            self.ventana.blit(text, [text_x, text_y-40])
            
            contador_victorias, contador_derrotas = self.leer_resultados()
            text = font.render("Presiona ENTER para continuar :)", True, BLANCO)
            self.ventana.blit(text, [text_x-180, text_y+10])
            
            contador_victorias, contador_derrotas = self.leer_resultados()
            text = font.render("Victorias: "+str(contador_victorias)+" | Derrotas: "+str(contador_derrotas), True, BLANCO)
            self.ventana.blit(text, [text_x-100, text_y+50])

            # Se pausa el movimiento para todos los elementos del juego
            self.pausar_movimientos()

        elif self.game_over == True: #Si se perdio el juego
            self.fondo = pygame.image.load(FONDO_DERROTA)
            font = pygame.font.SysFont('Comic Sans', 30, bold=True)
            text = font.render("GAME OVER", True, BLANCO)
            # Posicion del texto
            text_x = ANCHO_VENTANA/2 - text.get_width()/2
            text_y = ALTO_VENTANA/2 - text.get_height()/2
            self.ventana.blit(text, [text_x, text_y-40])
            
            contador_victorias, contador_derrotas = self.leer_resultados()
            text = font.render("Presiona ENTER para continuar.", True, BLANCO)
            self.ventana.blit(text, [text_x-120, text_y+10])

            contador_victorias, contador_derrotas = self.leer_resultados()
            text = font.render("Victorias: "+str(contador_victorias)+" | Derrotas: "+str(contador_derrotas), True, BLANCO)
            self.ventana.blit(text, [text_x-100, text_y+50])

            # Se pausa el movimiento para todos los elementos del juego
            self.pausar_movimientos()

        pygame.display.flip() # Se actualiza el display
    
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

                    self.detect_hands_movement(fingers, box_up, box_left, box_right)
                
            k = cv2.waitKey(1) & 0xFF
        
    def detect_hands_movement(self, fingers, box_up, box_left, box_right):
        if self.fingers_in_box(fingers, box_up) == True:
            self.jugador.velocidad_y = -10
            self.alpha_up = 0.2
        else:
            self.alpha_up = 0.5

        if self.fingers_in_box(fingers, box_left) == True:
            self.jugador.velocidad_x = -10
            self.alpha_left = 0.2
        else:
            self.alpha_left = 0.5
        
        if self.fingers_in_box(fingers, box_right) == True:
            self.jugador.velocidad_x = 10
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
        self.ventana.blit(face_surf, [ANCHO_VENTANA/2-face_area_height/2, 0])

    def run(self):
        with self.mp_hands.Hands(
            static_image_mode = False,
            max_num_hands = 1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            while self.juego_iniciado == True:

                if self.game_over == None:
                    if not self.webcam.ready():
                        continue
                    self.process_camera(hands)

                self.generar_latas()
                self.procesar_eventos()
                self.iniciar_logica()
                self.display_frame()
                self.mostrar_informacion()
                self.reloj_fps.tick(60)
            pygame.quit()

# -------------------------------------------- Main -------------------------------------------------


if __name__== "__main__" :
    g = Juego()
    g.run()