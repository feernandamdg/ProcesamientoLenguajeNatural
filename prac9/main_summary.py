import re
from pathlib import Path
from gensim.models import Word2Vec
import numpy as np


ARCHIVO_TEXTO = Path("./prac9/texto_ia_educacion.txt")
ORACIONES_RESUMEN = 7
TAMANIO_VECTOR = 100
VENTANA = 4
MIN_COUNT = 1
PENALIZACION_REDUNDANCIA = 0.35


STOPWORDS = {
    "a", "al", "algo", "ante", "asi", "cada", "como", "con", "contra",
    "cuando", "de", "del", "desde", "donde", "dos", "e", "el", "en",
    "entre", "era", "es", "esa", "ese", "eso", "esta", "este", "esto",
    "estos", "fue", "ha", "hay", "la", "las", "lo", "los", "mas",
    "me", "mi", "mientras", "muy", "no", "o", "para", "pero", "por",
    "porque", "que", "se", "ser", "si", "sin", "sobre", "son", "su",
    "sus", "tambien", "un", "una", "uno", "y", "ya"
}


def contar_palabras(texto):
    return len(re.findall(r"\b\w+\b", texto, flags=re.UNICODE))


def separar_oraciones(texto):
    texto = re.sub(r"\s+", " ", texto.strip())
    oraciones = re.split(r"(?<=[.!?])\s+", texto)
    return [oracion.strip() for oracion in oraciones if oracion.strip()]


def tokenizar(texto):
    texto = texto.lower()
    tokens = re.findall(r"\b[a-záéíóúñü]+\b", texto)
    return [token for token in tokens if token not in STOPWORDS and len(token) > 2]


def entrenar_word2vec(oraciones_tokenizadas):

    modelo = Word2Vec(
        sentences=oraciones_tokenizadas,
        vector_size=TAMANIO_VECTOR,
        window=VENTANA,
        min_count=MIN_COUNT,
        workers=1,
        sg=1,
        epochs=200,
        seed=42,
    )
    return modelo


def vector_oracion(tokens, modelo):
    vectores = [modelo.wv[token] for token in tokens if token in modelo.wv]

    if not vectores:
        return np.zeros(TAMANIO_VECTOR)

    return np.mean(vectores, axis=0)


def similitud_coseno(vector_a, vector_b):
    norma_a = np.linalg.norm(vector_a)
    norma_b = np.linalg.norm(vector_b)

    if norma_a == 0 or norma_b == 0:
        return 0

    return np.dot(vector_a, vector_b) / (norma_a * norma_b)

def seleccionar_oraciones2(vectores_oraciones, vector_documento, cantidad):
    candidatas = list(range(len(vectores_oraciones)))
    puntajes = []

    #Tupla puntajes: indice, puntaje

    for indice in candidatas:
        relevancia = similitud_coseno(vectores_oraciones[indice], vector_documento)
        puntajes.append((indice,relevancia))
        
    oraciones_por_puntaje = sorted(puntajes, key=lambda x: x[1], reverse=True)
    
    oraciones_por_indice = sorted(oraciones_por_puntaje[:cantidad],key=lambda x: x[0]) 
    print(oraciones_por_indice)    
        
    return [index for index,points in oraciones_por_indice]


def resumir(texto, cantidad_oraciones=ORACIONES_RESUMEN):
    oraciones = separar_oraciones(texto)
    oraciones_tokenizadas = [tokenizar(oracion) for oracion in oraciones]

    modelo = entrenar_word2vec(oraciones_tokenizadas)

    vectores_oraciones = np.array([
        vector_oracion(tokens, modelo)
        for tokens in oraciones_tokenizadas
    ])

    vector_documento = np.mean(vectores_oraciones, axis=0)
    indices_resumen = seleccionar_oraciones2(
        vectores_oraciones,
        vector_documento,
        cantidad_oraciones
    )

    resumen = " ".join(oraciones[indice] for indice in indices_resumen)
    return resumen, indices_resumen


def main():
    texto = ARCHIVO_TEXTO.read_text(encoding="utf-8")
    resumen, indices = resumir(texto)

    print("PRACTICA 9 - RESUMEN CON WORD2VEC")
    print("=" * 45)
    print(f"Palabras del texto original: {contar_palabras(texto)}")
    print(f"Oraciones seleccionadas: {indices}")
    print()
    print("RESUMEN")
    print("-" * 45)
    print(resumen)
    print(f"Palabras del texto resumido: {contar_palabras(resumen)}")


if __name__ == "__main__":
    main()
