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


dir_videos_tv = sys.argv[1]
salida_descriptores =sys.argv[2]


def generar_descruptores(folder_video, dir_salida, frames_por_segundo= 1):
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

    nombre_videos = os.listdir(dir_videos_tv)
    nombre_videos = [name for name in nombre_videos if name.endswith('.mp4')]


    text_file = open(dir_salida+".txt", "w")
    vectors = np.empty((1, 100))
    for video in nombre_videos:
        contador = 0
        cap = cv2.VideoCapture(os.path.join(dir_videos_tv, video))
        frameRate = cap.get(5) #frame rate
        #print(frameRate)
        name = video
        while(cap.isOpened()):
            frameId = cap.get(1) #current frame number
            ret, frame = cap.read()
            if (ret != True):
                break
            if (frameId % math.floor(frameRate /frames_por_segundo) == 0):
                time = frameId / math.floor(frameRate / frames_por_segundo)
                text_file.write(name+'\t' + str(time) + '\n')
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                img =  cv2.resize(img, (10, 10))
                data = np.array(img)
                flattened = data.reshape((1, 100))
                vectors = np.concatenate((vectors,flattened), axis = 0)
                contador += 1
                #print(vectors.shape)
            
                
            if cv2.waitKey(10) & 0xFF == ord('q') :

                    # break out of the while loop
                    break
        cap.release()
        print(name, contador, ' frames extraidos')
    vectors = np.delete(vectors, 0, axis=0)
    print(vectors.shape)
    vectors.tofile(dir_salida)
    text_file.close()







def load_path_videos(dir_videos_tv):

    return os.listdir(dir_videos_tv)



    
 


generar_descruptores(dir_videos_tv, dir_videos_tv + '/descriptores', frames_por_segundo= 1)

#frames_1 = extractFrames(dir_videos_tv, list_videos[0])
#print(frames_1)





# python tarea2-descriptores.py dataset_a/television/ dataset_a/descriptores_tv
# python tarea2-descriptores.py dataset_a/comerciales/ dataset_a/descriptores_comerciales

