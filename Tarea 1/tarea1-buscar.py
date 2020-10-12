import sys
import os
import numpy
from cv2 import cv2
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import numpy as np
import os
import sys
from scipy.spatial import distance

dataset_q = sys.argv[1]
datos_r = sys.argv[2]
resultados = sys.argv[3] 


def buscar_images_from_folder(folder, datos_r, matrix_r, resultados):
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
    dataset_q = folder
    text_file = open(os.getcwd()+ '/'+resultados, "w")
    for filename in os.listdir(dataset_q):
        #print(name)
        img = cv2.imread(os.path.join(dataset_q,filename))        
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img =  cv2.resize(img, (10, 10))
            data = np.array(img)
            flattened = data.reshape((1, 100))
            index, minimo = calcular_distancia(flattened, matrix_r)
            escribir_linea(datos_r, index, filename, minimo, text_file)

    text_file.close()

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
    vector = vector.reshape(1,100)
    dis = distance.cdist(vector, matrix, metric)
    minimo = np.amin(dis)
    index_tupla = np.where(dis == np.amin(dis))
    index = index_tupla[1][0]
    return index, minimo

def escribir_linea(datos, index, filename, minimo, text_file):
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
    dir_r_txt = os.getcwd() + '/'+ datos + '.txt'
    file = open(dir_r_txt)
    all_lines = file.readlines()
    nombre_imagen_r = all_lines[index]
    text = filename+'\t'+ nombre_imagen_r + '\t'+ str(minimo)
    text_file.write(text.replace('\n', '') + '\n' )
   
def Cargar_R(datos_r):
    '''
    Utilidad para cargar la matriz de descriptores

    Parametros
    -------------------
    str: datos_r
        Ruta hacia el archivo
    Salida
    ------------------
    numpy.array: matrix_r
        Matriz con de forma (numero_images, largo_descriptor)

    '''
    matrix_r = np.fromfile(os.getcwd() +'/' +datos_r )
    matrix_r = matrix_r.reshape((2000 , 100))
    return matrix_r


# Cargar matrices R
matrix_r = Cargar_R(datos_r)
buscar_images_from_folder(os.getcwd() +'/' +dataset_q ,datos_r ,  matrix_r, resultados)

