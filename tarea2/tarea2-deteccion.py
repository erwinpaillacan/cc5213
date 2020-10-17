# -*- coding: utf-8 -*-
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

def buscar_vecinos(similares_file,detecciones_file , k_vecinos ):
    file = open(similares_file)
    similares_txt = file.readlines()
    tv_name_i, _, _, comercial_name_i, comercial_tiempo_i = similares_txt[0].split('\t')
    text_file = open(detecciones_file, "w")
    contador = 0
    linea_vecinos = []
    desde = 0
    for linea in similares_txt[1:]:
        tv_name, tv_tiempo, comercial_name, comercial_tiempo, dis= linea.split('\t')
        if tv_name == tv_name_i and comercial_name== comercial_name_i and comercial_tiempo_i< comercial_tiempo:
            if contador == 0:
                desde = "{0:.2f}".format(float(tv_tiempo))
            comercial_tiempo_i = comercial_tiempo
            largo = "{0:.2f}".format(float(tv_tiempo) - float(desde) )
            linea_vecinos.append(tv_name +'\t'+ str(desde) + '\t' + str(largo) + '\t'+ comercial_name + '\t' + dis)
            contador += 1
        else:        

            if contador> k_vecinos:
                text_file.write(linea_vecinos[-1] + '\n')
                #print(linea_vecinos)                
            contador = 0
            linea_vecinos = []
            comercial_tiempo_i = comercial_tiempo
            tv_name_i = tv_name
            comercial_name_i = comercial_name
    text_file.close()


buscar_vecinos(similares_file,  detecciones_file, k_vecinos=10)
# python tarea2-deteccion.py work_a/similares.txt work_a/detecciones.txt