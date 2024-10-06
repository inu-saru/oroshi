from flask import Flask, request, jsonify
from googletrans import Translator
import spacy
import en_core_web_sm

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
    targets = params['targets']
    exclude_poses = params['exclude_poses']
    language_type = 'en'

    nlp = spacy.load("en_core_web_sm")
    # TODO: language_typeを元に多言語対応する
    nlp = en_core_web_sm.load()
    doc = nlp(q)
    
    dicts = []
    for i, w in enumerate(doc):
        if w.pos_ in exclude_poses:
            continue

        vocabulary = translate_dict(w.text.lower(), targets)
        if len(vocabulary) == 0:
            continue
        
        dict = { 'vocabulary': vocabulary, 'relationship': { 'positions': [i], 'language_type': language_type }, 'meta': { 'pos': w.pos_ } }
        dicts.append(dict)

    return jsonify(dicts)

def translate_dict(q, targets):
    dict = {}
    for target in targets:
        dict.update(g_translate(q, target))
    return dict

def g_translate(q, target):
    translator = Translator()
    try:
        tr = translator.translate(q, dest=target)
        return { tr.src: q, tr.dest: tr.text }
    except Exception as e:
        # print(e, flush=True)
        return {}