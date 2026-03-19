import string
import nltk
from nltk.corpus import wordnet as wn

# --- FUNCIONES DE PROCESAMIENTO  ---

def A_minusculas(texto):
    letras = ""
    for letra in texto:
        # Conversión mediante tabla ASCII
        if ord(letra) >= 65 and ord(letra) <= 90:
            letra = chr(ord(letra) + 32)
        letras += letra
    return letras

def tokenizador(texto):
    token = ""
    tokens = []
    delimitadores = string.whitespace + string.punctuation
    
    # Asegurar que termine en delimitador para procesar el último token
    if texto[-1] not in delimitadores:
        texto = texto + '.'

    for i in range(len(texto)):
        char = texto[i]
        if char in delimitadores:
            if token != "":
                tokens.append(token)
            token = ""
        else:
            token += char
    return tokens

def removedor_stop_words(tokenized_text):
    stop_words = ["the","of","that","in","and","to","a","for","with", "on","at","by","from","as","is","are","was","were","it", "una", "de", "la", "el", "en", "que"]
    new_text = [item for item in tokenized_text if item not in stop_words]
    return new_text

# --- LÓGICA DE SIMILITUD ---

def best_wup_similarity(word1, word2):
    syns1 = wn.synsets(word1)
    syns2 = wn.synsets(word2)
    max_score = 0
    for s1 in syns1:
        for s2 in syns2:
            score = s1.wup_similarity(s2)
            if score is not None and score > max_score:
                max_score = score
    return max_score

def get_similarity_score(text_list, word_to_compare, k=5):
    scores = []
    for word in text_list:
        score = best_wup_similarity(word, word_to_compare)
        if score > 0:
            scores.append(score)
    
    if not scores:
        return 0

    scores.sort(reverse=True)
    top_k = scores[:k]
    return sum(top_k) / len(top_k)

# --- BASE DE DATOS DE ECUACIONES ---

DATASET = [
    {
        "nombre": "Ecuación de la recta",
        "ecuacion": "y = mx + b",
        "texto": "variable dependiente independiente pendiente inclinada línea intersección eje vertical estadística física ingeniería relaciones lineales"
    },
    {
        "nombre": "Teorema de Pitágoras",
        "ecuacion": "a² + b² = c²",
        "texto": "triángulo rectángulo catetos hipotenusa longitudes lados arquitectura navegación geometría analítica"
    },
    {
        "nombre": "Derivada",
        "ecuacion": "f'(x) = lim (h→0) [f(x+h) − f(x)] / h",
        "texto": "cálculo diferencial función tasa cambio instantánea velocidad posición tiempo"
    },
    {
        "nombre": "Distribución Normal",
        "ecuacion": "f(x) = (1 / (σ√(2π))) e^{-(x−μ)² / (2σ²)}",
        "texto": "probabilidad estadística media desviación estándar fenómenos naturales alturas errores medición biológicas"
    },
    {
        "nombre": "Energía de Einstein",
        "ecuacion": "E = mc²",
        "texto": "física masa velocidad luz equivalente transformación energía"
    },
    {
        "nombre": "Regresión Lineal (Error)",
        "ecuacion": "J(θ) = (1 / 2n) Σ (hθ(xᵢ) − yᵢ)²",
        "texto": "algoritmos inteligencia artificial minimizar función error modelo observaciones predicción parámetros óptimos"
    }
]

def main():
    nltk.download('wordnet', quiet=True)
    
    entrada = input("Escribe una palabra relacionada con una ecuación: ")
    palabra_usuario = A_minusculas(entrada)
    
    mejor_puntaje = -1
    ganador = None

    print("\nAnalizando similitud con WordNet...")

    for item in DATASET:
        # Procesamos el texto descriptivo de la base de datos
        tokens = tokenizador(A_minusculas(item["texto"]))
        limpios = removedor_stop_words(tokens)
        
        score = get_similarity_score(limpios, palabra_usuario)
        
        if score > mejor_puntaje:
            mejor_puntaje = score
            ganador = item

    if ganador and mejor_puntaje > 0:
        print(f"\n--- Resultado ---")
        print(f"Palabra detectada como relacionada con: {ganador['nombre']}")
        print(f"Ecuación: {ganador['ecuacion']}")
        print(f"Confianza (WUP Score): {mejor_puntaje:.4f}")
    else:
        print("No se encontró una relación clara con ninguna ecuación.")

if __name__ == "__main__":
    main()