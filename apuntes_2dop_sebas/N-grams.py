import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# ======================================================
# A) DETECTOR DE IDIOMAS CON N-GRAMAS DE CARACTERES
# ======================================================

def limpiar_texto(texto):
    texto = texto.lower()
    texto = texto.replace("\n", " ")
    return texto


def obtener_ngramas_caracteres(texto,n):
    texto = limpiar_texto(texto)
    texto = texto.replace(" ", "_")

    ngramas = []

    for i in range(len(texto) - n + 1):
        ngrama = texto[i:i+n]
        ngramas.append(ngrama)

    return ngramas


def perfil_ngramas(texto, n=3, top=200):
    ngramas = obtener_ngramas_caracteres(texto, n)

    frecuencias = {}

    for ng in ngramas:
        if ng not in frecuencias:
            frecuencias[ng] = 0
        frecuencias[ng] += 1

    ordenados = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)

    perfil = {}

    for rango, dato in enumerate(ordenados[:top]):
        ngrama = dato[0]
        perfil[ngrama] = rango

    return perfil


def distancia(perfil1, perfil2):
    ngramas = set(perfil1.keys()) | set(perfil2.keys())

    penalizacion = max(len(perfil1), len(perfil2)) + 1

    distancia_total = 0

    for ng in ngramas:
        r1 = perfil1.get(ng, penalizacion)
        r2 = perfil2.get(ng, penalizacion)

        distancia_total += abs(r1 - r2)

    return distancia_total


texto_es = """
La inteligencia artificial permite que las computadoras aprendan a partir de datos.
El procesamiento de lenguaje natural estudia cómo las máquinas pueden analizar textos,
identificar patrones y generar respuestas en lenguaje humano.

La visión por computadora capacita a los sistemas para extraer información a partir de imágenes.
Este campo de estudio investiga cómo los algoritmos pueden procesar videos,
reconocer objetos y comprender entornos visuales con precisión humana.

El aprendizaje por refuerzo enseña a los agentes autónomos a tomar decisiones mediante la experiencia.
Esta vertiente del desarrollo evalúa cómo los modelos pueden explorar escenarios,
acumular recompensas y optimizar conductas en entornos dinámicos y complejos.

Los sistemas de recomendación filtran grandes volúmenes de opciones según las preferencias del usuario.
Esta tecnología analiza el historial de navegación,
predecir intereses futuros y personalizar sugerencias de manera automática y fluida.
"""

texto_en = """
The artificial intelligence allows computers to learn from data.
Natural language processing studies how machines can analyze texts,
identify patterns and generate responses in human language.

Computer vision enables digital systems to extract meaningful information from visual data.
This field of study investigates how algorithms can process videos,
recognize objects and understand visual environments with human-like accuracy.

Reinforcement learning teaches autonomous agents to make decisions through trial and error.
This branch of development evaluates how models can explore scenarios,
maximize rewards and optimize behaviors in complex, dynamic environments.

Recommendation systems filter massive volumes of choices based on user preferences.
This technology analyzes browsing history,
predicts future interests and customizes suggestions in an automatic, seamless way.
"""

texto_fr = """
L'intelligence artificielle permet aux ordinateurs d'apprendre à partir des données.
Le traitement du langage naturel étudie comment les machines peuvent analyser des textes,
identifier les structures et générer des réponses en langage humain.

La vision par ordinateur permet aux systèmes numériques d'extraire des informations des données visuelles.
Ce domaine d'étude examine comment les algorithmes peuvent traiter des vidéos,
reconnaître des objets et comprendre des environnements visuels avec une précision humaine.

L'apprentissage par renforcement enseigne aux agents autonomes à prendre des décisions par l'expérience.
Cette branche du développement évalue comment les modèles peuvent explorer des scénarios,
accumuler des récompenses et optimiser des comportements dans des environnements dynamiques.

Les systèmes de recommandation filtrent de grands volumes de choix selon les préférences de l'utilisateur.
Cette technologie analyse l'historique de navigation,
prédire les intérêts futurs et personnaliser les suggestions de manière automatique et fluide.

"""

textos_idioma = {
    "español": texto_es,
    "ingles": texto_en,
    "frances": texto_fr
}

modelos_idioma = {}

for idioma in textos_idioma:
    modelos_idioma[idioma] = perfil_ngramas(textos_idioma[idioma])

print(modelos_idioma)


def detectar_idioma(texto):
    pf = perfil_ngramas(texto)

    mejor_idioma = None
    mejor_dist = None

    for idioma in modelos_idioma:
        dist = distancia(pf, modelos_idioma[idioma])
        
        print(idioma,dist)

        if mejor_dist is None or dist < mejor_dist:
            mejor_dist = dist
            mejor_idioma = idioma

    return mejor_idioma


print("->",detectar_idioma("El modelo aprende patrones del lenguaje."))
print("->",detectar_idioma("The model learns patterns from language."))
print("->",detectar_idioma("Le modèle apprend des motifs du langage."))


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
# 3. ONE-HOT
# ============================

X_oh = []

for fila in X:
    vector = []

    for idx in fila:
        one_hot = np.zeros(vocab_size)
        one_hot[idx] = 1
        vector.extend(one_hot)

    X_oh.append(vector)

X_oh = np.array(X_oh)

y_oh = tf.one_hot(y, depth=vocab_size).numpy()

# ============================
# 4. RED NEURONAL SIMPLE
# ============================

input_size = X_oh.shape[1]
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


loss_fn = tf.keras.losses.CategoricalCrossentropy(from_logits=True)

# ============================
# 5. ENTRENAMIENTO
# ============================

optimizer = tf.optimizers.Adam(learning_rate=0.01)

loss_history = []
epochs = 200

X_tensor = X_oh.astype(np.float32)
y_tensor = y_oh.astype(np.float32)

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
# 6. GRÁFICA
# ============================

plt.plot(loss_history)
plt.xlabel("Época")
plt.ylabel("Pérdida")
plt.title("Pérdida durante el entrenamiento")
plt.show()

# ============================
# 7. PREDICCIÓN
# ============================

def predecir_siguiente(frase):
    frase = frase.lower().replace("\n", " ")
    palabras = frase.split()

    contexto = palabras[-(n-1):]

    if len(contexto) < n - 1:
        return "Faltan palabras para formar el contexto."

    fila = []

    for w in contexto:
        if w not in word2idx:
            return f"La palabra '{w}' no está en el vocabulario."
        fila.append(word2idx[w])

    vector = []

    for idx in fila:
        one_hot = np.zeros(vocab_size)
        one_hot[idx] = 1
        vector.extend(one_hot)

    vector = np.array([vector], dtype=np.float32)

    logits = forward(vector)
    probs = tf.nn.softmax(logits).numpy()[0]

    pred_idx = np.argmax(probs)
    return idx2word[pred_idx]


print(predecir_siguiente("la inteligencia"))
print(predecir_siguiente("modelos de"))
print(predecir_siguiente("redes neuronales"))