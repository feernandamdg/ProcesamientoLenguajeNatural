# Usamos encoding='utf-8' para asegurar que los acentos y la letra 'ñ' se lean correctamente.

with open('archivo1.txt', 'r', encoding='utf-8') as f:
    doc1 = f.read()

with open('archivo2.txt', 'r', encoding='utf-8') as f:
    doc2 = f.read()

with open('archivo3.txt', 'r', encoding='utf-8') as f:
    doc3 = f.read()

# Guardamos los textos leídos en la lista para pasar al preprocesamiento
documentos_crudos = [doc1, doc2, doc3]

print("¡Archivos leídos con éxito!")
print("Caracteres en Doc 1:", len(doc1))
print("Caracteres en Doc 2:", len(doc2))
print("Caracteres en Doc 3:", len(doc3))
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#limpieza
def limpiar_y_tokenizar(texto):
    palabras = []
    palabra_actual = ""
    
    for caracter in texto:
        codigo = ord(caracter)
        
        # Letras mayúsculas
        if codigo >= 65 and codigo <= 90:
            palabra_actual = palabra_actual + chr(codigo + 32)
            
        # Letras minúsculas (a-z)
        elif codigo >= 97 and codigo <= 122:
            palabra_actual = palabra_actual + caracter
            
        # Vocales con acento mayúsculas 
        elif codigo == 193 or codigo == 201 or codigo == 205 or codigo == 211 or codigo == 218 or codigo == 209:
            palabra_actual = palabra_actual + chr(codigo + 32)
            
        # Vocales con acento minúsculas
        elif codigo == 225 or codigo == 233 or codigo == 237 or codigo == 243 or codigo == 250 or codigo == 241:
            palabra_actual = palabra_actual + caracter
            
        #números (0-9) -> Ignorar (Elimina ruido numérico)
        elif codigo >= 48 and codigo <= 57:
            continue
            
        #Cualquier otro caracter (espacios, saltos de línea, puntuación) funciona como separador
        else:
            if len(palabra_actual) > 0:
                palabras.append(palabra_actual)
                palabra_actual = ""
                
    #agregar la última palabra si el texto no terminó con un separador
    if len(palabra_actual) > 0:
        palabras.append(palabra_actual)
        
    return palabras

#pasar los 3 docs
documentos_tokenizados = []
for doc in documentos_crudos:
    documentos_tokenizados.append(limpiar_y_tokenizar(doc))

#-----------------------------------------------------------------------------------------------------------------------------
#INCISO A

import math

num_documentos = len(documentos_tokenizados)
vocabulario = []

#construir el vocabulario único
for doc in documentos_tokenizados:
    for palabra in doc:
        existe = False
        for v in vocabulario:
            if v == palabra:
                existe = True
                break
        if not existe:
            vocabulario.append(palabra)

#calcular matriz TF-IDF
matriz_tfidf = {}

for palabra in vocabulario:
    datos_palabra = []
    
    #calcular en cuántos documentos aparece la palabra para el IDF
    docs_con_palabra = 0
    for doc in documentos_tokenizados:
        aparece = False
        for p in doc:
            if p == palabra:
                aparece = True
                break
        if aparece:
            docs_con_palabra = docs_con_palabra + 1
            
    #calcular IDF
    idf = math.log10(num_documentos / docs_con_palabra)
    
    #calcular TF y TF-IDF para cada documento
    for doc in documentos_tokenizados:
        total_palabras_doc = len(doc)
        frecuencia_palabra = 0
        
        for p in doc:
            if p == palabra:
                frecuencia_palabra = frecuencia_palabra + 1
                
        tf = frecuencia_palabra / total_palabras_doc
        tf_idf = tf * idf
        
        datos_palabra.append((tf, idf, tf_idf))
        
    matriz_tfidf[palabra] = datos_palabra

#imprimir una muestra de la matriz (primeras 10)
print("--- INCISO A: MATRIZ TF-IDF (Muestra) ---")
print("Formato: Palabra -> DOC1(TF, IDF, TF-IDF) | DOC2(TF, IDF, TF-IDF) | DOC3(TF, IDF, TF-IDF)")
contador = 0
for palabra in vocabulario:
    if contador < 10:
        datos = matriz_tfidf[palabra]
        fila = palabra + " -> "
        for i in range(num_documentos):
            fila = fila + "DOC" + str(i+1) + ":(" + str(round(datos[i][0], 4)) + ", " + str(round(datos[i][1], 4)) + ", " + str(round(datos[i][2], 4)) + ") | "
        print(fila)
        contador = contador + 1




#---------------------------------------------------------------------------------------------------------------
#INCISO B
palabras_eliminadas = []
matriz_limpia = {}

for palabra in vocabulario:
    datos = matriz_tfidf[palabra]
    
    #verificamos el IDF. Como el IDF es igual para todos los documentos (sirve solo con laprimer tupla)
    idf_valor = datos[0][1]
    
    if idf_valor == 0.0:
        palabras_eliminadas.append(palabra)
    else:
        matriz_limpia[palabra] = datos

print("--- INCISO B: PALABRAS ELIMINADAS (TF-IDF = 0) ---")
print("Total de palabras eliminadas:", len(palabras_eliminadas))
print("Lista de palabras eliminadas:")
for p in palabras_eliminadas:
    print("- " + p)

print("\nComportamiento observado:")
print("El valor TF (frecuencia) de estas palabras es alto porque son conectores comunes (de, la, el, en).")
print("Sin embargo, al aparecer en TODOS los documentos, su IDF se vuelve Log(3/3) = Log(1) = 0.")
print("Al multiplicar TF * 0, su peso final es 0, lo que significa que no sirven para diferenciar de qué trata un documento frente a los demás.")


#------------------------------------------------------------------------------------------------------------------------------------
#INCISO C
print("--- INCISO C: PALABRAS MÁS SIGNIFICATIVAS POR DOCUMENTO ---")

for i in range(num_documentos):
    palabra_top = ""
    max_tfidf = -1.0
    tf_top = 0.0
    idf_top = 0.0
    
    #buscamos manualmente el valor máximo
    for palabra in matriz_limpia:
        datos = matriz_limpia[palabra]
        tfidf_actual = datos[i][2]
        
        if tfidf_actual > max_tfidf:
            max_tfidf = tfidf_actual
            palabra_top = palabra
            tf_top = datos[i][0]
            idf_top = datos[i][1]
            
    print("\nDOCUMENTO " + str(i+1) + ":")
    print("Palabra más significativa: '" + palabra_top + "'")
    print("TF: " + str(round(tf_top, 4)) + " (Aparece frecuentemente en ESTE documento)")
    print("IDF: " + str(round(idf_top, 4)) + " (Es rara en los OTROS documentos)")
    print("TF-IDF Final: " + str(round(max_tfidf, 4)))

print("\nComportamiento observado:")
print("Las palabras más significativas tienen un TF alto (se repiten mucho en su propio texto) y un IDF alto (no aparecen en los demás textos).")
print("Esto demuestra que el TF-IDF extrae exitosamente los 'temas centrales' o palabras clave de cada texto ignorando la paja.")




