import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from funcion_preprocesamiento import preprocesar_texto

# traer el corpus de este path
path = "Examen2/corpus.txt"
# abrir el archivo y leer su contenido
with open(path, "r") as file:
    corpus = file.read()

corpus_preprocesado = preprocesar_texto(corpus)
print(corpus_preprocesado)
