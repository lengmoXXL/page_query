#!python3

import logging
import yaml
import click
from typing import List

from pathlib import Path

from elasticsearch import Elasticsearch
from rich.console import Console
from rich.table import Table, Column
from rich.box import SIMPLE

from page_query.rule.manual_http_urls import ManualHttpUrls
from page_query.rule.manual_file_urls import ManualFileUrls
from page_query.rule.manual_http_urls_glob_md import ManualHttpUrlsGlobMarkdown



def update_pages(elasticsearch_stub: Elasticsearch, rules: List):
    r = elasticsearch_stub.delete_by_query('tldr', body={'query': {'match_all': {}}})
    logging.info(f'clear existing pages: {r}')
    for rule in rules:
        for page in rule.pages():
            r = elasticsearch_stub.index('tldr', body=page)
            logging.info(f'index page {page["title"]}: {r}')


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
        elif rule_dict['type'] == 'manual_http_urls_glob_md':
            rules.append(ManualHttpUrlsGlobMarkdown(
                glob=[f'{path.parent}/{p}' for p in rule_dict['glob']]))
        else:
            raise ValueError(f'{rule_dict["type"]} not known')
    return elasticsearch_stub, rules


def print_query_results(res: List):
    table = Table(
        Column("Id"),
        Column("Title", style='green'),
        Column("Summary", style="magenta"),
        Column("Tags", style='orange4'),
        Column("Urls"),
        box = SIMPLE
    )
    for idx, hit in enumerate(res['hits']):
        source = hit['_source']
        table.add_row(str(idx), source["title"], source["summary"],
                      ','.join(source["tags"]), '\n'.join(source.get('urls', [])))
    console = Console(width=150)
    console.print(table)


@click.command()
@click.option('--config', default='page_query_config.yaml', help='the path of config file')
@click.option('--update', is_flag=True, default=False)
@click.option('--query', default=None, type=str, help='query string')
def main(config: str, update: bool, query: str):
    elasticsearch_stub, rules = load_rules_from_config(config)
    if update:
        update_pages(elasticsearch_stub, rules)
    else:
        print_query_results(query_pages(elasticsearch_stub, query))
