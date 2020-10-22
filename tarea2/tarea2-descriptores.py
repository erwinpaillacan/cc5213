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
from tqdm import tqdm
import scipy
import math
from scipy.spatial import distance

if len(sys.argv) < 3:
    print("Uso: {} [videos_dir] [descriptores_dir]".format(sys.argv[0]))
    sys.exit(1)

videos_dir = sys.argv[1]
descriptores_dir = sys.argv[2]

if not os.path.exists(descriptores_dir):
    os.makedirs(descriptores_dir)

if not os.path.isdir(videos_dir):
    print("no existe directorio {}".format(videos_dir))
    sys.exit(1)



#videos_dir = sys.argv[1]
#descriptores_dir =sys.argv[2]


def generar_descriptores(folder_video, dir_salida, frames_por_segundo):
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
    #print('Extraer ' + str(frames_por_segundo) + ' frame por cada segundo')
    nombre_videos = os.listdir(videos_dir)
    nombre_videos = [name for name in nombre_videos if name.endswith('.mp4')]
    if not os.path.exists(dir_salida):
        os.makedirs(dir_salida)

    largo_descriptor = 400
    #largo_descriptor = 256
    
    
    for video in nombre_videos:
        name = video.split('.')[0]
        text_file = open(dir_salida+'/' + name+ ".txt", "w")
        vectors = np.empty((1, largo_descriptor))
        contador = 0
        cap = cv2.VideoCapture(os.path.join(videos_dir, video))
        frameRate = cap.get(5) #frame rate
        property_id = int(cv2.CAP_PROP_FRAME_COUNT) 
        length = int(cv2.VideoCapture.get(cap, property_id))
        pbar = tqdm(total=length)
        #print(frameRate)
        while(cap.isOpened()):
            frameId = cap.get(1) #current frame number
            ret, frame = cap.read()
            if (ret != True):
                break
            if (frameId % math.floor(frameRate /frames_por_segundo) == 0):
                time = frameId / frameRate
                time = "{0:.3f}".format(time)
                text_file.write(video+'\t' + str(time) + '\n')
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                dim = int(math.sqrt( largo_descriptor ))
                img =  cv2.resize(img, (dim, dim))
                data = np.array(img)
                flattened = data.reshape((1, largo_descriptor))
                vectors = np.concatenate((vectors,flattened), axis = 0)
                contador += 1
                #print(vectors.shape)
            
            pbar.update(1)
            if cv2.waitKey(10) & 0xFF == ord('q') :

                    # break out of the while loop
                    break
        cap.release()
        #print(name, contador, ' frames extraidos')
        vectors = np.delete(vectors, 0, axis=0)
        #print(vectors.shape)
        vectors.tofile(dir_salida +'/' + name)
        text_file.close()
        pbar.close()


#baseline = 2
generar_descriptores(videos_dir, descriptores_dir, frames_por_segundo= 4)

#frames_1 = extractFrames(videos_dir, list_videos[0])
#print(frames_1)





#python tarea2-descriptores.py dataset_a/television work_a/descriptores_television && python tarea2-descriptores.py dataset_a/comerciales work_a/descriptores_comerciales

