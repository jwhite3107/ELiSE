# Importamos los módulos necesarios
import speech_recognition as sr # Para el reconocimiento de voz
import pygame                   # Interfaz, vídeos y control
import time                     # Control del flujo de tiempo
# Importamos las archivos complementarios
import funciones # Contiene las funciones que usamos durante el programa
import dic       # Contiene el diccionario de palabras que se reconocen y de colores


# CONFIGURACIÓN DE LA VENTANA
# Inicializamos pygame, la biblioteca que nos permite crear la ventana
pygame.init()

# Guardamos las dimensiones de mi pantalla
mi_pantalla_ancho = 1300 //1.5 #mientras pruebo quiero que sea más pequeño que mi pantalla para ver la consola
mi_pantalla_alto = 730 //1.5
tamaño_ventana = (mi_pantalla_ancho, mi_pantalla_alto)

# Crea la ventana en la que estará la aplicación
SCREEN = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("ELiSE") # Nombre de la ventana
fuente = pygame.font.Font(None, 74)  # Letra base. Tamaño 74
print('Pantalla configurada')

# CONFIGURACIÓN DEL MICRÓFONO
# Por defecto, configura el micrófono predeterminado del dispositivo
mic=sr.Microphone() # This is an instance of the Microphone class.
# Si hemos conectado un micrófono, lo configuramos aquí
mic_options=sr.Microphone.list_microphone_names()
# print(mic_options) # To see which mic are available.
# Mis posibles micrófonos
#   Soundcore Q30 = los auriculares del Tito
#   Micrófono externo = los cascos gamer con micro (mejor opción)
micro_a_configurar='Micrófono externo'
if 'Micrófono externo' in mic_options:
    print(f'El índice de los auriculares externos es {mic_options.index(micro_a_configurar)}')
    mic = sr.Microphone(device_index=mic_options.index(micro_a_configurar)) # where device_index is the position in the mic_options list
print('Micrófono seleccionado')

# RECONOCIMIENTO DE VOZ
# Instancia de la clase que lleva a cabo el reconocimiento
r=sr.Recognizer()
# Variable para reconocer si ha funcionado el reconocimiento
que_se_ha_dicho = None
# Calibramos el ruido de fondo. ¡SE ESTÁ ASUMIENDO QUE PERMANECE CONSTANTE DURANTE TODO EL USO DE LA APP!
with mic as source:
    # Estos print los pondremos en la pantalla
    print("Ajustando al ruido de fondo")
    r.adjust_for_ambient_noise(source)
    print('Micrófono configurado')


# INTERACCIÓN DEL USUARIO
# Variables de control, con las que iremos cambiando de pantalla
ELISE_en_marcha = True             # Todo el programa
switch_bienvenida = True           # Pantalla de bienvenida
switch_escucha = False             # Escucha
switch_procesando = False          # Procesado
switch_videos = False              # Videos
switch_adios = False               # Despedida


# Variables del modo escucha
transcripcion = ' '
grabando = False  # Variable para controlar el estado de la grabación
# Output del modo escucha, que se usará para los siguientes apartados
response_escucha = {
    "success": True,
    "error": None,
    "transcription": 'DIC '
    }

# IMÁGENES DE LAS PANTALLAS
# Para cada pantalla, la importamos y la ajustamos a la ventana
# Es más eficiente importar las pantallas aquí fuera y llamarlas en el bucle pincipal.
imagen_pantalla_bienvenida = pygame.image.load("Recursos graficos/pantalla_bienvenida.png")
imagen_pantalla_bienvenida = pygame.transform.scale(imagen_pantalla_bienvenida, tamaño_ventana)
imagen_pantalla_error = pygame.image.load("Recursos graficos/pantalla_error.png")
imagen_pantalla_error = pygame.transform.scale(imagen_pantalla_error, tamaño_ventana)
imagen_pantalla_escucha = pygame.image.load("Recursos graficos/pantalla_escucha.png")
imagen_pantalla_escucha = pygame.transform.scale(imagen_pantalla_escucha, tamaño_ventana)
imagen_pantalla_esperando = pygame.image.load("Recursos graficos/pantalla_esperando.png")
imagen_pantalla_esperando = pygame.transform.scale(imagen_pantalla_esperando, tamaño_ventana)
imagen_pantalla_procesando = pygame.image.load("Recursos graficos/pantalla_procesando.png")
imagen_pantalla_procesando = pygame.transform.scale(imagen_pantalla_procesando, tamaño_ventana)
imagen_pantalla_despedida = pygame.image.load("Recursos graficos/pantalla_despedida.png")
imagen_pantalla_despedida = pygame.transform.scale(imagen_pantalla_despedida, tamaño_ventana)

# BOTONES
# Colocamos un botón transparente
# en la esquina superior derecha
boton_home = pygame.Rect(0, 0, 80, 80)
boton_home.center = (827, 40)
# Colocamos un botón central
boton_central = pygame.Rect(0,0,150,150)
boton_central.center = (434,244)
# en la esquina inferior derecha
boton_flecha = pygame.Rect(0, 0, 80, 80)
boton_flecha.center = (827, 447)
# Loop principal.
while ELISE_en_marcha:
    # LO QUE PASA AQUI FUERA NO SE CUMPLE!! PQ ESTAMOS SIEMPRE DENTRO DE OTRO WHILE

# BIENVENIDA
    while switch_bienvenida:
        #  PANTALLA
        # Imagen de la pantalla
        SCREEN.blit(imagen_pantalla_bienvenida,(0,0))

        # SIEMPRE. Actualizar ventana y, si se presiona X, cerrar el programa
        pygame.display.flip()
        for event in pygame.event.get():
            # Para salir en caso de que se presione la X de la ventana
            if event.type == pygame.QUIT:
                # Sale de este bucle
                switch_bienvenida = False
                # Cierra el programa
                ELISE_en_marcha = False
            # INTERACCIÓN
            # Si se presiona el ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Comprueba si el clic fue dentro del botón de escucha
                if boton_central.collidepoint(event.pos):
                    # Cambia a la pantalla de escucha
                    print('Cambiar a menú de escucha')
                    switch_bienvenida = False
                    switch_escucha = True


# ESCUCHA = RECONOCIMIENTO DE VOZ
    while switch_escucha:
        # SIEMPRE. Actualizar ventana y, si se presiona X, cerrar el programa
        for event in pygame.event.get():
            # Para salir en caso de que se presione la X de la ventana
            if event.type == pygame.QUIT:
                # Sale de este bucle
                switch_escucha = False
                # Cierra el programa
                ELISE_en_marcha = False
            # Se vuelve a la pantalla de inicio si se presiona Q
            if event.type == pygame.KEYDOWN:
                # Salir a la pantalla de bienvenida. Else: presionar boton home
                if event.key == pygame.K_q:
                    print("Has presionado 'q'. Volviendo a la pantalla de inicio")
                    switch_escucha = False
                    switch_bienvenida = True
        # INTERACCIÓN
            if event.type == pygame.KEYDOWN:
                # Iniciar grabación al presionar espacio.
                if event.key == pygame.K_SPACE and not grabando:
                    grabando = True
                    print("Grabando...")
                # Detener grabación al presionar T. Tarda en reaccionar
                if event.key == pygame.K_t and grabando:
                    grabando = False
                    print("Grabación detenida.")
                    # Actualiza el diccionario de salida. Transcription almacena string
                    response_escucha["transcription"] = transcripcion
                    print(response_escucha)


                # Salida de escucha
                if event.key == pygame.K_RETURN:
                    # Actualiza el diccionario de salida. Transcription almacena string
                    response_escucha["transcription"] = transcripcion
                    print(response_escucha)

                    # Pasamos a procesar si se ha dicho algo
                    if response_escucha["transcription"] != ' ':
                        print('Pasamos a procesar')
                        switch_procesando = True
                        switch_escucha = False
                        # Por si luego volvemos
                        grabando = False
                    else:
                        print('No se ha reconocido nada. Volvemos a intentarlo')
                        SCREEN.blit(imagen_pantalla_error, (0, 0))
                        grabando = False
                        pygame.display.flip()
                        time.sleep(5)

            # Botones
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Comprueba si el clic fue dentro del botón central
                if boton_central.collidepoint(event.pos) and not grabando:
                    grabando = True
                    print("Grabando...")
                elif boton_central.collidepoint(event.pos) and grabando:
                    grabando = False
                    print("Grabando...")
                if boton_home.collidepoint(event.pos):
                    print("Has presionado 'Home'. Volviendo a la pantalla de inicio")
                    switch_escucha = False
                    switch_bienvenida = True
                if boton_flecha.collidepoint(event.pos):
                    # Actualiza el diccionario de salida. Transcription almacena string
                    response_escucha["transcription"] = transcripcion
                    print(response_escucha)

                    # Pasamos a procesar si se ha dicho algo
                    if response_escucha["transcription"] != ' ':
                        print('Pasamos a procesar')
                        switch_procesando = True
                        switch_escucha = False
                        # Por si luego volvemos
                        grabando = False
                    else:
                        print('No se ha reconocido nada. Volvemos a intentarlo')
                        SCREEN.blit(imagen_pantalla_error, (0, 0))
                        grabando = False
                        pygame.display.flip()
                        time.sleep(5)



        if not grabando:
            #  PANTALLA
            # Imagen de la pantalla
            SCREEN.blit(imagen_pantalla_esperando, (0, 0))
            pygame.display.flip()

        if grabando:
            # Pantalla correspondiente
            SCREEN.blit(imagen_pantalla_escucha, (0, 0))
            pygame.display.flip()
            with mic as source:

                # try recognizing the speech in the recording
                # if a RequestError or UnknownValueError exception is caught,
                #  update the response object accordingly
                try:
                    # Obtiene el audio del micrófono
                    audio = r.listen(source)
                    # Convierte a texto lo escuchado
                    text = r.recognize_google(audio, language='es-ES')
                    print(f"Dices: {text}") # Muestralo en la consola, para comprobar

                    # Introduce las nuevas palabras en la transcripción global
                    transcripcion += f' {text}'
                    print(transcripcion)
                    # Actualiza el diccionario de salida. Transcription almacena string
                    response_escucha["transcription"] += f' {text}'
                    print(response_escucha['transcription'])

                # Manejo de errores:
                except sr.UnknownValueError:
                    # No se entiende lo que se ha dicho
                    # Actualización de la salida
                    response_escucha['success']: False
                    response_escucha["error"] = "Unable to recognize speech"
                    print("Error en el reconocimiento del habla")


                except sr.RequestError as e:
                    # No se puede acceder a la API o ésta no responde.
                    # Actualización de la salida
                    response_escucha["success"] = False
                    response_escucha["error"] = f"API unavailable,{e}"
                    print("El servicio de transcripción de Google no responde")


# IDENTIFICACIÓN DE PALABRAS
    while switch_procesando:
        # SIEMPRE
        SCREEN.blit(imagen_pantalla_procesando,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            # Para salir en caso de que se presione la X de la ventana
            if event.type == pygame.QUIT:
                # Sale de este bucle
                switch_procesando = False
                # Cierra el programa
                ELISE_en_marcha = False
                # Se vuelve a la pantalla de inicio si se presiona Q
            if event.type == pygame.KEYDOWN:
                 # Salir a la pantalla de bienvenida. Else: presionar boton home
                if event.key == pygame.K_q:
                    print("Has presionado 'q'. Volviendo a la pantalla de inicio")
                    switch_procesando = False
                    switch_bienvenida = True

        # Response_escucha es el diccionario de salida del bloque de escucha
        # Guardamos lo que se ha dicho en una variable. Siempre tendrá palabras
        que_se_ha_dicho = response_escucha["transcription"] #string que contiene lo que se ha dicho.

        # Hay dos posibilidades. Que haya o no coincidencias con el diccionario de LSE
        # IDENTIFICACIÓN DE LAS PALABRAS
        # Para los próximos pasos, convierto el string en una lista, cada elemento una palabra dicha.
        palabras_dichas = que_se_ha_dicho.split()
        # Revisamos el diccionario y vemos qué palabras se han dicho.
        # Apuntamos las palabras en el orden en el que se han dicho
        matches = funciones.superlist(palabras_dichas, dic.nuestro_diccionario)
        print(matches)
        # Limpia el objeto del modo escucha, para que cuando se vuelva al modo escucha no recuerda lo que se haya dicho
        response_escucha = {
            "success": True,
            "error": None,
            "transcription": 'DIC '
        }
        transcripcion = ''
        if matches: # Si hay coincidencias
            switch_videos = True
            switch_procesando = False
        else: # Si no hay coincidencias
            print('No hay coincidencias. Volvemos a la pantalla de escucha') # Lo ponemos en la consola
            #y en la pantalla
            SCREEN.blit(imagen_pantalla_error, (0, 0))
            pygame.display.flip()
            # Tiempo para que se pueda leer
            time.sleep(5)
            # Pasamos al modo escucha
            switch_escucha = True
            switch_procesando = False


# REPRODUCCIÓN DE VÍDEOS
    while switch_videos:
        # SIEMPRE
        pygame.display.flip()
        for event in pygame.event.get():
            # Para salir en caso de que se presione la X de la ventana
            if event.type == pygame.QUIT:
                # Sale de este bucle
                switch_videos = False
                # Cierra el programa
                ELISE_en_marcha = False
                # Se vuelve a la pantalla de inicio si se presiona Q
            if event.type == pygame.KEYDOWN:
                # Salir a la pantalla de bienvenida. Else: presionar boton home
                if event.key == pygame.K_q:
                    print("Has presionado 'q'. Volviendo a la pantalla de inicio")
                    switch_videos = False
                    switch_bienvenida = True

        for item in matches:
            funciones.reproducir_video_en_pantalla(f'{item}', SCREEN)
        # Vaciamos la transcripción, para poder volver a decir cosas y que no se repita
        response_escucha = {
            "success": True,
            "error": None,
            "transcription": 'DIC '
        }
        # Cuando acaba con los vídeos, vuelve a escucha
        switch_videos = False
        switch_escucha = True

if not ELISE_en_marcha:
    print('Gracias por usar ELiSE :)')
    SCREEN.blit(imagen_pantalla_despedida,(0,0))
    pygame.display.flip()
    time.sleep(5)
    switch_adios = True