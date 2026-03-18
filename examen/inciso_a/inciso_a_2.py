import string
import nltk
from nltk.corpus import wordnet as wn

def tokenizador(texto):
    token = ""
    tokens = []

    whites = string.whitespace
    delimitadores = string.whitespace + string.punctuation + "¿¡”“’‘—–[]{}()<>…=+-/*^%|\\,:;\"'"
    numbers = string.digits
    not_letters = delimitadores + numbers

    if len(texto) > 0 and texto[-1] not in delimitadores:
        texto = texto + '.'

    is_number = None

    for i in range(0, len(texto)):
        char = texto[i]

        if char == '.' or char in whites:
            if token != "":
                tokens += [token]
            token = ""
            is_number = None

        elif token == "" and char not in delimitadores:
            if char in numbers:
                is_number = True
            if char not in not_letters:
                is_number = False
            token += char

        elif char not in not_letters and is_number:
            token = char
            is_number = False

        elif (char in numbers and is_number) or (char not in not_letters and not is_number):
            token += char

    return tokens


def a_minusculas(texto):
    letras = ""
    for letra in texto:
        if ord(letra) >= 65 and ord(letra) <= 90:
            letra = chr(ord(letra) + 32)
        letras += letra
    return letras


def removedor_stop_words(tokenized_text, special_stop_words=None):
    if special_stop_words is None:
        special_stop_words = []

    og_stop_words = [
        "de", "la", "que", "el", "en", "y", "a", "los", "del", "se",
        "las", "por", "un", "para", "con", "una", "su", "al", "lo",
        "es", "como", "más", "menos", "si", "o", "u", "e", "ha",
        "han", "ser", "esta", "este", "estas", "estos", "cada",
        "entre", "sobre", "desde", "durante", "cuando", "donde",
        "porque", "también", "muy", "sin", "puede", "pueden"
    ]

    stop_words = og_stop_words + special_stop_words
    new_text = []

    for item in tokenized_text:
        if item not in stop_words:
            new_text += [item]

    return new_text


def best_wup_similarity(word1, word2):
    # WordNet en español
    syns1 = wn.synsets(word1, lang='spa')
    syns2 = wn.synsets(word2, lang='spa')
    
    if not syns2:
        print(f"No se encontró la palbra {word2} en synsets.")
        exit()

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
            scores += [score]

    if not scores:
        return 0

    scores.sort(reverse=True)
    top_k_scores = scores[:k]
    avg_score = sum(top_k_scores) / len(top_k_scores)

    return avg_score


FILE_INFO = [
    {
        "ecuacion": "y = mx + b",
        "texto": """
        La ecuación de la recta representa una relación lineal entre variables.
        La variable y depende de x. El parámetro m es la pendiente de la recta
        y b es la intersección con el eje vertical. Esta ecuación se usa en
        estadística, física e ingeniería para modelar relaciones lineales,
        crecimiento proporcional, tendencias y comportamiento de datos.
        """,
        "stop_words": ["variable", "variables", "ecuación", "recta"]
    },
    {
        "ecuacion": "a² + b² = c²",
        "texto": """
        El teorema de Pitágoras describe la relación entre los lados de un
        triángulo rectángulo. Los catetos se representan con a y b, mientras
        que c es la hipotenusa. Se utiliza en geometría, arquitectura,
        navegación y cálculo de distancias.
        """,
        "stop_words": ["ecuación", "teorema", "representa"]
    },
    {
        "ecuacion": "f'(x) = lim (h→0) [f(x+h) − f(x)] / h",
        "texto": """
        La derivada describe la tasa de cambio instantánea de una función.
        Permite analizar variación, cambio, pendiente, velocidad y comportamiento
        local. En física, la derivada de la posición respecto al tiempo es la
        velocidad. En cálculo diferencial se usa para estudiar funciones.
        """,
        "stop_words": ["ecuación", "función", "representa"]
    },
    {
        "ecuacion": "f(x) = (1 / (σ√(2π))) e^{-(x−μ)² / (2σ²)}",
        "texto": """
        La distribución normal modela fenómenos aleatorios alrededor de una media.
        Incluye conceptos como probabilidad, estadística, desviación estándar,
        media, error de medición, alturas y variables biológicas. Es fundamental
        en inferencia estadística y análisis de datos.
        """,
        "stop_words": ["ecuación", "función", "modelo"]
    },
    {
        "ecuacion": "E = mc²",
        "texto": """
        La ecuación de Einstein establece la equivalencia entre masa y energía.
        Relaciona la masa con la velocidad de la luz y explica fenómenos de la
        física moderna. Se usa en relatividad, energía nuclear y transformación
        de materia en energía.
        """,
        "stop_words": ["ecuación", "relación", "establece"]
    },
    {
        "ecuacion": "J(θ) = (1 / 2n) Σ (hθ(xᵢ) − yᵢ)²",
        "texto": """
        La función de error en regresión lineal mide qué tan lejos están las
        predicciones de los valores reales. Se usa en aprendizaje automático,
        inteligencia artificial, optimización, entrenamiento de modelos,
        observaciones, predicción y ajuste de parámetros.
        """,
        "stop_words": ["ecuación", "función", "modelo"]
    }
]


def main():
    nltk.download('wordnet')
    nltk.download('omw-1.4')

    palabra_usuario = input("Escribe una palabra relacionada con una ecuación: ")
    palabra_usuario = a_minusculas(palabra_usuario).strip()

    max_score = 0
    mejor_ecuacion = ""
    mejor_texto = ""

    for item in FILE_INFO:
        texto = item["texto"]
        minusc_text = a_minusculas(texto)
        tokenized_text = tokenizador(minusc_text)
        compressed_text_list = removedor_stop_words(tokenized_text, item["stop_words"])

        score = get_similarity_score(compressed_text_list, palabra_usuario, k=5)

        print("Ecuación:", item["ecuacion"])
        print("Score:", score)
        print("-" * 50)

        if score > max_score:
            max_score = score
            mejor_ecuacion = item["ecuacion"]
            mejor_texto = item["texto"]

    if max_score > 0:
        print("\nLa palabra se relaciona más con la ecuación:")
        print(mejor_ecuacion)
        print("\nDescripción asociada:")
        print(mejor_texto.strip())
    else:
        print("\nNo se encontró relación suficiente con ninguna ecuación.")


main()