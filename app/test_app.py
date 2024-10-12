from app import app

def test_index_route():
    params = dict(q = 'We must respect the will of the individual.', targets = ['en', 'ja', 'th'])
    response = app.test_client().post('/translate', json=params)
    json = response.get_json()

    assert response.status_code == 200
    assert json['en'] == 'We must respect the will of the individual.'
    assert json['ja'] == '私たちは個人の意志を尊重しなければなりません。'
    assert json['th'] == 'เราต้องเคารพเจตจำนงของแต่ละบุคคล'

def test_relations_route_en():
    params = dict(
        q = 'We must respect the will of the individual.',
        targets = ['en', 'ja', 'th'],
        exclude_poses = ['ADP', 'AUX', 'DET', 'PRON', 'PUNCT'])
    response = app.test_client().post('/translate_relations', json=params)
    json = response.get_json()

    assert response.status_code == 200
    assert json[0] == {'meta': {'pos': 'VERB'}, 'relationship': {'language_type': 'en', 'positions': [2]}, 'vocabulary': {'en': 'respect', 'ja': '尊敬', 'th': 'เคารพ'}}
    assert json[1] == {'meta': {'pos': 'NOUN'}, 'relationship': {'language_type': 'en', 'positions': [4]}, 'vocabulary': {'en': 'will', 'ja': '意思', 'th': 'จะ'}}
    assert json[2] == {'meta': {'pos': 'NOUN'}, 'relationship': {'language_type': 'en', 'positions': [7]}, 'vocabulary': {'en': 'individual', 'ja': '個人', 'th': 'รายบุคคล'}}

def test_relations_route_ja():
    params = dict(
        q = '個人の意志は尊重しなければいけない',
        targets = ['en', 'ja', 'th'],
        exclude_poses = ['ADP', 'AUX', 'DET', 'PRON', 'PUNCT', 'SCONJ'])
    response = app.test_client().post('/translate_relations', json=params)
    json = response.get_json()

    assert response.status_code == 200
    assert json[0] == {'meta': {'pos': 'NOUN'}, 'relationship': {'language_type': 'ja', 'positions': [0]}, 'vocabulary': {'en': 'personal', 'ja': '個人的', 'th': 'ส่วนตัว'}}
    assert json[1] == {'meta': {'pos': 'NOUN'}, 'relationship': {'language_type': 'ja', 'positions': [2]}, 'vocabulary': {'en': 'will', 'ja': '意思', 'th': 'จะ'}}
    assert json[2] == {'meta': {'pos': 'VERB'}, 'relationship': {'language_type': 'ja', 'positions': [4]}, 'vocabulary': {'en': 'respect', 'ja': '尊敬', 'th': 'เคารพ'}}
    assert json[3] == {'meta': {'pos': 'VERB'}, 'relationship': {'language_type': 'ja', 'positions': [8]}, 'vocabulary': {'en': 'Be', 'ja': 'いける', 'th': 'ไป'}}
