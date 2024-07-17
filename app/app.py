from flask import Flask
import spacy
import en_core_web_sm

app = Flask(__name__)

@app.route("/")
def index():
    nlp = spacy.load("en_core_web_sm")
    nlp = en_core_web_sm.load()
    doc = nlp("This is a sentence.")
    text = [(w.text, w.pos_) for w in doc]
    return text