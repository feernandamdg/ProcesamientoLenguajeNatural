import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

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
# 2. CO-OCURRENCIA + PCA
# ============================

def construir_concurrencia(vocab, doc_tokenizado, palabra_a_idx, ventana=2):
    n_vocab = len(vocab)
    matriz_conc = np.zeros((n_vocab, n_vocab)) #matriz de nxn 

    i = 0
    while i < len(doc_tokenizado):
        palabra_actual = doc_tokenizado[i]
        if palabra_actual not in palabra_a_idx:
            i += 1
            continue
        idx_actual = palabra_a_idx[palabra_actual] 

        inicio = i - ventana
        if inicio < 0:
            inicio = 0
        fin = i + ventana + 1
        if fin > len(doc_tokenizado):
            fin = len(doc_tokenizado)

        j = inicio
        while j < fin:
            if j != i:
                vecino = doc_tokenizado[j]
                if vecino in palabra_a_idx:
                    idx_vecino = palabra_a_idx[vecino]
                    matriz_conc[idx_actual][idx_vecino] += 1
            j += 1

        i += 1

    return matriz_conc

matriz_conc = construir_concurrencia(vocab, tokens, word2idx, ventana=2)
print("Forma de la matriz de co-ocurrencia:", matriz_conc.shape)

# PCA para reducir dimensionalidad
max_componentes = min(matriz_conc.shape[0], matriz_conc.shape[1])
n_componentes = min(20, max_componentes)

pca = PCA(n_components=n_componentes, random_state=42)
X_pca = pca.fit_transform(matriz_conc)

print("Forma después de PCA:", X_pca.shape)

# ============================
# 3. RED NEURONAL SIMPLE
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
# 4. ENTRENAMIENTO
# ============================

optimizer = tf.optimizers.Adam(learning_rate=0.001)

loss_history = []
epochs = 400

# X: cada palabra representada por su vector PCA
# y: el índice de la misma palabra (la red aprende a recuperar cada palabra desde su representación)
X_tensor = X_pca.astype(np.float32)
y_tensor = np.arange(vocab_size, dtype=np.int32)

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
# 5. PREDICCIÓN
# ============================

def predecir_siguiente(frase):
    frase = frase.lower().replace("\n", " ")
    palabras = frase.split()

    # Sumar los vectores PCA de cada palabra de la frase
    vector_contexto = np.zeros(n_componentes)

    for w in palabras:
        if w not in word2idx:
            return f"La palabra '{w}' no está en el vocabulario."
        vector_contexto += X_pca[word2idx[w]]

    X_nuevo_tensor = vector_contexto.reshape(1, -1).astype(np.float32)

    logits = forward(X_nuevo_tensor)
    probs = tf.nn.softmax(logits).numpy()[0]

    # Excluir las palabras de la frase para no repetirlas
    for w in palabras:
        if w in word2idx:
            probs[word2idx[w]] = 0

    pred_idx = np.argmax(probs)
    return idx2word[pred_idx]


print(predecir_siguiente( "inteligencia"))
print(predecir_siguiente("modelos"))
print(predecir_siguiente("redes"))