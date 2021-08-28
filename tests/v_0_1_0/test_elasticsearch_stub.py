from elasticsearch import Elasticsearch

def test_index_elasticsearch():
    es = Elasticsearch(hosts=['http://localhost:9200'])
    r = es.index(
        index='tldr',
        body={
            'title': 'python reverse list',
            'tag': ['python'],
            'summary': 'list(reversed(lst))',
            'body': 'no content'
        }
    )

    assert r['result'] == 'created'
    r = es.get('tldr', id=r['_id'])
    assert r['_source']['title'] == 'python reverse list'
    r = es.delete_by_query(
        'tldr',
        body={
            'query': {
                'match': {
                    'title': 'python reserve list'
                }
            }
        }
    )
    assert r['deleted'] >= 1