import string
import textwrap

# Texto original de biología
texto_biologia = """La biología es la ciencia que estudia los seres vivos y los procesos que permiten su funcionamiento, crecimiento y reproducción. Desde organismos microscópicos hasta ecosistemas completos, la biología busca comprender cómo interactúan las diferentes formas de vida y cuáles son los mecanismos que regulan su existencia.
Una de las unidades fundamentales de la vida es la célula. Todos los organismos vivos están formados por una o más células, y cada célula contiene estructuras especializadas llamadas orgánulos. Entre los orgánulos más importantes se encuentran el núcleo, las mitocondrias, el retículo endoplasmático y el aparato de Golgi.
El núcleo celular contiene el ADN, que es la molécula responsable de almacenar la información genética. El ADN está formado por secuencias de nucleótidos que codifican proteínas. Estas proteínas participan en prácticamente todos los procesos biológicos, desde la digestión hasta la replicación celular.
Uno de los procesos más importantes en biología celular es la replicación del ADN. Durante este proceso, la molécula de ADN se duplica para que cada célula hija reciba una copia completa del material genético. Este proceso ocurre antes de la división celular y es esencial para el crecimiento y la reparación de tejidos.
La división celular puede ocurrir mediante dos procesos principales: mitosis y meiosis. La mitosis es el proceso mediante el cual una célula se divide para formar dos células hijas genéticamente idénticas. Este proceso es fundamental para el crecimiento de los organismos multicelulares.
Por otro lado, la meiosis es un tipo especial de división celular que produce células reproductivas llamadas gametos. Durante la meiosis se generan cuatro células hijas que contienen la mitad del material genético de la célula original. Este mecanismo permite la diversidad genética en las poblaciones.
Las mitocondrias, conocidas como las centrales energéticas de la célula, participan en la producción de ATP. El ATP es una molécula que almacena energía y que es utilizada por la célula para realizar diferentes funciones metabólicas. Este proceso ocurre mediante la respiración celular, que incluye etapas como la glucólisis, el ciclo de Krebs y la cadena de transporte de electrones.
Además de los procesos celulares, la biología también estudia la interacción entre organismos y su entorno. Estas interacciones se analizan en el campo de la ecología. Los ecosistemas están formados por comunidades de organismos que interactúan entre sí y con factores abióticos como la temperatura, el agua y la luz solar.
Los organismos dentro de un ecosistema pueden ocupar diferentes niveles tróficos. Los productores, como las plantas y las algas, obtienen energía mediante la fotosíntesis. Los consumidores se alimentan de otros organismos, mientras que los descomponedores reciclan materia orgánica y devuelven nutrientes al suelo.
Otro concepto importante en biología es la evolución. La teoría de la evolución, propuesta por Charles Darwin, establece que las especies cambian a lo largo del tiempo mediante un proceso llamado selección natural. En este proceso, los individuos con características favorables tienen mayor probabilidad de sobrevivir y reproducirse.
La biología moderna combina conocimientos de genética, bioquímica y biología molecular para comprender los procesos que sustentan la vida. Gracias a estos avances, hoy es posible desarrollar medicamentos, mejorar cultivos agrícolas y estudiar enfermedades a nivel molecular."""

# --- Lematizar : regresar a su raíz ---
# --- Corpus: Conjunto de documentos ---
# --- Documento: Conjunto de textos ---

# diccionarios
lemmas_excepciones = {
    "fue":"ser", "fueron":"ser", "soy":"ser", "eres":"ser", "es":"ser", 
    "estaba":"ser", "son":"ser", "malas":"malo", "malos":"malo", 
    "buenas":"bueno", "peliculas":"pelicula", "actuaciones":"actuacion", 
    "tramas":"trama", "mejores":"bueno", "era": "ser", "iba": "ir", 
    "iban": "ir", "tuvo": "tener", "dijo" : "decir", "dijeron" : "decir", 
    "dirán" : "decir", "hizo" : "hacer", "árboles" : "árbol", "días" : "día",
    "seres": "ser", "vivos": "vivo", "procesos": "proceso", "ecosistemas": "ecosistema",
    "estructuras": "estructura", "llamadas": "llamado", "orgánulos": "orgánulo",
    "mitocondrias": "mitocondria", "nucleótidos": "nucleótido", "proteínas": "proteína",
    "tejidos": "tejido", "células": "célula", "gametos": "gameto", "poblaciones": "población",
    "centrales": "central", "energéticas": "energético", "funciones": "función",
    "metabólicas": "metabólico", "etapas": "etapa", "interacciones": "interacción",
    "factores": "factor", "abióticos": "abiótico", "niveles": "nivel",
    "tróficos": "trófico", "productores": "productor", "plantas": "planta",
    "algas": "alga", "consumidores": "consumidor", "descomponedores": "descomponedor",
    "nutrientes": "nutriente", "especies": "especie", "características": "característica",
    "favorables": "favorable", "individuos": "individuo", "conocimientos": "conocimiento",
    "avances": "avance", "medicamentos": "medicamento", "cultivos": "cultivo",
    "agrícolas": "agrícola", "enfermedades": "enfermedad", "formas": "forma",
    "mecanismos": "mecanismo", "completos": "completo", "organismos" : "organismo", 
    "especializadas": "especializada", "importantes": "importante", "secuencias": "secuencia", 
    "todos": "todo", "moleculares": "molecular", "conocidas": "conocida", "formados": "formado",
}

# --- Diccionarios de tiempos verbales ---
diccionario_ar_gerundio = ["hablando", "cantando", "estudiando", "interactuando", "participando"]
diccionario_ir_gerundio = ["viviendo", "escribiendo", "dividiendo", "ocurriendo"]
diccionario_er_gerundio = ["comiendo", "bebiendo", "comprendiendo", "conteniendo"]

diccionario_ar_preterito = ["hablé", "cantó", "estudió"]
diccionario_er_preterito = ["comí", "bebió", "comprendió"]
diccionario_ir_preterito = ["viví", "escribió", "ocurrió"]

diccionario_ar_futuro = ["hablaré", "cantará", "estudiará"]
diccionario_er_futuro = ["comeré", "beberá", "comprenderá"]
diccionario_ir_futuro = ["viviré", "escribirá", "ocurrirá"]

diccionario_ar_presente = [
    "estudia", "estudian", "regula", "regulan", "codifica", "codifican", 
    "participa", "participan", "duplica", "duplican", "genera", "generan",
    "almacena", "almacenan", "utiliza", "utilizan", "realiza", "realizan",
    "analiza", "analizan", "ocupa", "ocupan", "recicla", "reciclan",
    "cambia", "cambian", "combina", "combinan", "sustenta", "sustentan",
    "interactúa", "interactúan", "busca", "buscan"
]

diccionario_er_presente = [
    "comprende", "comprenden", "contiene", "contienen", "depende", "dependen",
    "establece", "establecen", "obtiene", "obtienen", "devuelve", "devuelven"
]

diccionario_ir_presente = [
    "ocurre", "ocurren", "divide", "dividen", "permite", "permiten", 
    "recibe", "reciben", "produce", "producen"
]

# 1. Función A_mayusculas (Sin .lower(), usando ASCII)
def A_mayusculas(texto):
    result = ""
    for char in texto:
        val = ord(char)
        if 65 <= val <= 90:
            result += chr(val + 32)
        elif val == 193: result += chr(225) # Á -> á
        elif val == 201: result += chr(233) # É -> é
        elif val == 205: result += chr(237) # Í -> í
        elif val == 211: result += chr(243) # Ó -> ó
        elif val == 218: result += chr(250) # Ú -> ú
        elif val == 209: result += chr(241) # Ñ -> ñ
        else:
            result += char
    return result

# 2. Tokenizador MANUAL (Sin librería RE)
def tokenizador(texto):
    tokens = []
    token_actual = ""
    # Definimos qué caracteres separan palabras
    separadores = string.whitespace + string.punctuation + "¿¡"
    
    for char in texto:
        if char not in separadores:
            token_actual += char
        else:
            if token_actual != "":
                tokens.append(token_actual)
                token_actual = ""
    
    # Agregar el último token si quedó algo pendiente
    if token_actual != "":
        tokens.append(token_actual)
        
    return tokens

# 3. Remover Stop Words
def removedor_stop_words(tokenized_text):
    stop_words = ["de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","una","su","al","lo","ese","desde","hasta","como","más","cada","entre","este","son","estas","uno","dos","otro","lado","sus","sí"]
    new_text = []
    for item in tokenized_text:
        if item not in stop_words:
            new_text.append(item)
    return new_text

# 4. Reglas Gramaticales
def grammar_rules(word):
    n = len(word)
    if n < 3: return None

    # --- GERUNDIO ---
    if word[n-4:] == "ando" and word in diccionario_ar_gerundio: return word[:n-4] + "ar"
    if word[n-5:] == "iendo" and word in diccionario_ir_gerundio: return word[:n-5] + "ir"
    if word[n-5:] == "iendo" and word in diccionario_er_gerundio: return word[:n-5] + "er"

    # --- PRESENTE ---
    if word[n-1:] == "a" and word in diccionario_ar_presente: return word[:n-1] + "ar"
    if word[n-2:] == "an" and word in diccionario_ar_presente: return word[:n-2] + "ar"
    if word[n-1:] == "e" and word in diccionario_er_presente: return word[:n-1] + "er"
    if word[n-2:] == "en" and word in diccionario_er_presente: return word[:n-2] + "er"
    if word[n-1:] == "e" and word in diccionario_ir_presente: return word[:n-1] + "ir"
    if word[n-2:] == "en" and word in diccionario_ir_presente: return word[:n-2] + "ir"

    # --- PASADO y FUTURO ---
    # (Se mantienen las lógicas de corte previas simplificadas para el ejemplo)
    if word[n-1:] == "é" and (word in diccionario_ar_preterito or word in diccionario_ar_futuro): return word[:n-1] + "ar"
    if word[n-1:] == "ó" and word in diccionario_ar_preterito: return word[:n-1] + "ar"

    return None

# 5. Lematizador
def lematizador1(corpus):
    lematized_words = []
    for word in corpus:
        lematized_word = grammar_rules(word)
        if lematized_word == None and word in lemmas_excepciones:
            lematized_word = lemmas_excepciones[word]
        elif lematized_word == None and word not in lemmas_excepciones:
            lematized_word = word
        lematized_words.append(lematized_word)
    return lematized_words

def main():
    print("Procesando texto de Biología...")
    
    minusc_text = A_mayusculas(texto_biologia)
    tokenized_text = tokenizador(minusc_text)
    compressed_text_list = removedor_stop_words(tokenized_text)
    lematized_list = lematizador1(compressed_text_list)
    
    final_text = " ".join(lematized_list)
    lineas_texto = textwrap.wrap(final_text, width=80)
    
    with open('nlp_resultado_final.txt', 'w', encoding="utf-8") as file:
        file.write("Resultado de NLP (Tokenizacion manual, Stopwords y Lematizacion)\n")
        file.write("-" * 70 + "\n\n")
        for linea in lineas_texto:
            file.write(linea + '\n')
            
    print("¡Proceso completado! Archivo 'nlp_resultado_final.txt' guardado.")

main()
