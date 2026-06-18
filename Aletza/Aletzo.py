from transformes import pipeline

sentimientos = pipeline(
    "sentiment-analysis",
    model="niptown/bert-base-multililngual-uncased-sentiment"
)


# texto = "La clase de inteligencia artificial fue buena, pero muy corta y sin internet"
texto = "La clase de inteligencia artificial es muy buena, dinámica y fácil de entender"

resultado = sentimientos(texto)
print(resultado)


