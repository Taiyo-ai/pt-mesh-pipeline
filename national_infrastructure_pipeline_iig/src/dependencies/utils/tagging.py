import pandas as pd
import numpy as np
import re
import unicodedata
import nltk

from ..utils import load_config_yaml


try:
    nltk.download("punkt")
    nltk.download("wordnet")
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords
except Exception as e:
    nltk.download("stopwords")
    from nltk.corpus import stopwords

from keybert import KeyBERT
import en_core_web_lg
import spacy


# Combine all columns containing raw data under the name: 'raw_text'
def extract_textual_info(df, columns):
    cols = columns
    obj_cols = list(df.select_dtypes(include=["object"]).columns)
    obj_cols = [i for i in obj_cols if i in cols]
    obj_cols = [i for i in obj_cols if "id" not in i and "date" not in i]
    obj_cols = [i for i in obj_cols if "start" not in i and "end" not in i]

    df["raw_text"] = df[obj_cols].apply(
        lambda x: " ".join([str(i) for i in x.tolist()]), axis=1
    )
    df["raw_text"] = (
        df["raw_text"].replace("NIL", "", regex=True).replace("nan", "", regex=True)
    )
    return df


def preprocess_sentence(sentence: str):
    sentence = unicode_to_ascii(sentence.lower().strip())
    # replacing email addresses with blank space
    sentence = re.sub(
        r"[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}", " ", sentence
    )
    # replacing urls with blank space
    sentence = re.sub(
        r"\bhttp:\/\/([^\/]*)\/([^\s]*)|https:\/\/([^\/]*)\/([^\s]*)", " ", sentence
    )
    sentence = sentence.strip()
    return sentence


def unicode_to_ascii(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def extract_keywords_func(df, entities, cols):
    ents = [
        "CARDINAL",
        "CONST",
        "DATE",
        "EVENT",
        "FAC",
        "FUND",
        "GPE",
        "GP",
        "LP",
        "LANGUAGE",
        "LAW",
        "LOC",
        "MONEY",
        "NORP",
        "ORDINAL",
        "ORG",
        "PERCENT",
        "PERSON",
        "PRODUCT",
        "QUANTITY",
        "TIME",
        "WORK_OF_ART",
    ]
    ents = [x.upper() for x in ents]
    print(df.head())
    kw_model = KeyBERT()
    df = extract_textual_info(df, cols)
    df["raw_text"] = df["raw_text"].apply(preprocess_sentence)
    raw_text = df["raw_text"]
    df["tags"] = [val for val in spacy_entity(raw_text)]
    for entity in ents:
        obj = []
        arr = []
        for row in df["tags"]:
            try:
                arr.append(row[entity])
            except Exception as e:
                arr.append([])
                pass
        df["tag_" + entity.lower()] = arr

    df["keywords"] = df["raw_text"].apply(
        lambda x: [
            str(list(w)[0]).lower()
            for w in kw_model.extract_keywords(
                x,
                keyphrase_ngram_range=(1, 3),
                stop_words="english",
                use_mmr=True,
                diversity=0.7,
                top_n=20,
            )
        ]
    )

    return df


def spacy_entity(raw_text, entites):
    nlp = spacy.load("en_core_web_lg")
    arr = []
    obj = {"GP": [], "LP": [], "FUND": [], "CONST": []}
    for i in range(len(raw_text)):
        doc = nlp(raw_text[i])
        for ent in doc.ents:
            if ent.label_ in obj.keys():
                obj[ent.label_].append(ent.text)
            else:
                obj[ent.label_] = [ent.text]

        for label in obj.keys():
            obj[label] = list(set(obj[label]))
        for org in obj["ORG"]:
            if org.lower() in list(entites["name"]):
                obj[list(entites[entites["name"] == org.lower()].iloc[0])[1]].append(
                    org
                )
        arr.append(obj)
    return arr
