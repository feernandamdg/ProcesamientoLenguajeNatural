import string
from pypdf import PdfReader
import nltk
from nltk.corpus import wordnet as wn
import math

def tokenizador(texto):

  token = ""
  tokens = []
  
  withes = string.whitespace
  delimitadores = string.whitespace + string.punctuation
  numbers = string.digits
  not_letters = delimitadores + numbers

  if texto[-1] not in delimitadores:
    texto = texto + '.'
    #print("Texto ingresado:", texto)
  else:
    print("No se agregó punto:", texto)
    
  is_number = None

  for i in range(0, len(texto)):
    char = texto[i]
    if texto[i] == '.' or texto[i] in withes:
      if token != "":
        tokens = tokens + [token]
      token = ""
      is_number = None
    elif token == "" and texto[i] not in delimitadores:
        if texto[i] in numbers:
            is_number = True
        if texto[i] not in not_letters:
            is_number = False
        token += texto[i]
    elif texto[i] not in not_letters and is_number: # Si comenzó como digito y encontró letra.
          token = texto[i]
          is_number = False
    elif (texto[i] in numbers and is_number) or (texto[i] not in not_letters and not is_number): #Si texto[i] corresponde a la bandera
          token += texto[i]

  return tokens

def A_mayusculas(texto):
    letras = ""
    
    for letra in texto:
        if ord(letra) >= 65 and ord(letra) <=90:
            letra = chr(ord(letra) +32)
        letras += letra
    return letras

def removedor_stop_words(tokenized_text, special_stop_words=[]):
    og_stop_words = [
    "the","of","that","in","and","to","a","for","with",
    "on","at","by","from","as","is","are","was","were","it"
    ]
    stop_words = og_stop_words+special_stop_words
    new_text = []
    for item in tokenized_text:
        if item not in stop_words:
            new_text = new_text + [item]
    return new_text

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path) #
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\\n" #
    return full_text

def count_words(text):
    count = 0
    withes = string.whitespace + '.'
    a_word = False
    
    for char in text:
        if char not in withes :
            if not a_word:
                count += 1
                a_word = True
        else:
            a_word = False

    return count

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
    total_score = 0
    valid_comparisons = 0
    max_word = ""
    score_max = 0

    for word in text_list:
        score = best_wup_similarity(word, word_to_compare)
        if score > 0:
            if score > score_max:
                max_word = word
                score_max = score
            total_score += score
            valid_comparisons += 1

    if valid_comparisons == 0:
        return 0

    print(max_word, total_score/valid_comparisons,"\n")    
    return total_score/valid_comparisons

def main():
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    
    word_to_compare = input("Write a word:")
    max_score = 0
    max_topic = ""
        
    for item in FILE_INFO:   
        texto = extract_text_from_pdf(item["file_location"])
        minusc_text = A_mayusculas(texto)
        tokenized_text = tokenizador(minusc_text)
        compressed_text_list = removedor_stop_words(tokenized_text,item["stop_words"])
        print(compressed_text_list)
        print(item["topic"])
        score = get_similarity_score(compressed_text_list, word_to_compare)
        if score > max_score:
            max_score = score
            max_topic = item["topic"]
    
    print(f"The word belongs to a {max_topic} text")    
        
        
    
FILE_INFO = [
    {"topic":"literary",
    "file_location": "literary_text.pdf",
    "stop_words" : [
        "had", "was", "seemed", "while", "then",
        "later", "that", "that_one", "where", "when",
        "toward", "about", "between", "some", "none",
        "but", "although", "perhaps", "maybe", "such"
    ]},

    {"topic":"mathematical",
    "file_location": "mathematical_text.pdf",
    "stop_words" : [
        "let", "given", "exists", "where", "then",
        "suppose", "such", "that", "satisfies", "always",
        "each", "all", "value", "result", "form",
        "defined", "obtained", "through", "property", "with_respect_to"
    ]},

    {"topic":"medical",
    "file_location": "medical_text.pdf",
    "stop_words" : [
        "denied", "presents", "clinical", "diagnosis", "treatment",
        "observed", "frequency", "associated", "chronic", "acute",
        "symptoms", "examination", "results", "indicated", "through",
        "process", "condition", "evaluation", "history", "reports"
    ]},

    {"topic":"biological",
    "file_location": "biological_text.pdf",
    "stop_words" : [
        "structure", "function", "system", "process", "activity",
        "level", "type", "development", "formation", "component",
        "present", "region", "group", "part", "characteristic",
        "condition", "interaction", "relationship", "composition", "dynamics"
    ]},

    {"topic":"musical",
    "file_location": "musical_text.pdf",
    "stop_words" : [
        "work", "piece", "performance", "style", "form",
        "sound", "section", "part", "structure", "passage",
        "element", "character", "variation", "repetition", "motif",
        "context", "set", "group", "moment", "effect"
    ]},

    {"topic":"computational",
    "file_location": "computational_text.pdf",
    "stop_words" : [
        "system", "process", "method", "structure", "component",
        "function", "element", "operation", "result", "input",
        "output", "model", "level", "type", "format",
        "set", "group", "state", "condition", "parameter"
    ]}
]

main()
    