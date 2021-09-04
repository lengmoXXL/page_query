import hashlib


def test_hash_page():
    page = {
        'title': 'abc',
        'tags': ['a', 'b'],
        'summary': 'dsfke',
        'urls': [
            'htt'
        ]
    }

    hv = hashlib.md5()
    hv.update(page['title'].encode('utf-8'))
    hv.update(('\n'.join(page['tags'])).encode('utf-8'))
    hv.update(page['summary'].encode('utf-8'))
    hv.update(('\n'.join(page['tags'])).encode('utf-8'))
    assert hv.hexdigest() == 'cb4800c681efcabe6d7dc8a53a0d585d'