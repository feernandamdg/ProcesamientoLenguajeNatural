import string
import nltk
from nltk.corpus import wordnet as wn

# Descargar recursos
nltk.download('wordnet')
nltk.download('omw-1.4')

# ----------------------------
# FUNCIONES BÁSICAS
# ----------------------------

def a_minusculas(texto):
    letras = ""
    for letra in texto:
        if ord(letra) >= 65 and ord(letra) <= 90:
            letra = chr(ord(letra) + 32)
        letras += letra
    return letras

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

# ----------------------------
# WORDNET SIMILITUD
# ----------------------------

def best_wup_similarity(word1, word2):
    syns1 = wn.synsets(word1, lang='spa')
    syns2 = wn.synsets(word2, lang='spa')

    if not syns2:
        print(f"No se encontró la palabra {word2} en synsets.")
        exit()

    max_score = 0

    for s1 in syns1:
        for s2 in syns2:
            score = s1.wup_similarity(s2)
            if score is not None and score > max_score:
                max_score = score

    return max_score

def score_texto(tokens, palabra_usuario, k=5):
    scores = []

    for token in tokens:
        score = best_wup_similarity(token, palabra_usuario)
        if score > 0:
            scores += [score]

    if not scores:
        return 0

    scores.sort(reverse=True)
    top_scores = scores[:k]

    suma = 0
    for item in top_scores:
        suma += item

    return suma / len(top_scores)

# ----------------------------
# SEPARAR TEXTO POR ECUACIONES
# ----------------------------

def separar_ecuaciones(texto):
    lineas = texto.split("\n\n")  # cada párrafo
    corpus = []

    for linea in lineas:
        if ":" in linea:
            partes = linea.split(":")
            
            texto_asociado = partes[0].strip()
            ecuacion = partes[1].strip()

            corpus += [{
                "ecuacion": ecuacion,
                "texto": texto_asociado
            }]

    return corpus

def main():
    with open("examen/inciso_a/ecuaciones.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    corpus = separar_ecuaciones(texto)

    palabra = input("Escribe una palabra relacionada con una ecuación: ")
    palabra = a_minusculas(palabra)

    mejor_score = 0
    mejor_ecuacion = ""
    mejor_texto = ""

    for item in corpus:
        texto_proc = a_minusculas(item["texto"])
        tokens = tokenizador(texto_proc)
        tokens = removedor_stop_words(tokens)

        score = score_texto(tokens, palabra, k=5)

        print("\nEcuación:", item["ecuacion"])
        print("Score:", score)
        print("-" * 50)

        if score > mejor_score:
            mejor_score = score
            mejor_ecuacion = item["ecuacion"]
            mejor_texto = item["texto"]

    print("\n----------------------------")
    if mejor_score > 0:
        print("La palabra se relaciona más con la ecuación:\n")
        print(mejor_ecuacion)
        print("\nTexto asociado:")
        print(mejor_texto.strip())
    else:
        print("No se encontró relación suficiente con ninguna ecuación.")

main()