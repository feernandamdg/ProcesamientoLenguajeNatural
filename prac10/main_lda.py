import argparse
import re
import string
from pathlib import Path


SALIDA_DIR = Path("./prac10/nubes")
NUM_DOCUMENTOS = 500
NUM_TOPICOS = 5
PALABRAS_POR_TOPICO = 10


def instalar_recursos_nltk():
    import nltk

    recursos = [
        "reuters",
        "stopwords",
        "wordnet",
        "omw-1.4",
        "punkt",
        "punkt_tab"
    ]

    for recurso in recursos:
        nltk.download(recurso, quiet=True)


def cargar_corpus(num_documentos):
    from nltk.corpus import reuters

    documentos_ids = reuters.fileids()[:num_documentos]
    documentos = [reuters.raw(doc_id) for doc_id in documentos_ids]
    return documentos


def limpiar_documento(texto, stop_words, lemmatizer):
    from nltk import word_tokenize

    texto = texto.lower()
    texto = texto.translate(str.maketrans("", "", string.punctuation)) #Quitar signos

    tokens = word_tokenize(texto)

    tokens_limpios = []

    for token in tokens:
        token = re.sub(r"[^a-z]", "", token)

        if len(token) <= 2:
            continue

        if token in stop_words:
            continue

        tokens_limpios.append(lemmatizer.lemmatize(token))

    return tokens_limpios


def preprocesar_documentos(documentos):
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    textos_limpios = [
        limpiar_documento(documento, stop_words, lemmatizer)
        for documento in documentos
    ]

    return [texto for texto in textos_limpios if texto]


def entrenar_lda(textos_limpios, num_topicos):
    from gensim import corpora
    from gensim.models import CoherenceModel, LdaModel

    diccionario = corpora.Dictionary(textos_limpios)
    diccionario.filter_extremes(no_below=3, no_above=0.55)

    corpus_bow = [diccionario.doc2bow(texto) for texto in textos_limpios]

    modelo_lda = LdaModel(
        corpus=corpus_bow,
        id2word=diccionario,
        num_topics=num_topicos,
        random_state=42,
        chunksize=100,
        passes=10,
        alpha="auto",
        per_word_topics=True,
    )

    coherencia = CoherenceModel(
        model=modelo_lda,
        texts=textos_limpios,
        dictionary=diccionario,
        coherence="c_v",
    )

    return modelo_lda, diccionario, corpus_bow, coherencia.get_coherence()


def mostrar_topicos(modelo_lda, palabras_por_topico):
    print("\nTOPICOS ENCONTRADOS")
    print("=" * 50)

    for indice, topico in modelo_lda.show_topics(
        num_topics=-1,
        num_words=palabras_por_topico,
        formatted=False,
    ):
        palabras = [palabra for palabra, peso in topico]
        print(f"Topico {indice + 1}: {', '.join(palabras)}")


def crear_nubes(modelo_lda, palabras_por_topico, salida_dir):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    salida_dir.mkdir(exist_ok=True)

    for indice in range(modelo_lda.num_topics):
        topico = modelo_lda.show_topic(indice, topn=palabras_por_topico)
        frecuencias = {palabra: peso for palabra, peso in topico}

        nube = WordCloud(
            width=900,
            height=500,
            background_color="black",
            colormap="viridis",
        ).generate_from_frequencies(frecuencias)

        plt.figure(figsize=(10, 6))
        plt.imshow(nube, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Topico {indice + 1}")
        plt.tight_layout()

        archivo = salida_dir / f"topico_{indice + 1}.png"
        plt.savefig(archivo, dpi=150)
        plt.close()

def main():

    instalar_recursos_nltk()
    documentos = cargar_corpus(NUM_DOCUMENTOS)
    textos_limpios = preprocesar_documentos(documentos)
    modelo_lda, diccionario, corpus_bow, coherencia = entrenar_lda(
        textos_limpios,
        NUM_TOPICOS,
    )

    mostrar_topicos(modelo_lda, PALABRAS_POR_TOPICO)
    crear_nubes(modelo_lda, PALABRAS_POR_TOPICO, SALIDA_DIR)

    print("\nPRACTICA 10 - LDA Y NUBE DE PALABRAS")
    print("=" * 50)
    print(f"Documentos usados: {len(documentos)}")
    print(f"Documentos procesados: {len(textos_limpios)}")
    print(f"Topicos generados: {NUM_TOPICOS}")
    print(f"Palabras por topico: {PALABRAS_POR_TOPICO}")
    print(f"Tamano del diccionario: {len(diccionario)}")
    print(f"Documentos en corpus BoW: {len(corpus_bow)}")
    print(f"Coherencia c_v: {coherencia:.4f}")
    print(f"Nubes guardadas en: {SALIDA_DIR.resolve()}")


if __name__ == "__main__":
    main()
