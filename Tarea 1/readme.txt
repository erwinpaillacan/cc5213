Nombre: Erwin Paillacán H.


Para evaluar la tarea completa ejecutar lo siguiente:
tarea1-evaluar.py 

$ python tarea1-evaluar.py dataset a
$ python tarea1-evaluar.py dataset b



tarea1-procesar.py
Uso tipico: python tarea1-procesar.py dataset/dataset_r_a datos_r_a

Este archivo transforma todas las imagenes a su representanción como vector.
La representanción como vector se implementa con la función resize de OpenCv
con esto cualquier imagen se reduce a un tamaño (10, 10) que luego es modificado
en cuanto a su forma para dejarlo de dimensiones (1, 100).
Una matriz es rellenada con cada uno de estos vectores. POr ejemplo, la carpeta
dataset_a_r contiene 2000 imagenes. Tras el procesamiento se exporta una matriz
de 2000 x 100. Que contiene 2000 descriptores de largo (1, 100).

tarea1-buscar.py
Uso tipico: python tarea1-buscar.py dataset/dataset_q_a datos_r_a resultados_a.txt

Este archivo carga los datos generador para el dataset r, y luego genera los vectores para q.
Tras lo cual se procede a calcular la distancia euclidiana de cada uno de los vectores. Se toma el mínimo
y el indice donde este minimo, el indice se toma con la finalidad de recuperar el nombre de la imagen
proveniente del dataset r. Una vez con todo lo necesario, se escribe en un archivo de texto el nombre de la imagen de q
+ el nombre de la imagen de r (la mas próxima en cuanto a distancia) + la distancia, para cada uno de los minimos.
De esta forma se encuentra la pareja de imagenes más parecidas para cada caso.

Estructura proyecto:

Tarea1
   |-----------dataset
   |               |-------dataset_q_a
   |               |-------dataset_r_a
   |               |-------dataset_q_b
   |               |-------dataset_r_b
   |               |-------dataset_gt_a.txt
   |               |-------dataset_gt_b.txt
   |-----------tarea1-buscar.py    
   |-----------tarea1-procesar.py   
   |-----------tarea1-evaluar.py   
