import numpy as np
import tensorflow as tf
import spacy
from funcion_preprocesamiento import preprocesar_texto
import warnings
warnings.filterwarnings('ignore')
import os

# 1. Obtiene la ruta de la carpeta "Aletza" (donde está este script)
carpeta_actual = os.path.dirname(__file__)

# 2. Une la carpeta "Aletza" con el nombre del archivo
ruta = os.path.join(carpeta_actual, "cuento.txt")

# 3. Ahora sí, abrirá el archivo sin importar desde dónde ejecutes
with open(ruta, "r", encoding="utf-8") as archivo:
    texto = archivo.read()

# ============================
# 0. LEMATIZACIÓN INVERSA  ← NUEVO
# Se hace ANTES del preprocesamiento para trabajar
# sobre el texto original (con stopwords, signos, etc.)
# spaCy analiza el texto crudo y construye el mapa
# lemma → forma original más frecuente en el texto
# ============================

"""nlp = spacy.load("es_core_news_sm") # para lematización inversa
doc = nlp(texto)

frecuencias = {}
for token in doc:
    if token.is_alpha:
        lemma = token.lemma_.lower()
        forma = token.text.lower()
        frecuencias.setdefault(lemma, {})
        frecuencias[lemma][forma] = frecuencias[lemma].get(forma, 0) + 1

# por cada lemma, quedarse con la forma que más apareció en el texto
lemma_a_original = {
    lemma: max(formas, key=formas.get)
    for lemma, formas in frecuencias.items()
}

print(f"Mapa lemma→original construido: {len(lemma_a_original)} entradas")"""

# ============================
# 1. PREPROCESAMIENTO
# ============================

tokens = preprocesar_texto(texto)
print(f"Cantidad de tokens ({len(tokens)}):")

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
    contexto = tokens[i:i+n]
    target   = tokens[i+1:i+1+n]

    fila_x = [word2idx[w] for w in contexto]
    fila_y = [word2idx[w] for w in target]

    X.append(fila_x)
    y.append(fila_y)

X = np.array(X)
y = np.array(y)

# ============================
# 3. RED NEURONAL
# ============================

modelo = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=64, input_length=n),
    tf.keras.layers.LSTM(128, return_sequences=True),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

modelo.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

modelo.summary()

print("\nEntrenando red neuronal...")
modelo.fit(X, y, epochs=100, verbose=1)

# ============================
# 4. PREDICCIÓN CON LA RED
# ============================

X_texto = []
for fila in X:
    palabras = [idx2word[idx] for idx in fila]
    X_texto.append(" ".join(palabras))

y_texto = []
for fila in y:
    palabras = [idx2word[idx] for idx in fila]
    y_texto.append(" ".join(palabras))

predicciones_idx = modelo.predict(X)
predicciones_idx = np.argmax(predicciones_idx, axis=-1)

y_texto_pred = []
for fila in predicciones_idx:
    palabras = [idx2word[idx] for idx in fila]
    y_texto_pred.append(" ".join(palabras))

print("\nResultados:")
for i in range(5):
    print(f"Contexto:      {X_texto[i]}")
    print(f"Target real:   {y_texto[i]}")
    print(f"Target pred:   {y_texto_pred[i]}")
    print()

# ============================
# 5. EVALUACIÓN
# ============================

correctos = sum(1 for real, pred in zip(y_texto, y_texto_pred) if real == pred)
total     = len(y_texto)
accuracy  = correctos / total
print(f"Exactitud: {correctos}/{total} = {accuracy:.2%}")

# ============================
# 6. RESUMEN POR UMBRAL
# ============================

UMBRAL_PCT = 0.20

probs           = modelo.predict(X)
confianza       = probs.max(axis=-1).mean(axis=1)
ranking         = np.argsort(confianza)[::-1]

tokens_objetivo = max(1, int(len(tokens) * UMBRAL_PCT))
top_contextos   = ranking[:tokens_objetivo]

palabras_importantes = set()
for i in top_contextos:
    for idx in predicciones_idx[i]:
        palabras_importantes.add(idx2word[idx])

tokens_resumen = [t for t in tokens if t in palabras_importantes]

# ============================
# 7. LEMATIZACIÓN INVERSA + CONECTORES  ← NUEVO
# Se aplica AL FINAL sobre los tokens del resumen,
# justo antes de convertirlos a texto legible.
#
# Lematización inversa: lemma → forma original
#   ej. "corpus" (lemma) → "corpus" / "corpora" (la más frecuente en el texto)
#
# Conectores: se insertan cada 8 tokens para dar
#   cohesión al resumen sin alterar el contenido
# ============================

# Simplemente asignamos los tokens filtrados a la variable de salida
resultado = tokens_resumen  

resumen = " ".join(resultado)

print(f"\nPalabras importantes: {len(palabras_importantes)}")
print(f"\nResumen ({len(tokens_resumen)} tokens, ~{UMBRAL_PCT*100:.0f}% del original):")
print(resumen)