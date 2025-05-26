# PAQUETES
import speech_recognition as sr
import keyboard
import pygame
import dic
import time
# For the Video class
# pymediainfo y ffpyplayer.player usan un mismo recurso en Mac y por eso no se puede usar ELiSE con este sistema operativo
from pymediainfo import MediaInfo
from ffpyplayer.player import MediaPlayer
from os.path import exists, basename, splitext
from os import strerror
from errno import ENOENT

# RECONOCIMIENTO DE VOZ

# Función que dados un micrófono (microphone) i un recognizer, saca la transcripción. Modificado para que sea en español.
# Es la usada en main_short. NO MODIFICAR
def recognize_speech_from_mic_short(recognizer:sr.Recognizer, microphone:sr.Microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        # Calibración el ruido ambiental. Si se dice algo aquí, no se transcribe.
        recognizer.adjust_for_ambient_noise(source)
        # Informa al usuario de que hable
        print('Habla ahora')
        # Grabación del enunciado del usuario
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='es-ES')
        # es-ES: Español
        # ca-ES: Català
        # nothing: English
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

# r = sr.Recognizer     mic = sr.Microphone
def recognize_speech_from_mic_pressing_space(r:sr.Recognizer, mic:sr.Microphone):
    transcripcion = ' '

    ''' Check that recognizer and microphone arguments are appropriate type
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    '''
    with mic as source:
        print("Ajustando al ruido de fondo")
        r.adjust_for_ambient_noise(source)
        print('Listo')

        while True:
            if keyboard.is_pressed('space'):  # Aqui poner presionar tecla

                # set up the response object
                response = {
                    "success": True,
                    "error": None,
                    "transcription": None
                }

                # try recognizing the speech in the recording
                # if a RequestError or UnknownValueError exception is caught,
                #     update the response object accordingly
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio, language='es-ES')
                    print(f"Dices: {text}")
                    transcripcion += f' {text}'
                except sr.UnknownValueError:
                    # speech was unintelligible
                    response["error"] = "Unable to recognize speech"
                except sr.RequestError as e:
                    # API was unreachable or unresponsive
                    response["success"] = False
                    response["error"] = f"API unavailable,{e}"
                if 'salir' in text.lower():
                    print('Has ordenado salir')
                    response["transcription"] = transcripcion
                    return response
            if keyboard.is_pressed('q'):
                print('Has presionado Q')
                response["transcription"] = transcripcion
                return response

# ESTA FUNCIÓN FUNCIONA FUERA DEL GAME LOOP. VAMOS A ADAPTARLA
def recognize_speech_from_mic_long(r:sr.Recognizer, mic:sr.Microphone, screen:pygame.surface.Surface, fuente:pygame.font.Font):
    transcripcion = ' '
    # Esta función también gestiona las pantallas, por eso las pide como argumento
    ''' Si la función está dentro del loop de main_hold, esto no le hace falta.
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with mic as source:
        # Estos print los pondremos en la pantalla
        print("Ajustando al ruido de fondo")
        r.adjust_for_ambient_noise(source)
        print('Listo')
    '''

    grabando = False # Variable para controlar el estado de la grabación
    ejecutando = True
    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Salir
                    print("Has presionado 'q'. Saliendo...")
                    response["transcription"] = transcripcion
                    return response
                if event.key == pygame.K_SPACE and not grabando:  # Iniciar grabación
                    grabando = True
                    print("Grabando...")
                elif event.key == pygame.K_RETURN and grabando :  # Detener grabación. Tarda en reaccionar
                    grabando = False
                    print("Grabación detenida.")

        if grabando:
            pantalla_escucha(screen, fuente)
            print('Escuchando')
            with mic as source:

                # set up the response object
                response = {
                    "success": True,
                    "error": None,
                    "transcription": None
                }

                # try recognizing the speech in the recording
                # if a RequestError or UnknownValueError exception is caught,
                #     update the response object accordingly
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio, language='es-ES')
                    print(f"Dices: {text}")
                    transcripcion += f' {text}'
                    response['error']: None
                    response["success"]: True
                except sr.UnknownValueError:
                    # speech was unintelligible
                    response['success']: False
                    response["error"] = "Unable to recognize speech"
                    print("Unable to recognize speech")
                    text = ' '

                except sr.RequestError as e:
                    # API was unreachable or unresponsive
                    response["success"] = False
                    response["error"] = f"API unavailable,{e}"
                    text = ' '

                 # Este bloque permite control por voz, útil para cuando el teclado no va
                if 'salir' in text.lower():
                    print('Has ordenado salir')
                    response["transcription"] = transcripcion
                    return response

                if 'parar' in text.lower():
                    grabando = False
                    print('Paramos de grabar')
                
            if not grabando:
                pantalla_espera_escucha(screen,fuente)
                print('Not grabando')


# IDENTIFICACIÓN DE PALABRAS
# Función que extrae los elementos en común de dos listas (en desorden)
def intersec_sets(list1:list,list2:list):
    set1=set(list1)
    set2=set(list2)
    out_set=set1.intersection(set2) # los sets de por si no tienen orden
    out=list(out_set) # La salida es una lista con los elementos en común
    return out

# Función que extrae los elementos en común de dos listas (en el orden de la primera lista)
def superlist(list1:list,list2:list):
    listout=list() # Así defino un set vacío
    for item in list1:
        if item in list2:
            listout.append(item)
    return listout

# REPRODUCCIÓN DE VÍDEOS
# La clase Video permite la reproducción de vídeos
class Video:
    def __init__(self, path):
        self.path = path

        if exists(path):
            self.video = MediaPlayer(path)
            info = self.get_file_data()

            self.duration = info["duration"]
            self.frames = 0
            self.frame_delay = 1 / info["frame rate"]
            self.size = info["original size"]
            self.image = pygame.Surface((0, 0))

            self.active = True
        else:
            raise FileNotFoundError(ENOENT, strerror(ENOENT), path)

    def get_file_data(self):
        info = MediaInfo.parse(self.path).video_tracks[0]
        return {"path": self.path,
                "name": splitext(basename(self.path))[0],
                "frame rate": float(info.frame_rate),
                "frame count": info.frame_count,
                "duration": info.duration / 1000,
                "original size": (info.width, info.height),
                "original aspect ratio": info.other_display_aspect_ratio[0]}

    def get_playback_data(self):
        return {"active": self.active,
                "time": self.video.get_pts(),
                "volume": self.video.get_volume(),
                "paused": self.video.get_pause(),
                "size": self.size}

    def restart(self):
        self.video.seek(0, relative=False, accurate=False)
        self.frames = 0
        self.active = True

    def close(self):
        self.video.close_player()
        self.active = False

    def set_size(self, size):
        self.video.set_size(size[0], size[1])
        self.size = size

    def set_volume(self, volume):
        self.video.set_volume(volume)

    def seek(self, seek_time, accurate=False):
        vid_time = self.video.get_pts()
        if vid_time + seek_time < self.duration and self.active:
            self.video.seek(seek_time)
            if seek_time < 0:
                while (vid_time + seek_time < self.frames * self.frame_delay):
                    self.frames -= 1

    def toggle_pause(self):
        self.video.toggle_pause()

    def update(self):
        updated = False
        while self.video.get_pts() > self.frames * self.frame_delay:
            frame, val = self.video.get_frame()
            self.frames += 1
            updated = True
        if updated:
            if val == "eof":
                self.active = False
            elif frame != None:
                self.image = pygame.image.frombuffer(frame[0].to_bytearray()[0], frame[0].get_size(), "RGB")
        return updated

    def draw(self, surf, pos, force_draw=True):
        if self.active:
            if self.update() or force_draw:
                surf.blit(self.image, pos)


# Definimos una función que ejecute el vídeo en una ventana.
def reproducir_video(name_of_video:str):
    vid = Video(f"Videos/editados/{name_of_video}.mp4") # TODOS LOS VÍDEOS DEBEN ESTAR EN LA MISMA CARPETA
    info_del_video = vid.get_playback_data()  # devuelve un diccionario con las características del vídeo
    size_of_video = info_del_video['size'] # Conseguimos el tamaño del vídeo
    # El vídeo puede ser mayor o menor que la pantallla. Aquí lo ajustamos:
    # o creará una ventana del tamaño del video o ocupará toda la pantalla.
    # (estamos asumiendo vídeos horizontales) #
    mi_pantalla_ancho = 1366
    mi_pantalla_alto = 768
    ancho_ventana = min(mi_pantalla_ancho, size_of_video[0])
    if ancho_ventana == mi_pantalla_ancho:
        tamaño_ventana = (mi_pantalla_ancho, mi_pantalla_alto)
    else:
        tamaño_ventana = size_of_video
    vid.set_size(tamaño_ventana)  # Ajustamos el tamaño del vídeo
    SCREEN = pygame.display.set_mode(tamaño_ventana) # Creamos la ventana
    duration_of_video = vid.duration
    t0 = time.time() # Instante de tiempo en el que empieza la reproducción del vídeo
    pausado = False # Booleano que registra si está pausado
    tiempo_inicio_pausa=0
    tiempo_pausado = 0
    hold_tiempo_reproduccion=0
    while True:  #It will run until you exit the function
        vid.draw(SCREEN,(0,0))
        # Los argumentos de la función son:
        # surf = where you want to draw the video on (SCREEN)
        # pos = posición en la pantalla en la que colocamos la pantalla-display (0,0)
        pygame.display.update()
        # Queremos que se cierre la ventana automáticamente al acabar el vídeo.

        tiempo_de_reproduccion = time.time() -t0 - tiempo_pausado
        if pausado == True:
            tiempo_de_reproduccion=0 # Así, no apagará
        if tiempo_de_reproduccion > duration_of_video+1 and pausado == False:
            vid.close()
            break
            #pygame.quit()

        # Para que el usuario pueda interactuar con el vídeo
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # Si clicas el mouse:
                vid.toggle_pause()  # Pausa el video
                # Si se vuelve a hundir el ratón, continua la reproducción

                # El programa considera que el tiempo sigue pasando y pasados duration_of_video segundos cerrará la pantalla.
                # Esta sección arregla esto
                if pausado == False: # Cuando pausamos el video
                    tiempo_inicio_pausa=time.time() #registra el tiempo

                    pausado = True # Registra que estamos pausados
                elif pausado == True:
                    # Calcula el tiempo durante el que está pausado. Acumula en la misma variable todas las pausas
                    tiempo_pausado = time.time() - tiempo_inicio_pausa + tiempo_pausado
                    # Lo elimina del tiempo de reproducción, para que el vídeo no se cierre antes de que acabe.
                    pausado = False
                    # La actualización del tiempo de reproducción se da cuando se reanuda la reproducción del vídeo.
                    # Es decir, mientras está parado, tiempo de reproducción va aumentando y, en ponerlo en marcha, se elimina el tiempo pausado.
                    # Si mientras está pausado llega al límite, se cierra
            elif event.type == pygame.KEYDOWN: # Si se presiona una tecla
                if event.key == pygame.K_q: # Si esa tecla es la Q
                    vid.close() # Para el video, pero no cierra la ventana
                    #pygame.quit() #Cuando cierra pygame, no lo puede reiniciar en la misma sesión
                    return

def reproducir_video_en_pantalla(name_of_video:str, SCREEN:pygame.surface.Surface):
    vid = Video(f"Videos/editados/{name_of_video}.mp4")  # TODOS LOS VÍDEOS DEBEN ESTAR EN LA MISMA CARPETA
    # Conseguimos las dimensiones de la pantalla introducida
    mi_pantalla_ancho = SCREEN.get_width()
    mi_pantalla_alto = SCREEN.get_height()
    tamaño_ventana = (mi_pantalla_ancho, mi_pantalla_alto)
    vid.set_size(tamaño_ventana)  # Ajustamos el tamaño del vídeo
    duration_of_video = vid.duration # duración del vídeo
    t0 = time.time()  # Instante de tiempo en el que empieza la reproducción del vídeo
    pausado = False  # Booleano que registra si está pausado
    tiempo_inicio_pausa = 0
    tiempo_pausado = 0
    hold_tiempo_reproduccion = 0
    while True:  # It will run until you exit the function
        vid.draw(SCREEN, (0, 0))
        # Los argumentos de la función son:
        # surf = where you want to draw the video on (SCREEN)
        # pos = posición en la pantalla en la que colocamos la pantalla-display (0,0)
        pygame.display.update()

        # Queremos que se termine automáticamente al acabar el vídeo.
        tiempo_de_reproduccion = time.time() - t0 - tiempo_pausado
        if pausado:
            tiempo_de_reproduccion = 0  # Así, no apagará
        if tiempo_de_reproduccion > duration_of_video + 1 and not pausado:
            vid.close()
            return

        # Para que el usuario pueda interactuar con el vídeo
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # Si clicas el mouse:
                vid.toggle_pause()  # Pausa el video
                # Si se vuelve a hundir el ratón, continua la reproducción

                # El programa considera que el tiempo sigue pasando y pasados duration_of_video segundos cerrará la pantalla.
                # Esta sección arregla esto
                if not pausado:  # Cuando pausamos el video
                    tiempo_inicio_pausa = time.time()  # registra el tiempo
                    pausado = True  # Registra que estamos pausados

                elif pausado:
                    # Calcula el tiempo durante el que está pausado. Acumula en la misma variable todas las pausas
                    tiempo_pausado = time.time() - tiempo_inicio_pausa + tiempo_pausado
                    # Lo elimina del tiempo de reproducción, para que el vídeo no se cierre antes de que acabe.
                    pausado = False
                    # La actualización del tiempo de reproducción se da cuando se reanuda la reproducción del vídeo.
                    # Es decir, mientras está parado, tiempo de reproducción va aumentando y, en ponerlo en marcha, se elimina el tiempo pausado.
                    # Si mientras está pausado llega al límite, se cierra
            elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_q:  # Si esa tecla es la Q
                    vid.close()  # Para el video, pero no cierra la ventana
                    return


# INTERACCIÓN
def dibujar_boton_rect(screen:pygame.surface.Surface, text:str, color:tuple, text_color:tuple, fuente_texto:pygame.font.Font, pos_centro:tuple):
    text_surface = fuente_texto.render(text,True,text_color) # caracteristicas del texto a escribir
    text_rect= text_surface.get_rect() # Rectángulo que tiene el texto
    # Definir el rectángulo (figura) que será el botón. Su tamaño depende del texto
    text_rect.center = (pos_centro) # definimos la posición del centro del rectángulo
    rectangulo_del_boton = pygame.Rect(text_rect.x, text_rect.y, text_rect.width + 10,text_rect.height +10)
    # (x,y, ancho, alto) con x,y posicion de la esquina superior izquierda
    pygame.draw.rect(screen,color,rectangulo_del_boton) # Dibuja el cuadrado
    screen.blit(text_surface, text_rect) # Coloca el texto encima
    return rectangulo_del_boton # Sacamos el rectángulo del botón, para los collide

def dibujar_boton_circ(screen:pygame.surface.Surface, text:str, color:tuple, text_color:tuple, fuente_texto:pygame.font.Font, pos_centro:tuple):
    text_surface = fuente_texto.render(text,True,text_color) # caracteristicas del texto a escribir
    text_rect= text_surface.get_rect() # Rectángulo que tiene el texto
    text_rect.center = (pos_centro) # Lo centramos en la posición indicada

    # Definir el circulo (figura) que será el botón. Su tamaño depende del texto
    radio = max(text_rect.width,text_rect.height)
    pygame.draw.circle(screen,color,pos_centro,radio) # Dibuja el círculo

    # Creamos un cuadrado que contiene el círculo. Hace de collide object
    rectangulo_del_boton = pygame.Rect(text_rect.x, text_rect.y, 2*radio, 2*radio)
    rectangulo_del_boton.center=pos_centro # centramos el rectangulo
    screen.blit(text_surface, text_rect) # Coloca el texto encima del circulo
    return rectangulo_del_boton # Sacamos el rectángulo del botón, para los collide

# PANTALLAS A DIBUJAR
def pantalla_bienvenida(screen:pygame.surface.Surface, fuente:pygame.font.Font):
    screen.fill(dic.colores['azul oscuro'])
    texto = "Bienvenido a ELISE"
    superficie_texto = fuente.render(texto, True, dic.colores['amarillo'])

    # Para centrar el texto: Obtiene el rectángulo que contiene el texto
    rect_texto = superficie_texto.get_rect()
    # Coloca el rectángulo en el centro de la pantalla
    rect_texto.center = (screen.get_width()//2, screen.get_height()//2)
    # Dibuja el texto en las coordenadas de rect_texto
    screen.blit(superficie_texto, rect_texto)
    return

def pantalla_escucha(screen:pygame.surface.Surface, fuente:pygame.font.Font):
    screen.fill(dic.colores['azul claro'])
    texto = "Escuchando. T para pausar"
    superficie_texto = fuente.render(texto, True, dic.colores['azul oscuro'])

    # Para centrar el texto: Obtiene el rectángulo que contiene el texto
    rect_texto = superficie_texto.get_rect()
    # Coloca el rectángulo en el centro de la pantalla
    rect_texto.center = (screen.get_width()//2, screen.get_height()//2)
    # Dibuja el texto en las coordenadas de rect_texto
    screen.blit(superficie_texto, rect_texto)
    return

def pantalla_espera_escucha(screen:pygame.surface.Surface, fuente:pygame.font.Font):
    screen.fill(dic.colores['azul claro'])
    texto = "Presionar espacio para escuchar"
    superficie_texto = fuente.render(texto, True, dic.colores['azul oscuro'])

    # Para centrar el texto: Obtiene el rectángulo que contiene el texto
    rect_texto = superficie_texto.get_rect()
    # Coloca el rectángulo en el centro de la pantalla
    rect_texto.center = (screen.get_width()//2, screen.get_height()//2)
    # Dibuja el texto en las coordenadas de rect_texto
    screen.blit(superficie_texto, rect_texto)
    return

def pantalla_procesando(screen:pygame.surface.Surface, fuente:pygame.font.Font):
    screen.fill(dic.colores['amarillo'])
    texto = ("Procesando")
    superficie_texto = fuente.render(texto, True, dic.colores['azul oscuro'])

    # Para centrar el texto: Obtiene el rectángulo que contiene el texto
    rect_texto = superficie_texto.get_rect()
    # Coloca el rectángulo en el centro de la pantalla
    rect_texto.center = (screen.get_width()//2, screen.get_height()//2)
    # Dibuja el texto en las coordenadas de rect_texto
    screen.blit(superficie_texto, rect_texto)
    return

def pantalla_error(screen:pygame.surface.Surface, fuente:pygame.font.Font):
    screen.fill(dic.colores['blanco'])
    texto = "ERROR. Volvemos a escuchar"
    superficie_texto = fuente.render(texto, True, dic.colores['amarillo'])

    # Para centrar el texto: Obtiene el rectángulo que contiene el texto
    rect_texto = superficie_texto.get_rect()
    # Coloca el rectángulo en el centro de la pantalla
    rect_texto.center = (screen.get_width()//2, screen.get_height()//2)
    # Dibuja el texto en las coordenadas de rect_texto
    screen.blit(superficie_texto, rect_texto)
    return

def pantalla_despedida(screen:pygame.surface.Surface, fuente:pygame.font.Font):
    screen.fill(dic.colores['blanco'])
    texto = "Gracias por usar ELiSE :)"
    superficie_texto = fuente.render(texto, True, dic.colores['azul oscuro'])

    # Para centrar el texto: Obtiene el rectángulo que contiene el texto
    rect_texto = superficie_texto.get_rect()
    # Coloca el rectángulo en el centro de la pantalla
    rect_texto.center = (screen.get_width()//2, screen.get_height()//2)
    # Dibuja el texto en las coordenadas de rect_texto
    screen.blit(superficie_texto, rect_texto)
    return