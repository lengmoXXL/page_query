#!python3

import logging
import yaml

from pathlib import Path
from typing import List
from elasticsearch import Elasticsearch
from argparse import ArgumentParser

from page_query.rule.manual_http_urls import ManualHttpUrls
from page_query.rule.manual_file_urls import ManualFileUrls


def update_pages(elasticsearch_stub: Elasticsearch, rules: List):
    r = elasticsearch_stub.delete_by_query('tldr', body={'query': {'match_all': {}}})
    logging.info(f'clear existing pages: {r}')
    for rule in rules:
        r = elasticsearch_stub.index('tldr', body=rule.page())
        logging.info(f'index page {rule.title}: {r}')


def query_pages(elasticsearch_stub: Elasticsearch, query_string: str):
    r = elasticsearch_stub.search(
        index='tldr',
        body={
            'query': {
                'multi_match': {
                    'query': query_string,
                    'fields': ['title^3', 'tags^3', 'summary', 'body']
                }
            }
        },
    )
    return r['hits']

def load_rules_from_config(config_path: str):
    path = Path(config_path)
    if not path.is_file():
        raise IOError(f'{path} is not file')
    config_text = path.read_text()
    config_dict = yaml.safe_load(config_text)

    elasticsearch_url = config_dict.get('elasticsearch_url', 'http://127.0.0.1:9200')
    elasticsearch_stub = Elasticsearch(hosts=[elasticsearch_url])

    rules = []
    for rule_dict in config_dict['rules']:
        if rule_dict['type'] == 'manual_http_urls':
            rules.append(ManualHttpUrls(title = rule_dict['title'],
                                        tags = rule_dict['tags'],
                                        summary = rule_dict['summary'],
                                        http_urls = rule_dict['http_urls']))
        elif rule_dict['type'] == 'manual_file_urls':
            rules.append(ManualFileUrls(title = rule_dict['title'],
                                        tags = rule_dict['tags'],
                                        summary = rule_dict['summary'],
                                        file_urls = rule_dict['file_urls']))
        else:
            raise ValueError(f'{rule_dict["type"]} not known')
    return elasticsearch_stub, rules


def print_query_results(res: List):
    for idx, hit in enumerate(res['hits']):
        source = hit['_source']
        print('#{:5d}: title: {}'.format(idx, source["title"]))
        print('        summary: {}'.format(source["summary"]))
        print('        tags: {}'.format(source['tags']))
        print('        urls:')
        for url in source.get('urls', []):
            print('       - {}'.format(url))


def main():
    parser = ArgumentParser(description='query custom pages')
    parser.add_argument('--config', type=str, default='page_query_config.yaml')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--query', type=str, help='query string', default='')

    args = parser.parse_args()

    elasticsearch_stub, rules = load_rules_from_config(args.config)
    if args.update:
        update_pages(elasticsearch_stub, rules)
    else:
        print_query_results(query_pages(elasticsearch_stub, args.query))


if __name__ == '__main__':
    main()