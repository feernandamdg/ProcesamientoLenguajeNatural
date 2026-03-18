import re
import unicodedata
from functools import lru_cache
import nltk
from nltk.corpus import wordnet as wn

# Descargar recursos de NLTK (solo la primera vez)
nltk.download("wordnet")
nltk.download("omw-1.4")

def normalizar(texto):
    """Convierte a minúsculas y elimina tildes."""
    texto = texto.lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto

def tokenizar(texto):
    """Separa el texto en palabras."""
    return re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+", texto)

@lru_cache(maxsize=None)
def obtener_sinonimos_wordnet(palabra):
    """
    Busca sinónimos en WordNet en español.
    Si no encuentra, devuelve conjunto vacío.
    """
    sinonimos = set()
    try:
        synsets = wn.synsets(palabra, lang="spa")
        for syn in synsets:
            for lemma in syn.lemma_names("spa"):
                sinonimos.add(normalizar(lemma.replace("_", " ")))
    except:
        pass
    return sinonimos

def expandir_terminos(texto):
    """
    Devuelve las palabras del usuario + sinónimos encontrados con WordNet.
    """
    terminos = set()
    texto_norm = normalizar(texto)
    palabras = tokenizar(texto_norm)

    terminos.add(texto_norm)

    for palabra in palabras:
        palabra_norm = normalizar(palabra)
        terminos.add(palabra_norm)
        terminos.update(obtener_sinonimos_wordnet(palabra_norm))

    return terminos

# Diccionario de ecuaciones
ecuaciones = {
    "recta": {
        "nombre": "Ecuación de la recta",
        "ecuacion": "y = mx + b",
        "palabras_clave": ["recta", "linea", "pendiente", "interseccion", "lineal"]
    },
    "pitagoras": {
        "nombre": "Teorema de Pitágoras",
        "ecuacion": "a² + b² = c²",
        "palabras_clave": ["pitagoras", "triangulo", "hipotenusa", "catetos", "geometria"]
    },
    "derivada": {
        "nombre": "Definición de derivada",
        "ecuacion": "f'(x) = lim (h→0) [f(x+h) − f(x)] / h",
        "palabras_clave": ["derivada", "calculo", "cambio", "velocidad", "funcion"]
    },
    "normal": {
        "nombre": "Distribución normal",
        "ecuacion": "f(x) = (1 / (σ√(2π))) e^{-(x−μ)² / (2σ²)}",
        "palabras_clave": ["normal", "probabilidad", "estadistica", "media", "desviacion"]
    },
    "einstein": {
        "nombre": "Ecuación de energía de Einstein",
        "ecuacion": "E = mc²",
        "palabras_clave": ["einstein", "energia", "masa", "luz", "fisica"]
    },
    "regresion": {
        "nombre": "Función de error en regresión lineal",
        "ecuacion": "J(θ) = (1 / 2n) Σ (hθ(xᵢ) − yᵢ)²",
        "palabras_clave": ["regresion", "error", "modelo", "prediccion", "algoritmo", "inteligencia"]
    }
}

def buscar_ecuacion(entrada):
    entrada_norm = normalizar(entrada)
    terminos_usuario = expandir_terminos(entrada)

    resultados = []

    for clave, datos in ecuaciones.items():
        palabras_clave_expandida = set()

        for palabra in datos["palabras_clave"]:
            palabra_norm = normalizar(palabra)
            palabras_clave_expandida.add(palabra_norm)
            palabras_clave_expandida.update(obtener_sinonimos_wordnet(palabra_norm))

        # Buscar coincidencias directas o por sinónimos
        coincidencias = terminos_usuario.intersection(palabras_clave_expandida)

        if coincidencias or any(normalizar(p) in entrada_norm for p in datos["palabras_clave"]):
            resultados.append({
                "nombre": datos["nombre"],
                "ecuacion": datos["ecuacion"],
                "coincidencias": list(coincidencias)
            })

    return resultados

# Programa principal
print("=== Buscador de ecuaciones con WordNet y diccionarios ===")
print("Escribe una palabra o frase relacionada con una ecuación.")
print("Ejemplos: recta, hipotenusa, velocidad, energia, probabilidad\n")

consulta = input("Ingresa tu palabra o frase: ")

resultados = buscar_ecuacion(consulta)

if resultados:
    print("\nEcuaciones encontradas:\n")
    for r in resultados:
        print(f"{r['nombre']}:")
        print(f"  {r['ecuacion']}")
        if r["coincidencias"]:
            print(f"  Coincidencias encontradas: {', '.join(r['coincidencias'])}")
        print()
else:
    print("\nNo se encontró una ecuación relacionada con esa palabra.")