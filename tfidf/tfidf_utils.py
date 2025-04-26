import re
import math
import spacy
from nltk.corpus import stopwords

nlp = spacy.load("ru_core_news_sm")

RU_STOP = set(stopwords.words("russian"))
EN_STOP = set(stopwords.words("english"))
ALLOWED_POS = {"NOUN", "PROPN", "ADJ", "VERB", "NUM"}

def tokenize_doc(text: str) -> list[str]:
    # 1) spaCy-лемматизация
    doc = nlp(text)
    lemmas = [
        tok.lemma_.lower()
        for tok in doc
        if tok.is_alpha
           and tok.pos_ in ALLOWED_POS
           and tok.lemma_.lower() not in RU_STOP
    ]
    # 2) fallback 
    if not lemmas:
        words = re.findall(r'\b[А-Яа-яЁёA-Za-z0-9_]+\b', text.lower())
        lemmas = [w for w in words if w not in RU_STOP and w not in EN_STOP]

    tokens = lemmas.copy()
    for i in range(len(lemmas) - 1):
        tokens.append(f"{lemmas[i]} {lemmas[i+1]}")
    for i in range(len(lemmas) - 2):
        tokens.append(f"{lemmas[i]} {lemmas[i+1]} {lemmas[i+2]}")
    return tokens

def split_documents(text: str) -> list[str]:
    parts = re.split(r'[\.!\?;\n]+', text)
    return [p.strip() for p in parts if p.strip()]

def compute_tfidf(text: str) -> tuple[dict[str,int], dict[str,float]]:
    docs = split_documents(text)
    N = len(docs)

    # TF
    tf: dict[str,int] = {}
    doc_tokens: list[list[str]] = []
    for doc in docs:
        toks = tokenize_doc(doc)
        doc_tokens.append(toks)
        for w in toks:
            tf[w] = tf.get(w, 0) + 1

    # DF
    df: dict[str,int] = {}
    for toks in doc_tokens:
        for w in set(toks):
            df[w] = df.get(w, 0) + 1

    # IDF 
    idf: dict[str,float] = {
        w: math.log((N + 1) / (df.get(w, 0) + 1)) + 1
        for w in tf
    }

    return tf, idf
