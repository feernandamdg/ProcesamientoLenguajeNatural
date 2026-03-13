#Lematizar : regresar a su raíz
#Cropus: Conjunto de documentos
#Documento: COnjunto de textos

import string
from pypdf import PdfReader
corpus = [
    "Caminando corriendo montando",
    "Esta película fue terrible y aburrida",
    "Los actores actuaron muy bien ",
    "No me gustaron las tramas fueron malas",
    "Excelente dirección y guion brillante"
]

lemmas_excepciones = {
    "fue":"ser",
    "fueron":"ser",
    "soy":"ser",
    "eres":"ser",
    "es":"ser",
    "estaba":"ser",
    "son":"ser",
    "malas":"malo",
    "malos":"malo",
    "buenas":"bueno",
    "peliculas":"pelicula",
    "actuaciones":"actuacion",
    "tramas":"trama",
    "mejores":"bueno",
    "era": "ser",
    "iba": "ir",
    "iban": "ir",
    "tuvo": "tener",
    "dijo" : "decir",
    "dijeron" : "decir",
    "dirán" : "decir",
    "hizo" : "hacer",
    "tuvo" : "tener",
    "árboles" : "árbol",
    "días" : "día"
}

diccionario_ar_gerundio = [
    "hablando", "cantando", "bailando", "saltando", "caminando","mirando", "escuchando", "pensando", "trabajando", "jugando",
    "estudiando", "viajando", "comprando", "pagando", "usando","tocando", "dibujando", "pintando", "imaginando", "recordando",
    "olvidando", "buscando", "llevando", "dejando", "guardando","explicando", "preguntando", "contestando", "cuidando", "ayudando",
    "intentando", "probando", "creando", "deseando", "esperando","logrando", "empezando", "terminando", "cambiando", "mejorando",
    "organizando", "planeando", "preparando", "presentando", "analizando","observando", "comparando", "señalando", "marcando", "considerando"
]

diccionario_ir_gerundio = [
    "viviendo","escribiendo","recibiendo","abriendo","permitiendo","admitiendo","asistiendo","dividiendo","decidiendo","repitiendo",
    "exigiendo","corrigiendo","dirigiendo","eligiendo","siguiendo","persiguiendo","consiguiendo","prohibiendo","imprimiendo","suprimiendo",
    "comprimiendo","expandiendo","confundiendo","difundiendo","fundiendo","hundiendo","interrumpiendo","cumpliendo","descubriendo","cubriendo",
    "inscribiendo","describiendo","suscribiendo","reescribiendo","proscribiendo","incluyendo","concluyendo","excluyendo","atribuyendo","distribuyendo",
    "retribuyendo","construyendo","destruyendo","instruyendo","sustituyendo","instituyendo","constituyendo","restituyendo","destituyendo","intuyendo","caminando"] #Verbos en infinitivo con termicación ir conjugados en gerundio

diccionario_er_gerundio = [
    "comiendo", "bebiendo", "leyendo", "corriendo", "temiendo","vendiendo", "aprendiendo", "entendiendo", "dependiendo", "sorbiendo",
    "mordiendo", "rompiendo", "respondiendo", "perdiendo", "volviendo","resolviendo", "envolviendo", "moviendo", "removiendo", "devolviendo",
    "cociendo", "torciendo", "retorciendo", "creciendo", "ofreciendo","mereciendo", "obedeciendo", "pareciendo", "estableciendo", "perteneciendo",
    "agradeciendo", "desapareciendo", "conociendo", "reconociendo", "traduciendo","produciendo", "reduciendo", "conduciendo", "introduciendo", "deduciendo",
    "seduciendo", "bendiciendo", "convenciendo", "venciendo", "defendiendo","encendiendo", "tendiendo", "extendiendo", "suspendiendo", "pretendiendo"
]

diccionario_ar_preterito = [
    "hablé", "hablaste", "habló", "hablamos", "hablaron",
    "canté", "cantaste", "cantó", "cantamos", "cantaron",
    "bailé", "bailaste", "bailó", "bailamos", "bailaron",
    "caminé", "caminaste", "caminó", "caminamos", "caminaron",
    "salté", "saltaste", "saltó", "saltamos", "saltaron",
    "miré", "miraste", "miró", "miramos", "miraron",
    "escuché", "escuchaste", "escuchó", "escuchamos", "escucharon",
    "trabajé", "trabajaste", "trabajó", "trabajamos", "trabajaron",
    "jugué", "jugaste", "jugó", "jugamos", "jugaron",
    "estudié", "estudiaste", "estudió", "estudiamos", "estudiaron",
    "viajé", "viajaste", "viajó", "viajamos", "viajaron",
    "compré", "compraste", "compró", "compramos", "compraron",
    "pagué", "pagaste", "pagó", "pagamos", "pagaron",
    "usé", "usaste", "usó", "usamos", "usaron",
    "toqué", "tocaste", "tocó", "tocamos", "tocaron",
    "dibujé", "dibujaste", "dibujó", "dibujamos", "dibujaron",
    "pinté", "pintaste", "pintó", "pintamos", "pintaron",
    "olvidé", "olvidaste", "olvidó", "olvidamos", "olvidaron",
    "busqué", "buscaste", "buscó", "buscamos", "buscaron",
    "ayudé", "ayudaste", "ayudó", "ayudamos", "ayudaron",
    "comencé", "comenzaste", "comenzó", "comenzamos", "comenzaron",
    "trabajé","trabajaste", "trabajó", "trabajamos", "trabajaron",
    "expliqué", "explicaste", "explicó", "explicamos", "explicaron",
    "cambié", "cambiaste", "cambió", "cambiamos", "cambiaron",
    "regresé", "regresaste", "regresó", "regresamos", "regresaron",
    "practiqué", "practicaste", "practicó", "practicamos", "practicaron",
    "preparé", "preparaste", "preparó", "preparamos", "prepararon",
    "organicé", "organizaste", "organizó", "organizamos", "organizaron",
    "terminé", "terminaste", "terminó", "terminamos", "terminaron",
    "mejoré", "mejoraste", "mejoró", "mejoramos", "mejoraron",
    "recordé", "recordaste", "recordó", "recordamos", "recordaron",
    "imaginé", "imaginaste", "imaginó", "imaginamos", "imaginaron",
    "pensé", "pensaste", "pensó", "pensamos", "pensaron"
]

diccionario_er_preterito = [
    "comí", "comiste", "comió", "comimos", "comieron",
    "bebí", "bebiste", "bebió", "bebimos", "bebieron",
    "corrí", "corriste", "corrió", "corrimos", "corrieron",
    "leí", "leíste", "leyó", "leímos", "leyeron",
    "temí", "temiste", "temió", "temimos", "temieron",
    "vendí", "vendiste", "vendió", "vendimos", "vendieron",
    "aprendí", "aprendiste", "aprendió", "aprendimos", "aprendieron",
    "entendí", "entendiste", "entendió", "entendimos", "entendieron",
    "dependí", "dependiste", "dependió", "dependimos", "dependieron",
    "sorbí", "sorbiste", "sorbió", "sorbimos", "sorbieron",
    "mordí", "mordiste", "mordió", "mordimos", "mordieron",
    "rompí", "rompiste", "rompió", "rompimos", "rompieron",
    "respondí", "respondiste", "respondió", "respondimos", "respondieron",
    "perdí", "perdiste", "perdió", "perdimos", "perdieron",
    "volví", "volviste", "volvió", "volvimos", "volvieron",
    "resolví", "resolviste", "resolvió", "resolvimos", "resolvieron",
    "moví", "moviste", "movió", "movimos", "movieron",
    "devolví", "devolviste", "devolvió", "devolvimos", "devolvieron",
    "torcí", "torciste", "torció", "torcimos", "torcieron",
    "ofrecí", "ofreciste", "ofreció", "ofrecimos", "ofrecieron",
    "respondí", "respondiste", "respondió", "respondimos", "respondieron",
    "nací", "naciste", "nació", "nacimos", "nacieron"
]

diccionario_ir_preterito = [
    "viví", "viviste", "vivió", "vivimos", "vivieron",
    "escribí", "escribiste", "escribió", "escribimos", "escribieron",
    "recibí", "recibiste", "recibió", "recibimos", "recibieron",
    "abrí", "abriste", "abrió", "abrimos", "abrieron",
    "permití", "permitiste", "permitió", "permitimos", "permitieron",
    "admití", "admitiste", "admitió", "admitimos", "admitieron",
    "asistí", "asististe", "asistió", "asistimos", "asistieron",
    "dividí", "dividiste", "dividió", "dividimos", "dividieron",
    "decidí", "decidiste", "decidió", "decidimos", "decidieron",
    "repetí", "repetiste", "repitió", "repetimos", "repitieron",
    "exigí", "exigiste", "exigió", "exigimos", "exigieron",
    "corrigí", "corregiste", "corrigió", "corregimos", "corrigieron",
    "dirigí", "dirigiste", "dirigió", "dirigimos", "dirigieron",
    "elegí", "elegiste", "eligió", "elegimos", "eligieron",
    "seguí", "seguiste", "siguió", "seguimos", "siguieron","seguía",
    "persiguí", "perseguiste", "persiguió", "perseguimos", "persiguieron",
    "conseguí", "conseguiste", "consiguió", "conseguimos", "consiguieron",
    "prohibí", "prohibiste", "prohibió", "prohibimos", "prohibieron",
    "imprimí", "imprimiste", "imprimió", "imprimimos", "imprimieron",
    "descubrí", "descubriste", "descubrió", "descubrimos", "descubrieron",
]

diccionario_ar_futuro = [
"hablaré","hablarás","hablará","hablaremos","hablarán",
"cantaré","cantarás","cantará","cantaremos","cantarán",
"bailaré","bailarás","bailará","bailaremos","bailarán",
"caminaré","caminarás","caminará","caminaremos","caminarán",
"saltaré","saltarás","saltará","saltaremos","saltarán",
"miraré","mirarás","mirará","miraremos","mirarán",
"escucharé","escucharás","escuchará","escucharemos","escucharán",
"trabajaré","trabajarás","trabajará","trabajaremos","trabajarán",
"jugaré","jugarás","jugará","jugaremos","jugarán",
"estudiaré","estudiarás","estudiará","estudiaremos","estudiarán",
"viajaré","viajarás","viajará","viajaremos","viajarán",
"compraré","comprarás","comprará","compraremos","comprarán",
"pagaré","pagarás","pagará","pagaremos","pagarán",
"usaré","usarás","usará","usaremos","usarán",
"tocaré","tocarás","tocará","tocaremos","tocarán",
"dibujaré","dibujarás","dibujará","dibujaremos","dibujarán",
"pintaré","pintarás","pintará","pintaremos","pintarán",
"buscaré","buscarás","buscará","buscaremos","buscarán",
"ayudaré","ayudarás","ayudará","ayudaremos","ayudarán",
"intentaré","intentarás","intentará","intentaremos","intentarán"
]

diccionario_er_futuro = [
"comeré","comerás","comerá","comeremos","comerán",
"beberé","beberás","beberá","beberemos","beberán",
"correré","correrás","correrá","correremos","correrán",
"leeré","leerás","leerá","leeremos","leerán",
"temeré","temerás","temerá","temeremos","temerán",
"venderé","venderás","venderá","venderemos","venderán",
"aprenderé","aprenderás","aprenderá","aprenderemos","aprenderán",
"entenderé","entenderás","entenderá","entenderemos","entenderán",
"dependeré","dependerás","dependerá","dependeremos","dependerán",
"morderé","morderás","morderá","morderemos","morderán",
"romperé","romperás","romperá","romperemos","romperán",
"responderé","responderás","responderá","responderemos","responderán",
"perderé","perderás","perderá","perderemos","perderán",
"volveré","volverás","volverá","volveremos","volverán",
"resolveré","resolverás","resolverá","resolveremos","resolverán",
"moveré","moverás","moverá","moveremos","moverán",
"devolveré","devolverás","devolverá","devolveremos","devolverán",
"torceré","torcerás","torcerá","torceremos","torcerán",
"ofreceré","ofrecerás","ofrecerá","ofreceremos","ofrecerán",
"temeré","temerás","temerá","temeremos","temerán"
]

diccionario_ir_futuro = [
"viviré","vivirás","vivirá","viviremos","vivirán",
"escribiré","escribirás","escribirá","escribiremos","escribirán",
"recibiré","recibirás","recibirá","recibiremos","recibirán",
"abriré","abrirás","abrirá","abriremos","abrirán",
"permitiré","permitirás","permitirá","permitiremos","permitirán",
"admitiré","admitirás","admitirá","admitiremos","admitirán",
"asistiré","asistirás","asistirá","asistiremos","asistirán",
"dividiré","dividirás","dividirá","dividiremos","dividirán",
"decidiré","decidirás","decidirá","decidiremos","decidirán",
"repetiré","repetirás","repetirá","repetiremos","repetirán",
"exigiré","exigirás","exigirá","exigiremos","exigirán",
"corregiré","corregirás","corregirá","corregiremos","corregirán",
"dirigiré","dirigirás","dirigirá","dirigiremos","dirigirán",
"elegiré","elegirás","elegirá","elegiremos","elegirán",
"seguiré","seguirás","seguirá","seguiremos","seguirán",
"perseguiré","perseguirás","perseguirá","perseguiremos","perseguirán",
"conseguiré","conseguirás","conseguirá","conseguiremos","conseguirán",
"prohibiré","prohibirás","prohibirá","prohibiremos","prohibirán",
"imprimiré","imprimirás","imprimirá","imprimiremos","imprimirán",
"descubriré","descubrirás","descubrirá","descubriremos","descubrirán"
]

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
    print("No se agregó punto.")

  is_number = None

  for i in range(0, len(texto)):
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
        if letra == 'e':
            pass
        if ord(letra) >= 65 and ord(letra) <=90:
            letra = chr(ord(letra) +32)
        letras += letra
    return letras

def removedor_stop_words(tokenized_text):
    stop_words = ["de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","una","su","al","lo","ese"]
    new_text = []
    for item in tokenized_text:
        if item not in stop_words:
            new_text = new_text + [item]
    return new_text

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

def grammar_rules(word):
    n = len(word)
    
    if word[n-4:] == "ando" and word in diccionario_ar_gerundio:
        return word[:n-4] + "ar"
    if word[n-5:] == "iendo" and word in diccionario_ir_gerundio:
        return word[:n-5] + "ir"
    if word[n-5:] == "iendo" and word in diccionario_er_gerundio:
        return word[:n-5] + "er"

    # Pasado -ar
    if word[n-1:] == "é" and word in diccionario_ar_preterito:
        return word[:n-1] + "ar"
    if word[n-4:] == "aste" and word in diccionario_ar_preterito:
        return word[:n-4] + "ar"
    if word[n-1:] == "ó" and word in diccionario_ar_preterito:
        return word[:n-1] + "ar"
    if word[n-4:] == "amos" and word in diccionario_ar_preterito:
        return word[:n-4] + "ar"
    if word[n-4:] == "aron" and word in diccionario_ar_preterito:
        return word[:n-4] + "ar"

    # Pasado -er
    if word[n-1:] == "í" and word in diccionario_er_preterito:
        return word[:n-1] + "er"
    if word[n-2:] == "ía" and word in diccionario_er_preterito:
        return word[:n-2] + "er"
    if word[n-4:] == "iste" and word in diccionario_er_preterito:
        return word[:n-4] + "er"
    if word[n-2:] == "ió" and word in diccionario_er_preterito:
        return word[:n-2] + "er"
    if word[n-4:] == "imos" and word in diccionario_er_preterito:
        return word[:n-4] + "er"
    if word[n-5:] == "ieron" and word in diccionario_er_preterito:
        return word[:n-5] + "er"

    # Pasado -ir
    if word[n-1:] == "í" and word in diccionario_ir_preterito:
        return word[:n-1] + "ir"
    if word[n-2:] == "ía" and word in diccionario_ir_preterito:
        return word[:n-2] + "ir"
    if word[n-4:] == "iste" and word in diccionario_ir_preterito:
        return word[:n-4] + "ir"
    if word[n-2:] == "ió" and word in diccionario_ir_preterito:
        return word[:n-2] + "ir"
    if word[n-4:] == "imos" and word in diccionario_ir_preterito:
        return word[:n-4] + "ir"
    if word[n-5:] == "ieron" and word in diccionario_ir_preterito:
        return word[:n-5] + "ir"

    # Futuro -ar
    if word[-1:] == "é" and word in diccionario_ar_futuro:
        return word[:-1]
    if word[-2:] == "ás" and word in diccionario_ar_futuro:
        return word[:-2]
    if word[-1:] == "á" and word in diccionario_ar_futuro:
        return word[:-1]
    if word[-4:] == "emos" and word in diccionario_ar_futuro:
        return word[:-4]
    if word[-2:] == "án" and word in diccionario_ar_futuro:
        return word[:-2]

    # Futuro -er
    if word[-1:] == "é" and word in diccionario_er_futuro:
        return word[:-1]
    if word[-2:] == "ás" and word in diccionario_er_futuro:
        return word[:-2]
    if word[-1:] == "á" and word in diccionario_er_futuro:
        return word[:-1]
    if word[-4:] == "emos" and word in diccionario_er_futuro:
        return word[:-4]
    if word[-2:] == "án" and word in diccionario_er_futuro:
        return word[:-2]

    # Futuro -ir
    if word[-1:] == "é" and word in diccionario_ir_futuro:
        return word[:-1]
    if word[-2:] == "ás" and word in diccionario_ir_futuro:
        return word[:-2]
    if word[-1:] == "á" and word in diccionario_ir_futuro:
        return word[:-1]
    if word[-4:] == "emos" and word in diccionario_ir_futuro:
        return word[:-4]
    if word[-2:] == "án" and word in diccionario_ir_futuro:
        return word[:-2]
    

def lematizador1(corpus):
    lematized_words = []
    for word in corpus:
        lematized_word = grammar_rules(word)
        if lematized_word == None and word in lemmas_excepciones:
            lematized_word = lemmas_excepciones[word]
        elif lematized_word == None and word not in lemmas_excepciones:
            lematized_word = word
        lematized_words += [lematized_word]
    return lematized_words

def main():
    
    print("1. Texto A")
    print("2. Texto B")
    print("3. Texto C")
    print("4. Texto D")
    opc = input("Selecciona una opción:")
    
    if opc == "1":
        file_path = "lematizacion/textoA.txt"
    if opc == "2":
        file_path = "lematizacion/textoB.txt"
    if opc == "3":
        file_path = "lematizacio/textoC.txt"
    if opc == "4":
        file_path = "lematizacion/textoD.txt"
    
    with open(file_path, 'r',encoding='utf-8') as file:
        texto = file.read()
    
    print("Conteo del texto:", count_words(texto))
    minusc_text = A_mayusculas(texto)S
    print("Conteo después de quitar mayúsculas:", count_words(minusc_text))
    tokenized_text = tokenizador(minusc_text)
    print("Conteo tokenizado: ", len(tokenized_text))
    compressed_text_list = removedor_stop_words(tokenized_text)

    print("Conteo sin stop words: ", len(compressed_text_list))
    
    lematized_list = lematizador1(compressed_text_list)
    
    print(lematized_list)
    print("Conteo lematizado: ", len(lematized_list))
    
    final_text = ""

    for item in compressed_text_list:
        final_text += item + ' '

    with open('output.txt', 'w', encoding="utf-8") as file:
        file.write(final_text)

main()

