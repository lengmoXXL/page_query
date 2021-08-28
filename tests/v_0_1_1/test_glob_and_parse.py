import glob
import re
import yaml

from pathlib import Path


def test_glob_fiels():
    files = glob.glob('docs/*.md')
    assert len(files) > 0, files


def test_parse_file_name():
    fn = 'grep_process_in_linux.md'
    pattern = re.compile('([a-zA-Z0-9]+)(_([a-zA-Z0-9]+))*[.]md')
    pattern.fullmatch(fn)
    assert pattern is not None

    title = fn[:-3].replace('_', ' ')
    assert 'grep process in linux' == title


def test_parse_file_content():
    file_content = '\n'.join([
        "```yaml",
        "tags: [linux, process, grep, search]",
        "http_urls:",
        "- https://stackoverflow.com/questions/61105343/how-to-grep-a-specific-process-from-ps-in-linux",
        "```",
        "`ps aux | grep <to_grep>`",
    ])

    file_content = file_content.strip()
    assert file_content.startswith('```yaml')
    file_content = file_content[len('```yaml'):]
    end = file_content.find('```')

    meta_content = file_content[:end]
    file_content = file_content[end+len('```'):].strip()
    meta = yaml.safe_load(meta_content)
    assert meta['tags'] == ['linux', 'process', 'grep', 'search']
    assert file_content == "`ps aux | grep <to_grep>`"
