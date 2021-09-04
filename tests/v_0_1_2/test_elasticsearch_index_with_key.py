from elasticsearch import Elasticsearch


def test_index_elasticsearch():
    es = Elasticsearch(hosts=['http://localhost:9200'])
    if not es.indices.exists(index='tldr-test'):
        es.indices.create(index='tldr-test')
    es.delete_by_query(index='tldr-test', body={'query': {'match_all': {}}})
    r = es.index(
        index='tldr-test',
        body={
            'title': 'python reverse list',
            'tag': ['python'],
            'summary': 'list(reversed(lst))',
            'body': 'no content'
        },
        id = 'abc'
    )
    assert r['result'] == 'created', str(r)
    assert r['_id'] == 'abc'

    r = es.exists('tldr-test', id='abc')
    assert r == True, str(r)

    r = es.search(index='tldr', body={'query': {'match_all': {}}}, _source=['_id'])
    assert len(r['hits']) > 0, str(r)