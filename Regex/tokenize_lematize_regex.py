import regex as re
import string
from pypdf import PdfReader

lemmas_excepciones = {
    "fue":"ser",
    "fueron":"ser",
    "soy":"ser",
    "eres":"ser",
    "es":"ser",
    "son":"ser",
    "malas":"malo",
    "malos":"malo",
    "buenas":"bueno",
    "peliculas":"pelicula",
    "actuaciones":"actuacion",
    "tramas":"trama",
    "mejores":"bueno",
    "era": "ser",
    "iban": "ir",
    "iba": "ir",
    "tuvo": "tener"
}

bases_dict = {
    # Verbos terminación -AR
    "habl": "hablar", "cant": "cantar", "bail": "bailar", "salt": "saltar", "camin": "caminar",
    "mir": "mirar", "escuch": "escuchar", "pens": "pensar", "trabaj": "trabajar", "jug": "jugar",
    "estudi": "estudiar", "viaj": "viajar", "compr": "comprar", "pag": "pagar", "us": "usar",
    "toc": "tocar", "dibuj": "dibujar", "pint": "pintar", "imagin": "imaginar", "record": "recordar",
    "olvid": "olvidar", "busqu": "buscar", "busc": "buscar", "llev": "llevar", "dej": "dejar",
    "guard": "guardar", "explic": "explicar", "pregunt": "preguntar", "contest": "contestar", "cuid": "cuidar",
    "ayud": "ayudar", "intent": "intentar", "prob": "probar", "cre": "crear", "dese": "desear",
    "esper": "esperar", "logr": "lograr", "empez": "empezar", "termin": "terminar", "cambi": "cambiar",
    "mejor": "mejorar", "organiz": "organizar", "pagan": "pagar", "tocon": "tocar", "buscan": "buscar",
    "plan": "planear", "prepar": "preparar", "present": "presentar", "analiz": "analizar", "observ": "observar",
    "compar": "comparar", "señal": "señalar", "marc": "marcar", "consider": "considerar",

    # Verbos terminación -ER
    "com": "comer", "beb": "beber", "le": "leer", "corr": "correr", "tem": "temer",
    "vend": "vender", "aprend": "aprender", "entend": "entender", "depend": "depender", "sorb": "sorber",
    "mord": "morder", "romp": "romper", "respond": "responder", "perd": "perder", "volv": "volver",
    "resolv": "resolver", "envolv": "envolver", "mov": "mover", "remov": "remover", "devolv": "devolver",
    "coc": "cocer", "torc": "torcer", "retorc": "retorcer", "crec": "crecer", "ofrec": "ofrecer",
    "merec": "merecer", "obedec": "obedecer", "parec": "parecer", "establec": "establecer", "pertenec": "pertenecer",
    "agradec": "agradecer", "desaparec": "desaparecer", "conoc": "conocer", "reconoc": "reconocer", "traduc": "traducir",
    "produc": "producir", "reduc": "reducir", "conduc": "conducir", "introduc": "introducir", "deduc": "deducir",
    "seduc": "seducir", "bendic": "bendecir", "convenc": "convencer", "venc": "vencer", "defend": "defender",
    "encend": "encender", "tend": "tender", "extend": "extender", "suspend": "suspender", "pretend": "pretender",

    # Verbos terminación -IR
    "viv": "vivir", "escrib": "escribir", "recib": "recibir", "abr": "abrir", "permit": "permitir",
    "admit": "admitir", "asist": "asistir", "divid": "dividir", "decid": "decidir", "repet": "repetir",
    "exig": "exigir", "correg": "corregir", "corrig": "corregir", "dirig": "dirigir", "eleg": "elegir",
    "elig": "elegir", "segu": "seguir", "sigu": "seguir", "persigu": "perseguir", "persegu": "perseguir",
    "consigu": "conseguir", "consegu": "conseguir", "prohib": "prohibir", "imprim": "imprimir", "suprim": "suprimir",
    "comprim": "comprimir", "expand": "expandir", "confund": "confundir", "difund": "difundir", "fund": "fundir",
    "hund": "hundir", "interrump": "interrumpir", "cumpl": "cumplir", "descubr": "descubrir", "cubr": "cubrir",
    "inscrib": "inscribir", "describ": "describir", "suscrib": "suscribir", "reescrib": "reescribir", "proscrib": "proscribir",
    "inclu": "incluir", "conclu": "concluir", "exclu": "excluir", "atribu": "atribuir", "distribu": "distribuir",
    "retribu": "retribuir", "constru": "construir", "destru": "destruir", "instru": "instruir", "sustitu": "sustituir",
    "institu": "instituir", "constitu": "constituir", "restitu": "restituir", "destitu": "destituir", "intu": "intuir"
}

def regex_tokenaizer(texto):
  tokenized_text = re.findall(r"\w+",texto)
  return tokenized_text

def A_mayusculas(texto):
    letras = ""
    for letra in texto:
        if letra == 'e':
            pass
        if ord(letra) >= 65 and ord(letra) <=90:
            letra = chr(ord(letra) +32)
        letras += letra
    return letras

def removedor_stop_words(tokenized_text):
    stop_words = ["de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","una","su","al","lo"]
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

def regex_lematizer(text):
    lematized_words = []
    for word in text:
        word_length = len(word)
        ar_regex = re.match(r"(.+)(?:ando|é|aste|ó|amos|aron|aré|arás|ará|aremos|arán)",word)
        er_regex = re.match(r"(.+)(?:iendo|í|iste|ió|imos|ieron|eré|erás|eremos|erán)",word)
        ir_regex = re.match(r"(.+)(?:iendo|í|iste|ió|imos|ieron|iré|irás|iremos|irán)",word)
        
        if word in lemmas_excepciones:
            lematized_words += [lemmas_excepciones[word]]
        #ar
        elif ar_regex and ar_regex.group(1) in bases_dict:
            lematized_words += [bases_dict[ar_regex.group(1)]]
        #er
        elif er_regex and er_regex.group(1) in bases_dict:
            lematized_words += [bases_dict[er_regex.group(1)]]
        #ir
        elif ir_regex and ir_regex.group(1) in bases_dict:
            lematized_words += [bases_dict[ir_regex.group(1)]]
        else:
            lematized_words += [word]

    return lematized_words

if __name__ == "__main__":
    pdf_path = "./Regex/texto1.pdf"
    texto = extract_text_from_pdf(pdf_path)
    #texto = " ".join(corpus)
    print("Conteo del texto:", count_words(texto))
    minusc_text = A_mayusculas(texto)
    print("Conteo después de quitar mayúsculas:", count_words(minusc_text))
    tokenized_text = regex_tokenaizer(minusc_text)
    print("Conteo tokenizado: ", len(tokenized_text))
    compressed_text_list = removedor_stop_words(tokenized_text)

    print("Conteo sin stop words: ", len(compressed_text_list))
    
    lematized_list = regex_lematizer(compressed_text_list)
    
    print(lematized_list)
    print("Conteo lematizado: ", len(lematized_list))
    
    final_text = ""

    for item in compressed_text_list:
        final_text += item + ' '

    with open('./Regex/output.txt', 'w', encoding="utf-8") as file:
        file.write(final_text)