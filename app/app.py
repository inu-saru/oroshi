from flask import Flask, request, jsonify
from googletrans import Translator
import spacy
import en_core_web_sm
import ja_core_news_sm
from lingua import Language, LanguageDetectorBuilder

app = Flask(__name__)
    
@app.route("/translate", methods=['POST'])
def translate():
    params = request.get_json()
    q = params['q']
    targets = params['targets']
    
    dict = translate_dict(q, targets)
    return jsonify(dict)

@app.route("/translate_relations", methods=['POST'])
def translate_relations():
    params = request.get_json()
    q = params['q']
    language_type = detect_language_type(q)
    targets = params['targets']
    exclude_poses = params['exclude_poses']

    nlp = get_nlp(language_type)
    doc = nlp(q)
    translates = get_translates(language_type, doc, targets, exclude_poses)
    return jsonify(translates)

def translate_dict(q, targets):
    dict = {}
    for target in targets:
        dict.update(g_translate(q, target))
    restponse_translated_keys = list(dict.keys())
    unnecessary_keys = [i for i in restponse_translated_keys if i not in targets]
    for key in unnecessary_keys:
        dict.pop(key)

    return dict

def g_translate(q, target):
    translator = Translator()
    try:
        tr = translator.translate(q, dest=target)
        return { tr.src: q, tr.dest: tr.text }
    except Exception as e:
        # print(e, flush=True)
        return {}
    
def detect_language_type(strings):
    detector = build_detector()
    type = detector.detect_language_of(strings)
    dict = get_language_dict()
    return dict[type]

def build_detector():
    languages = [Language.ENGLISH, Language.JAPANESE, Language.THAI]
    return LanguageDetectorBuilder.from_languages(*languages).build()

def get_language_dict():
    return { Language.ENGLISH: 'en', Language.JAPANESE: 'ja', Language.THAI: 'th' }

def get_nlp(language_type):
    if language_type == 'en':
        nlp = spacy.load("en_core_web_sm")
        nlp = en_core_web_sm.load()
        return nlp
    elif language_type == 'ja':
        nlp = spacy.load("ja_core_news_sm")
        nlp = ja_core_news_sm.load()
    else:
        nlp = None
    return nlp

def get_translates(language_type, doc, targets, exclude_poses):
    dicts = []
    for i, w in enumerate(doc):
        if w.pos_ in exclude_poses:
            continue

        vocabulary = translate_dict(w.lemma_, targets)
        if len(vocabulary) == 0:
            continue
        
        dict = { 'vocabulary': vocabulary, 'relationship': { 'positions': [i], 'language_type': language_type }, 'meta': { 'pos': w.pos_ } }
        dicts.append(dict)
    return dicts