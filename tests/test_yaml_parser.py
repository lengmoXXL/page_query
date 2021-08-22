import yaml

def test_yaml_safe_load_example():
    text = '\n'.join([
        'elasticsearch_url: "http://localhost:9200"',
        'rules:',
        '   - type: manual_http_urls',
        '     title: www_baidu_com',
        '     tags: []',
        '     summary: the baidu website',
        '     http_urls: ["https://www.baidu.com"]',
    ])

    config = yaml.safe_load(text)
    assert config['elasticsearch_url'] == 'http://localhost:9200'
    assert len(config['rules']) == 1
    assert config['rules'][0]['type'] == 'manual_http_urls'
    assert config['rules'][0]['http_urls'] == ["https://www.baidu.com"]
