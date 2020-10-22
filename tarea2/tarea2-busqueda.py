# -*- coding: utf-8 -*-
import sys
import os
import numpy
from cv2 import cv2
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import numpy as np
import os
import sys
import scipy
import math
from scipy.spatial import distance
from tqdm import tqdm

if len(sys.argv) < 4:
    print("Uso: {} [descriptores_television_dir] [descriptores_comerciales_dir] [archivo-knn]".format(sys.argv[0]))
    sys.exit(1)

descriptores_television_dir = sys.argv[1]
descriptores_comerciales_dir = sys.argv[2]
similares_file = sys.argv[3]



if not os.path.isdir(descriptores_television_dir):
    print("no existe directorio {}".format(descriptores_television_dir))
    sys.exit(1)

if not os.path.isdir(descriptores_comerciales_dir):
    print("no existe directorio {}".format(descriptores_comerciales_dir))
    sys.exit(1)




#descriptores_television_dir = sys.argv[1]
#descriptores_comerciales_dir =sys.argv[2]
#similares_file = sys.argv[3]






def calcular_distancia(vector, matrix, metric = 'euclidean'):
    '''
    Utilidad a partir de un vector de entrada buscar su imagen mas parecida
    bajo el criterio de minima distancia en matrix.

    Parametros
    -------------------
    numpy array: vector
        descriptor imagen (1, largo_descriptor)
    numpy array: matrix
        Matriz de descriptores (numero_images, largo_descriptor)
    str: metric
        Tipo de distancia a calcular
    
    Salida
    ------------------
    int: index
        Posicion del minimo
    float: minimo
        Distancia minima
    '''
    largo_descriptor = 400
    #largo_descriptor= 256
    vector = vector.reshape(1,largo_descriptor)
    dis = distance.cdist(vector, matrix, metric)
    minimo = np.amin(dis)
    index_tupla = np.where(dis == np.amin(dis))
    index = index_tupla[1][0]
    return index, minimo

def escribir_linea(linea_tv, linea_comercial, minimo, text_file):
    '''
    Utilidad para escribir linea de informacion en un text file

    Parametros
    -------------------
    str: datos
        ruta hacia el archivo que contiene los nombres de las imagenes del dataset 
        (en este caso ruta hacia datos_r)
    int: index
        Indice donde se encuentra el vector de datos_r que da la distancia minima con respecto
        a la imagen filename
    str: filename
        Nombre de la imagen a la cual se le buscó el minimo    
    float: minimo
        Distancia minima calculada
    file: text_file
        Arhcivo donde se escibe la linea.
    
    Salida
    ------------------
    file: text_file
    
    '''
    text = linea_tv+'\t'+  linea_comercial + '\t'+ str(minimo) 
    #print(text.replace('\n', ''))
    text_file.write(text.replace('\n', '') + '\n' )
 
 
def busqueda(folder_tv, folder_comerciales, similares_file):
    '''
    Utilidad para cargar imagenes de una carpeta, calcular
    su descriptor y luego comparar con la matriz de descriptores matrix_r.

    Parametros
    -------------------
    str: folder
        ruta hacia el directorio de imagenes
    str: datos_r
        ruta hacia el archivo que contiene los nombres de las imagenes del dataset 
        (en este caso ruta hacia datos_r)
    numpy.array: matrix_r
        Matriz de descripctores con forma (numero_images, largo_descriptor)
    str: resultados
        nombre archivo de texto para guardar los resultados
    
    Salida
    ------------------
    file: resultados
        Archivo de texto separado por tabulador: nombre1  nombre2 distancia
    '''
    comerciales = [name for name in os.listdir(folder_comerciales) if name.endswith('.txt') == False]
    video_tv = [name for name in os.listdir(folder_tv) if name.endswith('.txt') ==False]
    #print(video_tv)
    #length = len(video_tv) * len()
    #pbar = tqdm(total=length)
    text_file = open(similares_file, "w")
    for tv in video_tv:
        #print(name)
        descriptor = np.fromfile(os.path.join(folder_tv, tv))
        #print(descriptor.shape)
        file = open(os.path.join(folder_tv, tv + '.txt'))
        info_descriptor = file.readlines()
        #print(info_descriptor[1])
        #print(len(info_descriptor))
        descriptor = descriptor.reshape(len(info_descriptor), int(len(descriptor) /len(info_descriptor) ))
        #print(descriptor.shape)
        #recorrer cada descriptor del video en particular
        for i in tqdm(range(len(info_descriptor))):
            d = descriptor[i,:]
            minimo_global = 100000000000000
            linea = ''
            for comercial in comerciales:
                descriptor_comer = np.fromfile(os.path.join(folder_comerciales, comercial))
                file = open(folder_comerciales + '/'+ comercial + '.txt')
                info_descriptor_comer = file.readlines()
                descriptor_comer = descriptor_comer.reshape(len(info_descriptor_comer), int(len(descriptor_comer) /len(info_descriptor_comer) ))
                #print(descriptor_comer.shape)
                idx, minimo = calcular_distancia(d, descriptor_comer, metric='euclidean')
                if minimo<minimo_global:
                    minimo_global = minimo
                    linea = info_descriptor_comer[idx]

            escribir_linea(info_descriptor[i], linea, minimo_global, text_file)



busqueda(descriptores_television_dir, descriptores_comerciales_dir, similares_file)


# python tarea2-busqueda.py work_a/descriptores_television work_a/descriptores_comerciales work_a/similares.txt