import string
import nltk
from nltk.corpus import wordnet as wn

def tokenizador(texto):
    token = ""
    tokens = []

    whites = string.whitespace
    delimitadores = string.whitespace + string.punctuation
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
    sum_top_scores = 0
    for item in top_k_scores:
        sum_top_scores +=item
    avg_score = sum_top_scores / len(top_k_scores)

    return avg_score


FILE_INFO = [
    {
        "ecuacion": "y = mx + b",
        "texto": """
        Una de las ecuaciones más conocidas es la ecuación de la recta.
        En esta expresión, la variable y representa la variable dependiente,
        mientras que x representa la variable independiente. El parámetro m
        es la pendiente de la recta y describe qué tan inclinada está la línea.
        El valor b corresponde a la intersección con el eje vertical, es decir,
        el punto donde la recta cruza el eje y cuando x = 0. Esta ecuación se
        utiliza ampliamente en estadística, física e ingeniería para modelar
        relaciones lineales entre variables.
        """,
        "stop_words": ["variable", "variables", "ecuación"]
    },
    {
        "ecuacion": "a² + b² = c²",
        "texto": """
        Otra ecuación muy conocida es el teorema de Pitágoras, que describe la
        relación entre los lados de un triángulo rectángulo.
        En esta ecuación, a y b representan los catetos del triángulo, mientras
        que c representa la hipotenusa. Si se conocen las longitudes de dos lados
        es posible calcular la longitud del tercero. Este teorema ha sido utilizado
        durante más de dos mil años en áreas como la arquitectura, la navegación y
        la geometría analítica.
        """,
        "stop_words": ["ecuación", "representa"]
    },
    {
        "ecuacion": "f'(x) = lim (h→0) [f(x+h) − f(x)] / h",
        "texto": """
        En cálculo diferencial aparece otra ecuación importante relacionada con la derivada. 
        Esta expresión describe la tasa de cambio instantánea de una función. La derivada
        permite analizar cómo cambia una variable con respecto a otra. Por ejemplo, en
        física la derivada de la posición respecto al tiempo corresponde a la velocidad.
        """,
        "stop_words": ["ecuación", "función", "representa"]
    },
    {
        "ecuacion": "f(x) = (1 / (σ√(2π))) e^{-(x−μ)² / (2σ²)}",
        "texto": """
        Probabilidad: En probabilidad y estadística encontramos la ecuación de la distribución normal.
        En esta fórmula se representa la media de la distribución y representa la
        desviación estándar. Esta distribución es fundamental para describir fenómenos 
        naturales como alturas de personas, errores de medición y muchas variables biológicas.
        """,
        "stop_words": ["ecuación", "función", "modelo"]
    },
    {
        "ecuacion": "E = mc²",
        "texto": """
        Otra ecuación muy conocida en física es la ecuación de energía de Einstein.
        Esta ecuación establece que la energía es igual a la masa multiplicada
        por el cuadrado de la velocidad de la luz. Esta relación demuestra que
        masa y energía son equivalentes y puede transformarse una en otra bajo ciertas condiciones.
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
    palabra_usuario = a_minusculas(palabra_usuario)

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