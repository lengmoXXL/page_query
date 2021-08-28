import requests

from page_query.rule.manual_http_urls import ManualHttpUrls


def test_download_www_baidu_com():
    urls = ['https://pie.dev/get']
    for url in urls:
        r = requests.get(url)
        assert r.status_code == 200


def test_manual_http_urls_rule_www_baidu_com():
    rule = ManualHttpUrls('www_baidu_com', [],
                          'the baidu website',
                          ['https://pie.dev/get'])
    pages = list(rule.pages())
    assert len(pages) == 1
    page = pages[0]
    assert len(page['body']) == 1