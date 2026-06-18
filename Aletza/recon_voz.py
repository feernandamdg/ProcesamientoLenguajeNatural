# Somos 5 integrantes
# Entrenaremos una red para detectar en tiempo real de quien es la voz (solo somos 5 integrantes)
import os
import numpy as np
import sounddevice as sd
import librosa
import pickle
from funcion_preprocesamiento import preprocesar_texto

# ══════════════════════════════════════════════
# HIPERPARÁMETROS
# ══════════════════════════════════════════════
DURACION      = 3      # segundos de grabación
SAMPLE_RATE   = 22050  # frecuencia de muestreo estándar
N_MFCC        = 13     # coeficientes MFCC (huella vocal)
EPOCAS        = 100
LR            = 0.0001

INTEGRANTES   = ["Fernanda", "Derek", "Sebastian", "Eduardo", "Jared"]  # nombres del equipo


# ══════════════════════════════════════════════
# PASO 1 — EXTRACCIÓN DE CARACTERÍSTICAS
# MFCC (Mel-Frequency Cepstral Coefficients):
# representan la "huella" del timbre de cada voz
# son 13 valores promedio que resumen el audio completo
# en un vector comparable entre personas
# ══════════════════════════════════════════════
def extraer_mfcc(audio, sample_rate=SAMPLE_RATE, n_mfcc=N_MFCC):
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
    # promedio por coeficiente → vector de 13 números fijo sin importar duración
    return np.mean(mfcc, axis=1)


# ══════════════════════════════════════════════
# PASO 2 — RECOLECCIÓN DE DATOS DE ENTRENAMIENTO
# Cada integrante graba N_CLIPS audios cortos
# Se guardan como vectores MFCC + etiqueta numérica
# ══════════════════════════════════════════════
def recolectar_datos(n_clips=15):
    X = []  # vectores MFCC
    y = []  # índice del integrante

    for idx, nombre in enumerate(INTEGRANTES):
        print(f"\n{'='*40}")
        print(f"Turno de: {nombre} ({n_clips} grabaciones)")
        print(f"{'='*40}")

        for clip in range(n_clips):
            input(f"  Clip {clip+1}/{n_clips} — presiona Enter y habla {DURACION}s...")
            audio = sd.rec(
                int(DURACION * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype='float32'
            )
            sd.wait()  # esperar a que termine la grabación
            audio = audio.flatten()

            mfcc = extraer_mfcc(audio)
            X.append(mfcc)
            y.append(idx)
            print(f"  ✓ Grabado")

    X = np.array(X)  # (n_clips * n_integrantes, 13)
    y = np.array(y)  # (n_clips * n_integrantes,)
    return X, y


# ══════════════════════════════════════════════
# PASO 3 — RED NEURONAL MANUAL
# Entrada:  vector MFCC de 13 valores
# Capas:    13 → 32 → 16 → n_integrantes
# Salida:   probabilidad para cada integrante (softmax)
#
# Todo manual: forward, backward, activaciones
# sin keras ni pytorch
# ══════════════════════════════════════════════
class RedVoz:
    def __init__(self, n_integrantes=len(INTEGRANTES)):
        # pesos iniciados aleatoriamente (pequeños para evitar saturación)
        self.W1 = np.random.randn(N_MFCC, 32) * 0.01   # (13, 32)
        self.b1 = np.zeros((1, 32))
        self.W2 = np.random.randn(32, 16) * 0.01        # (32, 16)
        self.b2 = np.zeros((1, 16))
        self.W3 = np.random.randn(16, n_integrantes) * 0.01  # (16, n)
        self.b3 = np.zeros((1, n_integrantes))

    # ── Activaciones ──────────────────────────
    def relu(self, z):
        return np.maximum(0, z)

    def relu_deriv(self, z):
        return (z > 0).astype(float)

    def softmax(self, z):
        e = np.exp(z - z.max(axis=1, keepdims=True))  # estabilidad numérica
        return e / e.sum(axis=1, keepdims=True)

    # ── Forward ───────────────────────────────
    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)

        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.relu(self.z2)

        self.z3 = self.a2 @ self.W3 + self.b3
        self.a3 = self.softmax(self.z3)   # probabilidades finales
        return self.a3

    # ── Loss: cross-entropy ───────────────────
    def loss(self, y_pred, y_true):
        m = len(y_true)
        # log de la probabilidad asignada a la clase correcta
        log_prob = -np.log(y_pred[range(m), y_true] + 1e-8)
        return log_prob.mean()

    # ── Backward (gradientes manuales) ────────
    def backward(self, X, y_true, lr=LR):
        m = len(y_true)

        # gradiente capa 3 (softmax + cross-entropy juntos)
        dz3 = self.a3.copy()
        dz3[range(m), y_true] -= 1
        dz3 /= m

        dW3 = self.a2.T @ dz3
        db3 = dz3.sum(axis=0, keepdims=True)

        # gradiente capa 2
        da2 = dz3 @ self.W3.T
        dz2 = da2 * self.relu_deriv(self.z2)
        dW2 = self.a1.T @ dz2
        db2 = dz2.sum(axis=0, keepdims=True)

        # gradiente capa 1
        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.relu_deriv(self.z1)
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0, keepdims=True)

        # actualizar pesos
        self.W3 -= lr * dW3;  self.b3 -= lr * db3
        self.W2 -= lr * dW2;  self.b2 -= lr * db2
        self.W1 -= lr * dW1;  self.b1 -= lr * db1

    # ── Entrenamiento ─────────────────────────
    def entrenar(self, X, y, epocas=EPOCAS):
        for epoca in range(epocas):
            y_pred = self.forward(X)
            perdida = self.loss(y_pred, y)
            self.backward(X, y, LR)

            if (epoca + 1) % 10 == 0:
                correctos = (np.argmax(y_pred, axis=1) == y).sum()
                print(f"  Época {epoca+1:>3}/{epocas} — "
                      f"Loss: {perdida:.4f} — "
                      f"Acc: {correctos}/{len(y)}")

    # ── Predicción ────────────────────────────
    def predecir(self, x):
        probs = self.forward(x.reshape(1, -1))
        idx   = np.argmax(probs)
        return INTEGRANTES[idx], probs[0][idx]  # nombre + confianza


# ══════════════════════════════════════════════
# PASO 4 — GUARDAR Y CARGAR MODELO
# Para no reentrenar cada vez que se use la Alexa
# ══════════════════════════════════════════════
def guardar_modelo(red, path="modelo_voz.pkl"):
    pesos = {
        'W1': red.W1, 'b1': red.b1,
        'W2': red.W2, 'b2': red.b2,
        'W3': red.W3, 'b3': red.b3
    }
    with open(path, 'wb') as f:
        pickle.dump(pesos, f)
    print(f"Modelo guardado en {path}")

def cargar_modelo(path="modelo_voz.pkl"):
    with open(path, 'rb') as f:
        pesos = pickle.load(f)
    red = RedVoz()
    red.W1 = pesos['W1'];  red.b1 = pesos['b1']
    red.W2 = pesos['W2'];  red.b2 = pesos['b2']
    red.W3 = pesos['W3'];  red.b3 = pesos['b3']
    print("Modelo cargado")
    return red


# ══════════════════════════════════════════════
# PASO 5 — RECONOCIMIENTO EN TIEMPO REAL
# Esta es la función que llamará tu Alexa
# ══════════════════════════════════════════════
def reconocer_hablante(red):
    print("Escuchando...")
    audio = sd.rec(
        int(DURACION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    audio   = audio.flatten()
    mfcc    = extraer_mfcc(audio)
    nombre, confianza = red.predecir(mfcc)
    print(f"Hablante reconocido: {nombre} (confianza: {confianza:.2%})")
    return nombre


# ══════════════════════════════════════════════
# FLUJO COMPLETO
# ══════════════════════════════════════════════
if __name__ == "__main__":

    # — Fase 1: entrenar (solo se hace una vez) —
    print("Recolectando datos de entrenamiento...")
    X, y = recolectar_datos(n_clips=15)

    print("\nEntrenando red neuronal...")
    red = RedVoz()
    red.entrenar(X, y, epocas=EPOCAS)
    guardar_modelo(red)

    # — Fase 2: uso dentro de Alexa —
    red = cargar_modelo()
    hablante = reconocer_hablante(red)
    print(f"Quien habló: {hablante}")