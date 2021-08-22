from pathlib import Path

from page_query.rule.manual_file_urls import ManualFileUrls

def test_load_example_file(tmp_path):
    example_path = tmp_path / 'example'
    example_path.write_bytes(b'abc\ncde\n')
    assert example_path.read_bytes() == b'abc\ncde\n'

def test_manual_file_urls_rule_example_file(tmp_path: Path):
    example_path = tmp_path / 'example'
    example_path.write_bytes(b'123\n456\n')

    rule = ManualFileUrls('local example', [], 'just for test', [str(example_path)])
    page = rule.page()
    assert len(page['body']) == 1
    assert page['body'][0] == b'123\n456\n'