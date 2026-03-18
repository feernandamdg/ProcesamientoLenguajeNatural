import unicodedata

def normalizar(texto):
    """Convierte a minúsculas y elimina tildes."""
    texto = texto.lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto

# Base de datos de ecuaciones
ecuaciones = [
    {
        "nombre": "Ecuación de la recta",
        "ecuacion": "y = mx + b",
        "palabras_clave": ["recta", "pendiente", "lineal", "interseccion", "eje y", "estadistica", "ingenieria"]
    },
    {
        "nombre": "Teorema de Pitágoras",
        "ecuacion": "a² + b² = c²",
        "palabras_clave": ["pitagoras", "triangulo", "hipotenusa", "catetos", "geometria", "arquitectura", "navegacion"]
    },
    {
        "nombre": "Definición de derivada",
        "ecuacion": "f'(x) = lim (h→0) [f(x+h) − f(x)] / h",
        "palabras_clave": ["derivada", "calculo", "tasa de cambio", "velocidad", "funcion", "diferencial"]
    },
    {
        "nombre": "Distribución normal",
        "ecuacion": "f(x) = (1 / (σ√(2π))) e^{-(x−μ)² / (2σ²)}",
        "palabras_clave": ["distribucion normal", "normal", "probabilidad", "estadistica", "media", "desviacion estandar", "errores"]
    },
    {
        "nombre": "Ecuación de energía de Einstein",
        "ecuacion": "E = mc²",
        "palabras_clave": ["einstein", "energia", "masa", "luz", "fisica", "relatividad"]
    },
    {
        "nombre": "Función de error en regresión lineal",
        "ecuacion": "J(θ) = (1 / 2n) Σ (hθ(xᵢ) − yᵢ)²",
        "palabras_clave": ["regresion lineal", "inteligencia artificial", "error", "modelo", "prediccion", "algoritmo", "machine learning"]
    }
]

def buscar_ecuacion(entrada):
    entrada_norm = normalizar(entrada)
    resultados = []

    for eq in ecuaciones:
        for palabra in eq["palabras_clave"]:
            palabra_norm = normalizar(palabra)
            if palabra_norm in entrada_norm or entrada_norm in palabra_norm:
                resultados.append(eq)
                break

    return resultados

# Programa principal
print("=== Buscador de ecuaciones ===")
print("Escribe una palabra o frase relacionada con una ecuación.")
print("Ejemplos: recta, hipotenusa, derivada, energia, probabilidad, regresion\n")

consulta = input("Ingresa tu palabra o frase: ")

resultados = buscar_ecuacion(consulta)

if resultados:
    print("\nEcuaciones encontradas:\n")
    for resultado in resultados:
        print(f"{resultado['nombre']}:")
        print(f"  {resultado['ecuacion']}\n")
else:
    print("\nNo se encontró una ecuación relacionada con esa palabra.")