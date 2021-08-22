import logging

from typing import Dict, List
from pathlib import Path


class ManualFileUrls:

    def __init__(self, title: str, tags: List[str],
                       summary: str, file_urls: List[str]) -> None:
        self._title = title
        self._tags = tags
        self._summary = summary
        self._file_urls = file_urls

    def page(self) -> Dict:
        body = []
        for url in self._file_urls:
            path = Path(url)            
            if not path.is_file():
                logging.warning(f'{path} is not file')
            else:
                body.append(path.read_bytes())
        return {
            'title': self._title,
            'tags': self._tags,
            'summary': self._summary,
            'body': body,
            'urls': self._file_urls
        }
    
    @property
    def title(self) -> str:
        return self._title