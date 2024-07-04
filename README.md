# MatemIAu:
Videojuego en pygame con IA protagonizado por la gata Maya :3 

## Para ejecutar:
### 1) Descargar e instalar Python 3.9.0:
De sitio oficial: https://www.python.org/downloads/release/python-390/
O desde el instalador que viene entre los archivos del repositorio
  
### 2) Descargar e instalar Visual Studio Code:
De su sitio oficial: https://code.visualstudio.com/
Una vez instalado, proceda a instalarle la extensión para Python de VS-Code de su preferencia.
         
### 3) Crear un entorno virtual:
###### 3.1) Luego de haber instalado Python 3.9.0 y VS-Code de manera exitosa, abra una terminal en VS-Code del símbolo del sistema en la ubicación de la raíz de las carpetas del programa.
###### 3.2) Asegúrese de tener pip instalado con el comando:  

    pip --version. 
         
###### 3.2) En la linea de comandos escriba el siguiente comando para instalar el entorno virtual: 

    pip install virtualenv 
         
###### 3.3) Escriba el siguiente comando **reemplazando [ruta]** por la ruta donde se encuentra instalado Python 3.9.0 y **[nombre]** por el nombre que desee colocarle al entorno virtual (por ejemplo: venv):

    virtualenv -p "[ruta]" [nombre]
  
###### 3.4) Una vez creado el entorno escriba el siguiente comando (Windows) para activar el entorno:

    .\venv\Scripts\activate
  
### 4) Instalar dependencias:
Una vez dentro del entorno virtual procedemos a instalar todas las dependencias desde el archivo requirements.txt:

    pip install -r requirements.txt
  
### 5) Ejecutar:
###### 5.1) Una vez instaladas todas las dependencias, nos dirigimos al archivo Webcam.py dentro de la carpeta Modelo.
En la linea 21:
         
    self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
             
El pimer parámetro del método VideoCapture (el número 0) representa a la cámara por defecto (en laptops) o al primer dispositivo de captura de video coenctado (en PCs de escritorio). 

Puede ajustar este valor según sea el dispositivo de captura de video que desee usar, teniendo en cuenta que este número depende del orden en el que los dispositivos fueron conectados (empezando del 0). Por ejemplo, si desea usar una webcam conectada a una laptop que ya tiene una cámara por defecto, el número que debería usar es el 1, de este modo el programa sabrá que debe usar el dispositivo en la posición 1, siendo el 0 siempre el valor de la cámara por defecto.

###### 5.2) Guarde lo cambios, en caso los haya.
###### 5.3) Procedemos a ejecutar el archivo desde el main.
###### 5.4) Disfrute el juego.
         
Creado en base a mate-game: https://github.com/jorgektch/videojuego-pygame-ia
