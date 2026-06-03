import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer

texto = """
La inteligencia artificial es una disciplina que busca crear sistemas capaces de aprender
y adaptarse a diferentes entornos. En los últimos años, el desarrollo de modelos de lenguaje
ha permitido avances significativos en la comprensión del texto. Estos modelos utilizan
grandes cantidades de datos para identificar patrones y generar resultados coherentes.

El uso de ngramas es una técnica clásica en procesamiento de lenguaje natural que permite
analizar secuencias de palabras. Un modelo basado en ngramas considera un conjunto de palabras
previas para predecir la siguiente palabra en una oración. Aunque es un enfoque simple, puede
ser muy efectivo cuando se combina con redes neuronales.

Las redes neuronales permiten modelar relaciones complejas entre los datos. En el contexto
del lenguaje, pueden capturar dependencias semánticas y sintácticas. Esto es especialmente útil
cuando se trabaja con textos largos o con estructuras gramaticales complejas.

Entrenar un modelo de predicción de palabras implica optimizar los pesos de la red para minimizar
el error entre las predicciones y las palabras reales. Este proceso se realiza mediante algoritmos
de optimización como el descenso de gradiente. Al final, el modelo es capaz de generar texto o
sugerir palabras basadas en el contexto previo.
"""
# ============================
# 1. PREPROCESAMIENTO
# ============================

texto = texto.lower().replace("\n", " ")
tokens = texto.split()

vocab = sorted(set(tokens))

word2idx = {}
idx2word = {}

for i, w in enumerate(vocab):
    word2idx[w] = i
    idx2word[i] = w

vocab_size = len(vocab)

# ============================
# 2. N-GRAMAS
# ============================

n = 3

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

UMBRAL_NGRAMAS = 200  # hiperparámetro

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