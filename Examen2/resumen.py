import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from funcion_preprocesamiento import preprocesar_texto

# texto de 509 palabras
texto = """
El PLN es una rama de la inteligencia artificial que se ocupa de la interacción entre computadoras y humanos utilizando el lenguaje natural. Los corpus lingüísticos son esenciales en este campo, ya que proporcionan los datos necesarios para que las máquinas aprendan y entiendan el lenguaje. Un corpus lingüístico en IA no es más que una base de datos estructurada que contiene ejemplos reales del uso del lenguaje, cuidadosamente recopilados y organizados para su análisis y procesamiento automáticos.
Los corpus son fundamentales para entrenar algoritmos de aprendizaje automático, desarrollar modelos de lenguaje y mejorar la precisión de las aplicaciones de PLN como los chatbots, los asistentes virtuales y los sistemas de traducción automática.
La creación de un corpus lingüístico es un proceso meticuloso que requiere una planificación cuidadosa y una ejecución precisa. Los lingüistas y los ingenieros de datos trabajan juntos para definir la metodología, recopilar textos, y llevar a cabo la anotación de corpus, que es el proceso de agregar información lingüística relevante a los textos. Esta anotación puede incluir aspectos como la estructura gramatical, el significado de las palabras y las entidades nombradas, lo que es crucial para el tratamiento automático del lenguaje.
La anotación de corpus se realiza normalmente a través de herramientas especializadas que permiten etiquetar grandes volúmenes de texto con precisión y coherencia. Este proceso es esencial para la generación de datos anotados que los sistemas de IA pueden utilizar para aprender y mejorar su comprensión del lenguaje.
Los corpus lingüísticos tienen una amplia gama de aplicaciones en el mundo de la inteligencia artificial. En el análisis semántico y pragmático, ayudan a las máquinas a comprender el significado y la intención detrás de las palabras. En los sistemas de conversación, permiten a los chatbots responder de manera coherente y natural a las preguntas de los usuarios. En la traducción automática, los corpus bilingües o multilingües facilitan la creación de sistemas capaces de traducir con precisión entre idiomas.
Un ejemplo notable de la aplicación práctica de los corpus lingüísticos es el proyecto colaborativo entre la Fundación Comillas y LIS Data Solutions. Juntos están creando el primer corpus lingüístico del español de los negocios, un recurso que mejorará significativamente la comunicación empresarial en aplicaciones de IA y en la enseñanza del Español de los Negocios.
Los corpus especializados, como el mencionado corpus del español de los negocios, son fundamentales para abordar necesidades específicas en el campo del PLN. Permiten el desarrollo de aplicaciones de IA con un alto grado de especialización, lo que se traduce en sistemas más precisos y eficaces en sus respectivos dominios.
Los avances recientes en IA y PLN han sido impulsados en gran medida por la disponibilidad de grandes corpus anotados y modelos de lenguaje sofisticados. Estos modelos, entrenados con corpus especializados, están alcanzando niveles de comprensión del lenguaje que eran impensables hace apenas unos años.
Uno de los mayores desafíos en la creación de corpus lingüísticos es la necesidad de recursos multilingües. En un mundo cada vez más globalizado, es esencial que las aplicaciones de IA puedan funcionar en múltiples idiomas. 
"""

# ============================
# 1. PREPROCESAMIENTO
# ============================

tokens = preprocesar_texto(texto)
print (f" cantidad deTokens ({len(tokens)}):")

vocab = sorted(set(tokens))

word2idx = {w: i for i, w in enumerate(vocab)}
idx2word = {i: w for i, w in enumerate(vocab)}

vocab_size = len(vocab)
print(f"Vocabulario ({vocab_size} palabras):")

# ============================
# 2. N-GRAMAS
# ============================

n = 4

X = []
y = []

for i in range(len(tokens) - n):
    contexto = tokens[i:i+n]        # n-grama actual (3 palabras)
    target = tokens[i+1:i+1+n]      # siguiente n-grama (corre una posición)

    fila_x = [word2idx[w] for w in contexto]
    fila_y = [word2idx[w] for w in target]

    X.append(fila_x)
    y.append(fila_y)

X = np.array(X)
y = np.array(y)

# ============================
# 3. TF-IDF
# ============================

X_texto = []

for fila in X:
    palabras_contexto = []

    for idx in fila:
        palabras_contexto.append(idx2word[idx])

    contexto_texto = " ".join(palabras_contexto)
    X_texto.append(contexto_texto)

print("Contextos en texto:")
print(X_texto)

# Convertir los contextos a matriz TF-IDF
vectorizador = TfidfVectorizer()
X_tfidf = vectorizador.fit_transform(X_texto)

print("Forma TF-IDF:", X_tfidf.shape)

# ============================
# 4. SIMILITUD COSENO
# ============================

# Convertir y a texto
y_texto = []

for fila in y:
    palabras_target = [idx2word[idx] for idx in fila]
    y_texto.append(" ".join(palabras_target))

print("Targets en texto:")
print(y_texto)

# Vectorizar y con el MISMO vectorizador de X
y_tfidf = vectorizador.transform(y_texto)

print("Forma TF-IDF y:", y_tfidf.shape)

# Similitud coseno entre cada contexto X[i] y su target y[i]
from sklearn.metrics.pairwise import cosine_similarity

similitudes = cosine_similarity(X_tfidf, y_tfidf)

print("Matriz de similitud (shape):", similitudes.shape)

# Para cada contexto, el índice del n-grama más similar
predicciones = np.argmax(similitudes, axis=1)

print("\nPredicciones (índice del n-grama más similar):")
print(predicciones)

# Mostrar resultados
print("\nResultados:")
for i in range(5):  # primeros 5 ejemplos
    contexto = X_texto[i]
    target_real = y_texto[i]
    target_pred = y_texto[predicciones[i]]
    print(f"Contexto:      {contexto}")
    print(f"Target real:   {target_real}")
    print(f"Target pred:   {target_pred}")
    print()

# ============================
# 5. PERFILES DE N-GRAMAS
# ============================

from collections import defaultdict

# Agrupar índices por n-grama de X
perfiles_sumas = defaultdict(lambda: np.zeros(X_tfidf.shape[1]))
perfiles_conteos = defaultdict(int)

for i, fila in enumerate(X_texto):
    perfiles_sumas[fila] += X_tfidf[i].toarray()[0]
    perfiles_conteos[fila] += 1

# Promediar
perfiles = {}
for ngrama, suma in perfiles_sumas.items():
    perfiles[ngrama] = suma / perfiles_conteos[ngrama]

print(f"Total de perfiles únicos: {len(perfiles)}")

# ============================
# 6. PREDICCIÓN CON PERFILES
# ============================

from sklearn.metrics.pairwise import cosine_similarity

# Convertir perfiles a matriz
perfiles_keys = list(perfiles.keys())
perfiles_matrix = np.array([perfiles[k] for k in perfiles_keys])

# Predecir para los primeros 5 contextos
print("\nPredicciones con perfiles:")
for i in range(5):
    vector_contexto = X_tfidf[i].toarray()
    sims = cosine_similarity(vector_contexto, perfiles_matrix)[0]
    idx_mejor = np.argmax(sims)

    print(f"Contexto:    {X_texto[i]}")
    print(f"Target real: {y_texto[i]}")
    print(f"Predicción:  {perfiles_keys[idx_mejor]}")
    print()

# ============================
# 7. EVALUACIÓN
# ============================

from sklearn.metrics import accuracy_score

y_texto_pred = []

for i in range(len(X_texto)):
    vector_contexto = X_tfidf[i].toarray()
    sims = cosine_similarity(vector_contexto, perfiles_matrix)[0]
    idx_mejor = np.argmax(sims)
    y_texto_pred.append(perfiles_keys[idx_mejor])

# Exactitud: ¿cuántas veces predijo el n-grama correcto?
correctos = sum(1 for real, pred in zip(y_texto, y_texto_pred) if real == pred)
total = len(y_texto)
accuracy = correctos / total

print(f"Exactitud: {correctos}/{total} = {accuracy:.2%}")

# Similitud promedio entre predicción y target real
sims_diagonales = cosine_similarity(X_tfidf, y_tfidf).diagonal()
print(f"Similitud coseno promedio (contexto vs target real): {sims_diagonales.mean():.4f}")

# ============================
# 8. RESUMEN POR UMBRAL DE N-GRAMAS
# ============================

UMBRAL_NGRAMAS = 120  # hiperparámetro

# Calcular score de cada n-grama (similitud promedio con todos los contextos)
scores = cosine_similarity(perfiles_matrix, perfiles_matrix).mean(axis=1)

# Rankear perfiles por score
ranking = np.argsort(scores)[::-1]

# Seleccionar los top-N según umbral
top_ngramas = [perfiles_keys[i] for i in ranking[:UMBRAL_NGRAMAS]]

print(f"Top {UMBRAL_NGRAMAS} n-gramas seleccionados:")
print(top_ngramas[:10], "...")  # muestra solo los primeros 10

# Reconstruir resumen: conservar solo tokens que aparecen en los top n-gramas
palabras_importantes = set()
for ngrama in top_ngramas:
    for palabra in ngrama.split():
        palabras_importantes.add(palabra)

# Filtrar el texto original conservando palabras importantes
tokens_resumen = [t for t in tokens if t in palabras_importantes]
resumen = " ".join(tokens_resumen)

print(f"\nPalabras importantes: {len(palabras_importantes)}")
print(f"\nResumen ({len(tokens_resumen)} tokens):")
print(resumen)