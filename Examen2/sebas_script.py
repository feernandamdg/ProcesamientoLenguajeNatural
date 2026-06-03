# ======================================================
# PERFIL DE N-GRAMAS POR PALABRA CON RANKING
# Entrada: lista de palabras ya preprocesada
# ======================================================

def create_word_ngram_profile(words, n=2, top=200):
    """
    Crea un perfil por palabra usando n-gramas de palabras.

    Entrada:
        words = ["el", "muchacho", "compró", "pan", "el", "perro"]

    Si n=2:
        palabra_actual -> palabra_siguiente -> ranking

        Ejemplo:
        {
            "el": {
                "muchacho": 0,
                "perro": 1
            }
        }

    Si n=3:
        palabra_actual -> (palabra_siguiente_1, palabra_siguiente_2) -> ranking
    """

    frequencies_by_word = {}

    for i in range(len(words) - n + 1):
        current_word = words[i]
        next_words = words[i+1:i+n]

        if n == 2:
            ngram_value = next_words[0]
        else:
            ngram_value = tuple(next_words)

        if current_word not in frequencies_by_word:
            frequencies_by_word[current_word] = {}

        if ngram_value not in frequencies_by_word[current_word]:
            frequencies_by_word[current_word][ngram_value] = 0

        frequencies_by_word[current_word][ngram_value] += 1

    profile = {}

    for word in frequencies_by_word:
        sorted_values = sorted(
            frequencies_by_word[word].items(),
            key=lambda x: x[1],
            reverse=True
        )

        profile[word] = {}

        for ngram_index, ngram_value in enumerate(sorted_values[:top]):
            value = ngram_value[0]
            profile[word][value] = ngram_index

    return profile


def show_word_ngram_profile(words, n=2, top=200):
    profile = create_word_ngram_profile(words, n, top)

    print("WORD N-GRAM PROFILE WITH RANKING:")
    print("")

    for word in profile:
        print(word, ":", profile[word])

    return profile


# ======================================================
# PRUEBA
# ======================================================

words = [
    "el", "muchacho", "compró", "pan",
    "el", "muchacho", "compró", "agua",
    "el", "perro", "compró", "pan"
]

with open('./Examen2/corpus.txt', 'r', encoding='utf-8') as file1:
    text_es = file1.read()

words = text_es.split(" ")

profile = show_word_ngram_profile(words, n=2, top=200)