import sys
import os.path

if len(sys.argv) < 3:
    print("Uso: {} [similares_file] [detecciones_file]".format(sys.argv[0]))
    sys.exit(1)

similares_file = sys.argv[1]
detecciones_file = sys.argv[2]

if not os.path.isfile(similares_file):
    print("no existe archivo {}".format(similares_file))
    sys.exit(1)

#leer archivo similares_file
#escribir comerciales detectados en detecciones_file



# python tarea2-deteccion.py work_a/similares.txt work_a/detecciones.txt