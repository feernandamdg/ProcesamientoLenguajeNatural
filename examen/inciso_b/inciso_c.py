"""
Inciso C) Tokenización + Remoción de stopwords + Lematización
Entrada : examen/biologia.txt
Salida  : examen/output_inciso_c.pdf  (se sobreescribe en cada ejecución)
"""
 
import string
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
 

# Diccionarios de lematización (estilo hecho antes)
 
lemmas_excepciones = {
    "fue": "ser", "fueron": "ser", "soy": "ser", "eres": "ser",
    "es": "ser", "son": "ser", "era": "ser", "estaba": "ser",
    "está": "ser", "están": "ser",
    "iba": "ir", "iban": "ir",
    "tuvo": "tener", "tienen": "tener", "tenía": "tener",
    "dijo": "decir", "dijeron": "decir",
    "hizo": "hacer", "hacen": "hacer",
    "células": "célula", "proteínas": "proteína", "enzimas": "enzima",
    "moléculas": "molécula", "organismos": "organismo",
    "reacciones": "reacción", "funciones": "función",
    "estructuras": "estructura", "membranas": "membrana",
    "tejidos": "tejido", "órganos": "órgano", "sistemas": "sistema",
    "procesos": "proceso", "tipos": "tipo", "grupos": "grupo",
    "niveles": "nivel", "factores": "factor", "genes": "gen",
    "árboles": "árbol", "días": "día", "años": "año",
    "malas": "malo", "buenos": "bueno", "grandes": "grande",
    "diferentes": "diferente", "importantes": "importante",
    "principales": "principal", "naturales": "natural",
}
 
gerundios_ar = [
    "caminando","trabajando","estudiando","usando","observando","realizando",
    "formando","generando","regulando","transportando","produciendo",
    "enviando","llevando","tomando","pasando","creando","aumentando",
    "disminuyendo","controlando","manteniendo","activando","sintetizando",
    "procesando","almacenando","liberando","adaptando","respirando"
]
gerundios_er = [
    "comiendo","bebiendo","corriendo","creciendo","respondiendo","dependiendo",
    "perdiendo","volviendo","comprendiendo","estableciendo","obteniendo",
    "reconociendo","descomponiendo"
]
gerundios_ir = [
    "viviendo","escribiendo","recibiendo","dividiendo","decidiendo","siguiendo",
    "repitiendo","dirigiendo","eligiendo","construyendo","destruyendo",
    "contribuyendo","distribuyendo","incluyendo","excluyendo"
]
 
preterito_ar = [
    "habló","hablaron","caminó","caminaron","trabajó","trabajaron",
    "estudió","estudiaron","usó","usaron","observó","observaron",
    "formó","formaron","generó","generaron","reguló","regularon",
    "creó","crearon","aumentó","aumentaron","controló","controlaron",
    "activó","activaron","adaptó","adaptaron","respiró","respiraron"
]
preterito_er = [
    "comió","comieron","bebió","bebieron","corrió","corrieron",
    "creció","crecieron","respondió","respondieron","dependió","dependieron",
    "perdió","perdieron","volvió","volvieron","obtuvo","obtuvieron",
    "estableció","establecieron","reconoció","reconocieron"
]
preterito_ir = [
    "vivió","vivieron","escribió","escribieron","recibió","recibieron",
    "dividió","dividieron","decidió","decidieron","siguió","siguieron",
    "dirigió","dirigieron","eligió","eligieron","construyó","construyeron",
    "distribuyó","distribuyeron","contribuyó","contribuyeron"
]
 
 
# Funciones hechas anteriormente
 
def tokenizador(texto):
    token = ""
    tokens = []
    withes      = string.whitespace
    delimiters  = string.whitespace + string.punctuation
    numbers     = string.digits
    not_letters = delimiters + numbers
 
    if texto[-1] not in delimiters:
        texto += '.'
 
    is_number = None
    for ch in texto:
        if ch == '.' or ch in withes:
            if token:
                tokens.append(token)
            token = ""
            is_number = None
        elif token == "" and ch not in delimiters:
            is_number = True if ch in numbers else (False if ch not in not_letters else None)
            token += ch
        elif ch not in not_letters and is_number:
            token = ch
            is_number = False
        elif (ch in numbers and is_number) or (ch not in not_letters and not is_number):
            token += ch
 
    return tokens
 
 
def a_minusculas(texto):
    resultado = ""
    for letra in texto:
        if 65 <= ord(letra) <= 90:
            letra = chr(ord(letra) + 32)
        resultado += letra
    return resultado
 
 
def removedor_stop_words(tokens):
    stop_words = {
        "de","la","el","en","y","a","los","del","se","las","por","un",
        "para","con","una","su","al","lo","que","es","son","no","o",
        "sus","este","esta","estos","estas","también","más","como",
        "pero","si","ya","entre","sobre","hacia","desde","hasta",
        "muy","así","hay","cada","todo","todos","toda","todas",
        "otro","otra","otros","otras","ser","está","han","fue",
        "sin","ante","bajo","tras","durante","mediante","dentro",
        "fuera","mismo","misma","cuando","donde","porque","aunque",
        "les","nos","me","te","le","cual","cuales","esto","eso",
        "aquí","allí","entonces","además","sin","solo","sólo"
    }
    return [t for t in tokens if t not in stop_words]
 
 
# Lematizador (estilo grammar_rules hecho anteriormente)
 
def grammar_rules(word):
    n = len(word)
 
    # Gerundios
    if word[n-4:] == "ando" and word in gerundios_ar:
        return word[:n-4] + "ar"
    if word[n-5:] == "iendo" and word in gerundios_er:
        return word[:n-5] + "er"
    if word[n-5:] == "iendo" and word in gerundios_ir:
        return word[:n-5] + "ir"
 
    # Pretéritos -ar
    if word[n-1:] == "ó" and word in preterito_ar:
        return word[:n-1] + "ar"
    if word[n-4:] == "aron" and word in preterito_ar:
        return word[:n-4] + "ar"
 
    # Pretéritos -er
    if word[n-2:] == "ió" and word in preterito_er:
        return word[:n-2] + "er"
    if word[n-5:] == "ieron" and word in preterito_er:
        return word[:n-5] + "er"
 
    # Pretéritos -ir
    if word[n-2:] == "ió" and word in preterito_ir:
        return word[:n-2] + "ir"
    if word[n-5:] == "ieron" and word in preterito_ir:
        return word[:n-5] + "ir"
 
    return None
 
 
def lematizador(tokens): # reutilizado
    resultado = []
    for word in tokens:
        lema = grammar_rules(word)
        if lema is None:
            lema = lemmas_excepciones.get(word, word)
        resultado.append(lema)
    return resultado
 
 
# Guardar en PDF (sobreescribe siempre)
 
def guardar_pdf(tokens_orig, tokens_sw, lemas, ruta):
    doc = SimpleDocTemplate(ruta, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
 
    estilo_titulo = ParagraphStyle('T', parent=styles['Title'], fontSize=15, spaceAfter=4,
                                   textColor=colors.HexColor('#1a1a2e'))
    estilo_sub    = ParagraphStyle('S', parent=styles['Heading2'], fontSize=11, spaceBefore=14,
                                   spaceAfter=4, textColor=colors.HexColor('#16213e'))
    estilo_meta   = ParagraphStyle('M', parent=styles['Normal'], fontSize=8,
                                   textColor=colors.grey, spaceAfter=16)
    estilo_normal = styles['Normal']
 
    story = []
    story.append(Paragraph("Inciso C — Procesamiento de Lenguaje Natural", estilo_titulo))
    story.append(Paragraph("Tokenización · Remoción de stopwords · Lematización", estilo_meta))
 
    # Tabla resumen
    stats = [
        ["Etapa",          "Tokens"],
        ["Tokenización",   str(len(tokens_orig))],
        ["Sin stopwords",  str(len(tokens_sw))],
        ["Lematización",   str(len(lemas))],
        ["Reducción total",f"{round((1 - len(lemas)/max(len(tokens_orig),1))*100, 1)} %"],
    ]
    tabla = Table(stats, colWidths=[3*inch, 1.5*inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#16213e')),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.whitesmoke, colors.white]),
        ('GRID',          (0,0), (-1,-1), 0.4, colors.lightgrey),
        ('ALIGN',         (1,0), (1,-1), 'CENTER'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tabla)
 
    # Secciones de texto procesado
    secciones = [
        ("1. Tokens (tokenización)",  tokens_orig),
        ("2. Tokens sin stopwords",   tokens_sw),
        ("3. Lemas (lematización)",   lemas),
    ]
    for titulo_sec, lista in secciones:
        story.append(Spacer(1, 8))
        story.append(Paragraph(titulo_sec, estilo_sub))
        story.append(Paragraph(" · ".join(lista), estilo_normal))
 
    doc.build(story)
    print(f"PDF guardado en: {ruta}")
 

# Main
def main():
    ruta_entrada = r"examen\biologia.txt"
    ruta_salida  = r"examen\output_inciso_c.pdf"   # se sobreescribe en cada ejecución
 
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        texto = f.read()
 
    print(f"Palabras en texto original : {sum(1 for w in texto.split())}")
 
    texto_minus = a_minusculas(texto)
    tokens      = tokenizador(texto_minus)
    print(f"Tokens tras tokenización   : {len(tokens)}")
 
    tokens_sw   = removedor_stop_words(tokens)
    print(f"Tokens sin stopwords       : {len(tokens_sw)}")
 
    lemas       = lematizador(tokens_sw)
    print(f"Lemas obtenidos            : {len(lemas)}")
 
    guardar_pdf(tokens, tokens_sw, lemas, ruta_salida)
 
main()