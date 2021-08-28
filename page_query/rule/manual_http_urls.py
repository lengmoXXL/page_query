import requests
import logging

from typing import Dict, List


class ManualHttpUrls:

    def __init__(self, title: str, tags: List[str],
                       summary: str, http_urls: List[str]) -> None:
        self._title = title
        self._tags = tags
        self._summary = summary
        self._http_urls = http_urls

    def pages(self) -> Dict:
        body = []
        for url in self._http_urls:
            r = requests.get(url)
            if r.status_code != 200:
                logging.warning(f'failed to request {url}, status code: {r.status_code}')
            else:
                body.append(r.text)
        yield {
            'title': self._title,
            'tags': self._tags,
            'summary': self._summary,
            'body': body,
            'urls': self._http_urls
        }

    @property
    def title(self) -> str:
        return self._title