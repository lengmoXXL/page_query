import requests

from page_query.rule.manual_http_urls import ManualHttpUrls


def test_download_www_baidu_com():
    urls = ['https://www.baidu.com']
    for url in urls:
        r = requests.get(url)
        assert r.status_code == 200


def test_manual_http_urls_rule_www_baidu_com():
    rule = ManualHttpUrls('www_baidu_com', [],
                          'the baidu website',
                          ['https://www.baidu.com'])
    page = rule.page()
    assert len(page['body']) == 1