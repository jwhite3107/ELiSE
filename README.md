# ELiSE
App para traducción de lenguaje hablado por lenguaje de signos (LSE) a través de vídeos. Al ejecutar, genera una ventana interactiva. Se parte en el menú de inicio, al que se pasa a la ventana de escucha. La grabación de voz se puede parar con 'espacio' y, cuando se esté listo, se debe presionar la flecha en la esquina inferior derecha. EL programa porcesará la grabación y si reconoce alguna palabra del diccionario, reproduce los vídeos correspondientes.

# Ejecución del programa
Se ejecuta con el 'main.py', que va llamando tanto a las funciones descritas en 'funciones.py' y tiene como diccionario las palabras en 'dic.py'.
Los paquetes necesarios se listan a continuación:
- speech_recognition
- keyboard
- pygame
- time
- pymediainfo
- ffplayer
- os
- errno (no sé si este se usa realmente)


# Futuro desarrollo
- Solo hay diez palabras a fecha de 05/2025, pero añadir nuevas palabras solo es poner la palabra en 'dic.py' y el video correspondiente en la carpeta de 'Videos'.
- Se tiene que comprobar si la lentitud de la aplicación es por el ordenador en el que se ha probado o por el código en sí mismo.
- Añadir archivo requirements para facilitar exportación
- Ahora mismo es incompatible con MAC, pero funciona con Windows
- ¿El reproductor de vídeos se puede mejorar?
