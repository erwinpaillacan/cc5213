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



dir_r = sys.argv[1]
dir_r_salida =sys.argv[2]




def load_images_from_folder(folder, dir_salida):
    '''
    Utilidad para cargar imagenes de una carpeta, calcular
    su descriptor y guardarlo. Tambien se escribe un .txt con
    el nombre de las imagenes.

    Parametros
    -------------------
    str: folder
        ruta hacia el directorio de imagenes
    str: dir_salida
        Ruta donde se guardara la matriz de descriptores.
    
    Salida
    ------------------
    numpy array: vectors
        Numpy to file de la matriz de descriptores
    file: text_file
        Archivo de texto con los nombres de las imagenes a la cuales se les
        calculó sus descriptor

    '''
    text_file = open(os.getcwd() +'/'+dir_salida+".txt", "w")
    vectors = np.empty((1, 100))
    for filename in os.listdir(folder):
        name = filename
        img = cv2.imread(os.path.join(folder,filename))
        n = text_file.write(name+'\n')
        
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img =  cv2.resize(img, (10, 10))
            data = np.array(img)
            flattened = data.reshape((1, 100))
            vectors = np.concatenate((vectors,flattened), axis = 0)
    vectors = np.delete(vectors, 0, axis=0)
    print(vectors.shape)
    vectors.tofile(os.getcwd() +'/'+dir_salida)
    text_file.close()
    



load_images_from_folder(os.getcwd() + '/'+dir_r, dir_r_salida )


