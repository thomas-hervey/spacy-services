# coding: utf8
from __future__ import unicode_literals

import json
import hug
from hug_middleware_cors import CORSMiddleware
import spacy


print("Loading models...")
MODELS = {
    "en_core_web_sm": spacy.load("en_core_web_sm"),
    # "en_core_web_md": spacy.load("en_core_web_md"),
    # "en_core_web_lg": spacy.load("en_core_web_lg"),
}
print("Models loaded!")


@hug.post("/tags")
def tags(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get all tags."""
    nlp = MODELS[model]
    doc = nlp(text)

    tags = []

    for token in doc:
        tags.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop
        })

    return tags


@hug.post("/ents")
def ents(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get all entities."""
    nlp = MODELS[model]
    doc = nlp(text)

    ents = []
    for ent in doc.ents:
        ents.append({
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "label": ent.label_
        })

    return ents



@hug.post("/deps")
def deps(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get all dependencies."""
    nlp = MODELS[model]
    doc = nlp(text)

    deps = []
    for token in doc:

        def listToString(s):
            # initialize an empty string
            string = ""

            # traverse in the string
            for element in s:
                string += element.text + ", "

            # return string
            return string

        children = listToString(token.children)


        deps.append({
            "text": token.text,
            "dep": token.dep_,
            "headText": token.head.text,
            "headPos": token.head.pos_,
            "children": children
        })

    return deps


if __name__ == "__main__":
    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8080)
