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
    return texto.lower()

def tokenizador(texto):
    tokens = []
    token = ""
    separadores = string.whitespace + string.punctuation + "¿¡"

    for char in texto:
        if char not in separadores:
            token += char
        else:
            if token != "":
                tokens.append(token)
                token = ""
    if token != "":
        tokens.append(token)

    return tokens

def removedor_stop_words(tokens):
    stop_words = [
        "de","la","que","el","en","y","a","los","del","se","las",
        "por","un","para","con","una","su","al","lo","como","más",
        "entre","esta","este","son","es"
    ]
    return [w for w in tokens if w not in stop_words]

# ----------------------------
# WORDNET SIMILITUD
# ----------------------------

def best_wup_similarity(w1, w2):
    syns1 = wn.synsets(w1, lang='spa')
    syns2 = wn.synsets(w2, lang='spa')

    max_score = 0

    for s1 in syns1:
        for s2 in syns2:
            score = s1.wup_similarity(s2)
            if score and score > max_score:
                max_score = score

    return max_score

def score_texto(tokens, palabra_usuario):
    scores = []

    for token in tokens:
        score = best_wup_similarity(token, palabra_usuario)
        if score > 0:
            scores.append(score)

    if not scores:
        return 0

    # promedio de los mejores
    scores.sort(reverse=True)
    top = scores[:5]
    return sum(top) / len(top)

# ----------------------------
# SEPARAR TEXTO POR ECUACIONES
# ----------------------------

def separar_ecuaciones(texto):
    bloques = texto.split("\n\n")  # párrafos

    corpus = []

    for i in range(len(bloques)):
        bloque = bloques[i]

        # detectar si contiene ecuación
        if "=" in bloque:
            corpus.append({
                "ecuacion": bloque.strip(),
                "texto": bloques[i-1] if i > 0 else ""
            })

    return corpus

def main():

    # leer archivo
    with open("examen\inciso_a\ecuaciones.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    corpus = separar_ecuaciones(texto)

    palabra = input("Escribe una palabra: ")
    palabra = a_minusculas(palabra)

    mejor_score = 0
    mejor_ecuacion = ""
    mejor_texto = ""

    for item in corpus:
        texto_proc = a_minusculas(item["texto"])
        tokens = tokenizador(texto_proc)
        tokens = removedor_stop_words(tokens)

        score = score_texto(tokens, palabra)

        print("\nEcuación:", item["ecuacion"])
        print("Score:", score)

        if score > mejor_score:
            mejor_score = score
            mejor_ecuacion = item["ecuacion"]
            mejor_texto = item["texto"]

    print("\n----------------------------")
    if mejor_score > 0:
        print("Mejor coincidencia:\n")
        #print("Ecuación:", mejor_ecuacion)
        print("\nTexto asociado:")
        print(mejor_texto.strip())
    else:
        print("No se encontró relación.")

main()