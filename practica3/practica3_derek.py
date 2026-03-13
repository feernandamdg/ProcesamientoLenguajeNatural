import string
from pypdf import PdfReader
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

#leemos documentos
FILE_INFO = [
    {"topic":"literary", "file_location": "sample_data/literary_text.pdf", "stop_words" : ["had", "was", "seemed", "while", "then", "later", "that", "that_one", "where", "when", "toward", "about", "between", "some", "none", "but", "although", "perhaps", "maybe", "such"]},
    {"topic":"mathematical", "file_location": "sample_data/mathematical_text.pdf", "stop_words" : ["let", "given", "exists", "where", "then", "suppose", "such", "that", "satisfies", "always", "each", "all", "value", "result", "form", "defined", "obtained", "through", "property", "with_respect_to"]},
    {"topic":"medical", "file_location": "sample_data/medical_text.pdf", "stop_words" : ["denied", "presents", "clinical", "diagnosis", "treatment", "observed", "frequency", "associated", "chronic", "acute", "symptoms", "examination", "results", "indicated", "through", "process", "condition", "evaluation", "history", "reports"]},
    {"topic":"biological", "file_location": "sample_data/biological_text.pdf", "stop_words" : ["structure", "function", "system", "process", "activity", "level", "type", "development", "formation", "component", "present", "region", "group", "part", "characteristic", "condition", "interaction", "relationship", "composition", "dynamics"]},
    {"topic":"musical", "file_location": "sample_data/musical_text.pdf", "stop_words" : ["work", "piece", "performance", "style", "form", "sound", "section", "part", "structure", "passage", "element", "character", "variation", "repetition", "motif", "context", "set", "group", "moment", "effect"]},
    {"topic":"computational", "file_location": "sample_data/computational_text.pdf", "stop_words" : ["system", "process", "method", "structure", "component", "function", "element", "operation", "result", "input", "output", "model", "level", "type", "format", "set", "group", "state", "condition", "parameter"]}
]

def to_lowercase_ascii(text):
    # Función para pasar a minúsculas por medio de ASCII sin usar .lower()
    result = ""
    for char in text:
        ascii_val = ord(char)
        # Si está entre 'A' (65) y 'Z' (90), sumamos 32 para llegar a la minúscula
        if 65 <= ascii_val <= 90:
            result += chr(ascii_val + 32)
        else:
            result += char
    return result

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        return full_text
    except FileNotFoundError:
        print(f"Error: Document wasn't found {pdf_path}")
        return ""

def procesar_texto(texto, special_stop_words):
    #Base de stop words
    og_stop_words = ["the","of","that","in","and","to","a","for","with", "on","at","by","from","as","is","are","was","were","it"]

    #convertimos las stop words en un 'set'. Las búsquedas en sets son instantáneas en Python.
    stop_words = set(og_stop_words + special_stop_words)

    #NLTK y conversión a minúsculas manual mediante ASCII
    tokens = word_tokenize(to_lowercase_ascii(texto))

    #Filtramos, nos quedamos con palabras (.isalpha()) que NO sean stop words
    tokens_limpios = [word for word in tokens if word.isalpha() and word not in stop_words]

    return tokens_limpios

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

def get_similarity_score(text_list, word_to_compare):
    #Optimizamos si una palabra aparece muchas veces solo se cuenta una vez
    vocabulario_unico = set(text_list)

    total_score = 0
    valid_comparisons = 0

    for word in vocabulario_unico:
        score = best_wup_similarity(word, word_to_compare)

        # Decimos que solo sumamos la palabra si tiene al menos un 0.3 de similitud
        # para no diluir el puntaje con palabras que no tienen nada que ver.
        if score > 0.3:
            total_score += score
            valid_comparisons += 1

    if valid_comparisons == 0:
        return 0

    return total_score / valid_comparisons

def main():
    # Descargas silenciosas de los paquetes necesarios de NLTK
    nltk.download('punkt', quiet=True) # Para word_tokenize
    nltk.download('punkt_tab', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

    #Ingresamos la palabra y la hacemos minuscula usando ASCII
    input_word = input("\nWrite a word to classify: ")
    word_to_compare = to_lowercase_ascii(input_word)

    max_score = 0
    max_topic = ""

    print("\nanalyzing documents (this may take a few seconds)...\n")

    for item in FILE_INFO:
        texto = extract_text_from_pdf(item["file_location"])

        if not texto:
            continue

        texto_limpio = procesar_texto(texto, item["stop_words"])
        score = get_similarity_score(texto_limpio, word_to_compare)

        print(f"-> analyzing document {item['topic']}... Score: {score:.4f}")

        if score > max_score:
            max_score = score
            max_topic = item["topic"]

    if max_score > 0:
        print(f"\nThe word '{word_to_compare}'  belongs to a  **{max_topic.upper()}** text.")
    else:
        print(f"\nNo sufficient similarity was found in any text for the word '{word_to_compare}'.")

main()
