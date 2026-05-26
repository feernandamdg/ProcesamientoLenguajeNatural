import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

# ======================================================
# B) PREDICCIÓN DE LA SIGUIENTE PALABRA CON N-GRAMAS
# ======================================================

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

for i in range(len(tokens) - n + 1):
    contexto = tokens[i:i+n-1]
    target = tokens[i+n-1]

    fila = []
    for w in contexto:
        fila.append(word2idx[w])

    X.append(fila)
    y.append(word2idx[target])

X = np.array(X)
y = np.array(y)

# ============================
# 3. TF-IDF + PCA
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

# PCA requiere matriz densa
X_tfidf_dense = X_tfidf.toarray()

# Número de componentes reducido
max_componentes = min(X_tfidf_dense.shape[0], X_tfidf_dense.shape[1])
n_componentes = min(20, max_componentes)

pca = PCA(n_components=n_componentes, random_state=42)
X_pca = pca.fit_transform(X_tfidf_dense)

print("Forma después de PCA:", X_pca.shape)

# ============================
# 4. RED NEURONAL SIMPLE
# ============================

input_size = X_pca.shape[1]
hidden_size = 32
output_size = vocab_size

W1 = tf.Variable(tf.random.normal([input_size, hidden_size], stddev=0.1))
b1 = tf.Variable(tf.zeros([hidden_size]))

W2 = tf.Variable(tf.random.normal([hidden_size, output_size], stddev=0.1))
b2 = tf.Variable(tf.zeros([output_size]))


def forward(X):
    h = tf.nn.relu(tf.matmul(X, W1) + b1)
    logits = tf.matmul(h, W2) + b2
    return logits

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# ============================
# 5. ENTRENAMIENTO
# ============================

optimizer = tf.optimizers.Adam(learning_rate=0.01)

loss_history = []
epochs = 200

X_tensor = X_pca.astype(np.float32)
y_tensor = y.astype(np.int32)

for epoch in range(epochs):

    with tf.GradientTape() as tape:
        logits = forward(X_tensor)
        loss = loss_fn(y_tensor, logits)

    grads = tape.gradient(loss, [W1, b1, W2, b2])
    optimizer.apply_gradients(zip(grads, [W1, b1, W2, b2]))

    loss_history.append(loss.numpy())

    if epoch % 20 == 0:
        print("Epoch:", epoch, "Loss:", float(loss.numpy()))


# ============================
# 6. PREDICCIÓN
# ============================

def predecir_siguiente(frase):
    frase = frase.lower().replace("\n", " ")
    palabras = frase.split()

    contexto = palabras[-(n-1):]

    if len(contexto) < n - 1:
        return "Faltan palabras para formar el contexto."

    contexto_texto = " ".join(contexto)

    X_nuevo_tfidf = vectorizador.transform([contexto_texto])
    X_nuevo_pca = pca.transform(X_nuevo_tfidf.toarray())

    X_nuevo_tensor = X_nuevo_pca.astype(np.float32)

    logits = forward(X_nuevo_tensor)
    probs = tf.nn.softmax(logits).numpy()[0]

    pred_idx = np.argmax(probs)

    return idx2word[pred_idx]


print(predecir_siguiente("la inteligencia"))
print(predecir_siguiente("modelos de"))
print(predecir_siguiente("redes neuronales"))