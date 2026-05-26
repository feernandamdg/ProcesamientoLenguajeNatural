# ======================================================
# A) DETECTOR DE languageS CON N-GRAMAS DE CARACTERES
# ======================================================

def clean_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    return text

def get_char_ngrams(text, n=3):
    text = clean_text(text)
    text = text.replace(" ", "_")

    ngrams = []

    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        ngrams.append(ngram)

    return ngrams


def ngram_profiles(text, n=3, top=200):
    ngrams = get_char_ngrams(text, n)

    frequencies = {}

    for ng in ngrams:
        if ng not in frequencies:
            frequencies[ng] = 0
        frequencies[ng] += 1

    sorted_ngrams = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    profile = {}

    for ngram_index, ngram_value in enumerate(sorted_ngrams[:top]):
        ngram = ngram_value[0]
        profile[ngram] = ngram_index

    return profile


def distance(profile1, profile2):
    ngrams = set(profile1.keys()) | set(profile2.keys())

    penalty = max(len(profile1), len(profile2)) + 1

    total_distance = 0

    for ng in ngrams:
        r1 = profile1.get(ng, penalty)
        r2 = profile2.get(ng, penalty)

        total_distance += abs(r1 - r2)

    return total_distance

def create_languages_dict(): 
    with open('./ngramas/texts/es.txt', 'r', encoding='utf-8') as file1:
        text_es = file1.read()
        
    with open('./ngramas/texts/en.txt', 'r', encoding='utf-8') as file2:
        text_en = file2.read()
        
    with open('./ngramas/texts/fr.txt', 'r', encoding='utf-8') as file3:
        text_fr = file3.read()

    texts_language = {
        "spanish": text_es,
        "english": text_en,
        "french": text_fr
    }

    languages_dict = {}

    for language in texts_language:
        languages_dict[language] = ngram_profiles(texts_language[language])
    return languages_dict


def detect_language(text,languages_dict):
    print("PHRASE:",text)
    pf = ngram_profiles(text)

    best_lang = None
    best_distance = None

    for language in languages_dict:
        dist = distance(pf, languages_dict[language])
        
        print(language,dist)

        if best_distance is None or dist < best_distance:
            best_distance = dist
            best_lang = language

    print("LANGUAGE DETECTED ->", str.upper(best_lang))
    print("")

    return best_lang

test_es = "El muchacho compró zanahorias en el mercado."
test_en = "The neighbor repaired the wooden chair yesterday."
test_fr = "La boulangerie vend du pain chaud chaque matin."

languages_dict = create_languages_dict()

detect_language(test_es,languages_dict)
detect_language(test_en,languages_dict)
detect_language(test_fr,languages_dict)

usr_input = input("Type a phrase in EN, ES or FR: ")
detect_language(usr_input,languages_dict)