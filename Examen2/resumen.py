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